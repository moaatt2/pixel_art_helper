import json
import math
from PIL import Image
from typing import Tuple

################
### Settings ###
################

# Cost settings
rings_per_bag       = 300
cost_per_bag_matte  = 7.58
cost_per_bag_bright = 9.12

# Palette Choice
palette_file = "palettes/ring_lord_palette_derived.json"

#################
### Load Data ###
#################

# Load palette
with open(palette_file, "r") as f:
    palette = json.load(f)


#################
### Functions ###
#################

# Returns a count of pixels by color in the image
def rings_by_color(file: str) -> dict:

    # Define output dictionary
    out = dict()

    # Iterate through pixels and count colors
    with Image.open(file) as img:
        for pixel in img.get_flattened_data():
            color = f"{pixel[0]:02X}{pixel[1]:02X}{pixel[2]:02X}"
            if color in out:
                out[color] += 1
            else:
                out[color] = 1
    
    return out


# Returns a count of pixels by palette name
def convert_to_palette(color_count: dict, palette: dict) -> dict:
    
    # Define output dictionary
    out = dict()

    # Invert palette
    palette_inv = {k: v for v, k in palette.items()}

    # Itterate through counted colors and convert to palette colors
    for color, count in color_count.items():
        name = palette_inv[color]
        out[name] = count
    
    return out


# Return the cost of the project and the breakown of the cost
def calculate_cost(rings_by_palette: dict) -> Tuple[float, dict]:
    global rings_per_bag, cost_per_bag_bright, cost_per_bag_matte

    # Instantiate output variables
    cost = 0
    breakdown = dict()

    # Itterate through palette
    for name, count in rings_by_palette.items():
        bags = math.ceil(count/rings_per_bag)

        if "matte" in name:
            cost += cost_per_bag_matte * bags
        else:
            cost += cost_per_bag_bright * bags

        breakdown[name] = {
            "rings": count,
            "bags": bags,
        }

    return cost, breakdown


# Generate a section of a markdown 
def generate_markdown(filename: str, cost: float, breakdown: dict) -> str:
    global rings_per_bag

    # Instantiate output variable
    out = ""

    # Section name
    name = filename.split('/')[-1][:-39]
    out += f"## {name}\n\n"

    # Source image
    out += "### Source Image\n\n"
    out += f'<img src="{{{{ site.baseurl }}}}{{{{ page.image_path }}}}/{name}.bmp" style="max-height: min(200px, 95vh)">\n\n\n'

    # Palette Application
    out += "### Palette Applied\n\n"
    out += f'<img src="{{{{ site.baseurl }}}}{{{{ page.image_path }}}}/{name}_ring_lord_palette_derived_in_stock.bmp" style="max-height: min(200px, 95vh)">\n\n\n'

    # Ring Version
    out += "### Ring Version\n\n"
    out += f'<img src="{{{{ site.baseurl }}}}{{{{ page.image_path }}}}/{name}_rings.bmp" style="max-height: min(200px, 95vh)">\n\n\n'

    # Cost Info
    out += "### Cost Info\n\n"
    out += f"Total Cost: ${cost:.2f}\n"

    # Write total rings
    total_rings = sum([v["rings"] for v in breakdown.values()])
    out += f"Total Rings: {total_rings}\n"

    # Write rings purchased
    rings_purchased = sum([v["bags"] * rings_per_bag for v in breakdown.values()])
    out += f"Rings Purchased: {rings_purchased}\n\n"

    # Write out breakdown
    for color, data in breakdown.items():
        out += f"* {color}:\n"
        out += f"\t* Bags:  {data['bags']}\n"
        out += f"\t* Rings: {data['rings']}\n"
        out += f"\t* Extra Rings: {data['bags'] * rings_per_bag - data['rings']}\n"
    
    out += "\n\n"

    return out


#############
### Tests ###
#############

# # Test Rings by color
# print(rings_by_color("test_images/outputs/exdeath_ring_lord_palette_derived_in_stock.bmp"))
# print()

# # Test convert to palette
# color_count = rings_by_color("test_images/outputs/exdeath_ring_lord_palette_derived_in_stock.bmp")
# print(convert_to_palette(color_count, palette))
# print()

# # Test calculate cost
# color_count = rings_by_color("test_images/outputs/exdeath_ring_lord_palette_derived_in_stock.bmp")
# rings_by_palette = convert_to_palette(color_count, palette)
# print(calculate_cost(rings_by_palette))
# print()

# Test generate markdown
filename = "test_images/winner/metroid_c1_2x2_ring_lord_palette_derived_in_stock.bmp"
color_count = rings_by_color(filename)
rings_by_palette = convert_to_palette(color_count, palette)
cost, breakdown = calculate_cost(rings_by_palette)
print(generate_markdown(filename, cost, breakdown))
print()


