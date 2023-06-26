import json
from typing import Dict, List
from my_types import FeedEntry, Links


def links_from_json(filename: str) -> Dict[str, List[str]]:
    with open(filename, "r") as file:
        data = json.loads(file.read())
        # for k, v in data.items():
            # print(f'{k} : {v}')
        return data


def entries_from_json(filename: str) -> dict[str, list[FeedEntry]]:
    with open(filename, "r") as file:
        data = json.loads(file.read())
        entries = {}
        for group, items in data.items():
            entries[group] = []
            for item in items:
                entries[group].append(FeedEntry(
                    group, 
                    item["subgroup"],
                    item["name"],
                    item["link"],
                    item["source"],
                    item["flags"]
                ))

        return entries


if __name__ == "__main__":
    print(links_from_json('../../RSS_feeds.json'))
    print(entries_from_json('../../RSS_feeds.json'))

