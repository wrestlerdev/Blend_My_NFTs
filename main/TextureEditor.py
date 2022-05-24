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
                                return # GET RID OF THIS L8R
                        else:
                            downres_all_textures_in_folder(texture_path, dims)
                            return # GET RID OF THIS L8R

    return


def downres_all_textures_in_folder(path, dims):
    image_extensions = ['jpg','jpeg', 'bmp', 'png', 'tif']
    og_texture_suffixes = ['_E', '_ID', '_M', '_N', '_R', '_D']


    texture_images = [fn for fn in os.listdir(path) if any(fn.endswith(ext) for ext in image_extensions)]
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
            resized.save(new_path, quality=95, optimize=True)
            print(new_path)
    return