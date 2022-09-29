# Purpose:
# This file generates the Outfit DNA based on a rule set

import bpy
import os
import json
import random
import importlib
import time
from datetime import datetime

from . import Outfit_Generator
importlib.reload(Outfit_Generator)

from . import config

count = 0

def count_all_rarities(batch_record_path, index):
    global count
    print("(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")
    json_name = os.path.join(batch_record_path, '_RarityCounter_{}.json'.format(index))
    DataDictionary = json.load(open(os.path.join(batch_record_path, "_NFTRecord_{}.json".format(index))))
    hierarchy = DataDictionary["hierarchy"]

    time_start = time.time()

    rarity_dict = {}
    for attribute in hierarchy.keys():
        rarity_dict[attribute] = {}
        rarity_dict[attribute]['absolute_rarity'] = 0.0
        for type in hierarchy[attribute].keys():
            rarity_dict[attribute][type] = {}
            rarity_dict[attribute][type]['absolute_rarity'] = 0.0
            rarity_dict[attribute][type]['relative_rarity'] = get_weighted_rarity(type, attribute)[0]
            for variant in hierarchy[attribute][type].keys():
                rarity_dict[attribute][type][variant] = {}
                rarity_dict[attribute][type][variant]['absolute_rarity'] = 0.0
                rarity_dict[attribute][type][variant]['relative_rarity'] = get_weighted_rarity(variant, type)[0]

    count = 0
    filled_slots = '0' * len(hierarchy.keys())
    rarity_dict = add_rarity_recurse(rarity_dict, 1, hierarchy, filled_slots, attribute='01-UT')

    logged_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    export_dict = {}
    export_dict["Date/Time Calculated"] = logged_time
    export_dict["Rarities"] = rarity_dict

    ledger = json.dumps(export_dict, indent=4, ensure_ascii=True)
    with open(json_name, 'w') as outfile:
        outfile.write(ledger + '\n')
    
    print(f"{config.bcolors.OK}Time taken to calculate rarity: {time.time() - time_start} seconds{config.bcolors.RESET}")
    print("Total number of possible combinations? {}".format(count))
    return


max_att = 20 # inclusive?

def add_rarity_recurse(rarity_dict, current_probability, hierarchy, filled_slots, attribute='', type='', branch_count=1):
    global count
    if attribute and filled_slots[int(attribute[:2]) - 1] == '1':
        null_type = bpy.data.collections[attribute].children[0]
        null_variant = null_type.children[0]
        rarity_dict[attribute]["absolute_rarity"] = rarity_dict[attribute]["absolute_rarity"] + current_probability
        rarity_dict[attribute][null_type.name]["absolute_rarity"] = rarity_dict[attribute][null_type.name]["absolute_rarity"] + current_probability 
        rarity_dict[attribute][null_type.name][null_variant.name]["absolute_rarity"] = rarity_dict[attribute][null_type.name][null_variant.name]["absolute_rarity"] + current_probability
        next_index = list(hierarchy.keys()).index(attribute) + 1
        if next_index != max_att:
        # if next_index != len(hierarchy.keys()):
            next_att = list(hierarchy.keys())[next_index]
            rarity_dict = add_rarity_recurse(rarity_dict, current_probability, hierarchy, filled_slots, attribute=next_att, branch_count=branch_count)
        else:
            count += branch_count
        return rarity_dict

    if not type: # this is a attribute
        percentage = 1.0
    else: # this is a type
        percentage = get_weighted_rarity(type, attribute)[0]

    new_probability = current_probability * percentage

    if new_probability == 0.0: # if 0 then it shouldn't need to go down branch?
        return rarity_dict
    
    if type:
        rarity_dict[attribute][type]["absolute_rarity"] = rarity_dict[attribute][type]["absolute_rarity"] + new_probability
        var_count = 0
        var_weight_total = 0
        for variant in rarity_dict[attribute][type].keys():
            if variant != "absolute_rarity" and variant != "relative_rarity":
                variant_percentage, var_weight_total = get_weighted_rarity(variant, type, var_weight_total)
                rarity_dict[attribute][type][variant]["absolute_rarity"] = rarity_dict[attribute][type][variant]["absolute_rarity"] + new_probability * variant_percentage
                if variant_percentage:
                    var_count += 1
        branch_count = branch_count * var_count

    else:
        rarity_dict[attribute]["absolute_rarity"] = rarity_dict[attribute]["absolute_rarity"] + new_probability

    if not type: # this is an attribute
        att_coll = bpy.data.collections[attribute]
        for coll in att_coll.children:
            rarity_dict = add_rarity_recurse(rarity_dict, new_probability, hierarchy, filled_slots, attribute=attribute, type=coll.name, branch_count=branch_count)
    else: # this is a type
        if 'Null' not in type and type[3:] in Outfit_Generator.ItemUsedBodySlot:
            new_slots = Outfit_Generator.ItemUsedBodySlot[type[3:]]
        else:
            new_slots = []

        if new_slots:
            for slot in new_slots:
                index = int(slot[:2]) - 1
                if filled_slots[index] == '0':
                    filled_slots = filled_slots[:index] + '1' + filled_slots[index+1:]

        next_index = (list(hierarchy.keys()).index(attribute)) + 1
        # if next_index != len(hierarchy.keys()):
        if next_index != max_att:
            next_att = list(hierarchy.keys())[next_index]
            rarity_dict = add_rarity_recurse(rarity_dict, new_probability, hierarchy, filled_slots, attribute=next_att, branch_count=branch_count)
        else:
            count += branch_count
    return rarity_dict



def get_weighted_rarity(current_name, parent_name, total = 0):
    if not total:
        for coll in bpy.data.collections[parent_name].children:
            if coll.get('rarity') != None:
                total += coll.get('rarity')

    if total:
        current_coll = bpy.data.collections[current_name]
        if current_coll.get('rarity') != None:
            percentage = current_coll.get('rarity') / total
            return percentage, total
        else:
            return 0.0, total

    else: # CHECK GREEN NULL
        if len(bpy.data.collections[parent_name].children) == 1:
            return 1.0, total
        else: # CHECK THIS
            if 'Null' in current_coll.name:
                return 1.0, total
            else:
                return 0.0, total


def count_all_items_in_batch(batches_path, batch_nums, save_path): # goes through all nfts in batches and counts up number of times a variant is used
    counter = {}
    has_init = False # has all items been added to json and set to 0
    characters = 0
    for index in range(batch_nums[1], batch_nums[0]-1, -1):
        batch_path = os.path.join(batches_path, "Batch_{}".format(index))
        if os.path.exists(batch_path):
            if not has_init:
                record_path = os.path.join(batch_path, "_NFTRecord_{}.json".format(index))
                record = json.load(open(record_path))
                hierarchy = record["hierarchy"]
                for slot in hierarchy.keys():
                    for type in hierarchy[slot].keys():
                        for var in hierarchy[slot][type].keys():
                            for tex in hierarchy[slot][type][var]["textureSets"]:
                                if not tex.startswith("BLANK"):
                                    var_name = tex.split('_')[3] + ' ' + tex.split('_')[4]
                                    counter[var_name] = {}
                                    counter[var_name]["count"] = 0
                                    counter[var_name]["full_name"] = tex
                has_init = True

            for dir in os.listdir(batch_path):
                folder_dir = os.path.join(batch_path, dir)
                if os.path.isdir(folder_dir):
                    json_path = os.path.join(folder_dir, "Batch_{}_{}.json".format(index, dir))
                    single_nft_json = json.load(open(json_path))
                    char_items = single_nft_json["CharacterItems"]
                    characters += 1

                    for slot in char_items.keys():
                        item_info = char_items[slot]
                        if item_info != "Null":
                            item = item_info[list(item_info)[0]]["item_texture"]
                            if item:
                                variant_name = item.split('_')[3] + ' ' + item.split('_')[4]
                                counter[variant_name]["count"] = counter[variant_name]["count"] + 1
                            else:
                                config.custom_print("THIS ITEM ({}) IS MISSING TEXTURE SETS".format(list(item_info)[0]), col=config.bcolors.ERROR)

    counter_sorted = {k: v for k, v in sorted(counter.items(), key=lambda item: -item[1]["count"])} # sort all items based on count
    counter_info = {}
    counter_info["Total Characters"] = characters
    counter_info["Items"] = counter_sorted
    counter_obj = json.dumps(counter_info, indent=1, ensure_ascii=True)
    with open(save_path, "w") as outfile:
        outfile.write(counter_obj)
    return


if __name__ == '__main__':
    count_all_rarities()