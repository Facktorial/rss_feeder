import tkinter as tk
from tkinter import ttk

from AppState import FetchData, write_config
from utils import change_theme
from GUIConf import *

import asyncio


def open_setting_window(root: tk.Tk, app):
    settings_window = tk.Toplevel(root)
    settings_window.grab_set()
    settings_window.title("Settings")
    
    title = tk.Label(settings_window, font=FONT_MID, text="Settings")
    title.pack(pady=10)

    days_label = tk.Frame(settings_window)
    days_label.pack()

    default_days_label = tk.Label(days_label, text="Scanning period:")
    default_days_label.grid(row=0, column=0)

    default_days_entry = tk.Entry(days_label)
    default_days_entry.grid(row=0, column=1)
    default_days_entry.insert(0, f"{app.app.config.default_days}")

    def toggle_theme():
        change_theme(root)

    switch_label = tk.Label(days_label, text="Change Theme:")
    switch_label.grid(row=1, column=0)

    switch_button = ttk.Checkbutton(days_label, command=toggle_theme)
    switch_button.grid(row=1, column=1)

    starred_label = tk.Label(days_label, text="Show only starred:")
    starred_label.grid(row=2, column=0)

    checkbox_var = tk.BooleanVar(value=app.app.only_starred)
    starred_button = ttk.Checkbutton(days_label, variable=checkbox_var)
    starred_button.grid(row=2, column=1)

    butts = tk.Frame(settings_window)
    butts.pack(pady=20)

    cancel_button = tk.Button(butts, text="Cancel", command=settings_window.destroy)
    cancel_button.pack(side="left")

    def apply_settings() -> None:
        default_days = default_days_entry.get()

        if (app.app.config.default_days != int(default_days)):
            app.app.fetched = False
            app.app.config.default_days = int(default_days)
            write_config(CONF_FILE, app.app.config)

            task = asyncio.create_task(app.app.load_data(TEST, BACKUP_DATA, FetchData.FETCH))
            task.add_done_callback(lambda _: app.save_callback())
            task.add_done_callback(lambda _: app.refresh())

        if checkbox_var.get() != app.app.only_starred:
            app.app.only_starred = checkbox_var.get()
            app.refresh()

        settings_window.destroy()

    apply_button = tk.Button(butts, text="Apply", command=apply_settings)
    apply_button.pack(side="left")

