
from tkinter import *
import tkinter as tk
from tkinter import ttk
from functools import partial
from typing import Final
# import numpy as np

from utils import create_circle, log
from App import AppState

from Frames.frames import *
from rss_feeder.my_types import PostRecord


class InitPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.label = Label(self, text="INIT PAGE")
        self.label.pack(fill="x")
