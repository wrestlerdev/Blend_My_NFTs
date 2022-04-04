# Purpose:
# 

from ctypes import sizeof
import bpy
import os
import re
import copy
import time
import json
import random
import importlib
from functools import partial

col = {"red" : 'COLOR_01', 'orange' : 'COLOR_02', 'yellow' : 'COLOR_03', "green" : "COLOR_04",
         "blue" : "COLOR_05", "purple" : "COLOR_06", "pink" : "COLOR_07", "brown" : "COLOR_08"}


def read_DNAList_from_file(index): # return DNA as string
    NFTRecord_save_path = bpy.context.scene.my_tool.NFTRecord_save_path
    DataDictionary = json.load(open(NFTRecord_save_path))
    DNAList = DataDictionary["DNAList"]

    if index < len(DNAList):
        DNA = DNAList[index]
        return len(DNAList), DNA
    else:
        return len(DNAList), ''

def get_total_DNA(): # get number of saved DNAs
    NFTRecord_save_path = bpy.context.scene.my_tool.NFTRecord_save_path
    DataDictionary = json.load(open(NFTRecord_save_path))
    DNAList = DataDictionary["DNAList"]
    return len(DNAList)


# def load_in_Rarity_file():
#     RarityFile = json.load(open("raritytest.json"))
#     hierarchy = RarityFile["raritytest"]
#     h_keys = list(hierarchy["01-UpperTorso"].keys())
#     for h in h_keys:
#         # print(hierarchy["01-UpperTorso"][h])
#         model_type_key = list(hierarchy["01-UpperTorso"][h].keys())
#         for m in model_type_key:
#             print(str(m) + " rarity: " + str(hierarchy["01-UpperTorso"][h][m]["rarity"]))

#     print()
#     return hierarchy

def init_batch(batch_data_path):
    delete_batch_files(batch_data_path)

    if not os.path.exists(batch_data_path):
        os.makedirs(batch_data_path)

    first_batch_path = os.path.join(batch_data_path, "Batch_1")
    if not os.path.exists(first_batch_path):
        os.makedirs(first_batch_path)
    
    return


def make_rarity_dict_from_NFTRecord(index, NFTRecord_save_path, batch_save_path):
    DataDictionary = json.load(open(NFTRecord_save_path))
    hierarchy = DataDictionary["hierarchy"]

    rarity_dict = {}
    type_dict = {}
    slot_dict= {}

    slots = list(hierarchy.keys())
    for slot in slots:
        types = list(hierarchy[slot].keys())
        type_dict = {}
        for type in types:
            variant_dict = {}
            variants = list(hierarchy[slot][type].keys())

            type_rarity = type.split('_') # gets type rarity from collection name atm
            type_rarity = int(type_rarity[1])
            total_rarity = 0
            for v in variants:
                rarity = hierarchy[slot][type][v]["rarity"]

                # print(str(v) + ", rarity: " + str(rarity))
                variant_dict[v] = int(float(rarity))
                total_rarity += int(float(rarity))
            type_dict[type] = {"type_rarity" : type_rarity, "variant_total" : total_rarity,  "variants" : variant_dict}
        slot_dict[slot] = type_dict
    rarity_dict = slot_dict

    rarity_dict_object = json.dumps(rarity_dict, indent=1, ensure_ascii=True)

    first_batch_save_path = os.path.join(batch_save_path, "Batch_1",'_RarityBatch{}.json'.format(index))

    with open(os.path.join('', (first_batch_save_path)), "w") as outfile:
        outfile.write(rarity_dict_object)

    update_collection_rarity_property(rarity_dict, NFTRecord_save_path)
    return



def load_rarity_batch_dict(index, save_path):
    batch_save_path = os.path.join(save_path, 'Batch_{}'.format(index))
    rarity_save_path = os.path.join(batch_save_path,'_RarityBatch{}.json'.format(index))
    RarityDict = json.load(open(rarity_save_path))
    print(RarityDict)

    return RarityDict




def update_collection_rarity_property(RarityDict, NFTRecord_save_path):
    DataDictionary = json.load(open(NFTRecord_save_path))
    hierarchy = DataDictionary["hierarchy"]

    slots = list(hierarchy.keys())
    for slot in slots:
        types = list(hierarchy[slot].keys())
        for type in types:
            variants = list(hierarchy[slot][type].keys())
            type_coll = bpy.data.collections[type]
            type_rarity = int(RarityDict[slot][type]["type_rarity"])
            type_coll["rarity"] =  type_rarity
            update_rarity_color(type, type_rarity)

            for v in variants:
                rarity = RarityDict[slot][type]["variants"][v]
                var_coll = bpy.data.collections[v]
                var_coll["rarity"] = int(rarity)
                update_rarity_color(v, int(float(rarity)))
                # print(str(v) + ", rarity: " + str(rarity))
    return


def save_collection_rarity_property(index, NFTRecord_save_path, batch_path):
    dir_name = 'Batch_' + str(index)
    dir_path = os.path.join(batch_path, dir_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    DataDictionary = json.load(open(NFTRecord_save_path))
    hierarchy = DataDictionary["hierarchy"]

    rarity_dict = {}
    type_dict = {}
    slot_dict= {}

    slots = list(hierarchy.keys())
    for slot in slots:
        types = list(hierarchy[slot].keys())
        type_dict = {}
        for type in types:
            variant_dict = {}
            variants = list(hierarchy[slot][type].keys())
            total_rarity = 0

            type_coll = bpy.data.collections[type]
            type_rarity = type_coll["rarity"]
            update_rarity_color(type, type_rarity)

            for v in variants:
                var_coll = bpy.data.collections[v]
                # print(str(v) + ", rarity: " + str(rarity))
                variant_dict[v] = var_coll["rarity"]
                update_rarity_color(v, int(float(var_coll["rarity"])))
                total_rarity += int(float(var_coll["rarity"]))


            type_dict[type] = {"type_rarity" : type_rarity, "variant_total" : total_rarity,  "variants" : variant_dict}
        slot_dict[slot] = type_dict
    rarity_dict = slot_dict
    # rarity_dict["variants"] = variant_dict
    # print(rarity_dict)
    current_batch_path = os.path.join(batch_path, 'Batch_{}'.format(index))
    rarity_save_path = os.path.join(current_batch_path, '_RarityBatch{}.json'.format(index))

    rarity_dict_object = json.dumps(rarity_dict, indent=1, ensure_ascii=True)
    with open(os.path.join('', (rarity_save_path)), "w") as outfile:
        outfile.write(rarity_dict_object)

    return



def delete_batch_files(batch_path):
    batches = os.listdir(batch_path)
    for i in batches:
        batch = os.path.join(batch_path, i)
        if os.path.exists(batch):
            try:
                # os.remove(os.path.join(batch_path, i))
                items = os.listdir(os.path.join(batch_path, i))
                for item in items:
                    os.remove(os.path.join(batch_path, i, item))
                os.rmdir(os.path.join(batch_path, i))
            except:
                print("can't delete >:^(")

    return


def batch_property_updated():
    if(bpy.context.scene.my_tool.BatchIndex != bpy.context.scene.my_tool.lastBatchIndex): # to stop recursion

        BatchRarity_save_path = bpy.context.scene.my_tool.batch_json_save_path
        
        newIndex = bpy.context.scene.my_tool.BatchIndex
        rarityBatches = len(os.listdir(BatchRarity_save_path))
        if newIndex > rarityBatches:
            bpy.context.scene.my_tool.BatchIndex = rarityBatches
            bpy.context.scene.my_tool.lastBatchIndex = rarityBatches

    return



def update_rarity_color(coll_name, rarity):
    if rarity > 80:
        bpy.data.collections[coll_name].color_tag = col["brown"]
    elif rarity > 60:
        bpy.data.collections[coll_name].color_tag = col["blue"]
    elif rarity > 40:
        bpy.data.collections[coll_name].color_tag = col["green"]
    elif rarity > 20:
        bpy.data.collections[coll_name].color_tag = col["orange"]
    elif rarity > 0:
        bpy.data.collections[coll_name].color_tag = col["yellow"]
    else:
        bpy.data.collections[coll_name].color_tag = col["red"]
    return


def update_current_batch(index, batch_path): # updates current batch record path to new batch record
    new_path = ("Batch_" + str(index))
    new_path = os.path.join(batch_path, new_path)
    new_record_path = os.path.join(new_path, ("_NFTRecord{}.json".format(index)))
    new_rarity_path = os.path.join(new_path, ("_RarityBatch{}.json".format(index)))
    bpy.context.scene.my_tool.NFTRecord_save_path = new_record_path
    bpy.context.scene.my_tool.Rarity_save_path = new_rarity_path


    new_batch_path = os.path.join(batch_path, 'Batch_{}'.format(index))
    if not os.path.exists(new_batch_path):
        os.makedirs(new_batch_path)
        return
    return