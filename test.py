
from PIL import Image
from itertools import product

#################
### Functions ###
#################


# Write function to resize an image by duplicating each pixel according to specified width and height multipliers.
def resize_image(input_file: str, width_mult: int, height_mult: int) -> str:
    """
    Resize an image by integer scale factors using pixel replication and save the result to a new file.
    This function opens an image file with Pillow (PIL), creates a new RGBA image whose
    dimensions are the original width multiplied by width_mult and the original height
    multiplied by height_mult, and fills the new image by replicating each source pixel
    into a width_mult x height_mult block (nearest-neighbor / pixel replication scaling).
    The output filename is constructed from the input path and saved using the original
    file extension.
    Args:
        input_file (str): Path to the input image file. The file is opened with PIL.
        width_mult (int): Horizontal scaling factor. Must be a positive integer. Each
            source pixel is duplicated width_mult times along the x axis.
        height_mult (int): Vertical scaling factor. Must be a positive integer. Each
            source pixel is duplicated height_mult times along the y axis.
    Returns:
        str: The path of the saved output file. The output name is formed by taking the
        portion of input_file before the first '.' and appending "_{width_mult}x{height_mult}."
        plus the original extension (for example, "sprite.png" -> "sprite_3x2.png").
        Note: filenames containing multiple dots will use only the portion before the
        first dot as the base name.
    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If width_mult or height_mult are not positive integers (or result
            in invalid image dimensions).
        OSError: If the image cannot be opened or the output file cannot be written.
    Example:
        >>> resize_image("sprite.png", 3, 2)
        'sprite_3x2.png'
    """
    with Image.open(input_file) as img:
        width, height = img.size
        new_img = Image.new("RGBA", (width * width_mult, height * height_mult))

        for x, y in product(range(width), range(height)):
            pixel = img.getpixel((x, y))
            for dx, dy in product(range(width_mult), range(height_mult)):
                new_img.putpixel((x * width_mult + dx, y * height_mult + dy), pixel)

        # Construct output filename
        input_filename  = input_file.split(".")[0]
        input_extension = input_file.split(".")[-1]
        output_file = f"{input_filename}_{width_mult}x{height_mult}.{input_extension}"

        # Save modified image
        new_img.save(output_file)

        # Return output filename
        return output_file


# Write function to replace all occurrences of a specific color in an image with another color.
def apply_palette(palette_file: str, image_file: str) -> str:
    pass


#############
### Tests ###
#############

# Test the resize_image function
input_file = "test_images/pixel_art_pheonix_base.bmp"
resize_image(input_file, 2, 2)
