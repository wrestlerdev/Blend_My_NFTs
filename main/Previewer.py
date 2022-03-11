# Purpose:
# This file generates NFT DNA based on a .blend file scene structure and exports NFTRecord.json.

from venv import create
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

lastPointer = []

class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR

class Last_Pointers(bpy.types.PropertyGroup):
      lastUpperTorso: bpy.props.PointerProperty(name="", type=bpy.types.Collection)


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
   collections = bpy.context.scene.collection.children
   coll_keys = collections.keys()
   DNAString = DNA.split("-")
   for strand in range(len(DNAString)):
      current_coll = collections[coll_keys[int(strand)+1]] # if script ignore is first folder
      for variant in current_coll.children:
         variant.hide_render = True
         variant.hide_viewport = True
      index = int(DNAString[int(strand)]) - 1
      current_coll.children[index].hide_render = False
      current_coll.children[index].hide_viewport = False
      

#  ----------------------------------------------------------------------------------


def get_random_from_collection(coll): # doesn't respect weights or filled slots
                                       # should check if from right collection
   rand_int = random.randint(0,len(coll.children)-1)
   chosen_coll = coll.children[rand_int]
   for child in coll.children:
      child.hide_render = True
      child.hide_viewport = True
   chosen_coll.hide_render = False
   chosen_coll.hide_viewport = False
   return chosen_coll
 


def set_from_collection(coll, variant): # hide all in coll and show given variant based on name
   if variant in coll.children:
      vname = variant.split('_')
      print(vname[3])
      DNA = ''
      for child in coll.children:
         child.hide_render = True
         child.hide_viewport = True
      new_index = int(vname[3])-1
      coll.children[new_index].hide_render = False
      coll.children[new_index].hide_viewport = False
      return new_index + 1
   return -1



def collections_have_updated(slots_key, Slots): # this is called from init properties
    if bpy.context.scene.my_tool.get(slots_key) is not None:
      coll_name, label = Slots[slots_key]
      collections = bpy.context.scene.collection.children
      new_dnastrand = set_from_collection(bpy.data.collections[coll_name], bpy.context.scene.my_tool.get(slots_key).name)

      if new_dnastrand >= 0 and not(bpy.context.scene.my_tool.get(slots_key).hide_viewport): # if is from correct collection
         dna_string = bpy.context.scene.my_tool.inputDNA
         coll_index = list(collections.keys()).index(coll_name)
         print(coll_index)
         DNA = dna_string.split('-') 
         DNA[coll_index - 1] = str(new_dnastrand) # including script ignore
         dna_string = '-'.join(DNA)
         last_key = slots_key.replace("input", "last")
         bpy.context.scene.my_tool[last_key] = bpy.context.scene.my_tool.get(slots_key)
         bpy.context.scene.my_tool.inputDNA = dna_string

      else:
         print("is not valid || clear")
         last_key = slots_key.replace("input", "last")
         bpy.context.scene.my_tool[slots_key] = None
         bpy.context.scene.my_tool[slots_key] = bpy.context.scene.my_tool.get(last_key)



def fill_pointers_from_dna(DNA):
   if(not lastPointer):
      print("wow")
   
   DNAString = DNA.split('-')
   collections = bpy.context.scene.collection.children
   coll_list = list(collections.keys())
   for i in range(len(DNAString)):
      strand_index = int(DNAString[i]) - 1
      current_coll = collections[coll_list[i+1]] # i+1  bc script ignore

      coll_name = current_coll.name
      if coll_name == "AUpperTorso":
            bpy.context.scene.my_tool.lastUpperTorso = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputUpperTorso = current_coll.children[strand_index]
      elif coll_name == "ILowerTorso":
            bpy.context.scene.my_tool.lastLowerTorso = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputLowerTorso = current_coll.children[strand_index]
      elif coll_name == "HHands":
            bpy.context.scene.my_tool.lastHands = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputHands = current_coll.children[strand_index]
      elif coll_name == "JCalf":
            bpy.context.scene.my_tool.lastCalf = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputCalf = current_coll.children[strand_index]
      elif coll_name == "KAnkle":
            bpy.context.scene.my_tool.lastAnkle = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputAnkle = current_coll.children[strand_index]
      elif coll_name == "LFeet":
            bpy.context.scene.my_tool.lastFeet = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputFeet = current_coll.children[strand_index]
      elif coll_name == "MNeck":
            bpy.context.scene.my_tool.lastNeck = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputNeck = current_coll.children[strand_index]
      elif coll_name == "BMiddleTorso":
            bpy.context.scene.my_tool.lastMiddleTorso = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputMiddleTorso = current_coll.children[strand_index]
      elif coll_name == "CLForeArm":
            bpy.context.scene.my_tool.lastLForeArm = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputLForeArm = current_coll.children[strand_index]
      elif coll_name == "DLWrist":
            bpy.context.scene.my_tool.lastLWrist = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputLWrist = current_coll.children[strand_index]
      elif coll_name == "ERForeArm":
            bpy.context.scene.my_tool.lastRForeArm = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputRForeArm = current_coll.children[strand_index]
      elif coll_name == "FRWrist":
            bpy.context.scene.my_tool.lastRWrist = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputRWrist = current_coll.children[strand_index]
      elif coll_name == "NLowerHead":
            bpy.context.scene.my_tool.lastLowerHead = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputLowerHead = current_coll.children[strand_index]
      elif coll_name == "OMiddleHead":
            bpy.context.scene.my_tool.lastMiddleHead = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputMiddleHead = current_coll.children[strand_index]
      elif coll_name == "PEarings":
            bpy.context.scene.my_tool.lastEarrings = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputEarrings = current_coll.children[strand_index]
      elif coll_name == "QUpperHead":
            bpy.context.scene.my_tool.lastUpperHead = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputUpperHead = current_coll.children[strand_index]
      elif coll_name == "RBackPack":
            bpy.context.scene.my_tool.lastBackpack = current_coll.children[strand_index]
            bpy.context.scene.my_tool.inputBackpack = current_coll.children[strand_index]

   return

if __name__ == '__main__':
   print("okay")