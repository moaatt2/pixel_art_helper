import json

with open("palettes/ring_lord_palette_derived.json", "r") as f:
    data = json.load(f)

for color, hex in data.items():

    # Convert hex to rgb
    r = int(hex[0:2],16)
    g = int(hex[2:4],16)
    b = int(hex[4:6],16)

    # Normalize rgb values to 0-1 range
    r /= 255.0
    g /= 255.0
    b /= 255.0

    # Create Variable Name
    var_name = f"base_ring_lord_palette_derived_{color}"

    # Create color name
    color = color.replace("_", " ").title()
    color = f"Base Ring Lord Derived {color}"

    print(f"{var_name} = bpy.data.materials.new(name='{color}')")
    print(f"{var_name}.use_nodes = True")
    print(f"nodes = {var_name}.node_tree.nodes")
    print(f"node = nodes.get('Principled BSDF')")
    print(f"node.inputs['Base Color'].default_value = ({r:.2f}, {g:.2f}, {b:.2f}, 1.0)")
    print("node.inputs['Roughness'].default_value = 1")
    print()
    print()
