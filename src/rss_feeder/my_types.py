from dataclasses import dataclass, field
from rich.console import Console


class Sandbox():
    def __init__(self, start):
        self.console = Console()
        self.cursor_pos = start
        self.topics = []


@dataclass
class PostRecord:
    title: str
    link: str
    published: str
    starred: bool

    def to_json(self):
        data = {
            "title": self.title,
            "link": self.link,
            "published": self.published,
            "starred": self.starred
        }
        return data


@dataclass
class FeedRecord:
    group: str
    name: str
    feed_link: str
    feed_source: str
    total_posts: int
    posts: list[PostRecord]  = field(default_factory=list)

    def to_json(self):
        data = {
            "group": self.group,
            "name": self.name,
            "feed_link": self.feed_link,
            "feed_source": self.feed_source,
            "total_posts": self.total_posts,
            # "posts": [PostRecord(**post) for post in self.posts]
            "posts": [post.to_json() for post in self.posts]
        }
        return data


@dataclass
class FeedEntry:
    group: str
    subgroup: str
    autor: str
    link: str
    source: str
    flags: str
    # comment: str

    def to_json(self):
        data = {
            "group": self.group,
            "subgroup": self.subgroup,
            "name": self.autor,
            "link": self.link,
            "source": self.source,
            "flags": self.flags
        }
        return data


RegistredFeeds = tuple[list[FeedRecord], set[str]]
Links = dict[str, list[tuple[str, str]]]
LinksEntried = dict[str, list[FeedEntry]]


