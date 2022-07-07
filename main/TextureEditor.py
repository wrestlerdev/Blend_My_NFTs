try:
    from PIL import Image
except:
    pass

from . import config
import os
import bpy
from . import config

def check_PIL():
    try:
        from PIL import Image
    except:
        print(f"{config.bcolors.ERROR}PIL needs to be installed to run this soz :<{config.bcolors.RESET}")
        return False
    else:
        return True


def rename_all_original_textures(input_path):
    if not check_PIL():
        return
    slots_path = os.path.join(input_path, 'SLOTS')
    for slot_dir in os.listdir(slots_path):
        slots = os.path.join(slots_path, slot_dir)
        for type_dir in os.listdir(slots):
            types = os.path.join(slots, type_dir)
            for var_dir in os.listdir(types):
                vars = os.path.join(types, var_dir)
                textures = os.path.join(vars, 'Textures')
                if os.path.exists(textures):
                    for texture_dir in os.listdir(textures):
                        texture_path = os.path.join(textures, texture_dir)
                        if len(next(os.walk(texture_path))[1]) > 0:
                            for multi_texture_dir in os.listdir(texture_path):
                                multi_texture_path = os.path.join(texture_path, multi_texture_dir)
                                number = '_' + ''.join(i for i in multi_texture_dir if i.isdigit())
                                rename_all_textures_in_folder(multi_texture_path, var_dir, '_' + texture_dir, number)
                                # return # GET RID OF THIS L8R
                        else:
                            rename_all_textures_in_folder(texture_path, var_dir, '_' + texture_dir)
                            # return # GET RID OF THIS L8R


def rename_all_textures_in_folder(folder_path, name, texture_set, variant_suffix=''):
    #og_texture_suffixes = ['_64', '_128', '_256', '_512', '_1k', '_2k']
    og_texture_suffixes = list(config.texture_suffixes.values()) 
    og_texture_suffixes.remove('')
    print(og_texture_suffixes)
    roughness_list = ['_R.', 'R_', 'Roughness', 'roughness']
    id_list = ['_ID.', 'ColorID']
    diffuse_list = ['_D.', 'Diffuse', 'BakedBaseColor', 'LightGreyScale', 'diffuse','BaseColor']
    metallic_list = ['_M.', 'Metallic', 'Metalic', 'metallic']
    normal_list = ['_N.', 'Normal', 'normal']
    emissive_list = ['_E.', 'Emmissive', 'Emissive', 'emissive', 'emmissive']
    opacity_list = ['_O.', 'Opacity', 'opacity',]
    intensity_list = ['_I.', 'Intensity', 'intensity']
    if os.path.isdir(folder_path): # to avoid .db file issue?
        texture_images = [fn for fn in os.listdir(folder_path) if any(fn.endswith(ext) for ext in config.image_extensions)] # find all images
        not_texture_images = [fn for fn in os.listdir(folder_path) if not any(fn.endswith(ext) for ext in config.image_extensions)]
        original_textures = [fn for fn in texture_images if not any( (fn.rpartition('.')[0]).endswith(suf) for suf in og_texture_suffixes)] # original 4k textures
        not_original_textures = [fn for fn in texture_images if any( (fn.rpartition('.')[0]).endswith(suf) for suf in og_texture_suffixes)]

        if not_original_textures:
            print(f"{config.bcolors.WARNING}These images ({not_original_textures}) within {folder_path} will not be renamed{config.bcolors.RESET}")
        if not_texture_images:
            print(f"{config.bcolors.WARNING}These files ({not_texture_images}) within {folder_path} will not be renamed{config.bcolors.RESET}")

        for texture in original_textures:
            new_name = texture
            file_type = texture.rpartition('.')[2]
            variant_name = name.split('_')[-1]
            if any(r in texture for r in roughness_list):
                new_name = 'T_' + variant_name + variant_suffix + texture_set + roughness_list[0] + file_type
            elif any(id in texture for id in id_list):
                new_name = 'T_' + variant_name + variant_suffix + texture_set + id_list[0] + file_type
            elif any(d in texture for d in diffuse_list):
                new_name = 'T_' + variant_name + variant_suffix + texture_set + diffuse_list[0] + file_type
            elif any(m in texture for m in metallic_list):
                new_name = 'T_' + variant_name + variant_suffix + texture_set + metallic_list[0] + file_type
            elif any(n in texture for n in normal_list):
                new_name = 'T_' + variant_name + variant_suffix + texture_set + normal_list[0] + file_type
            elif any(e in texture for e in emissive_list):
                new_name = 'T_' + variant_name + variant_suffix + texture_set + emissive_list[0] + file_type
            elif any(o in texture for o in opacity_list):
                new_name = 'T_' + variant_name + variant_suffix + texture_set + opacity_list[0] + file_type
            elif any(i in texture for i in intensity_list):
                new_name = 'T_' + variant_name + variant_suffix + texture_set + intensity_list[0] + file_type
            else:
                print(f"{config.bcolors.ERROR}This image ({config.bcolors.OK}{texture}{config.bcolors.ERROR}) within {folder_path} is not supported currently for rename system woops{config.bcolors.RESET}")
            print(new_name)
            if new_name != texture:
                old_texture_path = os.path.join(folder_path, texture)
                new_texture_path = os.path.join(folder_path, new_name)
                os.rename(old_texture_path, new_texture_path)
    return


def create_downres_textures(input_path, dims, should_overwrite):
    if not check_PIL():
        return

    slots_path = os.path.join(input_path, 'SLOTS')
    for slot_dir in os.listdir(slots_path):
        slots = os.path.join(slots_path, slot_dir)
        for type_dir in os.listdir(slots):
            types = os.path.join(slots, type_dir)
            for var_dir in os.listdir(types):
                vars = os.path.join(types, var_dir)
                textures = os.path.join(vars, 'Textures')
                if os.path.exists(textures):
                    for texture_dir in os.listdir(textures):
                        texture_path = os.path.join(textures, texture_dir)
                        if len(next(os.walk(texture_path))[1]) > 0:
                            for multi_texture_dir in os.listdir(texture_path):
                                multi_texture_set = os.path.join(texture_path, multi_texture_dir)
                                downres_all_textures_in_folder(multi_texture_set, dims, should_overwrite)
                                # return # GET RID OF THIS L8R
                        else:
                            downres_all_textures_in_folder(texture_path, dims, should_overwrite)
                            # return # GET RID OF THIS L8R

    return


def downres_all_textures_in_folder(path, dims, should_overwrite):
    og_texture_suffixes = ['_E', '_ID', '_M', '_N', '_R', '_D', '_O'] # don't put '_I' in here since it shouldn'be be downres'ed

    if os.path.isdir(path):
        texture_images = [fn for fn in os.listdir(path) if any(fn.endswith(ext) for ext in config.image_extensions)]
        
        original_textures = [fn for fn in texture_images if any((fn.rpartition('.')[0]).endswith(suf) for suf in og_texture_suffixes)] # original 4k textures
        print(original_textures)
        for image in original_textures:
            print(image)
            downres_single_texture(path, image, dims, should_overwrite)
    return


def downres_single_texture(path, image_name, dims, should_overwrite):
    if type(dims) != list:
        dims = [dims]
    for size in dims:
        image_path = os.path.join(path, image_name)

        old_name = image_name.rpartition('.')
        new_name = old_name[0] + config.texture_suffixes[size] + old_name[1] + old_name[2]
        new_path = os.path.join(path, new_name)

        if not should_overwrite:
            if os.path.exists(new_path):
                # print(new_path)
                continue

        with Image.open(image_path) as image:
            resized = image.resize([size, size])
            if size not in config.texture_suffixes:
                print("This isn't a valid dimension for {} atm".format(image_name))
                return
            if new_path.endswith('tif'):
                resized.save(new_path, optimize=True)
            else:
                resized.save(new_path, quality=95, optimize=True)
            print(new_path)
    return


# ------------------------------------------------------------------------------


def reimport_all_character_objects(folder_path):
    delete_all_actions()
    for dir in os.listdir(folder_path):
        if dir.endswith('.blend') and 'Rig' in dir:
            rig_blendfile_path = os.path.join(folder_path, dir)
    for char in config.Characters:
        reimport_character_objects(char, rig_blendfile_path)
        
    bpy.ops.file.make_paths_absolute()
    return


def reimport_character_objects(character, rig_blendfile_path):
    clear_old_character_objects(character)

    bpy.data.collections[character].hide_viewport = False
    bpy.data.collections[character].hide_render = False
    bpy.ops.outliner.orphans_purge()

    layer_collection = bpy.context.view_layer.layer_collection.children["Script_Ignore"].children[character]
    bpy.context.view_layer.active_layer_collection = layer_collection
    
    filename = character + '_Rig'
    file_path   = os.path.join(rig_blendfile_path, "Collection", filename)
    directory = os.path.join(rig_blendfile_path, "Collection")
    bpy.ops.wm.append(filepath=file_path, directory=directory, filename=filename)
    import_character_actions(character, rig_blendfile_path)

    rig = bpy.data.objects['armature_' + character.lower()]

    for obj in bpy.data.objects:
        if obj.parent == rig:
            # Do stuff
            obj.hide_viewport = False
            obj.hide_render =  False
            rigMesh = obj
            rigMesh.select_set( state = True, view_layer = bpy.context.view_layer )
            bpy.context.view_layer.objects.active = rigMesh
    if len(bpy.context.selected_objects) > 1:
        bpy.context.view_layer.objects.active = bpy.data.objects[character + "_Body"]            
        # bpy.ops.object.join() # OBJECTJOIN
        print("JOINING")
    
    # for col in bpy.data.collections[character].children:
    #     for obj in col.objects:
    #         if obj.type == 'ARMATURE':
    #             for bodyMesh in obj.objects:
    #                 if bodyMesh.type == 'MESH':
    #                     bodyMesh.hide_viewport = False
    #                     bodyMesh.hide_render =  False
    #                     cube = bodyMesh
    #                     cube.select_set( state = True, view_layer = bpy.context.view_layer )
    #                     bpy.context.view_layer.objects.active = cube
    # if len(bpy.context.selected_objects) > 1:                    
    #     bpy.ops.object.join()
    return

def import_character_actions(character, rig_blendfile_pathr):
    actions = []
    with bpy.data.libraries.load(rig_blendfile_pathr) as (data_from, data_to):
        #names = [name for name in data_from.collections]
        actions = [action for action in data_from.actions]
        for action in actions:
            if action.endswith(character.lower() + '_action'):
                dir = os.path.join(rig_blendfile_pathr, "Action")
                file_name = action
                file_path = os.path.join(dir, file_name)      
                bpy.ops.wm.append(filepath=file_path, directory=dir, filename=file_name, set_fake=True )
            
    return actions

def delete_all_actions():
    for action in bpy.data.actions:
        bpy.data.actions.remove(action)

def clear_old_character_objects(char_name):
    coll = bpy.data.collections[char_name]
    recurse_delete_collection(coll)
    bpy.ops.outliner.orphans_purge()
    return

def recurse_delete_collection(collection):
    for obj in collection.objects:
        collection.objects.unlink(obj)
        bpy.data.objects.remove(obj)
    for child in collection.children:
        recurse_delete_collection(child)
        collection.children.unlink(child)
    return


def reimport_lights(blend_path):
    parent_name = "Rendering"
    folder_name = "Lighting"

    if bpy.data.collections.get(parent_name) is None: # creates render folder
        render_folder = bpy.data.collections.new(parent_name)
        bpy.data.collections["Script_Ignore"].children.link(render_folder)
    else:
        render_folder = bpy.data.collections[parent_name]

    for obj in bpy.data.collections["Script_Ignore"].objects: # imports camera into render folder that exist in script ignore
        if obj.type == 'CAMERA':
            bpy.data.collections["Script_Ignore"].objects.unlink(obj)
            bpy.data.collections[folder_name].objects.link(obj)

    if bpy.data.collections.get(folder_name) is None: # delete all within lighting folder, purge, then reimport from lighting file
        folder = bpy.data.collections.new(folder_name)
        bpy.data.collections[parent_name].children.link(folder)
    else:
        folder = bpy.data.collections[folder_name]
        for coll in folder.children:
            for obj in coll.objects:
                coll.objects.unlink(obj)
            bpy.data.collections.remove(coll)
        bpy.ops.outliner.orphans_purge()
    layer_collection = bpy.context.view_layer.layer_collection.children["Script_Ignore"].children[render_folder.name].children[folder.name]
    bpy.context.view_layer.active_layer_collection = layer_collection

    file_path   = os.path.join(blend_path, "Collection", "light_setup")
    directory = os.path.join(blend_path, "Collection")
    filename = 'light_setup'
    bpy.ops.wm.append(filepath=file_path, directory=directory, filename=filename)
    return