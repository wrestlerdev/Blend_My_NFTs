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
    batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(index), "_NFTRecord{}.json".format(index))
    DataDictionary = json.load(open(NFTRecord_save_path))
    DNAList = DataDictionary["DNAList"]

    if index < len(DNAList):
        DNA = DNAList[index]
        return len(DNAList), DNA
    else:
        return len(DNAList), ''

def get_total_DNA(): # get number of saved DNAs
    index = bpy.context.scene.my_tool.CurrentBatchIndex
    batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(index), "_NFTRecord{}.json".format(index))
    DataDictionary = json.load(open(NFTRecord_save_path))
    DNAList = DataDictionary["DNAList"]
    return len(DNAList)


def init_batch(batch_data_path):
    delete_batch_files(batch_data_path)

    if not os.path.exists(batch_data_path):
        os.makedirs(batch_data_path)

    first_batch_path = os.path.join(batch_data_path, "Batch_1")
    if not os.path.exists(first_batch_path):
        os.makedirs(first_batch_path)
    
    return


# def make_rarity_dict_from_NFTRecord(index, NFTRecord_save_path, batch_save_path):
#     DataDictionary = json.load(open(NFTRecord_save_path))
#     hierarchy = DataDictionary["hierarchy"]

#     rarity_dict = {}
#     type_dict = {}
#     slot_dict= {}

#     slots = list(hierarchy.keys())
#     for slot in slots:
#         types = list(hierarchy[slot].keys())
#         type_dict = {}
#         for type in types:
#             variant_dict = {}
#             variants = list(hierarchy[slot][type].keys())

#             type_rarity = type.split('_') # gets type rarity from collection name atm
#             type_rarity = int(type_rarity[1])
#             total_rarity = 0
#             for v in variants:
#                 rarity = hierarchy[slot][type][v]["rarity"]

#                 variant_dict[v] = int(float(rarity))
#                 total_rarity += int(float(rarity))
#             type_dict[type] = {"type_rarity" : type_rarity, "variant_total" : total_rarity,  "variants" : variant_dict}
#         slot_dict[slot] = type_dict
#     rarity_dict = slot_dict

#     rarity_dict_object = json.dumps(rarity_dict, indent=1, ensure_ascii=True)

#     first_batch_save_path = os.path.join(batch_save_path, "Batch_1",'_RarityBatch{}.json'.format(index))

#     with open(os.path.join('', (first_batch_save_path)), "w") as outfile:
#         outfile.write(rarity_dict_object)

#     update_collection_rarity_property(NFTRecord_save_path)
#     return



def update_collection_rarity_property(NFTRecord_save_path):
    DataDictionary = json.load(open(NFTRecord_save_path))
    hierarchy = DataDictionary["hierarchy"]

    slots = list(hierarchy.keys())
    for slot in slots:
        types = list(hierarchy[slot].keys())
        for type in types:
            variants = list(hierarchy[slot][type].keys())
            type_coll = bpy.data.collections[type]
            type_rarity = hierarchy[slot][type][variants[0]]["type_rarity"]
            type_coll["rarity"] =  int(float(type_rarity))
            update_rarity_color(type, type_rarity)

            for v in variants:
                rarity = hierarchy[slot][type][v]["rarity"]
                var_coll = bpy.data.collections[v]
                var_coll["rarity"] = int(float(rarity))
                update_rarity_color(v, int(float(rarity)))
    return


def save_collection_rarity_property(index, NFTRecord_save_path, batch_path):
    dir_name = 'Batch_' + str(index)
    dir_path = os.path.join(batch_path, dir_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    DataDictionary = json.load(open(NFTRecord_save_path))
    hierarchy = DataDictionary["hierarchy"]

    slots = list(hierarchy.keys())
    for slot in slots:
        types = list(hierarchy[slot].keys())
        for type in types:
            variant_dict = {}
            variants = list(hierarchy[slot][type].keys())
            total_rarity = 0

            type_coll = bpy.data.collections[type]
            if type_coll.get('rarity') is not None:
                type_rarity = type_coll["rarity"]
            else:
                rarity = type.split('_')[4]
                type_rarity = rarity
                type_coll["rarity"] = rarity
            update_rarity_color(type, type_rarity)

            for v in variants:
                var_coll = bpy.data.collections[v]
                # print(str(v) + ", rarity: " + str(rarity))
                if var_coll.get('rarity') is not None:
                    variant_dict[v] = var_coll["rarity"]
                    update_rarity_color(v, int(float(var_coll["rarity"])))
                    total_rarity += int(float(var_coll["rarity"]))
                else:   
                    v_rarity = v.split('_')[4]
                    var_coll['rarity'] = int(v_rarity)
                    variant_dict[v] = v_rarity # TODO
                    update_rarity_color(v, int(v_rarity))
                    total_rarity += int(v_rarity)
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
    if(bpy.context.scene.my_tool.BatchSliderIndex != bpy.context.scene.my_tool.lastBatchSliderIndex): # to stop recursion

        Batch_save_path = bpy.context.scene.my_tool.batch_json_save_path
        
        newIndex = bpy.context.scene.my_tool.BatchSliderIndex
        batches = len(os.listdir(Batch_save_path))
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
    elif rarity > 0:
        bpy.data.collections[coll_name].color_tag = col["yellow"]
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



def check_if_paths_exist(batch_num=1):
    # return
    if bpy.context.scene.my_tool.batch_json_save_path == '':
        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        Blend_My_NFTs_Output = os.path.join(save_path, "Blend_My_NFTs Output", "NFT_Data")
        bpy.context.scene.my_tool.batch_json_save_path = os.path.join(Blend_My_NFTs_Output, "Batch_Data")
        bpy.context.scene.my_tool.CurrentBatchIndex = batch_num
