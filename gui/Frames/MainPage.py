import tkinter as tk
from tkinter import ttk
from tkinter import Frame

from functools import partial
from typing import Final

from utils import create_circle
from App import AppState

from Frames.IPage import IPage
from Frames.TabFrame import TabFrame


log = partial(print, "[MainPage] ")


class MainPage(IPage):
	def __init__(self, parent, controller):
		super().__init__(parent, controller)
		
		self.tabControl = ttk.Notebook(self)

		self.app = controller.app

		self.tabs = [Frame(self.tabControl) for _ in controller.app.topics]
		_ = [self.tabControl.add(x, text=x_name)
			 for x, x_name in zip(self.tabs, controller.app.topics)
		]
		self.tabControl.pack(fill="both")
		self.tabControl.bind("<<NotebookTabChanged>>", self.on_tab_change)

		self.tab_frame = TabFrame(self, controller)
		self.tab_frame.pack(expand=1, fill="both")
		
	def refresh(self):
		self.tab_frame.refresh()
		for idx, _ in enumerate(self.tabs):
			tmp = self.tabControl.tab(idx, "text")
			
			if tmp not in self.app.topics:
				self.add_tab(tmp)

	def add_tab(self, tab_name):
		new_tab = Frame(self.tabControl)
		self.tabs.append(new_tab)
		self.tabControl.add(new_tab, text=tab_name)

	def remove_tab(self, tab_name):
		for index, x_name in enumerate(self.app.topics):
			if x_name == tab_name:
				self.tabControl.forget(index)
				self.tabs.pop(index)
				break

	def on_tab_change(self, event):
		self.tab_frame.switch_topics(self.get_tab_name())

	def get_tab_name(self) -> str:
		return self.tabControl.tab(self.tabControl.select(), "text")
