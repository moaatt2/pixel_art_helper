import tkinter
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from accordian import Accordion, Chord

#################
### Variables ###
#################

tk_image = None


################################
### Initalize Tkinter Window ###
################################

# Initialize Tkinter Window
window = tkinter.Tk()
window.title("Chainmail Inlay Helper")
window.geometry("600x600")

#################
### Functions ###
#################

# Load Image Function
def load_image() -> None:
    global tk_image

    image_path = filedialog.askopenfilename()

    image = Image.open(image_path)

    tk_image = ImageTk.PhotoImage(image)
    
    image_label.config(image=tk_image)


################
### Menu Bar ###
################

# Initalize menu bar
menu_bar = tkinter.Menu(window)

# Add file menu
file_menu = tkinter.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=load_image)
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

# Section for Image Options
image_options = Chord(acc, title='Image Options', bg='white')

# Section for Pattern Options
pattern_options = Chord(acc, title='Pattern Options', bg='white')

# append list of chords to Accordion instance
acc.append_chords([palette_options, image_options, pattern_options])
acc.pack(fill='both', expand=1)


#######################
### Palette Options ###
#######################

# Create container for spacer and accordian menu
palette_option_wrapper = ttk.Frame(palette_options)
palette_option_wrapper.pack(fill="x")

# Create spacer to increase clarity of heirarchy
palette_option_spacer = ttk.Frame(palette_option_wrapper, width=10)
palette_option_spacer.pack(side="left", fill="y")


# Initialze Accordian sidebar menu
palette_acc = Accordion(palette_option_wrapper)

# Section for Palette Selection
palette_selection = Chord(palette_acc, title='Palette Selection', bg='white')
tkinter.Label(palette_selection, text='hello world', bg='white').pack()

# Manual Color Matching
manual_matches = Chord(palette_acc, title='Manual Color Matches', bg='white')
tkinter.Label(manual_matches, text='hello world', bg='white').pack()

# append list of chords to Accordion instance
palette_acc.append_chords([palette_selection, manual_matches])
palette_acc.pack(side='left', fill="both", expand=True)


#####################
### Image Options ###
#####################

# Create container for spacer and accordian menu
image_option_wrapper = ttk.Frame(image_options)
image_option_wrapper.pack(fill="x")

# Create spacer to increase clarity of heirarchy
image_option_spacer = ttk.Frame(image_option_wrapper, width=10)
image_option_spacer.pack(side="left", fill="y")

# Create accordian menu
iamge_acc = Accordion(image_option_wrapper)

# Section for Resizing Image
resize_section = Chord(iamge_acc, title='Resize Image', bg='white')
tkinter.Label(resize_section, text='hello world', bg='white').pack()

# Section for handling rotation of the image
rotate_section = Chord(iamge_acc, title='Rotate Image', bg='white')
tkinter.Label(rotate_section, text='hello world', bg='white').pack()

# Add sections to accordian menu and pack
iamge_acc.append_chords([resize_section, rotate_section])
iamge_acc.pack(side='left', fill="both", expand=True)


#######################
### Pattern Options ###
#######################

# Create container for spacer and accordian menu
pattern_option_wrapper = ttk.Frame(pattern_options)
pattern_option_wrapper.pack(fill="x")

# Create spacer to increase clarity of heirarchy
pattern_option_spacer = ttk.Frame(pattern_option_wrapper, width=10)
pattern_option_spacer.pack(side="left", fill="y")

# Create Variable
pattern_option = tkinter.StringVar(pattern_option_wrapper, "base")

# Add Radio Options
tkinter.Radiobutton(pattern_option_wrapper, text="Base image",              variable=pattern_option, value="base",    indicator=0).pack(fill="x")
tkinter.Radiobutton(pattern_option_wrapper, text="Palette Applied",         variable=pattern_option, value="palette", indicator=0).pack(fill="x")
tkinter.Radiobutton(pattern_option_wrapper, text="Chainmail - Half Strech", variable=pattern_option, value="half",    indicator=0).pack(fill="x")
tkinter.Radiobutton(pattern_option_wrapper, text="Chainmail - Right Way",   variable=pattern_option, value="right",   indicator=0).pack(fill="x")
tkinter.Radiobutton(pattern_option_wrapper, text="Chainmail - Wrong Way",   variable=pattern_option, value="wrong",   indicator=0).pack(fill="x")

#####################
### Image Section ###
#####################

# Create Image section
image_label = tkinter.Label(preview, image=tk_image)
image_label.pack(fill="both", expand=True)


#######################
### Start Main Loop ###
#######################

# Start window
window.mainloop()