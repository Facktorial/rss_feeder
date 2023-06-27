from tkinter import Frame, Text, RIDGE, Label, END, LabelFrame, Entry
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.messagebox import showerror, showwarning, showinfo

import asyncio
import copy

from functools import partial

from Frames.IPage import IPage
from GUIConf import *
from App import refresh

from MultiSelectCombobox import MultiSelectCombobox

log = partial(print, "[EntryForm] ")


def count_open_windows(root):
    open_windows = 0
    for window in root.winfo_children():
        if isinstance(window, tk.Toplevel):
            open_windows += 1
    return open_windows


def open_form_window(root: tk.Tk, source_dict, app_state, entry, x, refresh_callback, text: str):
	if count_open_windows(root) > 0:
		return

	form_window = tk.Toplevel(root)
	form_window.wm_minsize(720, 540)
	# form_window.grab_set()

	group, title, _ = entry
	log(group)
	# INCORRECT - get copy, but works
	source_record = None
	# if source_dict.get(group, False):
	if title:
		source_record = [x for x in source_dict[group] if x.autor == title]
		if len(source_record):
			source_record = source_record[0]
			log("[REF]", source_record)
		else:
			log(source_dict[group])
			log("[NONE]", source_record)
	else:
		# FIXME
		source_record = [x for x in source_dict.values()]
		source_record = source_record[0]
		source_record = source_record[0]
		source_record = copy.deepcopy(source_record)

		for field_name, field_value in source_record.__annotations__.items():
			setattr(source_record, field_name, field_value())
		source_record.group = group
		log("[COPY]", source_record)
	# CORRECT - get reference
	# source_record = next(x for x in source_dict[group] if x.autor == title)
	# source_record.autor = "XXXXX"
	# form_window.destroy()
	# return

	form_window.title(f"{text} {title} source")

	title = Label(form_window, font=FONT_MID, text=f"{text} {title} source", pady=30)
	title.pack()

	groups = [gr for gr in source_dict.keys()]
	subgroups = list(set([record.subgroup
		for gr in source_dict.values()
		for record in gr
		# if record.group == group or print(record.subgroup, group, record.group)
		if record.group == group
	]))
	log(subgroups)
	tags = list(set([tag
		for group in source_dict.values()
		for record in group
		for tag in record.flags
	]))
	log(tags)

	form = Form(form_window, groups, subgroups, tags, source_record, source_dict, text)
	form.pack()

	buttons = Frame(form_window)
	buttons.pack(pady=20)

	cancel_button = ttk.Button(
		buttons, text="Cancel", command=form_window.destroy
	)
	submit_button = ttk.Button(
		buttons,text="Submit", command=partial(
			form.submit_form, form_window, text, app_state, refresh_callback
		)
	)
	cancel_button.grid(row=0, column=0, padx=20)
	submit_button.grid(row=0, column=1, pady=20)


class Form(Frame):
    def __init__(self, parent, groups, subgroups, tags, record, source_dict, text):
        super().__init__(parent, padx=10)
        self.source_dict = source_dict
        self.parent = parent
        self.record = record
        self.text = text
        
        group_label = Label(self, text="Group:")
        subgroup_label = Label(self, text="Subgroup:")
        author_label = Label(self, text="Author:")
        link_label = Label(self, text="Webpage:")
        source_link_label = Label(self, text="Source RSS link:")
        tags_label = Label(self, text="Tags:")
        commentary_label = Label(self, text="Commentary:")
        
        self.group_entry = ttk.Combobox(self, values=groups)
        if record.group:
            self.group_entry.current(groups.index(record.group))
        self.group_entry.bind("<<ComboboxSelected>>", self.on_group_selection)
        
        self.subgroup_entry = ttk.Combobox(self, values=subgroups)
        if record.subgroup:
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

    def submit_form(self, window, purpose: str, app_state, refresh_callback):
        new_record = copy.deepcopy(self.record)
        for field_name, field_value in new_record.__annotations__.items():
            setattr(new_record, field_name, field_value())

        new_record.group = self.group_entry.get()
        new_record.subgroup = self.subgroup_entry.get()
        # self.record.tags = self.tags_entry.get_selected_options()
        new_record.flags = self.tags_entry.get_selected_options()
        new_record.link = self.link_entry.get()
        new_record.source = self.source_link_entry.get()
        # self.record.author = self.author_entry.get()
        new_record.autor = self.author_entry.get()
        # TODO commentary = self.commentary_text.get("1.0", tk.END).strip()
	
        log("self.record:", self.record)
        log("new_record:", new_record)

        is_new_item: bool = self.record.autor == ""
        is_same_group: bool = self.record.group == new_record.group

        if is_new_item:
            log(self.source_dict[new_record.group])
            self.source_dict[new_record.group].append(new_record)
            log(self.source_dict[new_record.group])
            log("add new")
        else:
            if is_same_group:
                data = self.source_dict[new_record.group]
                data[data.index(self.record)] = new_record
                log("rewrite")
            else:
                self.source_dict[new_record.group].append(new_record)
                item = self.source_dict[self.record.group]
                del item[item.index(self.record)]
                log("switch groups")

        app_state.fetched = False
        
        print("Group:", self.record.group)
        print("Subgroup:", self.record.subgroup)
        print("Tags:", self.record.flags)
        print("Link:", self.record.link)
        print("Source Link:", self.record.source)
        print("Author:", self.record.autor)
        print("Commentary:", self.commentary_text.get("1.0", tk.END).strip())
        print("-----------")
        print("Group:", new_record.group)
        print("Subgroup:", new_record.subgroup)
        print("Tags:", new_record.flags)
        print("Link:", new_record.link)
        print("Source Link:", new_record.source)
        print("Author:", new_record.autor)
        print("Commentary:", self.commentary_text.get("1.0", tk.END).strip())

        log(self.source_dict)

        refresh_callback()
        window.destroy()
        messagebox.showinfo(f"Source entry {purpose}d!", f"You just {purpose}d source entry.")

    def update_title(self):
        self.parent.title(f"{self.text} {self.author_entry.get()} source") 
        title_widget = self.parent.children['!label']
        title_widget.config(text=f"{self.text} {self.author_entry.get()} source")

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
