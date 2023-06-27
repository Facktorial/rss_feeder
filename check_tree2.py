import tkinter as tk
from tkinter import ttk

class CheckboxTreeview(ttk.Treeview):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.tag_configure("unchecked", image=unchecked_img)
        self.tag_configure("checked", image=checked_img)
        self.tag_configure("halfchecked", image=halfchecked_img)
        self.bind("<Button-1>", self._on_click_checkbox)
        self._checked_items = set()

    def insert(self, parent, index, *args, **kwargs):
        item = super().insert(parent, index, *args, **kwargs)
        self.item(item, tags=("unchecked",))
        self._update_checkbox(item)
        return item

    def item_checked(self, item):
        return item in self._checked_items

    def _update_checkbox(self, item):
        tags = self.item(item, "tags")
        if "checked" in tags or "halfchecked" in tags:
            self.item(item, tags=("unchecked",))
        else:
            self.item(item, tags=("checked",))

    def _on_click_checkbox(self, event):
        item = self.identify_row(event.y)
        if item and event.x < self.bbox(item, "text")[0]:
            tags = self.item(item, "tags")
            if "checked" in tags or "halfchecked" in tags:
                self.item(item, tags=("unchecked",))
                self._checked_items.discard(item)
            else:
                self.item(item, tags=("checked",))
                self._checked_items.add(item)

def check_all():
    for item in tree.get_children():
        tree.item(item, tags=("checked",))
        tree._checked_items.add(item)

def delete_items():
    items_to_delete = list(tree._checked_items)
    for item in items_to_delete:
        tree.delete(item)
    tree._checked_items.clear()

root = tk.Tk()
root.title("TreeView Example")

# Load checkbox images
unchecked_img = tk.PhotoImage(file="unchecked.png")
checked_img = tk.PhotoImage(file="checked.png")
halfchecked_img = tk.PhotoImage(file="halfchecked.png")

# Create CheckboxTreeview
tree = CheckboxTreeview(root, columns=("Data",), show="headings")
tree.heading("Data", text="Data")

# Add sample data
data = [("Item 1",), ("Item 2",), ("Item 3",)]
for item_data in data:
    item_id = tree.insert("", "end", values=item_data)

# Configure column
tree.column("Data", width=200)

tree.pack()

# Create buttons
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

check_all_button = tk.Button(buttons_frame, text="Check All", command=check_all)
check_all_button.pack(side="left", padx=5)

delete_button = tk.Button(buttons_frame, text="Delete", command=delete_items)
delete_button.pack(side="left", padx=5)

cancel_button = tk.Button(buttons_frame, text="Cancel", command=root.destroy)
cancel_button.pack(side="left", padx=5)

root.mainloop()
