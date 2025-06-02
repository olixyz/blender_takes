import bpy
import os
import sys

argv = sys.argv
takenames = argv[argv.index("--") + 1 :]  # get all args after "--"


# Get blendfile path and name
main_file = bpy.data.filepath
path_and_file = os.path.split(main_file)
blendpath = os.path.join(path_and_file[0])
filename = os.path.splitext(path_and_file[1])[0]  # w/o extension

output_path = os.path.join(
    blendpath,
    "output",
    filename,
)

os.makedirs(output_path, exist_ok=True)


for name in takenames:
    output_file = os.path.join(output_path, filename + "." + name + ".blend")

    # Find script data-block named "takes"
    takes = bpy.data.texts["takes"].as_module()
    take_def = getattr(takes, name)
    take_def()

    take_data_block = bpy.data.texts["takes"]
    take_data_block.clear()
    take_data_block.write("this is a renderfile")

    # Save
    bpy.ops.wm.save_as_mainfile(copy=True, check_existing=False, filepath=output_file)

    # Re-open original file
    bpy.ops.wm.open_mainfile(filepath=main_file)
