from tkinter import *
from tkinter import ttk
from tkinter import font

from enum import Enum
from typing import Protocol, Final, Type
from dataclasses import dataclass, field
from functools import partial, lru_cache
import json
import asyncio
from time import sleep

import MultiListbox as table
from utils import log
from App import App, AppState, PageFrame

from Frames.frames import *
from Frames.MainPage import *
from Frames.InitPage import *

from src.rss_feeder.my_types import *


TEST: Final[str] = "RSS_feeds_test.json"
SOURCE: Final[str] = "RSS_feeds.json"
BACKUP_DATA: Final[str] = "backup_data"


PAGES: Final[dict[PageFrame, Type[Frame]]] = {
    PageFrame.INIT: InitPage,
    PageFrame.MAIN: MainPage,
    PageFrame.EDIT: EditPage,
    PageFrame.GROUPNEW: GroupCreateNewPage,
    PageFrame.INFO: GroupInfoPage,
    PageFrame.APP: AppInfoPage
}


class RSSFeederGUI(App):
    def __init__(self):
        self.app: AppState = AppState()

        # self.as_load(TEST)
        self.load(TEST, BACKUP_DATA)
        
        super().__init__("RSS Feeder", PAGES, self.app)
        
        self.save_data(BACKUP_DATA)

    async def async_sleep_and_show(self):
        while(not False): 
            log("async")
            await asyncio.sleep(2)
            self.show_frame(PageFrame.MAIN)  # Show the main page
            log("async [END]")
            await asyncio.sleep(5)

        
    def load(self, file: str, from_file: str=None) -> None:
        self.app.load_data(file, from_file)
        # asyncio.run(self.app.load_data(file)) # FIXME
        # FIXME
        # TODO
        log(" [load]")
        # self.show_frame("main")

    def as_load(self, file: str, from_file: str=None) -> None:
        pass
        # loop = asyncio.get_event_loop()
        # task = loop.create_task(self.as_load_internal(file, from_file))

    async def as_load_internal(self, file: str, from_file: str=None) -> None:
        asyncio.run(self.app.load_data(file, from_file))
        log(" [async] [load]")

    def save_data(self, filename: str) -> None:
        with open(filename, "w") as file:
            converted_data = [ r.to_json() for r in self.app.data ]
            json.dump(converted_data, file)


async def main():
    app = RSSFeederGUI()
    await asyncio.gather(
        asyncio.create_task(app.async_sleep_and_show()),
        asyncio.create_task(app.run())
    )


if __name__ == "__main__":
    asyncio.run(main())
