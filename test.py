
from PIL import Image

input_file = "test_images/pixel_art_pheonix_base.bmp"


# Write function to replace each pixel with 2x2 block of same color.
def resize_image(input_file: str) -> None:
    with Image.open(input_file) as img:
        width, height = img.size
        new_img = Image.new("RGBA", (width * 2, height * 2))

        for x in range(width):
            for y in range(height):
                pixel = img.getpixel((x, y))
                new_img.putpixel((x * 2, y * 2), pixel)
                new_img.putpixel((x * 2 + 1, y * 2), pixel)
                new_img.putpixel((x * 2, y * 2 + 1), pixel)
                new_img.putpixel((x * 2 + 1, y * 2 + 1), pixel)

        # Construct output filename
        input_filename  = input_file.split(".")[0]
        input_extension = input_file.split(".")[-1]
        output_file = f"{input_filename}_2x2.{input_extension}"

        # Save modified image
        new_img.save(output_file)

        # Return output filename
        return output_file

resize_image(input_file)