import MultiListbox as table
from tkinter import Frame, Text, RIDGE, Label, END, LabelFrame, Entry
import tkinter as tk
from tkinter import ttk

import asyncio

from functools import partial, reduce
from typing import Any, Callable, Final, TypeVar
from dataclasses import dataclass

from Frames.IPage import IPage
from Frames.EntryForm import open_form_window
from GUIConf import *
from App import refresh

from MultiListbox import MultiListbox
from MultiSelectCombobox import MultiSelectCombobox


log = partial(print, "[EditPage] ")
Record = TypeVar('Record')


def toggle_visibility(item):
    is_visible = item.winfo_viewable()
    if not is_visible:
        # pack.grid_forget()
    # else:
        item.pack()


class EditPage(IPage):
	def __init__(self, parent: IPage, controller):
		super().__init__(parent, controller)
		self.app_state = controller.app
		self.application= controller

		self.title = Label(self, font=FONT_HEADLINE, text="Update source")
		self.title.pack(pady=20)

		self.options = self.app_state.topics

		self.dropdown = ttk.Combobox(self, values=self.options)
		self.dropdown.pack(pady=10)
		self.dropdown.bind("<<ComboboxSelected>>", self.on_selection)

		self.form_frame = Frame(self)

		self.table = MultiListbox(self.form_frame, (
			('Group', 20), ('Author', 20), ('Post count', 20)
		))
		self.table.grid(row=0, column=0)
	
		self.table.subscribe(
			lambda x: open_form_window(
				controller.root,
				self.app_state.source,
				self.app_state,
				self.table.get(self.table.curselection()),
				x,
				self.refresh_submit,
				"Update"
			)
		)

	def on_selection(self, event):
		selected_item = self.dropdown.get()
		print("Selected item:", selected_item)
		toggle_visibility(self.form_frame)

		self.table.delete(0, self.table.size())

		for record in [rec for rec in self.app_state.data if rec.group==selected_item]:
			self.table.insert(END, (record.group, record.name, record.total_posts))	

	def refresh(self):
		self.on_selection(None)
		self.form_frame.forget()
		
	def refresh_submit(self):
		log("REFRESH")
		task = asyncio.create_task(
			self.app_state.load_cached_records(BACKUP_DATA)
		)
		task.add_done_callback(lambda _: self.application.save_callback())
		task.add_done_callback(lambda _: self.application.refresh())
		task.add_done_callback(lambda _: self.on_selection(None))
