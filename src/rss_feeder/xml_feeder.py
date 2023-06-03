import feedparser
import time
import datetime
from typing import Dict, List, Tuple, Any, Coroutine, Callable, Set
import httpx  # 10s -> 7.76s
import asyncio

from links_parser import links_from_json
from app_tui import wrap
from my_types import PostRecord, FeedRecord, Sandbox, LinksEntried, FeedEntry, RegistredFeeds


def actuality_index(a: Any, b: Any):
    return datetime.timedelta(seconds=b - time.mktime(a)).days


async def clienting(links: Dict[str, List[Tuple[str, str]]], sandbox):
    links_count : Dict[str, int] = { url[0]: len(url[1]) for url in links.items()}
    links_progress : Dict[str, int] = { url[0]: 0 for url in links.items()}
    
    async with httpx.AsyncClient() as client:
        tasks: Coroutine = (
                wrap(
                    links_count,
                    links_progress,
                    url[0],
                    client.get(v),
                    sandbox
                ) for url in links.items() for u in url[1] for _, v in u.items()
        )
        reqs = await asyncio.gather(*tasks)
        return reqs


async def clienting_entries(links: LinksEntried, sandbox: Sandbox):
    links_count : Dict[str, int] = { name: len(ents) for name, ents in links.items()}
    links_progress : Dict[str, int] = { key: 0 for key in links.keys()}
    
    async with httpx.AsyncClient() as client:
        tasks: Coroutine = (
                wrap(
                    links_count,
                    links_progress,
                    name,
                    client.get(entry.link),
                    sandbox
                ) for name, entries in links.items() for entry in entries
        )
        reqs = await asyncio.gather(*tasks)
        return reqs


async def filtred_feeder(
                links: Dict[str, List[Tuple[str, str]]] = None,
                **kwargs
          ) -> Tuple[List[FeedRecord], Set[str]]:

    timestamp = time.time()

    if links is None:
        return None

    reqs = await clienting(links, kwargs["sandbox"])

    authors = [(k, v1, v2) for k, v in links.items() for v_dict in v for v1, v2 in v_dict.items()]
    NewsFeed = [(x[0], feedparser.parse(x[1])) for x in zip(authors, reqs)]

    dely: List[FeedRecord] = [] # = [None] * len(links)
    topics: Set[str] = set()
    for i, (base, x) in enumerate(NewsFeed):
        tmp = []
        for element in x.entries:
            if actuality_index(element.published_parsed, timestamp) < kwargs["days"] + 1:
                tmp.append(PostRecord(
                                element.title,
                                element.link,
                                element.published
                 ))
        dely.append(FeedRecord(base[0], base[1], base[2], len(tmp), tmp))
        topics.add(base[0])

    return (dely, topics)


async def process_feeder(links: LinksEntried = None, **kwargs) -> RegistredFeeds:
    timestamp = time.time()

    if links is None:
        return None

    reqs = await clienting_entries(links, kwargs["sandbox"])

    authors = [
        (name, entry.autor, entry.link) for name, entries in links.items()
        for entry in entries
    ]
    NewsFeed = [(x[0], feedparser.parse(x[1])) for x in zip(authors, reqs)]

    dely: List[FeedRecord] = [] # = [None] * len(links)
    topics: Set[str] = set()
    for i, (base, x) in enumerate(NewsFeed):
        tmp = []
        for element in x.entries:
            if actuality_index(element.published_parsed, timestamp) < kwargs["days"] + 1:
                tmp.append(PostRecord(
                                element.title,
                                element.link,
                                element.published
                 ))
        dely.append(FeedRecord(base[0], base[1], base[2], len(tmp), tmp))
        topics.add(base[0])

    return (dely, topics)


def main():
    asyncio.run(filtred_feeder(links_from_json('RSS_feeds.json')))


if __name__ == '__main__':
    main()
