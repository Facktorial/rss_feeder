from tkinter import *
import tkinter as tk
from tkinter import ttk
from utils import create_circle, log
from App import AppState
from functools import partial
# import numpy as np


class EditPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.label = Label(self, text ="Editpage", font=("Verdana", 35))
        self.label.pack()
        # self.label.grid(row = 0, column = 4, padx = 10, pady = 10)

        self.but1 = Button(self, text="Tlacitko1", command=self.quit)
        self.but2 = Button(self, text="Tlacitko2",
            command=lambda : controller.show_frame(StartPage)
        )
        
        self.but1.pack(side="top")
        self.but2.pack(side="right")

class GroupCreateNewPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.label = Label(self, text ="Create new group page")
        self.label.pack()


class AppInfoPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.but = Button(self, text="Tlacitko7 vede na jinou str", command=lambda : controller.show_frame(EditPage))
        self.but.pack(side="bottom")

        self.label = Label(self, text ="App infopage", font=("Verdana", 35))
        self.label.pack()

        # values: list[int] = [i for i in range(len(parent.tabs))]

        # figure = Figure(figsize=(6, 4), dpi=100) 
        # figure_canvas = FigureCanvasTkAgg(figure, self)
        # NavigationToolbar2Tk(figure_canvas, self)
        # axes = figure.add_subplot()

        # axes.bar(parent.topics, values)
        # axes.set_title("My Topics")
        # axes.set_ylabel('Some random values')

        # figure_canvas.get_tk_widget().pack(side="top", fill=BOTH) # , exapand=1)


class GroupInfoPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # self.label = Label(self, text ="Group infopage")

        # np.random.seed(42)
        # df = pd.DataFrame(np.random.poisson(10,(24,7)))
        # df.columns = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        # df.head()

        # # %matplotlib inline
        # x_range = list(range(24))
        # fig, axes = joypy.joyplot(df, kind="values", x_range=x_range, figsize=(6, 4))
        # axes[-1].set_xticks(x_range);
        # 
        # # figure = Figure(figsize=(6, 4), dpi=100) 
        # figure_canvas = FigureCanvasTkAgg(fig, self)
        # NavigationToolbar2Tk(figure_canvas, self)
        # # axes = figure.add_subplot()

        # figure_canvas.get_tk_widget().pack(side="top", fill=BOTH) # , exapand=1)


class MainOverViewFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.label = Label(self, text ="Overview links")
        self.label.pack()


class QuickDetailPanel(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.label = Label(self, text ="Detail panel")
        self.label.pack()


class ContentViewFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.label = Label(self, text ="Contentview panel")
        self.label.pack()


class TabsPanel(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.label = Label(self, text="Tabs with groubs")
        self.label.pack()

