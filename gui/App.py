from tkinter import *
from tkinter import ttk
from tkinter import font

from enum import Enum
from typing import Any, Callable, Final, Type
from functools import partial, lru_cache, reduce

from utils import WrappClass, log, create_circle

from PIL import Image

from Frames.FilterWindow import open_setting_window
from Frames.SearchWindow import open_search_window
from Observer import Observer, Observable
from AppState import AppState
from GUIConf import *


log_p = partial(log, " [PAGE] ")


CANVAS_SIZE: Final[int] = 56

FETCHED_COL: Final[str] = "green"
FETCHED_OUTLINE: Final[str] = "#0F0"

NOT_FETCHED_COL: Final[str] = "red"
NOT_FETCHED_OUTLINE: Final[str] = "#F00"


# TODO
# class DataState(Enum):
# 	UP_TO_DATE = "up_to_date"
# 	SAVED = "saved"
# 	FETCHED = "fetched"	
# 	OUT_DATED = "outdated"


class PageFrame(Enum):
    INIT = "init"
    MAIN = "main"
    EDIT = "edit"
    GROUP_EDIT = "groupnew"
    # INFO = "info"
    # APP = "app"


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


def refresh(parent):
    parent.refresh()
    parent.save_callback()
    parent.app.fetched = True


def header_buttons_frame(root: Frame, app) -> Frame:
	buts = Frame(root, relief=RIDGE, bd=2)
	
	but0 = Button(buts, text="Save", command=partial(refresh, app))
	but5 = Button(buts, text="Homepage", command=lambda: app.show_frame(PageFrame.MAIN))
	but1 = Button(
        buts, text="Adjust groups", command=lambda: app.show_frame(PageFrame.GROUP_EDIT)
    )
	but2 = Button(buts,text="Update source",command=lambda:app.show_frame(PageFrame.EDIT))
	but6 = Button(
		buts, text="Debug: entries",
		command=lambda: print(f"[DEBUG][ENTRIES]: {app.app.source}")
	)
	but4 = Button(buts, text="Find post", command=partial(open_search_window, root, app))
	but3 = Button(buts, text="Settings", command=partial(open_setting_window, root, app))

	but0.pack(side="left", fill="x")
	but5.pack(side="left", fill="x")
	but1.pack(side="left", fill="x")
	but2.pack(side="left", fill="x")
	but6.pack(side="left", fill="x")
	but4.pack(side="left", fill="x")
	but3.pack(side="left", fill="x")
	
	return buts


class AppObserver(Observer):
	def __init__(self, app: 'App') -> None:
		self.app = app

	def update(self, observable: Observable, prop: str) -> None:
		match prop:
			case "fetched":
				self.data_fetched()
			case "fetch_need":
				pass
			case _:
				pass

		self.update_circle()

	def update_circle(self):
		log("UPDATE CIRCLE")
		log(self.app.app.fetched)
		event = Event()
		event.type = '<<Configure>>'
		event.widget = self.app.canvas
		event.width = self.app.canvas.winfo_width()
		event.height = self.app.canvas.winfo_height()
		
		self.app.circle = create_circle(
		    self.app.canvas, 20, 20, 19,
		    fill=fetched_circle_color(self.app.app.fetched),
		    outline=fetched_circle_outline(self.app.app.fetched),
		    width=1
		)
		_canvas_resize(self.app.canvas, self.app.circle, event)

	def data_fetched(self):
		match list(self.app.frames.keys()):
			case [PageFrame.INIT]:
				log(f"{self.app.app.fetched=}")
				log(self.app.frames)
				self.app.create_pages(self.app.pages)
				self.app.show_frame(PageFrame.MAIN)
			case _:
				pass
	

class App(WrappClass):
	frames: dict[PageFrame, Frame] = {}

	def __init__(
		self, title: str, pages: dict[PageFrame, Frame], app: AppState, imgs: dict[str, str]
	):
		super().__init__(title)
		
		self.pages: dict[PageFrame, Type[Frame]] = pages
		self.frames: dict[PageFrame, Frame] = {}
		self.images: dict[str, Image] = {
			key: Image.open(img) for (key, img) in imgs.items()
		}
		
		self.app: AppState = app
		self.app.add_observer(AppObserver(self))
		
		self.heading_frame = Frame(self.root, relief=RIDGE, bd=2)
		self.heading_frame.pack(side="top", fill="x")
		self.label = Label(
		    self.heading_frame, text=title, font=FONT_HEADLINE,
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
		
		self.heading_frame = header_buttons_frame(self.root, self)
		self.heading_frame.pack(pady=10)
		
		self.container = Frame(self.root)
		self.container.pack(side="top", fill = "both", expand = True)
		
		self.container.grid_rowconfigure(0, weight = 1)
		self.container.grid_columnconfigure(0, weight = 1)
		
		self.create_init_page(self.pages)
		self.save_callback = lambda _: _

	def create_init_page(self, pages: dict[PageFrame, Frame]) -> None:
		self.current_page: PageFrame = PageFrame.INIT
		self.frames[PageFrame.INIT] = pages[PageFrame.INIT](self.container, self)
		self.frames[self.current_page].grid(sticky="nsew")
		self.frames[self.current_page].refresh() # TODO

	def refresh(self) -> None:
		log("REFRESH ALL")
		self.app.fetched = True
		# self.frames[self.current_page].refresh()
		_ = [fr.refresh() for fr in self.frames.values()] 

	def create_pages(self, pages: dict[PageFrame, Frame]) -> None:
		for key, F in pages.items():
			if key == PageFrame.INIT:
				continue
			frame = F(self.container, self)
			self.frames[key] = frame

	def show_frame(self, frame: PageFrame) -> None:
		self.frames[self.current_page].grid_remove()
		self.current_page = frame
		self.frames[self.current_page].grid(sticky="nsew")
		self.frames[self.current_page].refresh() # TODO

