import bpy
import os
import json
import shutil

from . import config

# collection colours
col = {"red" : 'COLOR_01', 'orange' : 'COLOR_02', 'yellow' : 'COLOR_03', "green" : "COLOR_04",
         "blue" : "COLOR_05", "purple" : "COLOR_06", "pink" : "COLOR_07", "brown" : "COLOR_08"}


def read_DNAList_from_file(batch_index, index): # return DNA as string
    batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(batch_index), "_NFTRecord_{}.json".format(batch_index))
    DataDictionary = json.load(open(NFTRecord_save_path))
    DNAList = DataDictionary["DNAList"]

    if index <= len(DNAList):
        NFT_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(batch_index), "NFT_{}".format(index),
                                "Batch_{}".format(batch_index) + "_NFT_{}.json".format(index))
        NFTDictionary = json.load(open(NFT_save_path))
        DNA = NFTDictionary["DNAList"]
        NFTDict = NFTDictionary["CharacterItems"]
        return len(DNAList), DNA, NFTDict
    else:
        return len(DNAList), '', ''


def get_all_DNA_from_batch(index):
    batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(index), "_NFTRecord_{}.json".format(index))
    DataDictionary = json.load(open(NFTRecord_save_path))
    DNAList = DataDictionary["DNAList"]
    print(DataDictionary)
    return DNAList


def get_total_DNA(): # get number of saved DNAs
    index = bpy.context.scene.my_tool.CurrentBatchIndex
    batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(index), "_NFTRecord_{}.json".format(index))
    DataDictionary = json.load(open(NFTRecord_save_path))
    DNAList = DataDictionary["DNAList"]
    return len(DNAList)


def init_batch(batch_data_path): # delete all batch data then create first batch folder
    shutil.rmtree(batch_data_path)
    os.makedirs(batch_data_path)
    first_batch_path = os.path.join(batch_data_path, "Batch_{}".format(1))
    if not os.path.exists(first_batch_path):
        os.makedirs(first_batch_path)
    return



def update_collection_rarity_property(NFTRecord_save_path, Rarity_save_path=''): # update rarity value for in scene collections based on hierarchy file
    if Rarity_save_path:
        RarityDictionary = json.load(open(Rarity_save_path)) # sets any collection not in hierarchy as rarity = 0
        rarities = RarityDictionary["Rarities"]

    DataDictionary = json.load(open(NFTRecord_save_path)) # sets any collection not in hierarchy as rarity = 0
    hierarchy = DataDictionary["hierarchy"]

    slots = list(hierarchy.keys())
    for slot in slots:
        types = list(hierarchy[slot].keys())
        scene_type_colls = bpy.data.collections[slot].children
        for scene_type_coll in scene_type_colls:
            type = scene_type_coll.name
            if type in  hierarchy[slot].keys() != None: #This checks if a type has any variants in it
                variants = list(hierarchy[slot][type].keys())
                if len(variants) > 0:
                    for h_variant in variants: # check if any valid variants do exist
                        h_variant_exists = False # hierarchy variant
                        if len(list(hierarchy[slot][type][h_variant].keys())) > 0:
                            h_variant_exists = True
                            break
                    if h_variant_exists: # get rarity from hierarchy if type exists
                        type_rarity = hierarchy[slot][type][h_variant]["type_rarity"]
                        if type in types:
                            scene_type_coll["rarity"] =  float(type_rarity)
                            update_rarity_color(type, type_rarity)
                            if Rarity_save_path:
                                scene_type_coll["absolute_rarity"] = (rarities[slot][type]["absolute_rarity"]) * 100
                            elif scene_type_coll.get("absolute_rarity") is not None:
                                del(scene_type_coll["absolute_rarity"])
                        else:
                            scene_type_coll["rarity"] =  0
                            update_rarity_color(type, 0)

                        scene_var_colls = scene_type_coll.children

                        for scene_var_coll in scene_var_colls:
                            variant = scene_var_coll.name
                            if variant in variants and type in types: # does variant exist in heirarchy
                                variant_rarity = hierarchy[slot][type][variant]["variant_rarity"]
                                update_rarity_color(variant, float(variant_rarity))
                                scene_var_coll["rarity"] = float(variant_rarity)
                                if Rarity_save_path and variant in rarities[slot][type]:
                                    scene_var_coll["absolute_rarity"] = (rarities[slot][type][variant]["absolute_rarity"]) * 100
                                elif scene_var_coll.get("absolute_rarity") is not None:
                                    del(scene_var_coll["absolute_rarity"])

                                texture_objs = scene_var_coll.objects
                                for texture_obj in texture_objs:
                                    texture_name = texture_obj.name
                                    if texture_name in hierarchy[slot][type][variant]["textureSets"].keys():
                                        texture_rarity = hierarchy[slot][type][variant]["textureSets"][texture_name]
                                    else:
                                        texture_rarity = 0
                                    texture_obj["rarity"] = texture_rarity
                            else:
                                update_rarity_color(variant, 0)
                                scene_var_coll["rarity"] = 0

                    else: # collection doesn't exist in hierarchy, so delete value
                        current_var_coll = bpy.data.collections[h_variant]
                        if current_var_coll.get("rarity") is not None:
                            del(current_var_coll["rarity"])
                        if scene_type_coll.get("rarity") is not None:
                            del(scene_type_coll["rarity"])
                        
                        update_rarity_color(h_variant, 0)
                        update_rarity_color(type, 0)
                else:
                    if scene_type_coll.get("rarity") is not None:
                        del(scene_type_coll["rarity"])
                    update_rarity_color(type, 0)
            else:
                update_rarity_color(type, 0)
    bpy.context.scene.my_tool.NonElementalProbability = DataDictionary["RegularWeight"] if "RegularWeight" in DataDictionary.keys() else 0
    bpy.context.scene.my_tool.FullElementalProbability = DataDictionary["ElementalWeight"] if "ElementalWeight" in DataDictionary.keys() else 0
    bpy.context.scene.my_tool.OutfitElementalProbability = DataDictionary["ElementalOutfitWeight"] if "ElementalOutfitWeight" in DataDictionary.keys() else 0
    return



def update_batch_items(batch_num, record_path):
    default_type_rarity = 100 # for new items
    default_var_rarity = 100

    record = json.load(open(record_path))
    hierarchy = record['hierarchy']
    for attribute_coll in bpy.context.scene.collection.children: # go through scene collections to see if coll exists in hierarchy
        if attribute_coll.name in hierarchy.keys():
            pass
        elif attribute_coll.name != 'Script_Ignore':
            attribute_dict = {}
            hierarchy[attribute_coll.name] = attribute_dict
        else:
            # this is script_ignore
            continue

        for type_coll in attribute_coll.children:
            if type_coll.name in hierarchy[attribute_coll.name].keys():
                pass
            else:
                type_dict = {}
                hierarchy[attribute_coll.name][type_coll.name] = type_dict

            for variant_coll in type_coll.children:
                if variant_coll.name in hierarchy[attribute_coll.name][type_coll.name].keys():
                    pass
                else:
                    variant_split = variant_coll.name.split('_')
                    
                    item_dict = {}
                    item_dict["item_attribute"] = attribute_coll.name
                    item_dict["item_type"] = type_coll.name
                    item_dict["item_variant"] = variant_split[-1]
                    item_dict["item_index"] = variant_split[2]
                    item_dict["type_rarity"] = default_type_rarity
                    item_dict["variant_rarity"] = default_var_rarity
                    item_dict["textureSets"] = []

                    hierarchy[attribute_coll.name][type_coll.name][variant_coll.name] = item_dict

                hierarchy[attribute_coll.name][type_coll.name][variant_coll.name]["textureSets"] = get_texture_sets(variant_coll)


    record['hierarchy'] = hierarchy
    try:
        ledger = json.dumps(record, indent=1, ensure_ascii=True)
        with open(record_path, 'w') as outfile:
            outfile.write(ledger + '\n')
    except:
        print(f"{config.bcolors.ERROR} ERROR:\nBatch ({str(batch_num)}) could not be updated at {record}\n {config.bcolors.RESET}")
    return


def get_texture_sets(variant_coll):
    default_texture_rarity = 50
    texture_dict = {}
    for obj in variant_coll.objects:
        if obj.get('rarity') is not None:
            texture_dict[obj.name] = obj.get('rarity')
        else:
            texture_dict[obj.name] = default_texture_rarity
    return texture_dict



def batch_property_updated(): # check if batch is out of range then set in range if it is
    if(bpy.context.scene.my_tool.BatchSliderIndex != bpy.context.scene.my_tool.lastBatchSliderIndex): # to stop recursion

        Batch_save_path = bpy.context.scene.my_tool.batch_json_save_path
        newIndex = bpy.context.scene.my_tool.BatchSliderIndex
        batches = len(os.listdir(Batch_save_path))
        if batches == 0: # stop recursion?
            return
        if newIndex > batches:
            bpy.context.scene.my_tool.BatchSliderIndex = batches
            bpy.context.scene.my_tool.lastBatchSliderIndex = batches
    return


def update_rarity_color(coll_name, rarity):
    rarity = int(rarity)
    if rarity > 80:
        bpy.data.collections[coll_name].color_tag = col["brown"]
    elif rarity > 60:
        bpy.data.collections[coll_name].color_tag = col["blue"]
    elif rarity > 40:
        bpy.data.collections[coll_name].color_tag = col["green"]
    elif rarity > 20:
        bpy.data.collections[coll_name].color_tag = col["orange"]
    elif rarity > 5:
        bpy.data.collections[coll_name].color_tag = col["yellow"]
    elif rarity > 0:
        bpy.data.collections[coll_name].color_tag = col["purple"]
    else:
        bpy.data.collections[coll_name].color_tag = col["red"]
    return


def update_current_batch(index, batch_path): # updates current batch record path to new batch record
    bpy.context.scene.my_tool.CurrentBatchIndex = index

    new_batch_path = os.path.join(batch_path, 'Batch_{}'.format(index))
    if not os.path.exists(new_batch_path):
        os.makedirs(new_batch_path)
        return
    return



def check_if_paths_exist(batch_num=1): # may be redundant now
    if bpy.context.scene.my_tool.batch_json_save_path == '':
        # save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        save_path = bpy.context.scene.my_tool.save_path
        Blend_My_NFTs_Output = os.path.join(save_path, "Blend_My_NFT")
        bpy.context.scene.my_tool.batch_json_save_path = os.path.join(Blend_My_NFTs_Output, "OUTPUT")
        bpy.context.scene.my_tool.CurrentBatchIndex = batch_num
