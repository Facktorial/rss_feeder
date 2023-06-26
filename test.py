import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def on_tree_select(event):
    item = tree.focus()
    selected_values = tree.item(item)['values']
    print("Selected item:", selected_values)

# Create the main application window
root = tk.Tk()
root.title("Treeview Example")

# img = tk.PhotoImage(file="imgs/star.png")
# img2 = tk.PhotoImage(file="imgs/notstar.png")
img = Image.open("imgs/star.png")
img2 = Image.open("imgs/notstar.png")
image_references = []

def resize_image(tree, image, image_references) -> ImageTk:
    cell_width = tree.column("#0", "width")
    # cell_height = tree.column("#0", "height")
    cell_height = 20
    cell_size = cell_width if cell_width <= cell_height else cell_height
    print(f"({cell_size}, {cell_size})")

    resized_image = image.resize((cell_size, cell_size), Image.ANTIALIAS)

    photo = ImageTk.PhotoImage(resized_image)

    if photo not in image_references:
        image_references.append(photo)
        #FIXME

    return photo

style = ttk.Style()
style.layout(
    "Custom.Treeview.Item",
    [
        ("Treeitem.padding", {"sticky": "nswe", "children":
            [("Treeitem.indicator", {"side": "left", "sticky": ""}),
             ("Treeitem.image", {"side": "left", "sticky": ""}),
             ('Treeitem.focus', {'side': 'left', 'sticky': '', 'children': [
             ("Treeitem.text", {"side": "left", "sticky": "w"})]
         })
        ]        
            })]
)
# style.configure("Treeview", itemstyle="mystyle.Treeview.Item")
# style.configure(
    # "mystyle.Treeview.Item",
    # padding=(90, 0),  # Adjust the padding values here
# )

tree = ttk.Treeview(root, style="mystyle.Treeview", columns=('Column 1', 'Column 2'))
# tree = ttk.Treeview(root, columns=('Column 1', 'Column 2'))
# tree.bind("<Configure>", resize_image)

# Define column headings
tree.heading('#0', text='Item')
# tree.heading('Star', text='Star')
tree.heading('Column 1', text='Value 1')
tree.heading('Column 2', text='Value 2')


# Add sample data to the tree
item1 = tree.insert('', 'end', text='Item 1', image=resize_image(tree, img, image_references), values=('Value 1-1', 'Value 2-1'))
tree.insert(item1, 'end', text='Subitem 1', image=resize_image(tree, img2, image_references), values=('Subvalue 1-1', 'Subvalue 2-1'))
tree.insert(item1, 'end', text='Subitem 2', image=resize_image(tree, img2, image_references), values=('Subvalue 1-2', 'Subvalue 2-2'))

item2 = tree.insert('', 'end', text='Item 2', image=resize_image(tree, img, image_references), values=('Value 1-2', 'Value 2-2'))
tree.insert(item2, 'end', text='Subitem 1', image=resize_image(tree, img2, image_references), values=('Subvalue 1-1', 'Subvalue 2-1'))

item3 = tree.insert('', 'end', text='Item 3', image=resize_image(tree, img, image_references), values=('Value 1-3', 'Value 2-3'))

tree.bind('<<TreeviewSelect>>', on_tree_select)
tree.pack()

def on_image_click(event):
    item_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)
    # if column_id == '#0':  # Check if the click occurred in the image column
    if column_id == '#0' and 20 <= event.x <= 40:
        print("Image clicked for item:", item_id)

tree.bind('<ButtonPress-1>', on_image_click)

# img = Image.open("imgs/star.png")
# img = img.resize((25, 25)) 
# img = ImageTk.PhotoImage(img)
# panel = tk.Label(root, image = img)
# panel.pack(side = "bottom", fill = "both", expand = "yes")

# img2 = Image.open("imgs/notstar.png")
# img2 = img2.resize((25, 25)) 
# img2 = ImageTk.PhotoImage(img2)
# panel2 = tk.Label(root, image = img2)
# panel2.pack(side = "bottom", fill = "both", expand = "yes")


# Start the Tkinter event loop
root.mainloop()
