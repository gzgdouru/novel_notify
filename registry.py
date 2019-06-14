from collections import defaultdict


class NovelRegistry:
    def __init__(self):
        self.data = defaultdict(dict)

    def register(self, name, *, parse_info_func, parse_content_func):
        self.data[name]["parse_info_func"] = parse_info_func
        self.data[name]["parse_content_func"] = parse_content_func

    def __getitem__(self, key):
        return self.data[key]
