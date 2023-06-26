import MultiListbox as table
from tkinter import Frame, Entry, RIDGE, Label, END, LabelFrame
import tkinter as tk
from tkinter import ttk

import asyncio

from functools import partial, reduce
from typing import Any, Callable, Final, TypeVar
from dataclasses import dataclass

from Frames.IPage import IPage
from GUIConf import *
from App import PageFrame


log = partial(print, "[EditGroup] ")
Record = TypeVar('Record')


class EditGroup(IPage):
	def __init__(self, parent: IPage, controller):
		super().__init__(parent, controller)
		self.app_state = controller.app
		self.application= controller
		self.options = self.app_state.topics

		self.label_frame = LabelFrame(self, bd=2, text="Add new group")
		self.label_frame.pack(pady=5, padx=5, fill="x")

		self.title = Label(self.label_frame, font=FONT_HEADLINE, text="Add new group")
		self.title.grid(row=0, column=0, columnspan=2, pady=20)

		group_label = Label(self.label_frame, text="Group:")
		self.group_entry = Entry(self.label_frame)
		
		group_label.grid(row=1, column=0, sticky=tk.E, pady=5, padx=10)
		self.group_entry.grid(row=1, column=1, pady=5, padx=10, sticky=tk.W)
		
		submit_button = ttk.Button(
			self.label_frame, text="Submit", command=self.submit_new_group
		)
		submit_button.grid(row=2, column=0, pady=20, columnspan=2)

		self.label_frame.grid_columnconfigure(0, weight=1)
		self.label_frame.grid_columnconfigure(1, weight=1)
		self.label_frame.grid_rowconfigure(0, weight=1)
		self.label_frame.grid_rowconfigure(1, weight=1)
		self.label_frame.grid_rowconfigure(2, weight=1)


		self.combo_group = ttk.Combobox(self, values=self.options)
		self.combo_group.pack(pady=10)
		self.combo_group.bind("<<ComboboxSelected>>", self.on_selection)

   #      self.form_frame = Frame(self)

   #      self.table = MultiListbox(self.form_frame, (
   #          ('Group', 20), ('Author', 20), ('Post count', 20)
   #      ))
   #      self.table.grid(row=0, column=0)
	
   #      self.table.subscribe(
   #          lambda x: open_form_window(
   #              controller.root,
   #              self.app_state.source,
   #              self.app_state,
   #              self.table.get(self.table.curselection()),
   #              x,
   #              self.refresh_submit
   #          )
   #      )

	def on_selection(self, event):
		...
   #      selected_item = self.dropdown.get()
   #      print("Selected item:", selected_item)
   #      toggle_visibility(self.form_frame)

   #      self.table.delete(0, self.table.size())

   #      for record in [rec for rec in self.app_state.data if rec.group==selected_item]:
   #          self.table.insert(END, (record.group, record.name, record.total_posts))	
	def submit_new_group(self):
		if self.group_entry.get() not in self.app_state.topics:
			ngr = self.group_entry.get()
			self.app_state.source[ngr] = []
			self.app_state.topics.append(ngr)
            # self.combo_group['values'] = tuple([ngr, *self.app_state.topics])
			self.combo_group['values'] = tuple([*self.app_state.topics])
			self.application.frames[PageFrame.MAIN].add_tab(ngr)

			self.refresh_submit()

	def refresh(self):
		...
   #      self.on_selection(None)
   #      self.form_frame.forget()
		
	def refresh_submit(self):
		log("REFRESH")
		task = asyncio.create_task(
			self.app_state.load_cached_records(BACKUP_DATA)
		)
		task.add_done_callback(lambda _: self.application.save_callback())
		task.add_done_callback(lambda _: self.application.refresh())
		# task.add_done_callback(lambda _: self.refresh())
