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
    Blend_My_NFTs_Output = os.path.join("Blend_My_NFTs Output", "NFT_Data")
    NFTRecord_save_path = os.path.join(Blend_My_NFTs_Output, "NFTRecord.json")
    DataDictionary = json.load(open(NFTRecord_save_path))
    DNAList = DataDictionary["DNAList"]

    if index < len(DNAList):
        DNA = DNAList[index]
        return len(DNAList), DNA
    else:
        return len(DNAList), ''

def get_total_DNA(): # get number of saved DNAs
    Blend_My_NFTs_Output = os.path.join("Blend_My_NFTs Output", "NFT_Data")
    NFTRecord_save_path = os.path.join(Blend_My_NFTs_Output, "NFTRecord.json")
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


def make_rarity_dict_from_NFTRecord(index, NFTRecord_save_path, save_path):
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

    RarityBatch_save_path = os.path.join(save_path, 'RarityBatch{}.json'.format(index))

    with open(os.path.join('', (RarityBatch_save_path)), "w") as outfile:
        outfile.write(rarity_dict_object)

    update_collection_rarity_property(rarity_dict, NFTRecord_save_path)

    return



def load_rarity_batch_dict(index, save_path):
    RarityBatch_save_path = os.path.join(save_path, 'RarityBatch{}.json'.format(index))
    RarityDict = json.load(open(RarityBatch_save_path))
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

def save_collection_rarity_property(index, NFTRecord_save_path, save_path):
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

    RarityBatch_save_path = os.path.join(save_path, 'RarityBatch{}.json'.format(index))

    rarity_dict_object = json.dumps(rarity_dict, indent=1, ensure_ascii=True)
    with open(os.path.join('', (RarityBatch_save_path)), "w") as outfile:
        outfile.write(rarity_dict_object)

    return



def delete_rarity_files(save_path):
    batches = os.listdir(save_path)
    for i in batches:
        batch = os.path.join(save_path, i)
        if os.path.exists(batch):
            
            os.remove(os.path.join(save_path, i))
    return


def rarity_batch_property_updated():
    if(bpy.context.scene.my_tool.rarityBatchIndex != bpy.context.scene.my_tool.lastrarityBatchIndex): # to stop recursion
        BatchRarity_save_path = bpy.context.scene.my_tool.rarity_json_save_path
        
        newIndex = bpy.context.scene.my_tool.rarityBatchIndex
        rarityBatches = len(os.listdir(BatchRarity_save_path))
        if newIndex > rarityBatches:
            bpy.context.scene.my_tool.rarityBatchIndex = rarityBatches
            bpy.context.scene.my_tool.lastrarityBatchIndex = rarityBatches
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

