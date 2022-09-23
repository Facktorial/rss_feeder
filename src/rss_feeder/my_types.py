from dataclasses import dataclass  # , field
from typing import List
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


@dataclass
class FeedRecord:
    group: str
    name: str
    feed_link: str
    total_posts: int
    posts: List[PostRecord]  # = field(default_factory=list)


