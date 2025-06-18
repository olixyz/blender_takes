import bpy
import os
import sys

def warning_text():
    
    camera = bpy.context.scene.camera
    empt = bpy.data.objects.new( "empty", None )
    text = bpy.data.curves.new(type="FONT", name="take_warning")
    text.body = "TAKE!"
    text.align_x = "CENTER"
    text.align_y = "CENTER"

    text_obj = bpy.data.objects.new(name="Font Object", object_data=text)
    text_obj.parent = empt
    text_obj.hide_render = True
    con = empt.constraints.new(type="COPY_TRANSFORMS")
    con.target = camera

    scale_fac = 1 # Should be scaled according to aspect ratio
    text_obj.location.z = camera.data.lens * -0.028
    text_obj.scale.xyz = (scale_fac,scale_fac,scale_fac)

    collection_name = "take_warning"

    layer_collection = bpy.context.view_layer.layer_collection

    if not collection_name in bpy.data.collections:
        new_collection = bpy.data.collections.new(collection_name)
        layer_collection.collection.children.link(new_collection)

    bpy.data.collections[collection_name].objects.link(text_obj)
    bpy.data.collections[collection_name].objects.link(empt)

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

    # Setup warning text. This is so there is some indication
    # to not accidentally do work in this file.
    warning_text()

    # Save
    bpy.ops.wm.save_as_mainfile(copy=True, check_existing=False, filepath=output_file)

    # Re-open original file
    bpy.ops.wm.open_mainfile(filepath=main_file)
