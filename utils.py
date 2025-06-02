# import bpy
from bpy import context


def hide_all():
    print("UTILS::Hide all")
    coll = bpy.data.collections
    for c in coll:
        c.hide_render = True
        c.hide_viewport = True


def show(c_list):
    print("UTILS::Show list of collections")
    coll = bpy.data.collections
    current_vl = bpy.context.view_layer

    for x in c_list:
        try:
            coll[x].hide_render = False
            coll[x].hide_viewport = False
            current_vl.layer_collection.children[x].hide_viewport = False
        except:
            print("no collection named ", x)


def world(world_name):
    bpy.context.scene.world = bpy.data.worlds[world_name]


def set_range(in_marker, out_marker):
    scene = context.scene
    marker_in = context.scene.timeline_markers.get(in_marker)
    marker_out = context.scene.timeline_markers.get(out_marker)
    bpy.context.scene.frame_start = marker_in.frame
    bpy.context.scene.frame_end = marker_out.frame


def show_with_children(c_list):
    coll = bpy.data.collections
    for x in c_list:
        try:
            coll[x].hide_render = False
            coll[x].hide_viewport = False
            print("Show {a}".format(a=coll[x]))
            for c in coll[x].children:
                c.hide_render = False
                c.hide_viewport = False
                print("Show {a}".format(a=c))
        except:
            print("no collection named ", x)


def not_visible_to_camera(c_list):
    # Takes list of Collections
    for coll in c_list:
        for o in bpy.data.collections[coll].objects:
            if o.type == "MESH":
                o.cycles_visibility.camera = False


def holdout(c_list):
    # Takes list of Collections
    for coll in c_list:
        for o in bpy.data.collections[coll].objects:
            if o.type == "MESH":
                o.cycles.is_holdout = True


def overscan(o_fac):
    # bpy.context.scene.render.resolution_percentage *= o_fac
    bpy.context.scene.render.resolution_x *= o_fac
    bpy.context.scene.render.resolution_y *= o_fac

    cam = bpy.context.scene.camera
    cam.data.sensor_width *= o_fac


def all_mat_override(mat_name):
    # testing
    material = bpy.data.materials[mat_name]

    for o in list(bpy.data.objects):
        if o.type == "MESH":
            o.data.materials.clear()
            o.data.materials.append(material)
            # o.data.materials[0]=material


def collection_mat_override(coll, mat_name):
    # testing
    material = bpy.data.materials[mat_name]

    for o in bpy.data.collections[coll].objects:
        if o.type == "MESH":
            o.data.materials.clear()
            o.data.materials.append(material)


def remove_collections(colls):
    for coll in colls:

        if coll in bpy.data.collections:

            my_col = bpy.data.collections[coll]
            print("mycol    :", my_col)

            while my_col.objects:
                bpy.data.objects.remove(my_col.objects[0], do_unlink=True)


def create_collection(collection_name):
    """Taken from takes_update"""

    parent_collection = bpy.context.scene.collection

    if collection_name in bpy.data.collections:
        return bpy.data.collections[collection_name]
    else:
        new_collection = bpy.data.collections.new(collection_name)
        parent_collection.children.link(new_collection)
        return new_collection
