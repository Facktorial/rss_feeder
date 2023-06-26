from tkinter import Frame
from functools import partial
from abc import ABC, abstractmethod


class IPage(ABC, Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

    @abstractmethod
    def refresh(self):
        """Function to re-manage placing (to adjust to container)."""
