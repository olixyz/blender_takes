# import bpy
from bpy import context


# setup scene and viewlayer for take
def setup_take(scenename="Scene", viewlayername="ViewLayer"):
    # Catch if scenename and viewLayer do not exist
    if not bpy.data.scenes.get(scenename):
        raise Exception("Scene '{}' not in file".format(scenename))
                
    if not bpy.data.scenes[scenename].view_layers.get(viewlayername):
        raise Exception("ViewLayer '{}' not in Scene".format(viewlayername))
    
    # Loop over all viewLayer and delete if not the one we specified
    # vl = bpy.data.scenes[scenename].view_layers[viewlayername]
    for vl in bpy.data.scenes[scenename].view_layers:
        if vl.name != viewlayername:
            bpy.data.scenes[scenename].view_layers.remove(vl)               
            
            
    for s in bpy.data.scenes:
        if s.name != scenename:
            bpy.data.scenes.remove(s)
          
    # Create a new ViewLayer so we have clean ViewLayer settings
    
    
    # if takename not in bpy.context.scene.view_layers:
    bpy.context.scene.view_layers.new("take")
    
    # Delete the original viewLayer
    vl = bpy.data.scenes[scenename].view_layers[viewlayername]
    bpy.data.scenes[scenename].view_layers.remove(vl)  
    
    all_visible(scenename, "take")

# Only used in setup_take
def all_visible(scenename="Scene", viewlayername="ViewLayer"):
    # Turn all objects on for rendering
    for o in bpy.data.objects:
        o.hide_viewport = False
        o.hide_render = False
        
        # Handle object visibility in viewLayer    
        vl_o = bpy.data.scenes[scenename].view_layers[viewlayername].objects.get(o.name)
        vl_o.hide_set(0)


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

# Clear all material slots of objects in collection
def clear_materials(coll):
    for o in bpy.data.collections[coll].objects:
        if o.type == "MESH":
            o.data.materials.clear()

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
