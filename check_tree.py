import tkinter as tk
from tkinter import ttk

def check_all():
    for item in tree.get_children():
        tree.item(item, values=(True, tree.item(item)['values'][1]))

def delete_items():
    items_to_delete = []
    for item in tree.get_children():
        checked = tree.item(item)['values'][0]
        if checked:
            items_to_delete.append(item)
    for item in items_to_delete:
        tree.delete(item)

root = tk.Tk()
root.title("TreeView Example")

# Create TreeView
tree = ttk.Treeview(root, columns=("Checkbox", "Data"), show="headings")
tree.heading("Checkbox", text="Checkbox")
tree.heading("Data", text="Data")

# Add sample data
data = [("Item 1", "Data 1"), ("Item 2", "Data 2"), ("Item 3", "Data 3")]
for item_data in data:
    item_id = tree.insert("", "end", values=(False, item_data[0], item_data[1]))

# Configure checkbox column
tree.column("Checkbox", width=100)
tree.column("Data", width=200)

# Create checkboxes
def toggle_checkbox(event):
    item_id = tree.identify_row(event.y)
    values = tree.item(item_id)['values']
    checked = not values[0]
    tree.item(item_id, values=(checked, values[1]))

tree.bind("<Button-1>", toggle_checkbox)

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
