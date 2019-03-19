import asyncio
import aiohttp
from tornado.httpclient import AsyncHTTPClient

import settings


http_client = AsyncHTTPClient()


async def parser_novel(novel):
    urls = novel["urls"]
    for url in urls:
        try:
            resp = await http_client.fetch(url)
        except Exception as e:
            print("获取url:{}内容失败, 原因:{}".format(url, e))
        else:
            print(resp.body)


async def main():
    for novel in settings.NOVELS:
        asyncio.ensure_future(parser_novel(novel))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
