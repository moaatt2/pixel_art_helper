import glob
import json
import tkinter
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageOps
from accordian import Accordion, Chord
# from pprint import pprint

#################
### Variables ###
#################

# Set global base image
base_image = None

# Set global preview image
preview_image = None

# Set Global Palette list
palettes = dict()


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
    global base_image

    # Get Path of target image
    image_path = filedialog.askopenfilename()

    # Load image as PIL and store in global variable
    image = Image.open(image_path)
    base_image = image

    # call resize function to display image
    resize_preview()


# Resize the preview to fit section
def resize_preview() -> None:
    global base_image, preview_image

    # Exit the function if the base image has not been loaded yet
    if base_image is None:
        return

    # Get size of the base image and the preview window
    pil_size = base_image.size
    window_size = (preview.winfo_width(), preview.winfo_height())

    # Actually resize the image while keeping aspect ratio
    resized_image = ImageOps.contain(base_image, window_size)

    # Convert resized image to tkinter format
    preview_image = ImageTk.PhotoImage(resized_image)

    # Display Image
    image_label.config(image=preview_image)


# Toggle the container when the header is clicked, but not when the checkbox is clicked
def toggle_color_container(event, check, container, arrow) -> None:
    if event.widget is not check:
        if container.winfo_ismapped():
            container.pack_forget()
            arrow.config(text="▶")
        else:
            container.pack(side="left", fill="x", expand=True)
            arrow.config(text="▼")


# Load Palette Files
def load_palettes() -> None:
    global palettes

    # TODO: Only disable color checkboxes when the palette is disabled, not hide the whole section
    # TODO: Make color sections scrollable
    # TODO: Trigger toggle when arrow is clicked, not just the header
    # TODO: Use cleaner name for palettes, split by '_' and title case?

    # Itterate over palette files
    for path in glob.glob("palettes/*.json"):
        palette_name = path.split("/")[-1].split("\\")[-1].split(".")[0]

        # Load palette files
        with open(path, "r") as f:
            raw = json.load(f)
        
        # Create dict in palettes dict for current palette
        palettes[palette_name] = {
            "enabled": tkinter.BooleanVar(),
            "colors": dict(),
        }

        # Convert hex color codes to RGB tuples and store in palette dict
        for k, v in raw.items():
            r = int(v[0:2], 16)
            g = int(v[2:4], 16)
            b = int(v[4:6], 16)
            palettes[palette_name]["colors"][k] = {
                "rgb": (r, g, b),
                "hexstring": v,
                "enabled": tkinter.BooleanVar(value=True),
            }

    # If no palettes were found alert the user
    if len(palettes) == 0:
        tkinter.Label(palette_selection, text='You have no palettes', bg='white').pack()

    # # Print the palettes for debugging
    # pprint(palettes)

    # Create Palette Sections
    for palette_name in palettes.keys():
        palette = palettes[palette_name]

        # Header Container
        palette_label_container = ttk.Frame(palette_selection)
        palette_label_container.pack(fill="x")

        # Header Button
        palette_status_arrow = ttk.Label(palette_label_container, text="▶")
        palette_status_arrow.pack(side="left")

        # Header Checkbox
        palette_checkbox = ttk.Checkbutton(palette_label_container, text=palette_name, variable=palette["enabled"])
        palette_checkbox.pack(side="left")

        # Container for palette colors
        color_container = ttk.Frame(palette_selection)
        color_container.pack(fill="x")

        # Create Spacer to increase clarity of heirarchy
        ttk.Frame(color_container, width=14).pack(side="left", fill="y")

        # Container for Actual Color Rows
        color_row_container = ttk.Frame(color_container)
        color_row_container.pack(side="left", fill="x", expand=True)

        # Create Color Rows
        for color_name in palette["colors"].keys():
            color = palette["colors"][color_name]

            # Container for each color row
            color_row = ttk.Frame(color_row_container)
            color_row.pack(fill="x")

            # Color Preview
            canvas = tkinter.Canvas(color_row, width=12, height=12, background="#" + color["hexstring"], highlightthickness=0)
            canvas.pack(side="left", padx=2)

            # Color Checkbox
            color_checkbox = ttk.Checkbutton(color_row, text=color_name, variable=color["enabled"], state="disabled")
            color_checkbox.pack(side="left")

        # Hide color container by default
        color_row_container.pack_forget()

        # Event binding to toggle color container when header is clicked, but not when the checkbox is clicked
        palette_label_container.bind("<Button-1>", lambda event, check=palette_checkbox, container=color_row_container, arrow=palette_status_arrow: toggle_color_container(event, check, container, arrow))



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
file_menu.add_command(label="Reload Palettes", command=load_palettes)
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
image_label = tkinter.Label(preview, Image=None)
image_label.pack(fill="both", expand=True)


######################
### Event Bindings ###
######################

# Resize the image as the window is resized
preview.bind("<Configure>", lambda event: resize_preview())


#############################
### Inital Load Functions ###
#############################

load_palettes()


#######################
### Start Main Loop ###
#######################

# Start window
window.mainloop()