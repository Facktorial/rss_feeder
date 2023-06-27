import yaml
import asyncio
from Observer import Observable
from dataclasses import dataclass, field
from enum import Enum
from functools import partial
from typing import Any, Callable
import json

from GUIConf import *

from src.rss_feeder.xml_feeder import process_feeder
from src.rss_feeder.links_parser import entries_from_json
from src.rss_feeder.my_types import *


log = partial(print, "[AppState] ")


class FetchData(Enum):
    FETCH = "fetch"
    BACKUP = "backup"


@dataclass
class AppConfig:
	default_days: int = 28


def write_config(path: str, config: AppConfig) -> None:
    with open(path, 'w') as file:
        yaml.dump(config.__dict__, file)


def read_config(path: str) -> AppConfig:
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    return AppConfig(**config)


@dataclass
class AppState(Observable):
	_fetched: bool = False
	topics: list[str] = field(default_factory=list)
	source: dict[str, list[FeedEntry]] = field(default_factory=dict) 
	data: list[FeedRecord] = field(default_factory=list) # TODO rework to use dict
	load_callback: Callable[[str, str], None] = partial(print, "something is wrong")
	config: AppConfig = None
	only_starred: bool = False

	def __post_init__(self) -> None:
		super().__init__()
		self.config = read_config(CONF_FILE)

	@property
	def fetched(self) -> bool:
		return self._fetched

	@fetched.setter
	def fetched(self, val: bool) -> None:
		self._fetched = val
		self.notify_observers('fetched' if self._fetched else 'fetch_need')

	async def wrapp_load(self, file: str, local_data: str, do_fetch: FetchData) -> None:
		await self.load_callback(file, local_data, do_fetch)
		self.fetched = True

	async def load_data(self, file: str, local_data: str, do_fetch: FetchData) -> None:
		self.source = entries_from_json(file)
		self.topics = [k for k, _ in self.source.items()]

		if do_fetch == FetchData.FETCH:
			self.data, self.topics = await process_feeder(
				self.source, days=self.config.default_days, sandbox=Sandbox(0)
			)
			await self.sync_starred(local_data)
			log(self.data)
			return
		
		self.data = await self.load_records(local_data)
		log(self.data)
		await asyncio.sleep(0.0)
 
	@staticmethod
	async def load_records(path: str) -> list[FeedRecord]:
		data = []
		try:
			with open(path, "r") as file:
				records = json.load(file)	
				for x in records:
					posts = [PostRecord(**post) for post in x['posts']]
					data.append(FeedRecord(**x))    
					data[-1].posts = posts
		except FileNotFoundError:
			print("File not found: " + path)

		return data

	async def load_cached_records(self, local_data) -> None:
		import copy
		backup = copy.deepcopy(self.topics)

		self.data, self.topics = await process_feeder(
			self.source, days=self.config.default_days, sandbox=Sandbox(0)
		)
		# FIXME, WTF
		# self.topics = [*self.topics]
		self.topics = backup
		await self.sync_starred(local_data)

	async def sync_starred(self, backup_file: str) -> None:
		data_sync_with: list[FeedRecord] = await self.load_records(backup_file) 

		common_recs = [(item, other)
			for item in self.data
			for other in data_sync_with
			if item.name == other.name 
		]
		for new_r, sync_r in common_recs:
			common_posts = [(npost, cpost)
				for npost in new_r.posts
				for cpost in sync_r.posts
				if npost.title == cpost.title 
			]
			for npost, cpost in common_posts:
				log(f"{npost}", f"{cpost}")
				npost.starred = cpost.starred 
