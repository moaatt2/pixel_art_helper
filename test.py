import os
import glob
import json
import numpy as np
from PIL import Image, ImageDraw
from typing import Optional, Tuple
from itertools import product
from math import sqrt, atan2, degrees, sin, cos, exp, radians

################
### Settings ###
################

# Width reduction value assuming a 30 degree angle
ANGLE_FACTOR = 0.866


######################
### Inlay Settings ###
######################

# Ring Settings
RING_WIDTH     = 40
RING_HEIGHT    = 50
RING_THICKNESS = 8
RING_OUTLINE   = 1

# Inlay structure settings
INLAY_DELTA_V  = 26
INLAY_DELTA_H  = 30
INLAY_OFFSET_H = 16

# Horizontal ring split for alternating rows
LEFT_HALF_DX = 13


########################
### Create Ring Sets ###
########################

# Create template image
buf_img = Image.new("RGBA",(RING_WIDTH, RING_HEIGHT))

# Determine ring size from buffer size
x1, y1 = 0, 0
x2, y2 = RING_WIDTH-1, RING_HEIGHT-1

# Use thickness to determine size of inner ring
x3, y3, x4, y4 = x1+RING_THICKNESS, y1+RING_THICKNESS, x2-RING_THICKNESS, y2-RING_THICKNESS

# Draw sample ring in image buffer
draw = ImageDraw.Draw(buf_img)
draw.ellipse((0,0,x2,y2),   fill="white",   outline="black", width=1)
draw.ellipse((x3,y3,x4,y4), fill=(0,0,0,0), outline="black", width=1)

ring_template = np.asarray(buf_img)
ring_white_mask = (ring_template[:, :, :3] == 255).all(axis=-1)

del buf_img


#################
### Load Data ###
#################

# Load wire guage data
with open("data/wire_gauges.json") as file:
    wire_gauges = json.load(file)


################################
### Function Unit Conversion ###
################################

def sin_d(x):
    return sin(radians(x))


def cos_d(x):
    return cos(radians(x))


def atan2_d(y, x):
    return degrees(atan2(y, x))


# Take channel value and apply gamma correction
def gamma_correction(value: float) -> float:
    if value <= 0.04045:
        return value / 12.92
    else:
        return ((value + 0.055) /1.055) ** 2.4


# Helper function to apply CIELABs nonlinear transfer function
def cielab_ntf(value: float) -> float:
    if value > 216 / 24389:
        return value ** (1/3)
    else:
        return value / (72/841) + 4/29


# Helper function to convert RGB to cielab for cie_lab delta e metrics
def rgb_to_cielab(input_color: tuple) -> tuple:
    r, g, b = input_color

    # Normalize RGB
    r = r/255.0
    g = g/255.0
    b = b/255.0
    
    # Apply gamma correction
    r = gamma_correction(r)
    g = gamma_correction(g)
    b = gamma_correction(b)

    # Convert to XYZ
    m = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ])

    x, y, z = m @ np.array([r, g, b])

    # Normalized by white reference - D65
    x = float(x) / 0.95047
    y = float(y) / 1.00000
    z = float(z) / 1.08883

    # Convert to CIELAB
    l = 116 * cielab_ntf(y) - 16
    a = 500 * (cielab_ntf(x) - cielab_ntf(y))
    b = 200 * (cielab_ntf(y) - cielab_ntf(z))

    # Return LAB values
    return (l, a, b)


#################
### Functions ###
#################

# Helper function to find the closest color in the palette to a given input color.
def closest_color_euclidean(input_color: tuple, palette: list) -> tuple:

    # Get components of input color
    r1, g1, b1 = input_color

    # Set default values for loop
    closest_color = None
    min_distance = float('inf')

    # Loop over all colors in palette
    for color in palette:

        # Get components of palette color
        r2, g2, b2 = color
        distance = (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2

        # Check if current color is the closest so far
        if distance < min_distance:
            min_distance = distance
            closest_color = color

    # Return the closest color found
    return closest_color


# Helper function to calculate delta e for 2 colors using cielab 76 formula
def cielab_76(color_1: tuple[float, float, float], color_2: tuple[float, float, float]) -> float:
    l1, a1, b1 = color_1
    l2, a2, b2 = color_2

    squared_distance = (l1-l2)**2 + (a1-a2)**2 + (b1-b2)**2

    return squared_distance ** (1/2)


# Helper function to calculate delta e for 2 colors using cielab 00 formula
def cielab_00(color_1: tuple[float, float, float], color_2: tuple[float, float, float]) -> float:
    l1, a1, b1 = color_1
    l2, a2, b2 = color_2

    kl = 1
    kc = 1
    kh = 1

    dlp = l2 - l1

    lh = (l1 + l2) / 2

    cs1 = (a1**2 + b1**2) ** (1/2)
    cs2 = (a2**2 + b2**2) ** (1/2)

    ch = (cs1 + cs2) / 2

    ap1 = a1 + a1/2 * (1 - sqrt(ch**7/(ch**7 + 25**7)))
    ap2 = a2 + a2/2 * (1 - sqrt(ch**7/(ch**7 + 25**7)))

    cp1 = sqrt(ap1**2 + b1**2)
    cp2 = sqrt(ap2**2 + b2**2)

    chp = (cp1 + cp2) /2
    dcp = cp2 - cp1

    hp1 = atan2_d(b1, ap1) % 360
    hp2 = atan2_d(b2, ap2) % 360

    dhp = None
    if abs(hp2 - hp1) <= 180:
        dhp = hp2 - hp1
    elif (hp2 - hp1) > 180:
        dhp = hp2 - hp1 - 360
    elif (hp2 - hp1) < -180:
        dhp = hp2 - hp1 + 360
    else:
        print("uh-oh")
    
    dHp = 2 * sqrt(cp1 * cp2) * sin_d(dhp/2)

    hhp = None
    if abs(hp1 - hp2) <= 180:
        hhp = (hp1 + hp2) / 2
    elif hp1 + hp2 < 360:
        hhp = (hp1 + hp2 + 360) / 2
    elif hp1 + hp2 > 360:
        hhp = (hp1 + hp2 - 360) / 2
    else:
        print("uh-oh")


    t = 1 - 0.17*cos_d(hhp - 30) + 0.24*cos_d(2*hhp) + 0.32 * cos_d(3*hhp + 6) - 0.20*cos_d(4*hhp - 63)

    sl = 1 + (0.015 * (lh - 50)**2) / sqrt(20 + (lh - 50)**2)

    sc = 1 + 0.045 * chp

    sh = 1 + 0.015 * chp * t

    rt = -2 * sqrt(chp ** 7 / (chp **7 + 25**7)) * sin_d(60 * exp(-1 * ((hhp - 275)/25)**2))

    de = sqrt((dlp/(kl * sl))**2 + (dcp/(kc * sc))**2 + (dHp/(kh * sh))**2 + rt * (dcp/(kc * sc)) * (dHp/(kh * sh)))

    return de


# Find the color in the palette with the lowest delta_e
def closest_color_cie_76(color: tuple, palette: list) -> tuple:
    closest = None
    min_de = float('inf')
    for option in palette:
        de = cielab_76(color, option)

        if de < min_de:
            closest = option
            min_de = de
    
    return closest


# Find the color in the palette with the lowest delta_e
def closest_color_cie_00(color: tuple, palette: list) -> tuple:
    closest = None
    min_de = float('inf')
    for option in palette:
        de = cielab_00(color, option)

        if de < min_de:
            closest = option
            min_de = de
    
    return closest


# Return True if pixel is white (or close) false otherwise
def ignore_white(pixel: tuple, white_level: int = 250) -> bool:
    r, g, b = pixel[0], pixel[1], pixel[2]

    if r > white_level and g > white_level and b > white_level:
        return True
    else:
        return False


####################################
### Image Manipulation Functions ###
####################################

# Rotate an image
def rotate_image(image: Image.Image, angle: float, clockwise: bool = False) -> Image.Image:

    # Adjust angle if clockwise is desired
    angle = -angle if clockwise else angle

    # Rotate image and expand incase it isnt large enough
    return image.rotate(angle, expand=True)


# Resize an image by integer scale factors using pixel duplication
def resize_image(image: Image.Image, width_mult: int, height_mult: int) -> Image.Image:
    width, height = image.size
    new_img = Image.new("RGB", (width * width_mult, height * height_mult))

    for x, y in product(range(width), range(height)):
        pixel = image.getpixel((x, y))
        for dx, dy in product(range(width_mult), range(height_mult)):
            new_img.putpixel((x * width_mult + dx, y * height_mult + dy), pixel)
    
    return new_img


# Apply a palette to an image - replaces colors with the closest color in the palette as determined by the color selection function
def apply_palette(palette: dict, image: Image.Image, color_selection_func: object, selection_func_color_space: str) -> Image.Image:
    # Instantiate color mapping dict
    color_map = dict()

    # If selection function is in cielab color space prep a lookup table to get values
    palette_map = dict()
    palette_lab = list()
    if selection_func_color_space == "cielab":
        for color in palette.values():
            cielab = rgb_to_cielab(color)
            palette_map[str(cielab)] = color
            palette_lab.append(cielab)


    width, height = image.size
    new_img = Image.new("RGB", (width, height))

    # Loop over all pixels in input image
    for x, y in product(range(width), range(height)):

        # get pixel in rgb color
        pixel = image.getpixel((x, y))

        # Find best color
        if str(pixel) in color_map:
            new_color = color_map[str(pixel)]
        elif selection_func_color_space == "cielab":
            pixel_lab = rgb_to_cielab(pixel)
            best_lab = color_selection_func(pixel_lab, palette_lab)
            new_color = palette_map[str(best_lab)]
            color_map[str(pixel)] = new_color
        else:
            new_color = color_selection_func(pixel, list(palette.values()))
            color_map[str(pixel)] = new_color

        # Set color in new image
        new_img.putpixel((x, y), new_color)

    # Return output filename
    return new_img


# Get average color of an image, ignoring pixels that match the ignore function.
def get_average_color_f(image: Image.Image, ignore_function: object = None) -> Optional[str]:

    # Instantiate accumulators
    total_r, total_g, total_b = 0, 0, 0
    count = 0

    width, height = image.size
    for x, y in product(range(width), range(height)):
        pixel = image.getpixel((x, y))

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
        average_r = hex(total_r // count)[-2:]
        average_g = hex(total_g // count)[-2:]
        average_b = hex(total_b // count)[-2:]

        return f"{average_r}{average_g}{average_b}".upper()


# Estimate physical size of resulting inlay project based on wire size
def estimate_size(image: Image.Image, gauge: int, gauge_system: str, internal_diameter: float, units: str) -> Tuple[float, float]:

    # Verify gauge system
    gauge_system = gauge_system.lower()
    assert gauge_system in ('awg', 'swg'), "Invalid gauge system. Must be one of [AWG, SWG]"

    # Find wire diameter
    wire_diameter = wire_gauges[gauge_system][str(gauge)][units]

    # Calculate AR and apply sanity filter
    ar = internal_diameter / wire_diameter
    assert ar >= 2, "ring too small for inlay"

    # Calculate Ring Width
    ring_diameter = 2*wire_diameter + internal_diameter

    width_px, height_px = image.size

    height = ring_diameter * (1 + (height_px - 1)/2)
    width  = ANGLE_FACTOR * (ring_diameter + (ring_diameter - wire_diameter) * (width_px - 1))

    height, width = round(height, 2), round(width, 2)

    return (width, height)


# Create inlay preview from image
def convert_to_inlay(image: Image.Image) -> Image.Image:


    ########################
    ### Create New Image ###
    ########################

    # Create new image
    width, height = image.size
    new_width = (width-1) * INLAY_DELTA_H + RING_WIDTH + INLAY_OFFSET_H
    new_height = (height-1) * INLAY_DELTA_V + RING_HEIGHT
    new_img = np.zeros((new_height, new_width, 4), dtype=np.uint8)


    ##############################
    ### Load Source Image Data ###
    ##############################

    source_data = image.convert("RGBA").load()


    ##############################
    ### Precompute Ring Colors ###
    ##############################

    # Get set of unique colors in source image
    unique_colors = set(tuple(source_data[x, y]) for x, y in product(range(width), range(height)))

    # Create dictionary mapping unique colors to ring templates with that color
    ring_colors = dict()
    for color in unique_colors:
        tmp = ring_template.copy()
        tmp[ring_white_mask] = color
        ring_colors[color] = tmp

    ##################
    ### Draw Image ###
    ##################

    # Handle even layers
    for x, y in product(range(width), range(height)):
        if y%2 == 1:
            continue

        # Get target color
        pixel = source_data[x, y]

        # Full circle co-ordinates
        x1, y1 = x*INLAY_DELTA_H,  y*INLAY_DELTA_V
        
        # Get ring
        ring = ring_colors[tuple(pixel)]

        # Copy ring to image under existing pixels
        sub = new_img[y1:y1+RING_HEIGHT, x1:x1+RING_WIDTH]
        np.copyto(sub, ring, where=(sub == 0).all(axis=-1)[..., None])


    # Handle odd layers
    for x, y in product(range(width), range(height)):
        if y%2 == 0:
            continue

        # Get target color
        pixel = source_data[x, y]

        # Full circle co-ordinates
        x1, y1 = x*INLAY_DELTA_H + INLAY_OFFSET_H,  y*INLAY_DELTA_V
        
        # Get ring
        ring = ring_colors[tuple(pixel)]

        # Copy left of ring to image over existing pixels
        ring_left = ring[:, :LEFT_HALF_DX, :]
        sub = new_img[y1:y1+RING_HEIGHT, x1:x1+LEFT_HALF_DX]
        np.copyto(sub, ring_left, where=(ring_left[...,3] != 0)[..., None])


        # Copy right of ring to image under existing pixels
        ring_right = ring[:, LEFT_HALF_DX:, :]
        sub = new_img[y1:y1+RING_HEIGHT, x1+LEFT_HALF_DX:x1+RING_WIDTH]

        if ring_right.shape != sub.shape:
            print(f"Shape mismatch: {ring_right.shape} vs {sub.shape}")
            print(f"x1: {x1}, y1: {y1}")
            print(f"Ring shape: {ring.shape}")
            print(f"Sub shape: {sub.shape}")
            continue

        np.copyto(sub, ring_right, where=(sub == 0).all(axis=-1)[..., None])

    # Convert numpy array to PIL image
    new_img = Image.fromarray(new_img.astype('uint8'), 'RGBA')

    # Replace alpha with grey and convert to RGB
    grey_layer = Image.new("RGBA", (new_width, new_height), (127,127,127,255))
    new_img = Image.alpha_composite(grey_layer, new_img)
    new_img = new_img.convert("RGB")

    # Return inlay image
    return new_img


###############################
### File Operation Wrappers ###
###############################

# Wrapper to resize an image from a file and save the result to a new file
def resize_image_f(input_file: str, width_mult: int, height_mult: int) -> str:

    image = Image.open(input_file)
    new_img = resize_image(image, width_mult, height_mult)

    # Construct output filename
    input_filename  = input_file.split(".")[0]
    input_extension = input_file.split(".")[-1]
    output_file = f"{input_filename}_{width_mult}x{height_mult}.{input_extension}"

    # Save modified image
    new_img.save(output_file)

    # Return output filename
    return output_file


# Wrapper to rotate an image from a file and save the result to a new file
def rotate_image_f(filename: str, angle: float, clockwise: bool = False) -> str:
    with Image.open(filename) as img:

        # Apply rotate logic
        rotated_img = rotate_image(img, angle, clockwise)

        # Construct output filename
        input_filename  = filename.split(".")[0]
        input_extension = filename.split(".")[-1]
        output_file = f"{input_filename}_rotated.{input_extension}"

        rotated_img.save(output_file)

        return output_file


# Wrapper for apply_palette that operates on files and saves the result to a new file
def apply_palette_f(palette_file: str, image_file: str, color_selection_func: object, selection_func_color_space: str) -> str:

    # Load palette
    with open(palette_file, 'r') as pf:
        palette = json.load(pf)

    # Convert hex colors to RGB tuples
    for name, hex_color in palette.items():
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        palette[name] = (r, g, b)

    # Open image and apply palette    
    with Image.open(image_file) as source:
        new_img = apply_palette(palette, source, color_selection_func, selection_func_color_space)

        # Construct output filename
        input_filename  = image_file.split(".")[0]
        input_extension = image_file.split(".")[-1]
        palette_name    = palette_file.split("/")[-1].split(".")[0]
        output_file = f"{input_filename}_{palette_name}.{input_extension}"

        # Save modified image
        new_img.save(output_file)

        # Return output filename
        return output_file


# Wrapper for get_average_color that operates on files
def get_average_color_f(filename: str, ignore_function: object = None) -> Optional[str]:
    with Image.open(filename) as img:
        return get_average_color_f(img, ignore_function)


# Wrapper for estimate_size that operates on files
def estimate_size_f(filename: str, gauge: int, gauge_system: str, internal_diameter: float, units: str) -> Tuple[float, float]:
    with Image.open(filename) as img:
        return estimate_size(img, gauge, gauge_system, internal_diameter, units)


# Wrapper for convert to inlay that operates on files
def convert_to_inlay_f(filename: str) -> str:

    # Open image and convert to inlay
    with Image.open(filename) as source:
        new_img = convert_to_inlay(source)

        # Construct output filename
        input_filename  = filename.split(".")[0]
        input_extension = filename.split(".")[-1]
        output_file = f"{input_filename}_inlay.{input_extension}"

        # Save modified image
        new_img.save(output_file)

        # Return output filename
        return output_file


# Only run tests when this file is called
if __name__ == "__main__":

    ################
    ### Use case ###
    ################

    # apply_palette("palettes/ring_lord_palette_derived.json", "test_images/blog/finalists/super_metroid_metroid_sprite.bmp", closest_color_euclidean, "rgb")
    # apply_palette("palettes/ring_lord_palette_derived.json", "test_images/blog/finalists/super_metroid_metroid_sprite_2x2.bmp", closest_color_euclidean, "rgb")


    ################################
    ### Inlay Conversion Testing ###
    ################################

    from datetime import datetime as dt

    # Original function
    start = dt.now()
    convert_to_inlay_f("test_images/img_to_ring_testing/test_input.png")
    end = dt.now()
    print(f"\tTest Input: {(end-start).total_seconds():.2f} seconds")

    start = dt.now()
    convert_to_inlay_f("test_images/TADC/caine.bmp")
    end = dt.now()
    print(f"\tCaine: {(end-start).total_seconds():.2f} seconds")

    start = dt.now()
    convert_to_inlay_f("test_images/exdeath_2x2.bmp")
    end = dt.now()
    print(f"\tExdeath 2x2: {(end-start).total_seconds():.2f} seconds")

    #############
    ### Tests ###
    #############

    # # Test the resize_image function
    # input_file = "test_images/pixel_art_pheonix_base.bmp"
    # resize_image(input_file, 2, 2)

    # # Test the apply_palette function
    # palette_file = "palettes/ring_lord_rings.json"
    # image_file = "test_images/pixel_art_pheonix_base.bmp"
    # apply_palette(palette_file, image_file, closest_color_euclidean)

    # ## RGB TO CIELAB tests
    # print("RGB TO CIELAB Black (0, 0, 0)")
    # print("Expected: (0, 0, 0)")
    # print(f"Result:   {rgb_to_cielab((0, 0, 0))}")
    # print()

    # print("RGB TO CIELAB Grey (127, 127, 127)")
    # print("Expected: (53.5850, 0, 0)")
    # print(f"Result:   {rgb_to_cielab((128, 128, 128))}")
    # print()

    # print("RGB TO CIELAB White (255, 255, 255)")
    # print("Expected: (100, 0, 0)")
    # print(f"Result:   {rgb_to_cielab((255, 255, 255))}")
    # print()

    # print("RGB TO CIELAB Red (255, 0, 0)")
    # print("Expected: (53.2408, 80.0925, 67.2032)")
    # print(f"Result:   {rgb_to_cielab((255, 0, 0))}")
    # print()

    # print("RGB TO CIELAB Green (0, 255, 0)")
    # print("Expected: (87.7347, -86.1827, 83.1793)")
    # print(f"Result:   {rgb_to_cielab((0, 255, 0))}")
    # print()

    # print("RGB TO CIELAB Blue (0, 0, 255)")
    # print("Expected: (32.2970, 79.1875, -107.8602)")
    # print(f"Result:   {rgb_to_cielab((0, 0, 255))}")
    # print()


    # ## CIELAB 2000 Delta E tests
    # print("Identical Colors")
    # color_1, color_2 = (50, 2.6772, -79.7751), (50, 2.6772, -79.7751)
    # ee, de = 0, cielab_00(color_1, color_2)
    # print(f"Color 1: {color_1}")
    # print(f"Color 2: {color_2}")
    # print(f"Actual Result:   {de:.4f}")
    # print(f"Expected Result: {ee:.4f}")
    # print(f"Difference:      {abs(ee-de):.4f}")
    # print()

    # print("Small Hue Shift")
    # color_1, color_2 = (50, 2.6772, -79.7751), (50, 0.0000, -82.7485)
    # ee, de = 2.0425, cielab_00(color_1, color_2)
    # print(f"Color 1: {color_1}")
    # print(f"Color 2: {color_2}")
    # print(f"Actual Result:   {de:.4f}")
    # print(f"Expected Result: {ee:.4f}")
    # print(f"Difference:      {abs(ee-de):.4f}")
    # print()

    # print("Medium Hue Shift")
    # color_1, color_2 = (50, 2.8361, -74.0200), (50, 0.0000, -82.7485)
    # ee, de = 3.4412, cielab_00(color_1, color_2)
    # print(f"Color 1: {color_1}")
    # print(f"Color 2: {color_2}")
    # print(f"Actual Result:   {de:.4f}")
    # print(f"Expected Result: {ee:.4f}")
    # print(f"Difference:      {abs(ee-de):.4f}")
    # print()

    # print("Large Hue Shift")
    # color_1, color_2 = (50, -1.3802, -84.2814), (50, 0.0000, -82.7485)
    # ee, de = 1, cielab_00(color_1, color_2)
    # print(f"Color 1: {color_1}")
    # print(f"Color 2: {color_2}")
    # print(f"Actual Result:   {de:.4f}")
    # print(f"Expected Result: {ee:.4f}")
    # print(f"Difference:      {abs(ee-de):.4f}")
    # print()

    # print("Symmetry Test")
    # color_1, color_2 = (50, 0.0000, -82.7485), (50, -1.3802, -84.2814)
    # ee, de = cielab_00(color_2, color_1), cielab_00(color_1, color_2)
    # print(f"Color 1: {color_1}")
    # print(f"Color 2: {color_2}")
    # print(f"Actual Result:   {de:.4f}")
    # print(f"Expected Result: {ee:.4f}")
    # print(f"Difference:      {abs(ee-de):.4f}")
    # print()

    # print("Low Chroma Test")
    # color_1, color_2 = (50, 0, 0), (50, -1, -2)
    # ee, de = 2.3669, cielab_00(color_1, color_2)
    # print(f"Color 1: {color_1}")
    # print(f"Color 2: {color_2}")
    # print(f"Actual Result:   {de:.4f}")
    # print(f"Expected Result: {ee:.4f}")
    # print(f"Difference:      {abs(ee-de):.4f}")
    # print()

    # print("Large Lighness Difference")
    # color_1, color_2 = (90, -2.0831, 1.4410), (59, -0.4250, -1.4530)
    # ee, de = 23.0539, cielab_00(color_1, color_2)
    # print(f"Color 1: {color_1}")
    # print(f"Color 2: {color_2}")
    # print(f"Actual Result:   {de:.4f}")
    # print(f"Expected Result: {ee:.4f}")
    # print(f"Difference:      {abs(ee-de):.4f}")
    # print()


    # Test Size Estimation Function
    # size = estimate_size("test_images/finalists/metroid_c1_2x2.bmp", 16, "SWG", 1/4, "inches")
    # print(size)

    # Test Rotate Function
    # rotate_image_f("test_images/finalists/metroid_c1_2x2.bmp", 90, True)

