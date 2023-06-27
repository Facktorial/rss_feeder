import atexit
import signal
import sys

from tkinter import Frame

from typing import Final, Type, Callable, TypeVar
from functools import partial, lru_cache
import json
import asyncio

from App import App, PageFrame
from AppState import AppState, FetchData

from Frames.MainPage import *
from Frames.InitPage import *
from Frames.EditPage import *
from Frames.EditGroup import *
from Frames.IPage import IPage

from GUIConf import *

from src.rss_feeder.my_types import *


log = partial(print, "[main] ")


PAGES: Final[dict[PageFrame, Type[IPage]]] = {
    PageFrame.INIT: InitPage,
    PageFrame.MAIN: MainPage,
    PageFrame.EDIT: EditPage,
    PageFrame.GROUP_EDIT: EditGroup
}

LOAD_FUNC = Callable[[str, str], None]
SAVE_FUNC = Callable[[str, str], None]


async def as_load(app: AppState, file: str, from_file: str, fetch: FetchData) -> None:
	log("[async] [load]")
	await app.load_data(file, from_file, fetch)
	app.fetched = True
	save_data(app, BACKUP_DATA)


def on_exit(app: AppState, filename: str) -> None:
	save_data(app, filename)
	log("[exit]")


def save_data(app: AppState, filename: str) -> None:
	with open(filename, "w") as file:
		converted_data = [r.to_json() for r in app.data]
		json.dump(converted_data, file)
    # FIXME
	with open(TEST, "w") as file:
		print("source", app.source)
		converted_data = {gr: [r.to_json() for r in ls]
			for (gr, ls) in app.source.items()
		}
		print("converted", converted_data)
		json.dump(converted_data, file)
	log("[save]")


class RSSFeederGUI(App):
	def __init__(self):
		self.app: AppState = AppState()
		self.app.load_callback = partial(as_load, self.app)

		loop = asyncio.get_event_loop()
		# _ = loop.create_task(self.app.wrapp_load(TEST, BACKUP_DATA, FetchData.FETCH))
		_ = loop.create_task(self.app.wrapp_load(TEST, BACKUP_DATA, FetchData.BACKUP))
		
		super().__init__("RSS Feeder", PAGES, self.app, IMAGES)
		self.save_callback = partial(save_data, self.app, BACKUP_DATA)
		
	async def async_sleep_and_show(self):
		while(not False): 
			log("async")
			await asyncio.sleep(2)
			self.app.fetched = True if not self.app.fetched else False
			log("async [END]")
			await asyncio.sleep(5)


async def main():
    app = RSSFeederGUI()
    app.root.minsize(960, 540)
    atexit.register(partial(on_exit, app.app, BACKUP_DATA))

    await asyncio.gather(
        # asyncio.create_task(app.async_sleep_and_show()),
        asyncio.create_task(app.run())
    )


if __name__ == "__main__":
	signal.signal(signal.SIGINT, lambda signal, frame: sys.exit(0))
	asyncio.run(main())
