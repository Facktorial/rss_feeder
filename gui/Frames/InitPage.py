from tkinter import Frame, Label
from functools import partial
from Frames.IPage import IPage


log = partial(print, "[InitPage] ")


class InitPage(IPage):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.label = Label(self, text="INIT PAGE")
        self.label.pack(fill="x")

    def refresh(self):
        pass
