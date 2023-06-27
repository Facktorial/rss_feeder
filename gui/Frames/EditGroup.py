import MultiListbox as table
from tkinter import Frame, Entry, RIDGE, Label, END, LabelFrame, messagebox
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo

import asyncio

from functools import partial, reduce
from typing import Any, Callable, Final, TypeVar
from dataclasses import dataclass

from Frames.IPage import IPage
from Frames.EntryForm import open_form_window
from Frames.ManageWindow import open_manage_window
from GUIConf import *
from App import PageFrame


log = partial(print, "[EditGroup] ")
Record = TypeVar('Record')


class AddingGroups(LabelFrame):
	def __init__(self, parent, text, callback, button):
		super().__init__(parent, text=text, bd=2)

		self.title = Label(self, font=FONT_HEADLINE, text=text)
		self.title.grid(row=0, column=0, columnspan=2, pady=10)

		group_label = Label(self, text="Group:")
		self.group_entry = Entry(self)
		
		group_label.grid(row=1, column=0, sticky=tk.E, pady=5, padx=10)
		self.group_entry.grid(row=1, column=1, pady=5, padx=10, sticky=tk.W)
		
		submit_button = ttk.Button(
			self, text=button, command=callback
		)
		submit_button.grid(row=2, column=0, pady=10, columnspan=2)

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)
		self.grid_rowconfigure(1, weight=1)
		self.grid_rowconfigure(2, weight=1)


class RemovingGroups(LabelFrame):
	def __init__(self, parent, text, callback, button):
		super().__init__(parent, text=text, bd=2)

		self.title = Label(self, font=FONT_HEADLINE, text=text)
		self.title.grid(row=0, column=0, columnspan=2, pady=10)

		group_label = Label(self, text="Group:")
		self.group_entry = ttk.Combobox(self, value=parent.options)
		
		group_label.grid(row=1, column=0, sticky=tk.E, pady=5, padx=10)
		self.group_entry.grid(row=1, column=1, pady=5, padx=10, sticky=tk.W)
		
		submit_button = ttk.Button(
			self, text=button, command=callback
		)
		submit_button.grid(row=2, column=0, pady=10, columnspan=2)

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)
		self.grid_rowconfigure(1, weight=1)
		self.grid_rowconfigure(2, weight=1)


class EditGroup(IPage):
	def __init__(self, parent: IPage, controller):
		super().__init__(parent, controller)
		self.app_state = controller.app
		self.application= controller
		self.options = self.app_state.topics

		self.add_frame = AddingGroups(
			self, "Add new group", self.submit_new_group, "Create"
		)
		self.add_frame.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")

		self.remove_frame = RemovingGroups(
			self, "Remove group", self.submit_del_group, "Remove"
		)
		self.remove_frame.grid(row=0, column=1, pady=5, padx=5, sticky="nsew")


		self.add_records = LabelFrame(self, text="Add source records")
		self.add_records.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5)

		self.group_label = Label(self.add_records, text="Manage records", font=FONT_HEADLINE)
		self.group_label.pack(pady=10)
		
		self.buttons = Frame(self.add_records)
		self.buttons.pack(fill="both", pady=10)

		self.delete_some_button = ttk.Button(
			self.buttons, text="Manage sources", command=lambda: open_manage_window(
				self.application.root,
				self.app_state,
				self.combo_group.get(),
				self.refresh_submit
			)
		)

		self.combo_group = ttk.Combobox(self.buttons, values=self.options)
		self.combo_group.grid(row=0, column=0, columnspan=3)
		self.combo_group.bind("<<ComboboxSelected>>", self.on_selection)

		self.add_button = ttk.Button(
			self.buttons, text="Add new source", command=lambda: open_form_window(
				self.application.root,
				self.app_state.source,
				self.app_state,
				(self.combo_group.get(), "", "null"),
				None,
				self.refresh_submit,
				"Create new"
			)
		)
		self.buttons.columnconfigure(0, weight=1)
		self.buttons.columnconfigure(1, weight=1)
		self.buttons.columnconfigure(2, weight=1)

		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		# self.rowconfigure(1, weight=1)

	def on_selection(self, event):
		log(self.combo_group.get())

		self.combo_group.grid_forget()
		self.combo_group.grid(row=0, column=1)

		self.delete_some_button.grid(row=0, column=0)
		self.add_button.grid(row=0, column=2)

	def submit_new_group(self):
		ngr = self.add_frame.group_entry.get()
		if ngr in self.app_state.topics:
			messagebox.showwarning(
				"Trying add existing group",
				f"Unfortunately group \'{ngr}\' already exist."
			)
			return

		self.app_state.source[ngr] = []
		self.app_state.topics.append(ngr)
		self.combo_group['values'] = tuple([*self.app_state.topics])

		main = self.application.frames[PageFrame.MAIN]
		main.add_tab(ngr)
		main.tab_frame.trees[ngr] = main.tab_frame.make_tree(
			main.tab_frame.tree_frame, self.app_state, ngr
		)

		self.app_state.fetched = False
		self.refresh()
		messagebox.showinfo(
			"New group added", f"Group \'{ngr}\' was added."
		)

	def submit_del_group(self):
		ngr = self.remove_frame.group_entry.get()
		del self.app_state.source[ngr]
		self.combo_group['values'] = tuple([*self.app_state.topics])
	
		main = self.application.frames[PageFrame.MAIN]
		main.remove_tab(ngr)
		del main.tab_frame.trees[ngr]

		self.app_state.topics.remove(ngr)
		self.app_state.fetched = False
		self.refresh()
		messagebox.showwarning(
			"Group was deleted", f"You just deleted \'{ngr}\' and its entries."
		)

	def refresh(self):
		self.combo_group['values'] = self.app_state.topics
		self.remove_frame.group_entry['values'] = self.app_state.topics
		self.application.frames[PageFrame.EDIT].dropdown['values'] = self.app_state.topics

	def refresh_submit(self):
		task = asyncio.create_task(
		    self.app_state.load_cached_records(BACKUP_DATA)
		)
		task.add_done_callback(lambda _: self.application.save_callback())
		task.add_done_callback(lambda _: self.application.refresh())
