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
import shutil

col = {"red" : 'COLOR_01', 'orange' : 'COLOR_02', 'yellow' : 'COLOR_03', "green" : "COLOR_04",
         "blue" : "COLOR_05", "purple" : "COLOR_06", "pink" : "COLOR_07", "brown" : "COLOR_08"}


def read_DNAList_from_file(batch_index, index): # return DNA as string
    batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(batch_index), "_NFTRecord_{:03d}.json".format(batch_index))
    DataDictionary = json.load(open(NFTRecord_save_path))
    DNAList = DataDictionary["DNAList"]

    if index <= len(DNAList):
        DNA = DNAList[index - 1]
        return len(DNAList), DNA
    else:
        return len(DNAList), ''

def get_total_DNA(): # get number of saved DNAs
    index = bpy.context.scene.my_tool.CurrentBatchIndex
    batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(index), "_NFTRecord_{:03d}.json".format(index))
    DataDictionary = json.load(open(NFTRecord_save_path))
    DNAList = DataDictionary["DNAList"]
    return len(DNAList)


def init_batch(batch_data_path): # delete all batch data then create first batch folder
    # delete_batch_files(batch_data_path)
    shutil.rmtree(batch_data_path)

    os.makedirs(batch_data_path)
    first_batch_path = os.path.join(batch_data_path, "Batch_{:03d}".format(1))
    if not os.path.exists(first_batch_path):
        os.makedirs(first_batch_path)
    return



def update_collection_rarity_property(NFTRecord_save_path): # update rarity value for in scene collections
    DataDictionary = json.load(open(NFTRecord_save_path)) # sets any collection not in hierarchy as rarity = 0
    hierarchy = DataDictionary["hierarchy"]

    slots = list(hierarchy.keys())
    # scene_slot_colls = bpy.data.collections[slot].children
    for slot in slots:
        types = list(hierarchy[slot].keys())
        scene_type_colls = bpy.data.collections[slot].children
        for scene_type_coll in scene_type_colls:
            type = scene_type_coll.name
            variants = list(hierarchy[slot][type].keys())
            #This checks if a type has any varinets in it BETA_1.0
            if len(variants) > 0:
                #This checks if a varients has any texture sets in it BETA_1.0
                for h_variant in variants:
                    h_variant_exists = False
                    if len(list(hierarchy[slot][type][h_variant].keys())) > 0:
                        h_variant_exists = True
                        break
                if h_variant_exists:
                # if len(list(hierarchy[slot][type][variants[0]].keys())) > 0 or len(list(hierarchy[slot][type][variant].keys())) > 0:
                    first_texture = list(hierarchy[slot][type][h_variant].keys())[0]
                    type_rarity = hierarchy[slot][type][h_variant][first_texture]["type_rarity"]
                    if type in types:
                        scene_type_coll["rarity"] =  int(float(type_rarity))
                        update_rarity_color(type, type_rarity)
                    else:
                        scene_type_coll["rarity"] =  0
                        update_rarity_color(type, 0)

                    scene_var_colls = scene_type_coll.children

                    for scene_var_coll in scene_var_colls:
                        variant = scene_var_coll.name
                        if variant in variants and type in types:
                            first_texture = list(hierarchy[slot][type][variant].keys())[0]
                            variant_rarity = hierarchy[slot][type][variant][first_texture]["variant_rarity"]
                            update_rarity_color(variant, int(float(variant_rarity)))
                            scene_var_coll["rarity"] = int(float(variant_rarity))
                        
                            textures = list(hierarchy[slot][type][variant].keys())
                        else:
                            update_rarity_color(variant, 0)
                            scene_var_coll["rarity"] = 0

                            textures = []
                        scene_tex_colls = scene_var_coll.children
                        for scene_text_coll in scene_tex_colls:
                            texture = scene_text_coll.name
                            if texture in textures:
                                texture_rarity = hierarchy[slot][type][variant][texture]["texture_rarity"]
                                scene_text_coll["rarity"] = int(float(texture_rarity))
                                update_rarity_color(texture, int(float(texture_rarity)))
                            else:
                                scene_text_coll["rarity"] = 0
                                update_rarity_color(texture, 0)
                else: # BETA_1.0
                    current_var_coll = bpy.data.collections[h_variant]
                    # current_var_coll["rarity"] = 0
                    # scene_type_coll["rarity"] = 0
                    if current_var_coll.get("rarity") is not None:
                        del(current_var_coll["rarity"])
                    if scene_type_coll.get("rarity") is not None:
                        del(scene_type_coll["rarity"])
                    
                    update_rarity_color(type, 0)
                    update_rarity_color(h_variant, 0)
            else: # BETA_1.0
                if scene_type_coll.get("rarity") is not None:
                    del(scene_type_coll["rarity"])
                # scene_type_coll["rarity"] = 0
                update_rarity_color(type, 0)
    return


def save_collection_rarity_property(index, NFTRecord_save_path, batch_path): # save current rarity from collections to record
    dir_name = 'Batch_{:03d}'.format(index)
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
            # first_texture = list(hierarchy[slot][type][variants[0]].keys())[0]

            type_coll = bpy.data.collections[type]
            if type_coll.get('rarity') is not None:
                type_rarity = type_coll["rarity"]
            else:
                # rarity = type.split('_')[4]
                rarity = 50 # BETA_1.0
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
                    # v_rarity = v.split('_')[4]
                    v_rarity = 50 # BETA_1.0
                    var_coll['rarity'] = int(v_rarity)
                    variant_dict[v] = v_rarity # TODO
                    update_rarity_color(v, int(v_rarity))
                    total_rarity += int(v_rarity)

                textures = list(hierarchy[slot][type][v].keys())
                for tex in textures:
                    tex_coll = bpy.data.collections[tex]
                    if tex_coll.get('rarity') is not None:
                        tex_rarity = int((float(tex_coll["rarity"])))
                    else:
                        tex_rarity = int(float(hierarchy[slot][type][v][tex]["texture_rarity"]))
                        tex_coll['rarity'] = int(tex_rarity)
                    update_rarity_color(tex, tex_rarity)
    return


def batch_property_updated(): # check if batch is out of range then set in range if it is
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

    new_batch_path = os.path.join(batch_path, 'Batch_{:03d}'.format(index))
    if not os.path.exists(new_batch_path):
        os.makedirs(new_batch_path)
        return
    return



def check_if_paths_exist(batch_num=1): # may be redundant now
    root_output_path = os.path.join(bpy.context.scene.my_tool.root_dir, "Blend_My_NFTs Output", "OUTPUT")
    if bpy.context.scene.my_tool.batch_json_save_path == '':
        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        Blend_My_NFTs_Output = os.path.join(save_path, "Blend_My_NFTs Output")
        bpy.context.scene.my_tool.batch_json_save_path = os.path.join(Blend_My_NFTs_Output, "OUTPUT")
        bpy.context.scene.my_tool.CurrentBatchIndex = batch_num
    # elif root_output_path != bpy.context.scene.my_tool.batch_json_save_path:
    #     bpy.context.scene.my_tool.batch_json_save_path = root_output_path
