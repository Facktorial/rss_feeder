from tkinter import Frame, RIDGE, Label, END
from tkinter import ttk

from functools import partial, reduce
from typing import Any, Callable, Final, TypeVar
from dataclasses import dataclass

from Frames.IPage import IPage
from Frames.PostFrame import PostFrame
from GUIConf import *

from utils import open_url

from PIL import ImageTk, Image

from src.rss_feeder.my_types import FeedRecord


log = partial(print, "[TabFrame] ")
Record = TypeVar('Record')


def on_star_click(tree, images, app, event) -> None:
    item_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)
    if column_id == '#0' and 2.5 * TREE_IMG_SIZE <= event.x <= 3.5 * TREE_IMG_SIZE:
        item = tree.item(item_id)

        if item["values"][1] == "?":
            return

        log(item)
        is_starred: bool = item["image"][0] == str(images[STAR])

        item["image"] = images[NOT_STAR] if is_starred else images[STAR]
        tree.item(item_id, **item)
        app.fetched = False

        for record in app.data:
            if record.name == item["values"][0]:
                for post in record.posts:
                    if post.title == item["values"][1]:
                        post.starred = not is_starred
            

class TabCurrent(Frame):
	def __init__(self, parent: IPage): 
		super().__init__(parent)

		self.curr_headline = Label(
			self, text=f"?", font=FONT_BOLD, fg="blue", cursor="hand2"
		)
		self.curr_headline.grid(row=0, columnspan=2)
		self.curr_headline.bind("<Button-1>", lambda e: open_url(e, self.link))

		self.link = None

		self.curr_link = Label(self, text="Posts: ", font=FONT_BOLD)
		self.posts_curr = Label(self, text=f"?", font=FONT)
		
		self.curr_link. grid(row=1, column=0)
		self.posts_curr.grid(row=1, column=1)

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=3)

	def update_focus(self, record: Record) -> None:
		self.curr_headline.config(text=f"{record.name}")
		self.link = record.feed_link
		num = record.total_posts
		self.posts_curr.config(text=f"{num if num >= 0 else ''}")


class TabOverview(Frame):
	def __init__(
		self, parent: IPage, data: dict[str, Record], get_tab_name_fn: Callable[[], str]
	):
		super().__init__(parent)
		
		filter_data: list[Record] = [entry
			for entry in data.values()
			if entry.group == get_tab_name_fn()
		]
		count_records: int = len(filter_data)
		count_posts: int = reduce(lambda a, rec: a + rec.total_posts, filter_data, 0)

		self.group_label = Label(self, text="Group: ", font=FONT_BOLD)
		self.group_value = Label(self, text=f"{get_tab_name_fn()}", font=FONT)

		self.records_label = Label(self, text="Sources: ", font=FONT_BOLD)
		self.records_value = Label(self, text=f"{count_records}", font=FONT)

		self.posts_label = Label(self, text="Posts: ", font=FONT_BOLD)
		self.posts_value = Label(self, text=f"{count_posts}", font=FONT)

		self.group_label.grid(row=0, column=0)
		self.group_value.grid(row=0, column=1)
		self.records_label.grid(row=1, column=0)
		self.records_value.grid(row=1, column=1)
		self.posts_label.grid(row=2, column=0)
		self.posts_value.grid(row=2, column=1)

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=3)

	def update_tab(self, data: dict[str, Record], tab: str) -> None:
		filter_data: dict[Record] = [entry
			for entry in data.values()
			if entry.group == tab
		]
		count_records: int = len(filter_data)
		count_posts: int = reduce(lambda a, rec: a + rec.total_posts, filter_data, 0)

		self.group_value.config(text=f"{tab}")
		self.records_value.config(text=f"{count_records}")
		self.posts_value.config(text=f"{count_posts}")


class TabFrame(IPage):
	def __init__(self, parent: IPage, controller):
		super().__init__(parent, controller)
		self.app = parent.app

		self.records: dict[str, Record] = dict((x.name, x) for x in controller.app.data)

		self.images: dict[str, ImageTk.PhotoImage] = {
			key: ImageTk.PhotoImage(
				img.resize((TREE_IMG_SIZE, TREE_IMG_SIZE), Image.Resampling.BILINEAR)
			) for (key, img) in controller.images.items()
		}
		
		self.get_tab_name: Callable[[], str] = parent.get_tab_name
		self.overview = TabOverview(self, self.records, self.get_tab_name)
		self.overview.configure(relief=RIDGE, bd=5)
		self.overview.grid(row=0, column=0, sticky="nsew")

		self.current = TabCurrent(self)
		self.current.configure(relief=RIDGE, bd=5)
		self.current.grid(row=1, column=0, sticky="nsew")

		self.tree_frame = Frame(self, relief=RIDGE, bd=3)
		self.tree_frame.grid(row=2, column=0, sticky="nsew")
		self.tree_frame.bind("<Configure>", self.update_treeview_text)
		
		# self.detail_frame = PostFrame(self, controller, self.get_tab_name())
		self.detail_frame = PostFrame(self, controller)
		self.detail_frame.grid(row=0, column=1, rowspan=3, sticky="nsew")

		self.tree: ttk.Treeview = ttk.Treeview()
		self.trees = self.get_trees(self.tree_frame, controller.app)
		self.switch_topics_tree(self.get_tab_name())

		self.tree_frame.grid_columnconfigure(0, weight=1)
		self.tree_frame.grid_rowconfigure(0, weight=1)
		
		self.grid_columnconfigure(0, weight=3, uniform="locked")
		self.grid_columnconfigure(1, weight=7, uniform="locked")
		self.grid_rowconfigure(0, weight=0)
		self.grid_rowconfigure(1, weight=0)
		self.grid_rowconfigure(2, weight=1)

	def make_tree(self, parent, app_state, gr: str) -> ttk.Treeview:
		tree = ttk.Treeview(parent)
		tree.heading('#0', text='Topics')
	
		log("MAKING tree: ", gr)
		
		for idx, d in enumerate(app_state.data):
			if d.group == gr:
				item = tree.insert('', END,
					values=(d.name, "?"),
					text=d.name,
					open=True
				)
				for p_idx, post in enumerate(d.posts):
					if app_state.only_starred and not post.starred:
						continue

					post_item = tree.insert(
						item,
			    	    END,
	                    text=post.title,
			    	    iid=f"{post.title}",
			    	    values=(d.name, post.title),
						image=self.images[STAR if post.starred else NOT_STAR] # TODO
			    	)
		return tree

	def get_trees(self, placement: Frame, app_state: Frame) -> dict[str, ttk.Treeview]:
		trees: dict[str, ttk.Treeview] = {}
		trees[None] = ttk.Treeview(placement)

		for gr in app_state.topics:
			tree = self.make_tree(placement, app_state, gr)

			trees[gr] = tree
			tree.bind("<<TreeviewSelect>>", partial(self.on_tree_change, tree))
			tree.bind('<ButtonPress-1>',
				partial(on_star_click, tree, self.images, self.app)
			)
		return trees

	def on_tree_change(self, tree, event):
		# _ = [print(f"{k}: {v}") for k, v in self.records.items()]
		item = tree.item(self.tree.focus())
		record = None
		post_title = ""
		post_link = ""
		post_date = ""
		if not item["values"]:
			record = FeedRecord(self.get_tab_name(), "?", "?", "?", -1, [])
		else:
			r_item = item["values"][0]
			post_title = item["values"][1]
			record = self.records[r_item]
			posts = [p for p in record.posts if p.title == post_title]
			post_link = posts[0].link if len(posts) else ""
			post_date = posts[0].published if len(posts) else ""

		# self.switch_topics_focus(record.group, record, post_title, post_link)
		self.switch_topics_focus(record, post_title, post_link, post_date)

	def switch_topics(self, tab: str) -> None:
		self.overview.update_tab(self.records, tab)
		self.switch_topics_tree(tab)
		self.on_tree_change(self.tree, None)

	def switch_topics_focus(self, focus_item: Record, title: str, link: str, date: str):
		self.current.update_focus(focus_item)
		self.detail_frame.change_tab(f"{title}", link, date)

	def switch_topics_tree(self, group: str) -> None:
		self.tree.grid_forget()
		self.tree = self.trees[group]
		self.tree.grid(sticky="nsew")

	# FIXME
	def get_shortened_text(self, text: str) -> str:
		frame_width = self.tree_frame.winfo_width()
		if frame_width < (len(text) + 0) * SOME_FACTOR:
			return f"{text[:((frame_width-30)//SOME_FACTOR - 1)]}..."
		return text

	def update_treeview_text(self, event):
		log("update")
		for tree in self.trees.values():
			for item in tree.get_children():
				for post in tree.get_children(item):
					text = self.get_shortened_text(tree.item(post)["values"][1])
					tree.item(post, text=text)

	def refresh(self):
		log("[REFRESH]")
		self.records: dict[str, Record] = dict((x.name, x) for x in self.app.data)
		self.trees = self.get_trees(self.tree_frame, self.app)
		self.switch_topics(self.get_tab_name())
		self.on_tree_change(self.tree, None)

