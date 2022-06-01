try:
    from PIL import Image
except:
    pass

from sys import prefix
from . import config
import os

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
                                rename_all_textures_in_folder(multi_texture_path, var_dir, number)
                                # return # GET RID OF THIS L8R
                        else:
                            rename_all_textures_in_folder(texture_path, var_dir)
                            # return # GET RID OF THIS L8R


def rename_all_textures_in_folder(folder_path, name, variant_suffix=''):
    og_texture_suffixes = ['_128', '_256', '_512', '_1k', '_2k']
    roughness_list = ['_R.', 'R_', 'Roughness', 'roughness']
    id_list = ['_ID.', 'ColorID']
    diffuse_list = ['_D.', 'Diffuse', 'BakedBaseColor', 'LightGreyScale', 'diffuse','BaseColor']
    metallic_list = ['_M.', 'Metallic', 'Metalic', 'metallic']
    normal_list = ['_N.', 'Normal', 'normal']
    emissive_list = ['_E.', ' Emmissive', 'emmissive']
    opacity_list = ['_O.', ' Opacity', 'opacity']

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
            new_name = 'T_' + variant_name + variant_suffix + roughness_list[0] + file_type
        elif any(id in texture for id in id_list):
            new_name = 'T_' + variant_name + variant_suffix + id_list[0] + file_type
        elif any(d in texture for d in diffuse_list):
            new_name = 'T_' + variant_name + variant_suffix + diffuse_list[0] + file_type
        elif any(m in texture for m in metallic_list):
            new_name = 'T_' + variant_name + variant_suffix + metallic_list[0] + file_type
        elif any(n in texture for n in normal_list):
            new_name = 'T_' + variant_name + variant_suffix + normal_list[0] + file_type
        elif any(e in texture for e in emissive_list):
            new_name = 'T_' + variant_name + variant_suffix + emissive_list[0] + file_type
        elif any(o in texture for o in opacity_list):
            new_name = 'T_' + variant_name + variant_suffix + opacity_list[0] + file_type
        else:
            print(f"{config.bcolors.ERROR}This image ({config.bcolors.OK}{texture}{config.bcolors.ERROR}) within {folder_path} is not supported currently for rename system woops{config.bcolors.RESET}")
        print(new_name)
        if new_name != texture:
            old_texture_path = os.path.join(folder_path, texture)
            new_texture_path = os.path.join(folder_path, new_name)
            os.rename(old_texture_path, new_texture_path)
        

    return


def create_downres_textures(input_path, dims):
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
                                downres_all_textures_in_folder(multi_texture_set, dims)
                                # return # GET RID OF THIS L8R
                        else:
                            downres_all_textures_in_folder(texture_path, dims)
                            # return # GET RID OF THIS L8R

    return


def downres_all_textures_in_folder(path, dims):
    og_texture_suffixes = ['_E', '_ID', '_M', '_N', '_R', '_D', '_O']

    texture_images = [fn for fn in os.listdir(path) if any(fn.endswith(ext) for ext in config.image_extensions)]
    original_textures = [fn for fn in texture_images if any((fn.rpartition('.')[0]).endswith(suf) for suf in og_texture_suffixes)] # original 4k textures

    for image in original_textures:
        downres_single_texture(path, image, dims)
    return


def downres_single_texture(path, image_name, dims):
    
    if type(dims) != list:
        dims = [dims]
    for size in dims:
        image_path = os.path.join(path, image_name)
        with Image.open(image_path) as image:
            resized = image.resize([size, size])
            if size not in config.texture_suffixes:
                print("This isn't a valid dimension for {} atm".format(image_name))
                return
            old_name = image_name.rpartition('.')
            new_name = old_name[0] + config.texture_suffixes[size] + old_name[1] + old_name[2]
            new_path = os.path.join(path, new_name)
            if new_path.endswith('tif'):
                resized.save(new_path, optimize=True)
            else:
                resized.save(new_path, quality=95, optimize=True)
            print(new_path)
    return