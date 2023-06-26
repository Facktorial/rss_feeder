import tkinter as tk
from tkinter import ttk
from functools import partial

from AppState import FetchData, write_config
from GUIConf import *
from Frames.PostFrame import PostFrame


log = partial(print, "[SearchWindow] ")


def wrap_text(listbox: tk.Listbox, found):
    font = tk.font.Font(font=listbox.cget("font"))
    width = listbox.winfo_width()

    for index in range(listbox.size()):
        text = listbox.get(index)

        if font.measure(text) > width:
            words = text.split()
            new_text = ""
            line = ""
            for word in words:
                if font.measure(new_text + " " + word) < width:
                    new_text += " " + word
                else:
                    new_text += "..."
                    break

            listbox.delete(index)
            listbox.insert(index, new_text)
			
            found[new_text] = found[text]
            del found[text]


def open_search_window(root: tk.Tk, app):
    search_window = tk.Toplevel(root)
    search_window.grab_set()
    search_window.title("Searching posts")
    
    posts = [(record.group, post)
        for record in app.app.data
        for post in record.posts
    ]
    found = {}

    title = tk.Label(search_window, font=FONT_MID, text="Start typing...")
    title.pack(pady=10)

    entry = tk.Entry(search_window)
    entry.pack()

    results = tk.Listbox(search_window, width=RESULTS_WIDTH)
    results.pack(pady=10)
    
    def update_list_box(found):
        results.delete(0, tk.END)
        _ = [results.insert(tk.END, title) for title in found.keys()]
        wrap_text(results, found)

    def check_query(found, e):
        typed: str = entry.get()

        if typed == '':
            found = {post.title: (group, post) for group, post in posts}
        else:
            found.clear()
            for group, post in posts:
                if typed.lower() in post.title.lower():
                    found[post.title] = (group, post)
        
        update_list_box(found)

    entry.bind("<KeyRelease>", lambda e: check_query(found, e))

    post = PostFrame(search_window, app)
    post.set_font_headline(FONT_BOLD)
    post.pack()

    def create_post_frame(e):
        selected_index = results.curselection()
        if selected_index:
            log(found)
            post_index = int(selected_index[0])
            key = results.get(post_index)
            group, selected = found[key]
            post.change_tab(
                f"{selected.title}", selected.link, selected.published, group=group
            )

    results.bind("<<ListboxSelect>>", create_post_frame)

    butts = tk.Frame(search_window)
    butts.pack(pady=20)

    # apply_button = tk.Button(butts, text="Cancel", command=search_window.destroy)
    # apply_button.pack(side="left")
