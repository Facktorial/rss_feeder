from tkinter import Frame, RIDGE, Label, END, Canvas, Text, scrolledtext
from tkinter import ttk

from functools import partial
from typing import Final
from datetime import datetime

from utils import open_url
from Frames.IPage import IPage
from GUIConf import *


log = partial(print, "[PostFrame] ")


SOME_TEXT = f"Here belongs some\nparagraphs from post,\n" \
            "but its not yet implemented\n" \
			"ssssss ....\n" \
            "sssss\n\n" \
			"ssssss ....\n" \
            "but its not yet implemented\n" \
			"ssssss ....\n" \
            "sssss\n\n" \
			"ssssss ....\n" \
            "but its not yet implemented\n" \
			"ssssss ....\n" \
            "sssss\n\n" \
			"ssssss ....\n" \
            "but its not yet implemented\n" \
			"ssssss ....\n" \
            "sssss\n\n" \
			"ssssss ....\n" \
            "sssss\n" \
            "sssss\n" \
            "sssss\n" \
            "but its not yet implemented\n" \
			"ssssss ....\n" \
            "sssss\n\n" \
            "but its not yet implemented\n" \
			"ssssss ....\n" \
            "sssss\n\n" \
            "but its not yet implemented\n" \
			"ssssss ....\n" \
            "sssss\n\n" \
			"ssssss ....\n" \
            "sssss"


class PostFrame(IPage):
	def set_font_headline(self, font):
		self.label_detail.config(font=font)

	# def __init__(self, parent: IPage, controller, tab_name: str):
	def __init__(self, parent: IPage, controller):
		super().__init__(parent, controller)
		
		self.detail_frame = Frame(self, relief=RIDGE, bd=RELIEF_DETAIL)
		self.detail_frame.pack(fill="x")

		self.label_detail = Label(
			self.detail_frame,text=f"", font=FONT_HEADLINE,
            wraplength=self.detail_frame.winfo_width(),
			fg="blue", cursor="hand2"
		)
		self.label_detail.pack()

		self.link = None
		self.label_detail.bind("<Button-1>", lambda e: open_url(e, self.link))

		self.label_date = Label(self.detail_frame, text=f"--", font=FONT)
		self.label_date.pack()

		self.cv_frame = Frame(self)
		self.cv_frame.pack(fill="both", expand=True)

		self.scrolled_text = scrolledtext.ScrolledText(
			self.cv_frame, wrap="word", font=FONT_PARAGRAPH
		)
		self.scrolled_text.pack(fill="both", expand=True)
		self.scrolled_text.insert("1.0", SOME_TEXT)

	def change_tab(self, tab: str, link: str, date: str, **kwargs) -> None:
		self.link = link
		self.label_detail.config(text=tab, wraplength=self.detail_frame.winfo_width())

		group = kwargs.get('group', '')
		author = kwargs.get('autor', '')

		who = ""
		if group or author:
			who = f"[{group}, {author}]" if group and author else f"[{group}{author}]"

		if date:
			date_formats = [
			    "%a, %d %b %Y %H:%M:%S %z",
			    "%a, %d %b %Y %H:%M:%S %Z",
			    "%d %b %Y %H:%M:%S %z",
			    "%Y-%m-%dT%H:%M:%S%z"
			]
			
			for format in date_formats:
			    try:
			        orig_date = datetime.strptime(date, format)
			        break
			    except ValueError:
			        pass

			fdate = orig_date.strftime("%a, %d %b %Y")
			self.label_date.config(text=f"{fdate}{who}")

	def refresh(self):
		log("Do we need refresh here?")
