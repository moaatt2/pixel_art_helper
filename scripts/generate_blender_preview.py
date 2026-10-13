"""Generate a blender script that creates a preview of an inlay in blender."""

##########################
### Imports & Settings ###
##########################

import pyperclip

# The path to the image you want to convert to a blender preview
IMAGE_PATH = ""


##################
### Main Logic ###
##################

def generate_preview(image_path: str) -> str:
    pass


if __name__ == "__main__":
    script = generate_preview(IMAGE_PATH)
    print(script)
    pyperclip.copy(script)
    print("Script Copied")

