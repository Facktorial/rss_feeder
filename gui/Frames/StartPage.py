from tkinter import *
import tkinter as tk
from tkinter import ttk

from functools import partial
from typing import Final

from utils import create_circle, log
from App import AppState

from Frames.frames import *
from rss_feeder.my_types import PostRecord


class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.heading_button_frame = header_buttons_frame(self.heading_frame, controller) 
        self.heading_button_frame.pack()

        self.tabControl = ttk.Notebook(self)
        self.tabControl.bind("<<NotebookTabChanged>>", self.on_tab_change)
          
        self.tabs = [ Frame(self.tabControl) for _ in parent.tabs ]
        _ = [self.tabControl.add(x, text = x_name) for x, x_name in zip(self.tabs, parent.tabs)]
        self.tabControl.pack(expand = 1, fill ="both", pady=16)

        self.highside_frame = Frame(self.tabControl, relief=RIDGE, bd=2)
        self.main_frame = Frame(self.tabControl, relief=RIDGE, bd=2)
        self.main_frame_left = Frame(self.main_frame, relief=RIDGE, bd=2)
        self.main_frame_right = Frame(self.main_frame, relief=RIDGE, bd=2)
        self.main_frame_right_buttons = Frame(self.main_frame_right, relief=RIDGE, bd=2)
        self.main_frame_right_head = Frame(self.main_frame_right, relief=RIDGE, bd=2)
        self.main_frame_right_body = Frame(self.main_frame_right, relief=RIDGE, bd=2)
        self.highside_frame.pack(side="left")
        self.main_frame.pack(side="right", fill="x")
        self.main_frame_left.pack(side="left")
        self.main_frame_right.pack(side="right")
        self.main_frame_right_buttons.pack()
        self.main_frame_right_head.pack()
        self.main_frame_right_body.pack()


        self.tree: ttk.Treeview = ttk.Treeview()
        self.trees = self.get_trees(self.main_frame_left, parent)
        self.switch_topics_tree(self.get_tab_name())

        self.filter_frame = FilterFrame(self.highside_frame, controller)
        self.add_link_frame = AddLinkFrame(self.highside_frame, controller)
        self.filter_frame.pack(side="top")
        self.add_link_frame.pack(side="top")

        # self.label_detail0 = Label(self.main_frame_left, text ="\n\nHere comes\n\nthe\n\ntree-like\n\nstructure\n\nmade of\n\nsources.")

        # self.termf = Frame(self.main_frame_left, width = 400, height = 200)

        # self.termf.pack(fill=BOTH, expand=YES)
        # self.wid = self.termf.winfo_id()
        # os.system('xterm -into %d -geometry 80x200 -sb &' % self.wid)
        
        # self.label_detail0.pack()

        # _ = [
        #     Label(x, text =f"Welcome to\n{x_name}").grid(column = 0, row = 0, padx = 50, pady = 50) 
        #     for x, x_name in zip(self.tabs, parent.tabs)
        # ]

        self.but4 = Button(self.main_frame_right_buttons, text="Info", command=lambda : controller.show_frame(AppInfoPage))
        self.but5 = Button(self.main_frame_right_buttons, text="Edit", command=lambda : controller.show_frame(EditPage))
        self.but6 = Button(self.main_frame_right_buttons, text="Remove", command=lambda : controller.show_frame(EditPage))
        self.but4.pack(side="right")
        self.but5.pack(side="right")
        self.but6.pack(side="right")

        self.label_detail = Label(self.main_frame_right_head, text ="Detail of x\nType of x", font=("Verdana", 35))
        self.label_detail.pack()
        self.label_detail2 = Label(self.main_frame_right_body, text ="Detail of x\n\nHere comes\n\nthe\n\nText.")
        self.label_detail2.pack()
        
        # self.view_frame = Frame(self.main_frame, relief=RIDGE, bd=5)
        # self.v_l = Label(self.view_frame, text ="Welcome to\n{x_name}")
        # self.v_l.pack()
        # self.view_frame.pack(side="right")

    def on_tab_change(self, event):
        self.switch_topics_tree(self.get_tab_name())

    def get_tab_name(self) -> str:
        return self.tabControl.tab(self.tabControl.select(), "text")

    def switch_topics_tree(self, group: str) -> None:
        self.tree.pack_forget()
        self.tree = self.trees[group]
        self.tree.pack()

    def get_trees(self, placement: Frame, parent: Frame) -> dict[str, ttk.Treeview]:
        trees: dict[str, ttk.Treeview] = {}

        trees[None] = ttk.Treeview(placement)

        for gr in parent.app.topics:
            tree = ttk.Treeview(placement)
            tree.heading('#0', text='Topics')

            # tree.insert('', tk.END, text=gr, iid=f"{gr}", open=True)

            for idx, d in enumerate(parent.app.data):
                if d.group == gr:
                    tree.insert(
                        # f'{d.group}', tk.END, text=d.name, iid=f"{idx}", open=True
                        '', tk.END, text=d.name, iid=f"{idx}", open=True
                    )
                    for p_idx, post in enumerate(d.posts):
                        # log("[XXX] ", post)
                        # if not isinstance(post, PostRecord):
                        #     log(type(post))
                        #     post = PostRecord(**post)
                        tree.insert(
                            f"{idx}",
                            tk.END,
                            text=post.title,
                            iid=f"{d.name}_{p_idx}",
                            open=True
                        )
                        # log(f"{d.group} {p}")

            trees[gr] = tree
        return trees


def header_buttons_frame(master: Frame, controller) -> Frame:
        heading_button_frame = Frame(master, relief=RIDGE, bd=2)

        but0 = Button(heading_button_frame, text="Refresh", command=lambda : controller.show_frame(AppInfoPage))
        but1 = Button(heading_button_frame, text="i", command=lambda : controller.show_frame(AppInfoPage))
        but2 = Button(heading_button_frame, text="Edit", command=lambda : controller.show_frame(EditPage))
        but3 = Button(heading_button_frame, text="Settings", command=lambda : controller.show_frame(GroupInfoPage))
        but0.pack(side="left", fill="x")
        but1.pack(side="left", fill="x")
        but2.pack(side="left", fill="x")
        but3.pack(side="left", fill="x")

        return heading_button_frame


class FilterFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, relief=RIDGE, bd=2)

        self.label = Label(self, text ="\n\nFilter frame\n\n")
        self.label.pack()


class AddLinkFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, relief=RIDGE, bd=2)

        self.label = Label(self, text ="\n\nAdd link frame\n\n")
        self.label.pack()
