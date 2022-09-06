try:
    from PIL import Image
except:
    pass

from genericpath import isdir
from . import config
import os
import bpy
from . import config

def check_PIL(): # check if python imaging lib module exists
    try:
        from PIL import Image
    except:
        config.custom_print("PIL needs to be installed to run this soz :<", col=config.bcolors.ERROR)
        return False
    else:
        return True


def rename_all_original_textures(input_path): # renaming all 4k texture images
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
                                # return
                        else:
                            rename_all_textures_in_folder(texture_path, var_dir, '_' + texture_dir)
                            # return


def rename_all_textures_in_folder(folder_path, name, texture_set, variant_suffix=''):
    og_texture_suffixes = list(config.texture_suffixes.values()) 
    og_texture_suffixes.remove('')

    roughness_list = ['_R.', 'R_', 'Roughness', 'roughness']
    id_list = ['_ID.', 'ColorID']
    diffuse_list = ['_D.', 'Diffuse', 'BakedBaseColor', 'LightGreyScale', 'diffuse','BaseColor']
    metallic_list = ['_M.', 'Metallic', 'Metalic', 'metallic']
    normal_list = ['_N.', 'Normal', 'normal', "nomal"]
    emissive_list = ['_E.', 'Emmissive', 'Emissive', 'emissive', 'emmissive']
    opacity_list = ['_O.', 'Opacity', 'opacity',]
    intensity_list = ['_I.', 'Intensity', 'intensity']
    if os.path.isdir(folder_path): # to avoid .db file issue?
        texture_images = [fn for fn in os.listdir(folder_path) if any(fn.endswith(ext) for ext in config.image_extensions)] # find all images
        not_texture_images = [fn for fn in os.listdir(folder_path) if not any(fn.endswith(ext) for ext in config.image_extensions)]
        original_textures = [fn for fn in texture_images if not any( (fn.rpartition('.')[0]).endswith(suf) for suf in og_texture_suffixes)] # original 4k textures
        not_original_textures = [fn for fn in texture_images if any( (fn.rpartition('.')[0]).endswith(suf) for suf in og_texture_suffixes)]

        if not_original_textures:
            config.custom_print("These images ({}) within {} will not be renamed".format(not_original_textures, folder_path), col=config.bcolors.WARNING)
        if not_texture_images:
            config.custom_print("These images ({}) within {} will not be renamed".format(not_texture_images, folder_path), col=config.bcolors.WARNING)

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
                config.custom_print(f"This image ({config.bcolors.OK}{texture}{config.bcolors.ERROR}) within {folder_path} is not supported currently for rename system", col=config.bcolors.ERROR)
            config.custom_print(new_name)
            if new_name != texture:
                old_texture_path = os.path.join(folder_path, texture)
                new_texture_path = os.path.join(folder_path, new_name)
                try:
                    os.rename(old_texture_path, new_texture_path)
                    config.custom_print("{} will be renamed to {}".format(texture, new_name), col=config.bcolors.OK)
                except Exception as e:
                    config.custom_print("{} could not be renamed to {}".format(texture, new_name), col=config.bcolors.ERROR)
                    config.custom_print(e, col=config.bcolors.ERROR)
    return


def create_downres_textures(input_path, dims, should_overwrite): # loop through all texture folders
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
                                # return
                        else:
                            downres_all_textures_in_folder(texture_path, dims, should_overwrite)
                            # return
    return


def downres_all_textures_in_folder(path, dims, should_overwrite):
    og_texture_suffixes = ['_E', '_ID', '_M', '_N', '_R', '_D', '_O', '_T'] # don't put '_I' in here since it shouldn't be be downres'ed
    if os.path.isdir(path):
        texture_images = [fn for fn in os.listdir(path) if any(fn.endswith(ext) for ext in config.image_extensions)]
        original_textures = [fn for fn in texture_images if any((fn.rpartition('.')[0]).endswith(suf) for suf in og_texture_suffixes)] # original 4k textures
        config.custom_print(original_textures)
        for image in original_textures:
            config.custom_print(image)
            downres_single_texture(path, image, dims, should_overwrite)
    return


def downres_single_texture(path, image_name, dims, should_overwrite): # create downres textures for given dimensions
    if type(dims) != list:
        dims = [dims]
    for size in dims:
        image_path = os.path.join(path, image_name)
        old_name = image_name.rpartition('.')
        new_name = old_name[0] + config.texture_suffixes[size] + old_name[1] + old_name[2]
        new_path = os.path.join(path, new_name)

        if not should_overwrite:
            if os.path.exists(new_path):
                continue

        with Image.open(image_path) as image:
            resized = image.resize([size, size])
            if size not in config.texture_suffixes:
                config.custom_print("This isn't a valid dimension for {} atm".format(image_name), config.bcolors.ERROR)
                return
            if new_path.endswith('tif'):
                resized.save(new_path, optimize=True)
            else:
                resized.save(new_path, quality=95, optimize=True)
            config.custom_print("Resized: {}".format(new_path), config.bcolors.OK)
    return


# ------------------------------------------------------------------------------


def downres_element_textures(elements_folder_path, dims, should_overwrite):
    for ele_dir in os.listdir(elements_folder_path):
        # print(ele_dir)
        elements = os.path.join(elements_folder_path, ele_dir)
        if os.path.isdir(elements):
            downres_all_textures_in_folder(elements, dims, should_overwrite)
        else:
            for sub_dir in os.listdir(elements):
                element = os.path.join(elements, sub_dir)
                downres_all_textures_in_folder(element, dims, should_overwrite)
    return