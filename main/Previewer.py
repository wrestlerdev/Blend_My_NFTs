# Purpose:
# This file generates NFT DNA based on a .blend file scene structure and exports NFTRecord.json.

import collections
from venv import create
from warnings import catch_warnings
import bpy
import os
import re
import copy
import time
import json
import random
import importlib
from functools import partial


enableGeneration = False
colorList = []

saved_hierarchy = collections.OrderedDict()

class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR


# def show_NFT(DNA, hierarchy):

#    print("DNA: " + str(DNA))
#    dnaDictionary = {}
#    listAttributes = list(hierarchy.keys())

#    listDNADeconstructed = DNA.split('-')
#    for i, j in zip(listAttributes, listDNADeconstructed): 
#                 dnaDictionary[i] = j

#    for x in dnaDictionary: 
#       for k in hierarchy[x]:
#                     kNum = hierarchy[x][k]["number"]
#                     if kNum == dnaDictionary[x]:
#                         dnaDictionary.update({x: k})

      
#    for c in dnaDictionary:
#       # bpy.data.collections[c].hide_render = False
#       # bpy.data.collections[c].hide_viewport = False
#       print(dnaDictionary[c])
#       objs = bpy.data.collections[c].children
#       mesh_collection = bpy.data.collections[c].children[str(dnaDictionary[c])]

#       for obj in objs:
#          print(obj)
#          if obj == mesh_collection:
#             mesh_collection.hide_render = False
#             mesh_collection.hide_viewport = False
#          else:
#             obj.hide_render = True
#             obj.hide_viewport = True

#       # for obj in mesh_collection.objects:
#       #    print(obj)


def show_nft_from_dna(DNA): # goes through collection hiearchy based on index to hide/show DNA
   hierarchy = get_hierarchy_ordered()

   coll_keys = list(hierarchy.keys())
   DNAString = DNA.split(",")
   for attribute in hierarchy:
      for type in hierarchy[attribute]:
            for variant in hierarchy[attribute][type]:
               print(variant)
               bpy.data.collections.get(variant).hide_viewport = True
               bpy.data.collections.get(variant).hide_render = True
   for strand in range(len(DNAString)):

      atttype_index, variant_index = DNAString[strand].split('-')
      slot = list(hierarchy.items())[strand]

      atttype = list(slot[1].items())[int(atttype_index)]
      variant = list(atttype[1].items())[int(variant_index)][0]
      bpy.data.collections[variant].hide_viewport = False
      bpy.data.collections[variant].hide_render = False
      # current_coll = bpy.context.scene.collection.children[slot[0]]
      # for variant in current_coll.children:
      #    variant.hide_render = True
      #    variant.hide_viewport = True
      # index = int(DNAString[int(strand)]) - 1
      # current_coll.children[index].hide_render = False
      # current_coll.children[index].hide_viewport = False


      
      

#  ----------------------------------------------------------------------------------


def get_random_from_collection(coll): # doesn't respect weights or filled slots
                                       # should check if from right collection
                                       # should set new dna too
   rand_int = random.randint(0,len(coll.children)-1)
   chosen_coll = coll.children[rand_int]
   for child in coll.children:
      child.hide_render = True
      child.hide_viewport = True
   chosen_coll.hide_render = False
   chosen_coll.hide_viewport = False
   return chosen_coll
 

def find_in_collection(variant_name, collection_name):
      collection = bpy.context.scene.collection.children[collection_name]
      set_from_collection(collection, variant_name)
      return collection.children[variant_name]


def set_from_collection(slot_coll, variant_name): # hide all in coll and show given variant based on name
   new_dna_strand = ''
   type_index = 0
   for type_coll in slot_coll.children:
      if variant_name in type_coll.children:
         type_list = list(type_coll.children)
         variant_index = type_list.index(bpy.data.collections[variant_name])

         new_dna_strand = (str(type_index) + '-' + str(variant_index))
      else:
         type_index += 1
   
   if new_dna_strand != '':
      for type_coll in slot_coll.children:
         for variant_coll in type_coll.children: # hide all
            variant_coll.hide_render = True
            variant_coll.hide_viewport = True
      bpy.data.collections[variant_name].hide_render = False
      bpy.data.collections[variant_name].hide_viewport = False


   return new_dna_strand # return dna strand or empty string if not valid





def collections_have_updated(slots_key, Slots): # this is called from init properties
    if bpy.context.scene.my_tool.get(slots_key) is not None:
      coll_name, label = Slots[slots_key]

      new_dnastrand = set_from_collection(bpy.data.collections[coll_name], bpy.context.scene.my_tool.get(slots_key).name)
      if new_dnastrand != '' and not(bpy.context.scene.my_tool.get(slots_key).hide_viewport): # if is from correct collection
         dna_string = bpy.context.scene.my_tool.inputDNA
         hierarchy = get_hierarchy_ordered()
         coll_index = list(hierarchy.keys()).index(coll_name)

         DNA = dna_string.split(',') 
         DNA[coll_index] = str(new_dnastrand)
         dna_string = ','.join(DNA)

         last_key = slots_key.replace("input", "last")
         bpy.context.scene.my_tool[last_key] = bpy.context.scene.my_tool.get(slots_key)
         bpy.context.scene.my_tool.lastDNA = dna_string
         bpy.context.scene.my_tool.inputDNA = dna_string

      else:
         print("is not valid || clear")
         last_key = slots_key.replace("input", "last")
         bpy.context.scene.my_tool[slots_key] = None
         bpy.context.scene.my_tool[slots_key] = bpy.context.scene.my_tool.get(last_key)


def dnastring_has_updated(DNA, lastDNA): # called from inputdna update, check if user has updated dna manually
   if DNA != lastDNA:
      DNA = DNA.replace('"', '')
      try:
         show_nft_from_dna(DNA)
         bpy.context.scene.my_tool.lastDNA = DNA
         bpy.context.scene.my_tool.inputDNA = DNA
         fill_pointers_from_dna(DNA, DNA)
      except:
         print("this is not a valid dna string")
   return


def create_item_dict(DNA):
   ohierarchy = get_hierarchy_ordered()
   coll_keys = list(ohierarchy.keys())
   
   uhierarchy = get_hierarchy_unordered()
   
   DNAString = DNA.split(",")

   item_dict = {}

   for strand in range(len(DNAString)):
      if DNAString[strand] == '0-0':
         item_dict[coll_keys[strand]] = "Null"
      else:
         atttype_index, variant_index = DNAString[strand].split('-')
         slot = list(ohierarchy.items())[strand]

         atttype = list(slot[1].items())[int(atttype_index)]
         variant = list(atttype[1].items())[int(variant_index)][0]
         
         variant_dict = {}
         coll_index = coll_keys[strand]
         # print("*****************************-----------------")
         # print(atttype[0])
         # print("*****************************")
         # print(variant)
         # print("*****************************-------------------")
         variant_dict[variant] = uhierarchy[coll_index][atttype[0]][variant]

         item_dict[coll_keys[strand]] = variant_dict
   nft_dict = {}
   nft_dict[DNA] = item_dict
   return nft_dict



def fill_pointers_from_dna(DNA, Slots):
   DNAString = DNA.split(',')
   ohierarchy = get_hierarchy_ordered()
   print(DNA)
   for i in range(len(DNAString)):

      atttype_index, variant_index = DNAString[i].split('-')

      # strand_index = int(DNAString[i]) - 1
      slot = list(ohierarchy.items())[i]
      atttype = list(slot[1].items())[int(atttype_index)]
      variant = list(atttype[1].items())[int(variant_index)][0]

      print(variant)
      print(slot[0])
      coll_name = slot[0][3:len(slot[0])]
      last_coll_name = "last" + str(coll_name)
      input_coll_name = "input" + str(coll_name)
      print(coll_name)
      # variant = variant[3:len(variant)]
      bpy.context.scene.my_tool[last_coll_name] = bpy.data.collections[variant]
      bpy.context.scene.my_tool[input_coll_name] = bpy.data.collections[variant]

      # coll_name = current_coll.name
      # coll_name = coll_name[3:int(len(coll_name))] # CHANGE 3 IF FOLDER NAMES CHANGE

      # last_coll_name = "last" + str(coll_name)
      # input_coll_name = "input" + str(coll_name)
      # bpy.context.scene.my_tool[last_coll_name] = current_coll.children[strand_index]
      # bpy.context.scene.my_tool[input_coll_name] = current_coll.children[strand_index]
   return




def get_hierarchy_ordered():
      global saved_hierarchy
      if(saved_hierarchy):
            return saved_hierarchy
      else:
            Blend_My_NFTs_Output = os.path.join("Blend_My_NFTs Output", "NFT_Data")
            NFTRecord_save_path = os.path.join(Blend_My_NFTs_Output, "NFTRecord.json")
            DataDictionary = json.load(open(NFTRecord_save_path), object_pairs_hook=collections.OrderedDict)
            hierarchy = DataDictionary["hierarchy"]
            DNAList = DataDictionary["DNAList"]
            saved_hierarchy = hierarchy
            return hierarchy
   

def get_hierarchy_unordered():
      Blend_My_NFTs_Output = os.path.join("Blend_My_NFTs Output", "NFT_Data")
      NFTRecord_save_path = os.path.join(Blend_My_NFTs_Output, "NFTRecord.json")
      DataDictionary = json.load(open(NFTRecord_save_path))
      hierarchy = DataDictionary["hierarchy"]

      return hierarchy




def assettest(DNA, library_path, inner_path, coll_name, Slot):

   coll = bpy.data.collections[coll_name]

   for child in coll.children:
      for obj in child.objects:
         bpy.data.objects.remove(obj)
      # coll.objects.unlink(coll.objects.get(obj))
      bpy.data.collections.remove(child)


   asset_name = 'Hands_Gloves_Mittens_2_20'
                 
   hierarchy = get_hierarchy_ordered()

   DNAString = DNA.split(",")
   slot_keys = list(Slot.keys())

   for strand in range(len(DNAString)):
      file_path = str(Slot[slot_keys[strand]][0]) + ".blend"
      new_path = os.path.join(library_path, file_path, inner_path)

      atttype_index, variant_index = DNAString[strand].split('-')
      slot = list(hierarchy.items())[strand]

      atttype = list(slot[1].items())[int(atttype_index)]
      variant = list(atttype[1].items())[int(variant_index)][0]

      asset_name = variant

      asset_path = os.path.join(new_path, asset_name)

      bpy.ops.wm.append(filepath=asset_path, directory=new_path,
                 filename=asset_name)

      # bpy.data.collections[variant].hide_viewport = False
      # bpy.data.collections[variant].hide_render = False


   for colls in bpy.data.collections["Imported"].children:
      colls.hide_viewport = False
      colls.hide_render = False
      print(colls)

   return


def assettest2(DNA, file_path, coll_name):

   coll = bpy.data.collections[coll_name]

   for child in coll.children:
      for obj in child.objects:
         bpy.data.objects.remove(obj)
      # coll.objects.unlink(coll.objects.get(obj))
      bpy.data.collections.remove(child)


   asset_name = 'Hands_Gloves_Mittens_2_20'
                 
   hierarchy = get_hierarchy_ordered()

   DNAString = DNA.split(",")

   for strand in range(len(DNAString)):

      atttype_index, variant_index = DNAString[strand].split('-')
      slot = list(hierarchy.items())[strand]

      atttype = list(slot[1].items())[int(atttype_index)]
      variant = list(atttype[1].items())[int(variant_index)][0]

      asset_name = variant

      asset_path = os.path.join(file_path, asset_name)

      bpy.ops.wm.append(filepath=asset_path, directory=file_path,
                 filename=asset_name)

      # bpy.data.collections[variant].hide_viewport = False
      # bpy.data.collections[variant].hide_render = False


   for colls in bpy.data.collections["Imported"].children:
      colls.hide_viewport = False
      colls.hide_render = False
      print(colls)





   return



if __name__ == '__main__':
   print("okay")