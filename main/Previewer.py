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
from mathutils import Color
from . import config

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




def show_nft_from_dna(DNA): # goes through collection hiearchy based on index to hide/show DNA
   hierarchy = get_hierarchy_ordered()

   DNAString = DNA.split(",")
   character = DNAString.pop(0)
   show_character(character)
   for attribute in hierarchy: # hide all
      for type in hierarchy[attribute]:
            for variant in hierarchy[attribute][type]:
               bpy.data.collections[variant].hide_viewport = True
               bpy.data.collections[variant].hide_render = True
               char_var = variant + '_' + character

               if bpy.data.collections.get(char_var) is not None:
                  bpy.data.collections.get(char_var).hide_viewport = True
                  bpy.data.collections.get(char_var).hide_render = True

               for texture in hierarchy[attribute][type][variant]:
                  bpy.data.collections[texture].hide_viewport = True
                  bpy.data.collections[texture].hide_render = True

   for strand in range(len(DNAString)):
      DNASplit = DNAString[strand].split('-')
      atttype_index = DNASplit[0]
      variant_index = DNASplit[1]
      texture_index = DNASplit[2]

      slot = list(hierarchy.items())[strand]
      atttype = list(slot[1].items())[int(atttype_index)]
      variant = list(atttype[1].items())[int(variant_index)]
      texture = list(variant[1].items())[int(texture_index)][0]
      texture_children = bpy.data.collections[texture].children
         
      if len(DNASplit) > 3:
         style = DNASplit[3]
         hex_01 = DNASplit[4]
         hex_02 = DNASplit[5]
         hex_03 = DNASplit[6]

         if texture_children:
            for child in texture_children:
               if child.name.split('_')[-1] == character:
                  meshes = child.objects
                  child.hide_viewport = False
                  child.hide_render = False
               else:
                  child.hide_viewport = True
                  child.hide_render = True
         else:
            meshes = bpy.data.collections.get(list(variant)[0]).objects
            #meshes = bpy.data.collections.get(texture).objects

         set_armature_for_meshes(character, meshes)

         for mesh in meshes:
            obj = bpy.data.objects[mesh.name]
            col_01 = Color(HexToRGB(hex_01))
            col_02 = Color(HexToRGB(hex_02))
            col_03 = Color(HexToRGB(hex_03))
            obj["TestColor"] = col_01
            obj["R"] = col_01
            obj["G"] = col_02
            obj["B"] = col_03
            obj.hide_viewport = False
            obj.hide_render = False


      bpy.data.collections[variant[0]].hide_viewport = False
      bpy.data.collections[variant[0]].hide_render = False

      bpy.data.collections[texture].hide_viewport = False
      bpy.data.collections[texture].hide_render = False


def HexToRGB(hex):
   string = hex.lstrip('#')
   rgb255 = tuple( int(string[i:i+2], 16) for i in (0,2,4) )
   rgb = tuple( (float(x) /255) for x in rgb255)
   return rgb
      
      

#  ----------------------------------------------------------------------------------



def set_from_collection(slot_coll, variant_name): # hide all in coll and show given variant based on name
   if str(variant_name.split('_')[-2]).isnumeric():
      print("this is a variant")
      texture_variant = 'A'
      variant_string = variant_name.split('_')
      variant_string[-2] = str(variant_string[-2]) + 'A'
      texture_name = '_'.join(variant_string)

   else: # get variant name by stripping out texture
      print("is this a texture var?")
      texture_name = variant_name
      variant_string = variant_name.split('_')

      version_num = ''. join(i for i in (variant_string[-2]) if i.isdigit())
      texture_variant = ''. join(i for i in (variant_string[-2]) if not i.isdigit())

      variant_string[-2] = version_num
      variant_name = '_'.join(variant_string)

   new_dna_strand = ''
   type_index = 0
   variant_index = 0

   lastDNA = bpy.context.scene.my_tool.lastDNA
   DNAString = lastDNA.split(",")
   character = DNAString.pop(0)

   hierarchy = get_hierarchy_unordered()
   attributeskeys = list(hierarchy.keys())
   attributes_index = attributeskeys.index(slot_coll.name)

   DNAStrand = DNAString[attributes_index]
   DNASplit = DNAStrand.split('-')
   last_color = DNASplit[3:]
   if not last_color:
      last_color = ['a'].append(["#FFFFFF"] * 3) #CHECK THIS

   for type_coll in slot_coll.children:
      if variant_name in type_coll.children:
         var_coll = bpy.data.collections[variant_name]
         type_list = list(type_coll.children)
         variant_index = type_list.index(var_coll)
         # for texture_coll in variant_coll.children:
         texture_index = ord(texture_variant) - 65 # 'A' is 65 in ASCII

         dna_string = [str(type_index), str(variant_index), str(texture_index)]
         dna_string += last_color

         new_dna_strand = '-'.join(dna_string)
         break # CHECK THIS
      else:
         type_index += 1
         print(type_coll.name)
         print(variant_name)
         # stop putting a break here lmao
   
   if new_dna_strand != '':
      for type_coll in slot_coll.children:
         for variant_coll in type_coll.children: # hide all
            variant_coll.hide_render = True
            variant_coll.hide_viewport = True
            for texture_coll in variant_coll.children:
               texture_coll.hide_render = True
               texture_coll.hide_viewport = True
            for variant_mesh in var_coll.objects: # placeholder
               variant_mesh.hide_render = True
               variant_mesh.hide_viewport = False

      texture_coll = bpy.data.collections[texture_name]

      var_coll.hide_render = False
      var_coll.hide_viewport = False
      texture_coll.hide_render = False
      texture_coll.hide_viewport = False

      if texture_coll.children:
         for child in texture_coll.children:
            if child.name.split('_')[-1] == character:
               meshes = child.objects
               child.hide_viewport = False
               child.hide_render = False
            else:
               child.hide_viewport = True
               child.hide_render = True
      else:
         meshes = bpy.data.collections.get(texture_name).objects

      for mesh in meshes:
         obj = bpy.data.objects[mesh.name]
         obj["TestColor"] = HexToRGB(last_color[1])
         obj["R"] = HexToRGB(last_color[1])
         obj["G"] = HexToRGB(last_color[2])
         obj["B"] = HexToRGB(last_color[3])
         obj.hide_viewport = False
         obj.hide_render = False

   return new_dna_strand # return dna strand or empty string if not valid





def collections_have_updated(slots_key, Slots): # this is called from init properties
    if bpy.context.scene.my_tool.get(slots_key) is not None:
      coll_name, label = Slots[slots_key]
      print("----")
      print(bpy.context.scene.my_tool.get(slots_key).name)
      print("")

      new_dnastrand = set_from_collection(bpy.data.collections[coll_name], bpy.context.scene.my_tool.get(slots_key).name)
      if new_dnastrand != '' and not(bpy.context.scene.my_tool.get(slots_key).hide_viewport): # if is from correct collection
         dna_string = bpy.context.scene.my_tool.inputDNA
         hierarchy = get_hierarchy_ordered()
         coll_index = list(hierarchy.keys()).index(coll_name)

         DNA = dna_string.split(',') 

         DNA[coll_index + 1] = str(new_dnastrand)
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
      show_nft_from_dna(DNA)
      bpy.context.scene.my_tool.lastDNA = DNA
      bpy.context.scene.my_tool.inputDNA = DNA
      fill_pointers_from_dna(DNA, DNA)
      # try:
      #    show_nft_from_dna(DNA)
      #    bpy.context.scene.my_tool.lastDNA = DNA
      #    bpy.context.scene.my_tool.inputDNA = DNA
      #    fill_pointers_from_dna(DNA, DNA)
      # except:
      #    print("this is not a valid dna string")
   return


def create_item_dict(DNA):
   ohierarchy = get_hierarchy_ordered()
   coll_keys = list(ohierarchy.keys())
   uhierarchy = get_hierarchy_unordered()
   DNAString = DNA.split(",")
   character = DNAString.pop(0)

   item_dict = {}

   for strand in range(len(DNAString)):
      if DNAString[strand] == '0-0-0':
         item_dict[coll_keys[strand]] = "Null"
      else:
         DNASplit = DNAString[strand].split('-')
         atttype_index = DNASplit[0]
         variant_index = DNASplit[1]
         texture_index = DNASplit[2]

         slot = list(ohierarchy.items())[strand]

         atttype = list(slot[1].items())[int(atttype_index)]
         variant = list(atttype[1].items())[int(variant_index)]
         texture = list(variant[1].items())[int(texture_index)][0]
         
         texturevariant_dict = {}
         coll_index = coll_keys[strand]
         uh_info = uhierarchy[coll_index][atttype[0]][variant[0]][texture]
         uh_info["color_style"] = DNASplit[3]
         uh_info["color_primary"] = DNASplit[4]
         uh_info["color_secondary"] = DNASplit[5]
         uh_info["color_tertiary"] = DNASplit[6]
         texturevariant_dict[texture] = uh_info
         item_dict[coll_keys[strand]] = texturevariant_dict
   nft_dict = {}
   nft_dict[DNA] = item_dict
   return nft_dict



def fill_pointers_from_dna(DNA, Slots):
   DNAString = DNA.split(',')
   character = DNAString.pop(0)
   show_character(character)
   
   ohierarchy = get_hierarchy_ordered()
   for i in range(len(DNAString)):

      DNASplit = DNAString[i].split('-')
      atttype_index = DNASplit[0]
      variant_index = DNASplit[1]
      texture_index = DNASplit[2]

      slot = list(ohierarchy.items())[i]
      atttype = list(slot[1].items())[int(atttype_index)]
      variant = list(atttype[1].items())[int(variant_index)]
      texture = list(variant[1].items())[int(texture_index)][0]

      coll_name = slot[0][3:len(slot[0])]
      last_coll_name = "last" + str(coll_name)
      input_coll_name = "input" + str(coll_name)
      bpy.context.scene.my_tool[last_coll_name] = bpy.data.collections[texture]
      bpy.context.scene.my_tool[input_coll_name] = bpy.data.collections[texture]

   return



def set_armature_for_meshes(character, meshes):
   armature_name = "armature_" + str(character).lower()
   if bpy.data.objects.get(armature_name) is not None:
      for mesh in meshes:
         if mesh.modifiers:
               for mod in mesh.modifiers:
                  if mod.type == 'ARMATURE':
                     print(mesh)
                     mod.object = bpy.data.objects[armature_name]
         else:
            mod = mesh.modifiers.new(name='armature', type='ARMATURE')
            mod.object = bpy.data.objects[armature_name]
   else:
      print("Armature '{}' does not exist atm".format(armature_name))



def get_hierarchy_ordered():
   global saved_hierarchy
   if(saved_hierarchy):
      return saved_hierarchy
   else:
      index = bpy.context.scene.my_tool.CurrentBatchIndex
      batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
      NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(index), "_NFTRecord_{:03d}.json".format(index))

      DataDictionary = json.load(open(NFTRecord_save_path), object_pairs_hook=collections.OrderedDict)
      hierarchy = DataDictionary["hierarchy"]
      saved_hierarchy = hierarchy
      return hierarchy


def get_hierarchy_unordered():
   index = bpy.context.scene.my_tool.CurrentBatchIndex
   batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
   NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(index), "_NFTRecord_{:03d}.json".format(index))      
   DataDictionary = json.load(open(NFTRecord_save_path))
   hierarchy = DataDictionary["hierarchy"]

   return hierarchy



def show_character(char_name):
   for c in config.Characters:
        if char_name == c:
            bpy.data.collections[c].hide_viewport = False
            bpy.data.collections[c].hide_render = False
        else:
            bpy.data.collections[c].hide_viewport = True
            bpy.data.collections[c].hide_render = True



#-----------------------------------------------------------------------------------


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