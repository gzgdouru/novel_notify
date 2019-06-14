from collections import namedtuple

from scrapy.selector import Selector

from registry import NovelRegistry

Chapter = namedtuple("Chapter", "url name")

novel_registry = NovelRegistry()


def dd_parse_chapter_info(html):
    selector = Selector(text=html)
    nodes = selector.css("#list dl dd")
    for node in nodes:
        url = node.css("a::attr(href)").extract_first()
        name = node.css("a::text").extract_first()
        yield Chapter(url=url, name=name)


def dd_parse_chapter_content(html):
    selector = Selector(text=html)
    content = selector.css("#content").extract_first()
    return content


novel_registry.register("dingdian", parse_info_func=dd_parse_chapter_info, parse_content_func=dd_parse_chapter_content)

if __name__ == "__main__":
    print(novel_registry["dingdian"])
