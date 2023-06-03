from tkinter import *

from async_tkinter_loop import main_loop
# from async_tkinter_loop.async_tkinter_loop import main_loop

from functools import partial
from dataclasses import dataclass, field
from typing import Protocol, Any, Callable
import asyncio
import json


import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
sys.path.append(f'{parent}/src')                                    
sys.path.append(f'{parent}/src/rss_feeder')
sys.path.append(f'{parent}/rss_feeder/src/rss_feeder')


log = partial(print, "[GUI] ")


DEFAULT_DAYS = 28
PADX_MAIN = 8
PADY_MAIN = 5
PADX = 2
PADY = 2
ROWSPAN = 2
COLSPAN = 2

LOGIN = "DVO0226"
FNAME = "Jakub"
LNAME = "Dvorak"


def header_label(frame: Tk) -> LabelFrame:
    footer = LabelFrame(frame, text="Footer")
    footer.footer_text_login = Label(footer, text=LOGIN, font=("ComicSans", 8))
    footer.footer_text_fname = Label(footer, text=FNAME, font=("ComicSans", 8))
    footer.footer_text_lname = Label(footer, text=LNAME, font=("ComicSans", 8))
    return footer 


def header_pack(footer_frame: Tk) -> None:
    footer_frame.footer_text_lname.pack(side="bottom")
    footer_frame.footer_text_fname.pack(side="bottom")
    footer_frame.footer_text_login.pack(side="bottom")


def change_theme(root):
    # NOTE: The theme's real bane is azure-<mode>
    if root.tk.call("ttk::style", "theme", "use") == "azure-dark":
        root.tk.call("set_theme", "light")
    else:
        root.tk.call("set_theme", "dark")


def create_circle(canvas, x, y, r, width=0, **kwargs):
    # return canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)
    return canvas.create_oval(x-r, y-r, x+r, y+r, width=width, **kwargs) 


def create_circle_arc(canvas, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return canvas.create_arc(x-r, y-r, x+r, y+r, **kwargs)


class WrappClass:
    def __init__(self, title_name: str):
        self.root = Tk()

        # Set the initial theme
        self.root.call("source", "azure.tcl")
        self.root.call("set_theme", "dark")

        self.root.title(title_name)

    async def run(self):
        await main_loop(self.root)


ComposableFunction = Callable[[Any], Any]

def compose(*functions: ComposableFunction) -> ComposableFunction:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)

