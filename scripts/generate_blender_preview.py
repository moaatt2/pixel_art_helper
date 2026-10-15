"""Generate a blender script that creates a preview of an inlay in blender."""

##########################
### Imports & Settings ###
##########################

# Imports
import tkinter
import pyperclip
from tkinter import filedialog

# Typing imports
from typing import Tuple

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


def linearize_channel(c: int) -> float:
    c /= 255.0

    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def srgb_to_linear(r: int, g: int, b:int) -> Tuple[float,float,float]:
    return tuple(map(linearize_channel, (r, g, b)))
    

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

