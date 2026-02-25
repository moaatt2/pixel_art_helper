import tkinter

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

# TODO

# Have image preview on Right

# Have Options bar, colapsable sections on left


#######################
### Start Main Loop ###
#######################

# Start window
window.mainloop()