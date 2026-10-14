"""Generate a blender script that creates a preview of an inlay in blender."""

##########################
### Imports & Settings ###
##########################

# Imports
import tkinter
import pyperclip
from tkinter import filedialog

# The path to the image you want to convert to a blender preview
IMAGE_PATH = ""

window = tkinter.Tk()
window.withdraw()


########################
### Helper Functions ###
########################


def get_image_path() -> str:
    if IMAGE_PATH != "":
        return IMAGE_PATH
    return filedialog.askopenfilename()
    

##################
### Main Logic ###
##################

def generate_preview(image_path: str) -> str:
    return get_image_path()


if __name__ == "__main__":
    script = generate_preview(IMAGE_PATH)
    print(script)
    pyperclip.copy(script)
    print("Script Copied")

