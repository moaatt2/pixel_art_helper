
##########################
### Imports & Settings ###
##########################

import json
from typing import Tuple

PALETTES = [
    ("palettes/ring_lord_palette_derived.json", "RLD")
]

########################
### Helper Functions ###
########################

def linearize_channel(c: int) -> float:
    c /= 255.0

    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def srgb_to_linear(r: int, g: int, b:int) -> Tuple[float,float,float]:
    return linearize_channel(r), linearize_channel(g), linearize_channel(b)


####################
### Setup Output ###
####################

output = """
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

ring_minor = 0.20
ring_major = 1.00

dist_1 = (ring_major + ring_minor) * 2


########################
### Helper Functions ###
########################

# Helper function to shade a ring
def shade_smooth(object):
    polygons = object.data.polygons
    for polygon in polygons:
            polygon.use_smooth = not polygon.use_smooth
    object.data.update()


##########################
### Tutorial Materials ###
##########################

"""


##########################
### Tutorial Materials ###
##########################

# Hard code values for materials from tutorials
tutoral_materials = [
    ("base_tutorial_blue",    "Base Tutorial Blue",    0.019, 0.332, 0.617),
    ("base_tutorial_green",   "Base Tutorial Green",   0.000, 1.000, 0.000),
    ("base_tutorial_grey",    "Base Tutorial Grey",    0.300, 0.300, 0.300),
    ("base_tutorial_yellow",  "Base Tutorial Yellow",  0.708, 0.624, 0.010),
    ("base_tutorial_red",     "Base Tutorial Red",     0.800, 0.000, 0.000),
    ("base_tutorial_orange",  "Base Tutorial Orange",  1.000, 0.333, 0.010),
]

# Add tutorial materials to output
for var_name, color, r, g, b in tutoral_materials:
    output += f"{var_name} = bpy.data.materials.new(name='{color}')\n"
    output += f"{var_name}.use_nodes = True\n"
    output += f"nodes = {var_name}.node_tree.nodes\n"
    output += f"node = nodes.get('Principled BSDF')\n"
    output += f"node.inputs['Base Color'].default_value = ({r:.2f}, {g:.2f}, {b:.2f}, 1.0)\n"
    output += "node.inputs['Roughness'].default_value = 1\n"
    output += "\n\n"


#########################
### Palette Materials ###
#########################

# Itterate through selected palettes
for path, prefix in PALETTES:

    section_length = len(prefix) + 16
    section_bar = "#" * section_length + "\n"

    output += section_bar
    output += f"### {prefix} Palette ###\n"
    output += section_bar
    output += "\n"

    # Read and itterate through palette
    with open(path, "r") as f:
        data = json.load(f)
        for color, hex in data.items():

            # Convert hex to rgb
            r = int(hex[0:2],16)
            g = int(hex[2:4],16)
            b = int(hex[4:6],16)

            # Convert sRGB to Linear
            r, g, b = srgb_to_linear(r, g, b)

            # Create Variable Name
            var_name = f"base_{prefix.lower()}_{color}"

            # Create color name
            color = color.replace("_", " ").title()
            color = f"Base {prefix} {color}"

            output += f"{var_name} = bpy.data.materials.new(name='{color}')\n"
            output += f"{var_name}.use_nodes = True\n"
            output += f"nodes = {var_name}.node_tree.nodes\n"
            output += f"node = nodes.get('Principled BSDF')\n"
            output += f"node.inputs['Base Color'].default_value = ({r:.2f}, {g:.2f}, {b:.2f}, 1.0)\n"
            output += "node.inputs['Roughness'].default_value = 1\n"
            output += "\n\n"




print(output)