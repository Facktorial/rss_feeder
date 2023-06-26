import MultiListbox as table
from tkinter import Frame, Text, RIDGE, Label, END, LabelFrame, Entry
import tkinter as tk
from tkinter import ttk

import asyncio

from functools import partial, reduce
from typing import Any, Callable, Final, TypeVar
from dataclasses import dataclass

from Frames.IPage import IPage
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


def count_open_windows(root):
    open_windows = 0
    for window in root.winfo_children():
        if isinstance(window, tk.Toplevel):
            open_windows += 1
    return open_windows


def open_form_window(root: tk.Tk, source_dict, app_state, entry, x, refresh_callback):
	if count_open_windows(root) > 0:
		return

	form_window = tk.Toplevel(root)
	# form_window.grab_set()

	group, title, _ = entry
	log(title)
	# INCORRECT - get copy, but works
	source_record = [x for x in source_dict[group] if x.autor == title][0]
	# CORRECT - get reference
	# source_record = next(x for x in source_dict[group] if x.autor == title)
	# source_record.autor = "XXXXX"
	# form_window.destroy()
	# return

	form_window.title(f"Update {title} source")

	title = Label(form_window, font=FONT_MID, text=f"Update {title} source", pady=30)
	title.pack()

	groups = [gr for gr in source_dict.keys()]
	subgroups = list(set([record.subgroup
		for gr in source_dict.values()
		for record in gr
		if record.group == group or print(record.subgroup, group, record.group)
	]))
	log(subgroups)
	tags = list(set([tag
		for group in source_dict.values()
		for record in group
		for tag in record.flags
	]))
	log(tags)

	form = Form(form_window, groups, subgroups, tags, source_record, source_dict)
	form.pack()

	buttons = Frame(form_window)
	buttons.pack(pady=20)

	cancel_button = ttk.Button(
		buttons, text="Cancel", command=form_window.destroy
	)
	submit_button = ttk.Button(
		buttons,text="Submit",command=partial(form.submit_form, form_window, app_state, refresh_callback)
	)
	cancel_button.grid(row=0, column=0, padx=20)
	submit_button.grid(row=0, column=1, pady=20)


class Form(Frame):
    def __init__(self, parent, groups, subgroups, tags, record, source_dict):
        super().__init__(parent, padx=10)
        self.source_dict = source_dict
        self.parent = parent
        self.record = record
        
        group_label = Label(self, text="Group:")
        subgroup_label = Label(self, text="Subgroup:")
        author_label = Label(self, text="Author:")
        link_label = Label(self, text="Webpage:")
        source_link_label = Label(self, text="Source RSS link:")
        tags_label = Label(self, text="Tags:")
        commentary_label = Label(self, text="Commentary:")
        
        self.group_entry = ttk.Combobox(self, values=groups)
        self.group_entry.current(groups.index(record.group))
        self.group_entry.bind("<<ComboboxSelected>>", self.on_group_selection)
        
        self.subgroup_entry = ttk.Combobox(self, values=subgroups)
        self.subgroup_entry.current(subgroups.index(record.subgroup))
        
        self.tags_entry = MultiSelectCombobox(self, options=tags)
        self.tags_entry.init_selection(tuple(tags.index(tag) for tag in record.flags))

        self.author_entry = Entry(self)
        self.author_entry.insert(0, f"{record.autor}")
        self.author_entry.bind("<KeyRelease>", lambda _: self.update_title())
        self.link_entry = Entry(self)
        self.link_entry.insert(0, f"{record.link}")
        self.source_link_entry = Entry(self)
        self.source_link_entry.insert(0, f"{record.source}")
        self.commentary_text = Text(self, height=5, width=30)

        group_label.grid(row=0, column=0, sticky=tk.E, pady=5, padx=10)
        self.group_entry.grid(row=0, column=1, pady=5, padx=10)

        subgroup_label.grid(row=1, column=0, sticky=tk.E, pady=5, padx=10)
        self.subgroup_entry.grid(row=1, column=1, pady=5, padx=10)

        tags_label.grid(row=2, column=0, sticky=tk.E, pady=5, rowspan=3, padx=10)
        self.tags_entry.grid(row=2, column=1, pady=5, rowspan=3, padx=10)

        author_label.grid(row=0, column=2, sticky=tk.E, pady=5, padx=10)
        self.author_entry.grid(row=0, column=3, pady=5, padx=10, sticky=tk.EW)

        link_label.grid(row=1, column=2, sticky=tk.E, pady=5, padx=10)
        self.link_entry.grid(row=1, column=3, pady=5, padx=10, sticky=tk.EW)

        source_link_label.grid(row=2, column=2, sticky=tk.E, pady=5, padx=10)
        self.source_link_entry.grid(row=2, column=3, pady=5, padx=10, sticky=tk.EW)

        commentary_label.grid(row=3, column=2, sticky=tk.E, pady=5, rowspan=2, padx=10)
        self.commentary_text.grid(row=3, column=3, pady=5, rowspan=2, sticky=tk.NSEW, padx=10)

    def submit_form(self, window, app_state, refresh_callback):
        self.record.group = self.group_entry.get()
        self.record.subgroup = self.subgroup_entry.get()
        # self.record.tags = self.tags_entry.get_selected_options()
        self.record.flags = self.tags_entry.get_selected_options()
        self.record.link = self.link_entry.get()
        self.record.source_link = self.source_link_entry.get()
        # self.record.author = self.author_entry.get()
        self.record.autor = self.author_entry.get()
        # TODO commentary = self.commentary_text.get("1.0", tk.END).strip()
	
        app_state.fetched = False
        
        print("Group:", self.record.group)
        print("Subgroup:", self.record.subgroup)
        print("Tags:", self.record.flags)
        print("Link:", self.record.link)
        print("Source Link:", self.record.source_link)
        print("Author:", self.record.autor)
        print("Commentary:", self.commentary_text.get("1.0", tk.END).strip())

        refresh_callback()
        window.destroy()

    def update_title(self):
        self.parent.title(f"Update {self.author_entry.get()} source") 
        title_widget = self.parent.children['!label']
        title_widget.config(text=f"Update {self.author_entry.get()} source")

    def on_group_selection(self, event):
        selected_item = self.group_entry.get()
        log(selected_item)

        subgroups = list(set([record.subgroup
            for group in self.source_dict.values()
            for record in group
            if record.group == selected_item
        ]))
        log(subgroups)

        self.subgroup_entry['values'] = subgroups


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
				self.refresh_submit
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
