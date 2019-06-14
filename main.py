import asyncio
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import traceback

import aiohttp

import settings
from models import objects, NovelModel, ChapterModel
from semail import SendEmail
from log import logger
from parsers import novel_registry

semaphore = asyncio.Semaphore(settings.CONCURRENCY)
executor = ThreadPoolExecutor(max_workers=5)


class HtmlException(Exception):
    pass


def send_email(subject, content, receivers):
    mail = SendEmail(settings.EMAIL_HOST, settings.EMAIL_USER, settings.EMAIL_PASSWORD)
    return mail.send_email(subject, content, receivers, mimeType="html")


async def fetch_html(session, url):
    async with session.get(url, ssl=False) as resp:
        if resp.status != 200:
            raise HtmlException("获取url:{} 内容失败, 错误码:{}".format(url, resp.status))
        html = await resp.text()
        return html


async def process_notify(session, novel):
    loop = asyncio.get_event_loop()
    parser = novel["parser"]
    parse_info_func = novel_registry[parser]["parse_info_func"]
    parse_content_func = novel_registry[parser]["parse_content_func"]
    while True:
        async with semaphore:
            try:
                html = await fetch_html(session, novel["url"])
            except Exception as e:
                logger.error(logger.error(traceback.format_exc()))
            else:
                novel_obj, is_create = await objects.create_or_get(NovelModel, name=novel["name"])
                chapters = await objects.execute(
                    ChapterModel.select(ChapterModel.name).where(ChapterModel.novel == novel_obj))
                all_chapter_name = {chapter.name for chapter in chapters}
                is_empty = not bool(all_chapter_name)

                for chapter in parse_info_func(html):
                    if chapter.name in all_chapter_name:
                        continue

                    # 如果小说已经存在并且已经存在章节信息(非第一次爬取), 则发送更新章节
                    if not is_create and not is_empty:
                        full_url = urljoin(novel["url"], chapter.url)
                        try:
                            html = await fetch_html(session, full_url)
                        except Exception as e:
                            logger.error(traceback.format_exc())
                            break
                        content = parse_content_func(html)
                        subject = "小说[{}]更新通知".format(novel["name"])
                        content = "<h3>{}</h3>{}".format(chapter.name, content)
                        receivers = novel["receivers"]
                        err = await loop.run_in_executor(executor, send_email, subject, content, receivers)
                        if err:
                            logger.error("send email to {} failed, error:{}".format(receivers, err))
                        else:
                            logger.info("send email to {} success.".format(receivers))

                    await objects.create(ChapterModel, novel=novel_obj, name=chapter.name)
                    all_chapter_name.add(chapter.name)
                    logger.info("save [{}] -> [{}].".format(chapter.name, novel_obj.name))
                logger.info("[{}]最新章节: {}".format(novel["name"], chapter.name))
        await asyncio.sleep(30 * 60)


async def main():
    async with aiohttp.ClientSession() as session:
        loop = asyncio.get_event_loop()
        tasks = [loop.create_task(process_notify(session, novel)) for novel in settings.NOVELS]

        for task in tasks:
            await task


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_until_complete(asyncio.sleep(0))
    # loop.close()
    print("end...")
