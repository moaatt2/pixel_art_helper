import tkinter
from tkinter import ttk

################################
### Initalize Tkinter Window ###
################################

# Initialize Tkinter Window
window = tkinter.Tk()
window.title("Chainmail Inlay Helper")
window.geometry("600x600")


################
### Menu Bar ###
################

# Initalize menu bar
menu_bar = tkinter.Menu(window)

# Add file menu
file_menu = tkinter.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=None)
file_menu.add_command(label="Save", command=None)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add menu bar to window
window.config(menu=menu_bar)


######################
### Tkinter Layout ###
######################

# Create paned window to split options and image preview
paned = ttk.Panedwindow(window, orient=tkinter.HORIZONTAL)
paned.pack(fill="both", expand=True)

# Container for options on left
sidebar = ttk.Frame(paned)
paned.add(sidebar, weight=1)

# Container for image preview on right
preview = ttk.Frame(paned)
paned.add(preview, weight=3)


###################
### Options Bar ###
###################


#######################
### Start Main Loop ###
#######################

# Start window
window.mainloop()