import os
import glob
import json
from PIL import Image
from typing import Optional
from itertools import product

#################
### Functions ###
#################


# Return True if pixel is greyscale (r=g=b) false otherwise
def ignore_greyscale(pixel: tuple) -> bool:
    r, g, b = pixel[0], pixel[1], pixel[2]
    if r == g == b:
        return True
    else:
        return False


# Return True if pixel is white (or close) false otherwise
def ignore_white(pixel: tuple, limit: int = 180) -> bool:
    r, g, b = pixel[0], pixel[1], pixel[2]

    if r > limit and g > limit and b > limit:
        return True
    else:
        return False


# Get average color of an image, ignoring pixels that match the ignore function. Return the average color as a hex string.
def get_average_color_ring_lord(filename: str, ignore_function: object = ignore_white) -> Optional[str]:

    # Instantiate accumulators
    total_r, total_g, total_b = 0, 0, 0
    count = 0

    # Open image and loop over all pixels
    with Image.open(filename) as img:
        # img = img.convert("RGB")
        width, height = img.size
        for x, y in product(range(width), range(height)):
            pixel = img.getpixel((x, y))

            # If pixel matches ignore function skip it
            if ignore_function is not None and ignore_function(pixel):
                continue

            # Add values to accumulators
            total_r += pixel[0]
            total_g += pixel[1]
            total_b += pixel[2]
            count += 1


    # Calculate Average color
    if count == 0:
        return None
    else:
        average_r = total_r // count
        average_g = total_g // count
        average_b = total_b // count

        return f"{average_r:02X}{average_g:02X}{average_b:02X}"


def show_area(filename: str, ignore_function: object = ignore_white) -> None:
    with Image.open(filename) as img:
        width, height = img.size

        new_img = Image.new("RGB", (width, height))

        for x, y in product(range(width), range(height)):
            pixel = img.getpixel((x, y))

            if ignore_function is not None and ignore_function(pixel):
                new_img.putpixel((x, y), (0,0,0))
            else:
                new_img.putpixel((x, y), pixel)

        new_img.show()


def show_area_and_color(filename: str, color: str, ignore_function: object = ignore_white) -> None:
    with Image.open(filename) as img:
        width, height = img.size

        new_img = Image.new("RGB", (width*2, height))

        for x, y in product(range(width), range(height)):
            pixel = img.getpixel((x, y))

            if ignore_function is not None and ignore_function(pixel):
                new_img.putpixel((x, y), (0,0,0))
            else:
                new_img.putpixel((x, y), pixel)
        
        # Convert hex to RGB tuple
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)

        # Fill right half of new image with average color
        for x, y in product(range(width), range(height)):
            new_img.putpixel((x+width, y), (r, g, b))

        new_img.show()


def save_area_and_color(src_filename: str, dest_filename: str, color: str, ignore_function: object = ignore_white) -> None:
    with Image.open(src_filename) as img:
        width, height = img.size

        new_img = Image.new("RGB", (width*2, height))

        for x, y in product(range(width), range(height)):
            pixel = img.getpixel((x, y))

            if ignore_function is not None and ignore_function(pixel):
                new_img.putpixel((x, y), (0,0,0))
            else:
                new_img.putpixel((x, y), pixel)
        
        # Convert hex to RGB tuple
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)

        # Fill right half of new image with average color
        for x, y in product(range(width), range(height)):
            new_img.putpixel((x+width, y), (r, g, b))

        new_img.save(dest_filename)


###############
### Scripts ###
###############

# Create settings file if it doesn't exist
if not os.path.exists("ring_lord_palette_settings.json"):
    print("Creating settings file.")
    settings = dict()
    for filename in glob.glob("test_images/ring_lord/ring_images/*.jpg"):
        filename = filename.replace("\\", "/")
        name = filename.split("/")[-1].split(".")[0]

        settings[name] = {
            "color_hex":       None,
            "file_path":       filename,
            "sample_path":     filename.replace("ring_images", "masks"),
            "white_threshold": 180,
        }

    # Save settings to file
    with open("ring_lord_palette_settings.json", 'w') as file:
        json.dump(settings, file, indent=4)

# Load settings
else:
    print("Loading settings file.")
    with open("ring_lord_palette_settings.json", 'r') as file:
        settings = json.load(file)

# Itterate over settings for each ring without a color
for ring_color, data in settings.items():
    if data["color_hex"] is None:
        color = get_average_color_ring_lord(data["file_path"], lambda pixel: ignore_white(pixel, data["white_threshold"]))
        save_area_and_color(data["file_path"], data["sample_path"], color, lambda pixel: ignore_white(pixel, data["white_threshold"]))
        settings[ring_color]["color_hex"] = color
        print(f"{ring_color}: {color}")
    
    # Save Updated Settings to file
    with open("ring_lord_palette_settings.json", 'w') as file:
        json.dump(settings, file, indent=4)


# Create Palette file from settings
out = dict()
for ring_color, data in settings.items():
    out[ring_color] = data["color_hex"]
with open("palettes/ring_lord_palette_derived.json", 'w') as file:
    json.dump(out, file, indent=4)