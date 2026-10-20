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


########################
### Helper Functions ###
########################

# Helper function to shade a ring
def shade_smooth(object):
    polygons = object.data.polygons
    for polygon in polygons:
            polygon.use_smooth = not polygon.use_smooth
    object.data.update()


#################
### Materials ###
#################

# Black Outline
outline = bpy.data.materials.new(name='Black Outline')
outline.use_nodes = True
outline.use_backface_culling = True
nodes = outline.node_tree.nodes
node = nodes.get("Principled BSDF")
node.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1.0)
node.inputs['Emission Color'].default_value = (0.0, 0.0, 0.0, 1.0)
node.inputs['Roughness'].default_value = 1


{materials}


###################
### Colour Data ###
###################

{colours}


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

        # Get Active ring
        obj = bpy.context.object
        
        # Shade ring smooth
        shade_smooth(obj)

        # Add materials
        obj.data.materials.append(outline)
        obj.data.materials.append(outline)
        
        # Add solidify modifier
        solidify = obj.modifiers.new(name="Solidify", type="SOLIDIFY")
        solidify.thickness = 0.10
        solidify.offset = 0
        solidify.use_flip_normals = True
        solidify.material_offset = 1
"""


##################
### Main Logic ###
##################

def generate_preview(image_path: str) -> str:

    # Open image
    image_path = get_image_path()
    with Image.open(image_path) as image:
        x, y = image.size

        colours = "colours = [\n"

        for _ in range(x):
            colours += f"\t{[None]*y},\n"
        colours += "]"


    return START.format(materials = "", colours = colours)




if __name__ == "__main__":
    script = generate_preview(IMAGE_PATH)
    print(script)
    pyperclip.copy(script)
    print("Script Copied")

