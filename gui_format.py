import tkinter
from tkinter import ttk
from accordian import Accordion, Chord

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
sidebar = ttk.Frame(paned, borderwidth=1, relief="solid")
paned.add(sidebar, weight=1)

# Container for image preview on right
preview = ttk.Frame(paned, borderwidth=1, relief="solid")
paned.add(preview, weight=3)


###################
### Options Bar ###
###################

# Initialze Accordian sidebar menu
acc = Accordion(sidebar)

# Section for Palette Options
palette_options = Chord(acc, title='Palette Options', bg='white')
# tkinter.Label(palette_options, text='hello world', bg='white').pack()

# Section for Image Options
image_options = Chord(acc, title='Image Options', bg='white')
tkinter.Label(image_options, text='hello world', bg='white').pack()

# Section for Pattern Options
pattern_options = Chord(acc, title='Pattern Options', bg='white')
tkinter.Label(pattern_options, text='hello world', bg='white').pack()

# append list of chords to Accordion instance
acc.append_chords([palette_options, image_options, pattern_options])
acc.pack(fill='both', expand=1)


#######################
### Palette Options ###
#######################

# Initialze Accordian sidebar menu
palette_acc = Accordion(palette_options)

# Section for Palette Selection
palette_selection = Chord(palette_acc, title='Palette Selection', bg='white')
tkinter.Label(palette_selection, text='hello world', bg='white').pack()

# Manual Color Matching
manual_matches = Chord(palette_acc, title='Manual Color Matches', bg='white')
tkinter.Label(manual_matches, text='hello world', bg='white').pack()

# append list of chords to Accordion instance
palette_acc.append_chords([palette_selection, manual_matches])
palette_acc.pack(fill='both', expand=1)



#####################
### Image Options ###
#####################



#######################
### Start Main Loop ###
#######################

# Start window
window.mainloop()