import MultiListbox as table
from tkinter import Frame, Entry, RIDGE, Label, END, LabelFrame, messagebox, Listbox, Button
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo

from MultiSelectCombobox import MultiSelectCombobox

from typing import Any, Callable, Final, TypeVar
from functools import partial

from Frames.IPage import IPage
from GUIConf import *
from App import PageFrame


log = partial(print, "[ManageWindow] ")
Entry = TypeVar('Entry')
Record = TypeVar('Record')


def open_manage_window(root: tk.Tk, app_state, group: str, refresh_callback):
    def delete_selected():
        result = messagebox.askokcancel(
            "Warning", "Are you sure you want to delete selected entries?"
        )
        if not result:
            return

        selected_indices = list_box.curselection()
        for index in reversed(selected_indices):
            app_state.source[group].pop(index)
            list_box.delete(index)
        refresh_callback()

    def delete_all():
        result = messagebox.askokcancel(
            "Warning", "Are you sure you want to delete all entries?"
        )
        if not result:
            return

        app_state.source[group].clear()
        list_box.delete(0, tk.END)
        form_window.destroy()
        refresh_callback()


    form_window = tk.Toplevel(root)
    form_window.wm_minsize(480, 540)
    form_window.grab_set()
    
    form_window.title(f"Manage sources window - {group}")
    title = Label(
        form_window, font=FONT_MID, text=f"Manage your {group} sources", pady=30
    ).pack()

    list_box = Listbox(form_window, selectmode='multiple', width=80)
    list_box.pack(padx=20, pady=20)

    zipped = [(entry, record)
        for entry in app_state.source[group]
        for record in [r for r in app_state.data if r.group == group]
        if entry.autor == record.name
    ]

    items: dict[str, (Entry, Record)] = {}
    for entry, record in zipped:
        items[entry.autor] = (entry, record) 
        list_box.insert(END, entry.autor)

    buttons = Frame(form_window)
    buttons.pack(fill="both", expand=True, padx=300)

    cancel_button = ttk.Button(
        buttons, text="Cancel", command=form_window.destroy
    )
    cancel_button.grid(row=0, column=0)

    delete_button = ttk.Button(
        buttons, text="Delete selected", command=delete_selected
    )
    delete_button.grid(row=0, column=1)

    delete_all = ttk.Button(
        buttons, text="Delete all", command=delete_all
    )
    delete_all.grid(row=0, column=2)

    buttons.columnconfigure(0, weight=1)
    buttons.columnconfigure(1, weight=1)
    buttons.columnconfigure(2, weight=1)

