import tkinter as tk
from tkinter import ttk

class MultiSelectCombobox(ttk.Frame):
    def __init__(self, parent, options):
        super().__init__(parent)
        self.options = options
        self.selected_options = []

        self.listbox = tk.Listbox(self, selectmode=tk.MULTIPLE, exportselection=False)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        for option in self.options:
            self.listbox.insert(tk.END, option)

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def get_selected_options(self):
        self.selected_options = [self.listbox.get(idx) for idx in self.listbox.curselection()]
        return self.selected_options

    def init_selection(self, indices: list[int]) -> None:
        self.listbox.selection_clear(0, tk.END)  # Clear any existing selections
        for index in indices:
            self.listbox.selection_set(index)
