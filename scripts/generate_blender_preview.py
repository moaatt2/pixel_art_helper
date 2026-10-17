"""Generate a blender script that creates a preview of an inlay in blender."""

##########################
### Imports & Settings ###
##########################

# Imports
import tkinter
import pyperclip
from PIL import Image
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
    

###############################
### Fixed Script Components ###
###############################

START = """
###############
### Imports ###
###############

import bpy
import math


############
### Prep ###
############

# Clear Scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()


##################
### Parameters ###
##################

weave_name = "European 4-in-1"

ring_minor = 0.20
ring_major = 1.20

dist_1 = 1.40 # Distance between rows - fixed at min distance
dist_2 = 1.10 # Distance in rows

angle_1 = math.radians(30)


###################
### Colour Data ###
###################

colours = [
"""


MODEL_CODE = """
##################
### Model Code ###
##################

rows    = len(colours)
columns = len(colours[0])

for i in range(rows):
    for j in range(columns):
        base_dist_y = i * dist_1
        base_dist_x = j * dist_2

        even = i%2 == 0
        mod = 1 if even else -1

        bpy.ops.mesh.primitive_torus_add(
            align="WORLD",
            location=(base_dist_y,base_dist_x,0),
            rotation=(mod*angle_1,0,0),
            major_radius=ring_major,
            minor_radius=ring_minor,
            major_segments=48,
            minor_segments=12,
        )
"""

##################
### Main Logic ###
##################

def generate_preview(image_path: str) -> str:
    out = START[:]

    # Open image
    image_path = get_image_path()
    with Image.open(image_path) as image:
        x, y = image.size


        for _ in range(x):
            out += f"\t{[None]*y},\n"
        out += "]\n\n"



    out += MODEL_CODE

    return out




if __name__ == "__main__":
    script = generate_preview(IMAGE_PATH)
    print(script)
    pyperclip.copy(script)
    print("Script Copied")

