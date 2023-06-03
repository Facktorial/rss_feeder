from tkinter import *
from tkinter import ttk
from tkinter import font

from enum import Enum
from typing import Any, Protocol, Final, Type
from dataclasses import dataclass, field
from functools import partial, lru_cache, reduce
import json

from utils import WrappClass, log, create_circle

from src.rss_feeder.xml_feeder import process_feeder
from src.rss_feeder.links_parser import entries_from_json
from src.rss_feeder.my_types import *


log_p = partial(log, " [PAGE] ")

CANVAS_SIZE: Final[int] = 56

FETCHED_COL: Final[str] = "green"
FETCHED_OUTLINE: Final[str] = "#0F0"

NOT_FETCHED_COL: Final[str] = "red"
NOT_FETCHED_OUTLINE: Final[str] = "#F00"


class PageFrame(Enum):
    INIT = "init"
    MAIN = "main"
    EDIT = "edit"
    GROUPNEW = "groupnew"
    INFO = "info"
    APP = "app"


def fetched_circle_color(fetched: bool) -> str:
    return FETCHED_COL if fetched else NOT_FETCHED_COL


def fetched_circle_outline(fetched: bool) -> str:
    return FETCHED_OUTLINE if fetched else NOT_FETCHED_OUTLINE


def _canvas_circle_resize():
    pass


def _canvas_resize(canvas, circle, event):
    # relwidth = event.width / 10
    # print(f"{event.height=} {event.width=}")
    r = 0.45 * min(event.width, event.height)
    x = y = 0.5 * min(event.width, event.height)
    canvas.coords(circle, x-r, y-r, x+r, y+r)


def width_font(size: int, title: str) -> int:
    text_font = font.Font(family="Verdana", size=size)
    char = 'A'
    char_width = text_font.measure(char)
    return len(title) * char_width


@dataclass
class AppState:
    fetched: bool = False
    topics: list[str] = field(default_factory=list)
    source: dict[str, list[FeedEntry]] = field(default_factory=dict) 
    data: list[FeedRecord] = field(default_factory=list)

    def load_data(self, file: str, local_data: str=None) -> None:
    # async def load_data(self, file: str) -> None:
        self.source = entries_from_json(file)
        self.topics = [k for k, _ in self.source.items()]

        if local_data is None:
            self.data, self.topics = asyncio.run(
                process_feeder(self.source, days=DEFAULT_DAYS, sandbox=Sandbox(0))
            )
        else:
            with open(local_data, "r") as file:
                records = json.load(file)
                
                data = []
                for x in records:
                    posts = [PostRecord(**post) for post in x['posts']]
                    data.append(FeedRecord(**x))    
                    data[-1].posts = posts

                self.data = data
            
        self.fetched = True


class App(WrappClass):
    frames: dict[PageFrame, Frame] = {}

    def __init__(self, title: str, pages: dict[PageFrame, Frame], app: AppState):
        super().__init__(title)

        self.pages: dict[PageFrame, Type[Frame]] = pages
        self.frames: dict[PageFrame, Frame] = {}

        self.app = app

        self.heading_frame = Frame(self.root, relief=RIDGE, bd=2)
        self.heading_frame.pack(side="top", fill="x")
        self.label = Label(
            self.heading_frame, text=title, font=("Verdana", 35),
            wraplength=width_font(35, title)
        )
        self.label.pack()
        self.label.pack_propagate(0)

        self.canvas = Canvas(
            self.heading_frame,
            # background="#000",
            width=CANVAS_SIZE, height=CANVAS_SIZE,
            borderwidth=1, highlightthickness=0
        ) 
        self.canvas.place(anchor="nw")

        self.circle = create_circle(
            self.canvas, 20, 20, 19,
            fill=fetched_circle_color(self.app.fetched),
            outline=fetched_circle_outline(self.app.fetched),
            width=1
        )
        self.canvas.bind("<Configure>", partial(_canvas_resize, self.canvas,self.circle))

        self.root.minsize(width_font(35, title) + 2 * (CANVAS_SIZE - 25), 0)

        self.container = Frame(self.root)
        self.container.pack(side="top", fill = "both", expand = True)
    
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)
        
        self.create_pages(self.pages)
        self.current_page: PageFrame = PageFrame.INIT
        self.show_frame(self.current_page)

    def create_pages(self, pages: dict[str, Frame]) -> None:
        for key, F in pages.items():
            frame = F(self.container, self)
            self.frames[key] = frame

    def show_frame(self, frame: PageFrame) -> None:
        self.frames[self.current_page].grid_forget()
        self.current_page = frame
        self.frames[self.current_page].grid()
        # self.root.update()

