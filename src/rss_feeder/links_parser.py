import json
from typing import Dict, List


def links_from_json(filename: str) -> Dict[str, List[str]]:
    with open(filename, "r") as file:
        data = json.loads(file.read())
        # for k, v in data.items():
            # print(f'{k} : {v}')
        return data

if __name__ == "__main__":
    links_from_json('../../RSS_feeds.json')

