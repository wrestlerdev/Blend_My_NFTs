# Purpose:
# This file generates NFT DNA based on a .blend file scene structure and exports NFTRecord.json.

import collections
import bpy
import os
import json
from mathutils import Vector
from mathutils import Matrix

from . import config
from . import ColorGen

enableGeneration = False
colorList = []


class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR




def show_nft_from_dna(DNA, NFTDict, Select = False): # goes through collection hiearchy based on index to hide/show DNA
   bpy.ops.object.select_all(action='DESELECT')
   
   hierarchy = get_hierarchy_ordered()
   for attribute in hierarchy: # hide all
      bpy.data.collections[attribute].hide_viewport = True
      bpy.data.collections[attribute].hide_render = True
      for type in hierarchy[attribute]:
            bpy.data.collections[type].hide_viewport = True
            bpy.data.collections[type].hide_render = True
            for variant in hierarchy[attribute][type]:
               bpy.data.collections[variant].hide_viewport = True
               bpy.data.collections[variant].hide_render = True
               for char in config.Characters:
                  char_var = variant + '_' + char
                  if bpy.data.collections.get(char_var) is not None:
                     bpy.data.collections.get(char_var).hide_viewport = True
                     bpy.data.collections.get(char_var).hide_render = True
                     for obj in bpy.data.collections.get(char_var).objects: # Should we re hide the object meshes?
                        obj.hide_viewport = True
                        obj.hide_render = True
   
   keys = list(NFTDict.keys())
   DNAString = DNA.split(",")
   character = DNAString.pop(0)
   style = DNAString.pop(0)
   reset_shape_keys(character + '_Rig')
   show_character(character, Select)

   for key in keys:
      for itemKey in NFTDict[key]:
         if(NFTDict[key] != "Null"):
            itemDictionary = NFTDict[key][itemKey]
            color_key = itemDictionary["color_key"] 
            variant_children = bpy.data.collections[list(NFTDict[key])[0]].children

            attr = bpy.data.collections.get(itemDictionary["item_attribute"])
            attr.hide_viewport = False
            attr.hide_render = False

            type = bpy.data.collections[itemDictionary["item_type"]]
            type.hide_viewport = False
            type.hide_render = False

            varient = bpy.data.collections[list(NFTDict[key])[0]]
            varient.hide_viewport = False
            varient.hide_render = False

            if variant_children:
               for child in variant_children:
                  if child.name.split('_')[-1] == character:
                     meshes = child.objects
                     child.hide_viewport = False
                     child.hide_render = False
                     for obj in meshes: # Should we re hide the object meshes?
                        obj.hide_viewport = False
                        obj.hide_render = False
                        if Select:
                           obj.select_set(True)

                     set_armature_for_meshes(character, meshes)
                     texture_mesh = bpy.data.objects[itemDictionary["item_texture"]]

                     resolution = '_' + bpy.context.scene.my_tool.textureSize
                     if resolution == '_4k':
                        resolution = 4096
                     else:
                        # print(resolution)
                        resolution = list(config.texture_suffixes.keys())[list(config.texture_suffixes.values()).index(resolution)]
                     # set_texture_on_mesh(variant, meshes, texture_mesh, color_key, resolution)
                     set_texture_on_mesh(varient, meshes, texture_mesh, color_key, resolution)

            if type.name[3:].startswith('Expression'):
            # if 'Expression' in type.name:
               variant_name = varient.name.rpartition('_')[2]
               set_shape_keys(character + '_Rig', variant_name)
            elif type.name[3:].startswith('Backpack'):
            # if backpack in type.name
               print("Backoroni")
               print(type.name[3:])
               RaycastPackpack(type.name[3:], character, NFTDict) 

   newTempDict = {}
   newTempDict["DNAList"] = DNA
   newTempDict["CharacterItems"] = NFTDict
   SaveTempDNADict(newTempDict)
   bpy.context.scene.my_tool.lastDNA = DNA
   bpy.context.scene.my_tool.inputDNA = DNA
   fill_pointers_from_dna(DNA, '')


# -----------------------------------------------------


def RaycastPackpack(backpackType, character, NFTDict):
   torsoObj = list(NFTDict["01-UpperTorso"].keys())[0]
   torsoObj = torsoObj + "_" + character
   objects = bpy.data.collections[torsoObj].objects
   if len(objects) > 0:
      cb = objects[0]
      src = bpy.data.objects[character + '_src']
      dst = bpy.data.objects[character + '_dst']
      null_loc = bpy.data.objects[character + '_loc']

      mw = cb.matrix_world
      mwi = mw.inverted()

      # src and dst in local space of cb

      origin = mwi @ src.matrix_world.translation
      dest = mwi @ dst.matrix_world.translation
      direction = (dest - origin).normalized()

      hit, loc, norm, face = cb.ray_cast(origin, direction)

      if hit:
         print("Hit at ", mw @ loc, " (local)")
         print(dst.matrix_world.to_translation())
         
         dir = (mw @ loc) - dst.matrix_world.to_translation()
         dist = dir.magnitude
         null_loc.location = Vector([0,2,0])
         null_loc.location.z -= dist
         #null_loc.location.z -= backpack.dimensions.z / 2


         if backpackType == "BackpackHigh":
            backpack = list(NFTDict["13-Neck"].keys())[0]
         else:
            backpack = list(NFTDict["18-Backpack"].keys())[0]
         backpack = backpack + "_" + character
         for obj in bpy.data.collections[backpack].objects:
            if len(obj.constraints) < 1:
               obj.constraints.new(type='CHILD_OF')
            obj.constraints["Child Of"].target = null_loc
            obj.constraints["Child Of"].inverse_matrix = Matrix(((1.0, 0.0, 0.0, 0.0),
                                                               (0.0, 1.0, 0.0, 0.0),
                                                               (0.0, 0.0, 1.0, 0.0),
                                                               (0.0, 0.0, 0.0, 1.0)))
            obj.location = Vector([0,0,0])
      else:
         print("No HIT")



def SaveTempDNADict(TempNFTDict):
   save_path = os.getcwd()
   file_name = os.path.join(save_path, "NFT_Temp.json")
   try:
      ledger = json.dumps(TempNFTDict, indent=1, ensure_ascii=True)
      with open(file_name, 'w') as outfile:
         outfile.write(ledger + '\n')
         print("Success update {}". format(file_name))
   except:
      print("Failed to update {}". format(file_name))

def LoadTempDNADict():
   save_path = os.getcwd()
   file_name = os.path.join(save_path, "NFT_Temp.json")
   TempNFTDict = json.load(open(file_name))
   return TempNFTDict

def OpenGlobalColorList():
    root_dir = bpy.context.scene.my_tool.root_dir
    path = os.path.join(root_dir, "INPUT\GlobalColorList.json")
    GlobalColorList = json.load(open(path))
    return GlobalColorList


# ------------------------------------------------------------


def CreateDNADictFromUI(): # Override NFT_Temp.json with info within the blender scene UI (e.g. inputDNA)
   CurrentDict = LoadTempDNADict()
   CurrentDNA = CurrentDict["DNAList"]
   DNA = bpy.context.scene.my_tool.inputDNA
   NewDict = {}
   if DNA != CurrentDNA:
      DNAString = DNA.split(',')
      character = DNAString.pop(0)
      style = DNAString.pop(0)
      show_character(character)
      ohierarchy = get_hierarchy_ordered()

      ItemsUsed = {}
      for i in range(len(DNAString)):
         VarientDict = {}
         current_entry = {}
         DNASplit = DNAString[i].split('-')
         atttype_index = DNASplit[0]
         variant_index = DNASplit[1]
         texture_index = DNASplit[2]

         attribute = list(ohierarchy.items())[i]
         type = list(attribute[1].items())[int(atttype_index)]
         variant = list(type[1].items())[int(variant_index)][0]

         variant_name = variant.rpartition('_')[2]
         item_index = variant.split('_')[-2]
         if len(list(bpy.data.collections[variant].objects)) > 0:
            last_texture = list(bpy.data.collections[variant].objects)[int(texture_index)].name
         else:
            last_texture = None

         if variant_name == 'Null':
            VarientDict = 'Null'
         else:
            current_entry["item_attribute"] = attribute[0]
            current_entry["item_type"] = type[0]
            current_entry["item_variant"] = variant_name
            current_entry["item_texture"] = last_texture
            current_entry["item_index"] = item_index
            current_entry["texture_index"] = int(texture_index)
            current_entry["type_rarity"] = bpy.data.collections[type[0]]['rarity']
            current_entry["variant_rarity"] = bpy.data.collections[variant]['rarity']
            current_entry["texture_rarity"] = ohierarchy[attribute[0]][type[0]][variant]["textureSets"][last_texture]
            current_entry["color_style"] = style
            current_entry["color_key"] = ColorGen.PickOutfitColors(attribute[0], style)[0]
            VarientDict[variant] = current_entry
         ItemsUsed[attribute[0]] = VarientDict
      NewDict["DNAList"] = DNA
      NewDict["CharacterItems"] = ItemsUsed
      SaveTempDNADict(NewDict)
      show_nft_from_dna(DNA, ItemsUsed)
   return


# -----------------------------------------------------

def set_shape_keys(rig_name, variant_name):
   print("is expression")
   shape_key_names = [variant_name, 
                     variant_name + "_mouth",
                     variant_name + "_eyes",
                     variant_name + "_brow",
                     variant_name + "_brows",
                     ]
   character_coll = bpy.data.collections[rig_name]
   for obj in character_coll.objects:
      if obj.type == 'MESH':
         if hasattr(obj.data, "shape_keys") and obj.data.shape_keys != None:
            for shape_key in obj.data.shape_keys.key_blocks:
               for shape_key_name in shape_key_names:
                  if shape_key.name == shape_key_name:
                     print(shape_key_name)
                     print(shape_key.name)
                     shape_key.value = 1
                     break
   return

def reset_shape_keys(rig_name):
   character_coll = bpy.data.collections[rig_name]
   for obj in character_coll.objects:
      if obj.type == 'MESH':
         if hasattr(obj.data, "shape_keys") and obj.data.shape_keys != None:
            for shape_key in obj.data.shape_keys.key_blocks:
               if shape_key.name != 'Basis':
                  shape_key.value = 0
   return


def set_texture_on_mesh(variant, meshes, texture_mesh, color_key, resolution):
   suffix = config.texture_suffixes[resolution]
   # if suffix == '':
   #    print("this should be 4k okay")
   GlobalColorList = OpenGlobalColorList()
   colorChoice = GlobalColorList[color_key]
   for child in meshes:
      for childMatSlot in child.material_slots:
         # print("!--------------------------------!")
         # print("Child Name: " + child.name  + " || Child Mat" + childMatSlot.name)
         for textureMatSlot in texture_mesh.material_slots:
            # print("Texture Mat: " + textureMatSlot.name)
            if textureMatSlot.material.name in childMatSlot.material.name or len(texture_mesh.material_slots) == 1 :
               # print("Child Name: " + childMatSlot.material.name + " || Texture Name: " + textureMatSlot.material.name)
               mat = textureMatSlot.material
               if mat.use_nodes:
                  for n in mat.node_tree.nodes:
                     if n.type == 'TEX_IMAGE':
                        if n.image is not None:
                           texture_info = get_new_texture_name(n, suffix)
                           if texture_info:
                              new_texture, new_texture_path, _type = texture_info
                              if os.path.exists(new_texture_path):
                                 file = new_texture_path.replace('/', '\\')
                                 if _type == '_N':
                                    newImage = bpy.data.images.load(file, check_existing=False)
                                    mat.node_tree.nodes["NormalNode"].image = newImage
                                    mat.node_tree.nodes["NormalNode"].image.colorspace_settings.name = 'Raw'
                                    mat.node_tree.nodes["NormalMix"].outputs["Value"].default_value = 1
                                 elif _type == '_D':
                                    newImage = bpy.data.images.load(file, check_existing=False)
                                    mat.node_tree.nodes["DiffuseNode"].image = newImage
                                    mat.node_tree.nodes["DiffuseMix"].outputs["Value"].default_value = 1
                                 elif _type == '_ID':
                                    newImage = bpy.data.images.load(file, check_existing=False)
                                    mat.node_tree.nodes["ColorIDNode"].image = newImage
                                    mat.node_tree.nodes["ColorIDNode"].image.colorspace_settings.name = 'Linear'
                                    mat.node_tree.nodes["ColorID_RGBMix"].outputs["Value"].default_value = 1
                                 elif _type == '_M':
                                    newImage = bpy.data.images.load(file, check_existing=False)
                                    mat.node_tree.nodes["MetallicNode"].image = newImage
                                    mat.node_tree.nodes["MetallicNode"].image.colorspace_settings.name = 'Linear'
                                    mat.node_tree.nodes["MetallicMix"].outputs["Value"].default_value = 1
                                 elif _type == '_R':
                                    newImage = bpy.data.images.load(file, check_existing=False)
                                    mat.node_tree.nodes["RoughnessNode"].image = newImage
                                    mat.node_tree.nodes["RoughnessNode"].image.colorspace_settings.name = 'Linear'
                                    mat.node_tree.nodes["RoughnessMix"].outputs["Value"].default_value = 1
                                 elif _type == '_E':
                                    newImage = bpy.data.images.load(file, check_existing=False)
                                    mat.node_tree.nodes["EmissiveNode"].image = newImage 
                                    mat.node_tree.nodes["EmissiveNode"].image.colorspace_settings.name = 'sRGB'
                                    mat.node_tree.nodes["EmissiveMix"].outputs["Value"].default_value = 1
                                 elif _type == '_O':
                                    newImage = bpy.data.images.load(file, check_existing=False)
                                    mat.node_tree.nodes["OpacityNode"].image = newImage 
                                    mat.node_tree.nodes["OpacityNode"].image.colorspace_settings.name = 'Linear'
                                    mat.node_tree.nodes["OpacityMix"].outputs["Value"].default_value = 1
                           # else:
                              # print("Texture image within this node is not named properly (e.g. missing _N)")
                     elif n.type == 'RGB':
                        if (n.label == "RTint"):
                           n.outputs["Color"].default_value = colorChoice["R"]
                        if (n.label == "GTint"):
                           n.outputs["Color"].default_value = colorChoice["G"]
                        if (n.label == "BTint"):
                           n.outputs["Color"].default_value = colorChoice["B"]
                        if (n.label == "AlphaTint"):
                           n.outputs["Color"].default_value = colorChoice["A"]
                        if (n.label == "WhiteTint"):
                           n.outputs["Color"].default_value = colorChoice["W"]
                           # print("This node ({}) doesn't have an image".format(n.name))
                           # then should it look for an image?
               childMatSlot.material = textureMatSlot.material #Check this - update to loop through all material slots
   return


def get_new_texture_name(node, suffix):
   types = ['_E', '_ID', '_M', '_N', '_R', '_D', '_O']
   for _type in types:
      filepath, partition, filename = node.image.filepath.rpartition('\\')
      if _type in filename:
         filesplit = filename.split(_type)
         file_suffix, f, file_type = filesplit[1].rpartition('.')
         if file_suffix == suffix:
            # print("then this should be the same texture?")
            return None
            return filename, node.image.filepath, _type
         else:
            # print("this is a different texture?")
            new_path = filepath + partition
            new_texture = filesplit[0] + _type + suffix + '.' + file_type 
            new_texture_path = new_path + new_texture

            return new_texture, new_texture_path, _type
   return None



#------------------------------------------------------------------------------------

def get_null_dna(character="Kae", style=""):
   hierarchy = get_hierarchy_unordered()
   DNASplit = [character, style]
   for slot in list(hierarchy.keys()):
      null_strand = '0-0-0'
      DNASplit.append(null_strand)
   DNA = ','.join(DNASplit)
   return DNA

#  ----------------------------------------------------------------------------------



def set_from_collection(slot_coll, variant_name): # get new dna strand from variant name
   new_dna_strand = ''
   type_index = 0
   variant_index = 0
   texture_index = 0

   lastDNA = bpy.context.scene.my_tool.lastDNA
   DNAString = lastDNA.split(",")
   character = DNAString.pop(0)
   style = DNAString.pop(0)

   for type_coll in slot_coll.children: # get type,variant,texture index by going through collection hierarchy
      if variant_name in type_coll.children.keys():
         var_coll = bpy.data.collections[variant_name]

         type_list = list(type_coll.children)
         variant_index = type_list.index(var_coll)
         texture_index = 0 # TODO HOW TO GET TEXTURE INDEX NOW

         dna_string = [str(type_index), str(variant_index), str(texture_index)]
         new_dna_strand = '-'.join(dna_string)
         break # CHECK THIS
      else:
         type_index += 1
   return new_dna_strand # return dna strand or empty string if not valid


def general_pointer_updated(Slots):
   if bpy.context.scene.my_tool.inputGeneral is not None:
      inputted_item = bpy.context.scene.my_tool.inputGeneral
      item = inputted_item.name
      try:
         att_name, type_name, i, var_name = item.split('_')
      except:
         print("Wrong type of collection")
         bpy.context.scene.my_tool.inputGeneral = None
         return
      input_name = 'input' + att_name
      att_coll = bpy.data.collections[Slots[input_name][0]]
      for types in att_coll.children:
         if types.name.endswith(type_name):
            for vars in types.children:
               if vars.name.endswith(var_name):
                  pointers_have_updated(input_name, Slots, vars.name)
                  break
      bpy.context.scene.my_tool.inputGeneral = None
   return


def pointers_have_updated(slots_key, Slots, variant_name=''): # this is called from init properties if pointerproperty updates
   last_key = slots_key.replace("input", "last")
   coll_name, label = Slots[slots_key]
   if variant_name != '': # from general pointer
      new_dnastrand = set_from_collection(bpy.data.collections[coll_name], variant_name)
      if new_dnastrand != '': # if is from correct collection
         dna_string, CharacterItems = update_DNA_with_strand(coll_name, new_dnastrand)
         bpy.context.scene.my_tool[last_key] = bpy.data.collections[variant_name]
         show_nft_from_dna(dna_string, CharacterItems)
      else:
         print("is not valid || clear")
         last_type = variant_name.rpartition('_')[2]
         if last_type not in ['Null', 'Nulll']:
            bpy.context.scene.my_tool[slots_key] = bpy.context.scene.my_tool[last_key]
         else:
            bpy.context.scene.my_tool[slots_key] = None

   elif bpy.context.scene.my_tool.get(slots_key) is not None: # pointer has been filled
      new_dnastrand = set_from_collection(bpy.data.collections[coll_name], bpy.context.scene.my_tool.get(slots_key).name)
      if new_dnastrand != '': # if is from correct collection
      # if new_dnastrand != '' and not(bpy.context.scene.my_tool.get(slots_key).hide_viewport): # if is from correct collection
         dna_string, CharacterItems = update_DNA_with_strand(coll_name, new_dnastrand)
         bpy.context.scene.my_tool[last_key] = bpy.context.scene.my_tool.get(slots_key)
         show_nft_from_dna(dna_string, CharacterItems)
      else:
         print("is not valid || clear")
         last_type = bpy.context.scene.my_tool[last_key].name.rpartition('_')[2]
         if last_type not in ['Null', 'Nulll']:
            bpy.context.scene.my_tool[slots_key] = bpy.context.scene.my_tool[last_key]
         else:
            bpy.context.scene.my_tool[slots_key] = None

   else: # remove item
      last_variant = bpy.context.scene.my_tool.get(last_key)
      last_type = last_variant.name.split('_')[1]
      if last_type not in ['Null', 'Nulll']: # gets null variant then fills pointer with it
         coll = bpy.data.collections[coll_name]
         null_type_coll = coll.children[0]
         null_var_coll = null_type_coll.children[0]
         new_dnastrand = set_from_collection(coll, null_var_coll.name)
         if new_dnastrand != '':
            dna_string, CharacterItems = update_DNA_with_strand(coll_name, new_dnastrand)

            bpy.context.scene.my_tool[slots_key] = None
            bpy.context.scene.my_tool[last_key] = null_var_coll
            show_nft_from_dna(dna_string, CharacterItems)
      else: # will refill pointer with null
         bpy.context.scene.my_tool[slots_key] = bpy.context.scene.my_tool.get(last_key)
         # bpy.context.scene.my_tool[slots_key] = None


def update_colour_random(coll_name):
   dna_string, CharacterItems = update_DNA_with_strand(coll_name)
   show_nft_from_dna(dna_string, CharacterItems)
   return


def update_DNA_with_strand(coll_name, dna_strand=''): # if dna_strand is given, update dna with new strand else randomize colour
   NFTDict = LoadTempDNADict()
   CharacterItems = NFTDict["CharacterItems"]
   dna_string = NFTDict["DNAList"]
   hierarchy = get_hierarchy_ordered()
   coll_index = list(hierarchy.keys()).index(coll_name)
   DNA = dna_string.split(',') 
   if dna_strand != '':
      new_dnastrand = dna_strand
      DNA[coll_index + 2] = str(new_dnastrand)
   else:
      new_dnastrand = DNA[coll_index + 2]
   dna_string = ','.join(DNA)

   if new_dnastrand == '0-0-0':
      CharacterItems[coll_name] = "Null"
      return dna_string, CharacterItems

   type_index, var_index, tex_index = new_dnastrand.split('-')
   batch_index = bpy.context.scene.my_tool.CurrentBatchIndex # get data from batch record json
   nftrecord_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{:03d}".format(batch_index), "_NFTRecord_{:03d}.json".format(batch_index))
   batch_record = json.load(open(nftrecord_save_path))
   type_coll = bpy.data.collections[coll_name].children[int(type_index)]
   var_coll = type_coll.children[int(var_index)]

   record_item = batch_record["hierarchy"][coll_name][type_coll.name][var_coll.name]
   last_item = CharacterItems[coll_name]
   if last_item != 'Null' and dna_strand != '': # get last used colour if exists
      last_variant = list(last_item.keys())[0]
      last_cstyle = last_item[last_variant]["color_style"]
      last_ckey = last_item[last_variant]["color_key"]
   else:
      print("get new colour key in here")
      last_cstyle = dna_string.split(',')[1]
      if dna_strand == '':
         max_attempts = 10
         last_variant = list(last_item.keys())[0]
         last_used_ckey = last_item[last_variant]["color_key"]
         for i in range(max_attempts):
            last_ckey, color_choice = ColorGen.PickOutfitColors(coll_name, last_cstyle)
            if last_ckey != last_used_ckey:
               break
      else:
         last_ckey, color_choice = ColorGen.PickOutfitColors(coll_name, last_cstyle)      

   new_tex = list(record_item['textureSets'].keys())[0]
   new_tex_rarity = record_item['textureSets'][new_tex]

   new_item = {}
   new_item["item_attribute"] = coll_name
   new_item["item_type"] = type_coll.name
   new_item["item_variant"] = var_coll.name
   new_item["item_texture"] = new_tex # TODO HOW TO CHOOSE TEXTURE?
   new_item["type_rarity"] = type_coll['rarity']
   new_item["variant_rarity"] = var_coll['rarity']
   new_item["texture_rarity"] = new_tex_rarity # TODO FIND THIS TOO
   new_item["color_style"] = last_cstyle
   new_item["color_key"] = last_ckey

   variant_dict = {}
   variant_dict[var_coll.name] = new_item
   CharacterItems[coll_name] = variant_dict
   return dna_string, CharacterItems



def randomize_color_style(): # if dna_strand is given, update dna with new strand else randomize colour
   NFTDict = LoadTempDNADict()
   CharacterItems = NFTDict["CharacterItems"]
   dna_string = NFTDict["DNAList"]
   hierarchy = get_hierarchy_ordered()
   DNASplit = dna_string.split(',') 

   new_style = ColorGen.SetUpCharacterStyle()

   # if DNASplit[1] == new_style:
   #    return dna_string, CharacterItems

   DNASplit[1] = new_style
   dna_string = ','.join(DNASplit)

   for coll_name in list(NFTDict["CharacterItems"].keys()):
      if CharacterItems[coll_name] != 'Null':
         index = list(NFTDict["CharacterItems"].keys()).index(coll_name)
         dna_strand = DNASplit[index + 2]

         type_index, var_index, tex_index = dna_strand.split('-')
         type_coll = bpy.data.collections[coll_name].children[int(type_index)]
         var_coll = type_coll.children[int(var_index)]

         new_key, color_choice = ColorGen.PickOutfitColors(coll_name, new_style)
         new_item = CharacterItems[coll_name][var_coll.name]
         new_item["color_style"] = new_style
         new_item["color_key"] = new_key

         variant_dict = {}
         variant_dict[var_coll.name] = new_item
         CharacterItems[coll_name] = variant_dict
      
   return dna_string, CharacterItems



def dnastring_has_updated(DNA, lastDNA): # called from inputdna update, check if user has updated dna manually
   # if DNA != lastDNA:
   #    DNA = DNA.replace('"', '')
   #    bpy.context.scene.my_tool.lastDNA = DNA
   #    bpy.context.scene.my_tool.inputDNA = DNA
   #    fill_pointers_from_dna(DNA, DNA)

   return



def fill_pointers_from_dna(DNA, Slots): # fill all pointer properties with variants
   DNAString = DNA.split(',')
   character = DNAString.pop(0)
   style = DNAString.pop(0)
   show_character(character)
   
   ohierarchy = get_hierarchy_ordered()
   for i in range(len(DNAString)):

      DNASplit = DNAString[i].split('-')
      atttype_index = DNASplit[0]
      variant_index = DNASplit[1]
      texture_index = DNASplit[2]

      slot = list(ohierarchy.items())[i]
      atttype = list(slot[1].items())[int(atttype_index)]
      variant = list(atttype[1].items())[int(variant_index)][0]

      coll_name = slot[0][3:len(slot[0])] # CHECK THIS FOR NEW HIERARCHY
      last_coll_name = "last" + str(coll_name)
      input_coll_name = "input" + str(coll_name)
      if variant.split('_')[3] != 'Null':
         bpy.context.scene.my_tool[last_coll_name] = bpy.data.collections[variant]
         bpy.context.scene.my_tool[input_coll_name] = bpy.data.collections[variant]
      else:
         bpy.context.scene.my_tool[last_coll_name] = bpy.data.collections[variant]
         bpy.context.scene.my_tool[input_coll_name] = None
   return



#  ----------------------------------------------------------------------------------


def set_armature_for_meshes(character, meshes):
   armature_name = "armature_" + str(character).lower()
   if bpy.data.objects.get(armature_name) is not None:
      for mesh in meshes:
         if mesh.modifiers:
               for mod in mesh.modifiers:
                  if mod.type == 'ARMATURE':
                     mod.object = bpy.data.objects[armature_name]
         else:
            #mod = mesh.modifiers.new(name='armature', type='ARMATURE')
            #mod.object = bpy.data.objects[armature_name]
            pass
   else:
      # print("Armature '{}' does not exist atm".format(armature_name)) # CHECK THIS 
      return


#---------------------------------------------------------------------------


def get_hierarchy_ordered(index=0):
   if not index:
         index = bpy.context.scene.my_tool.CurrentBatchIndex
   batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
   NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(index), "_NFTRecord_{:03d}.json".format(index))
   if os.path.exists(NFTRecord_save_path):
      DataDictionary = json.load(open(NFTRecord_save_path), object_pairs_hook=collections.OrderedDict)
      hierarchy = DataDictionary["hierarchy"]
      return hierarchy
   return None


def get_hierarchy_unordered(index=0):
   if not index:
         index = bpy.context.scene.my_tool.CurrentBatchIndex
   batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
   NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(index), "_NFTRecord_{:03d}.json".format(index))      
   if os.path.exists(NFTRecord_save_path):
      DataDictionary = json.load(open(NFTRecord_save_path))
      hierarchy = DataDictionary["hierarchy"]
      return hierarchy
   return None


def show_character(char_name, Select = False):
   for c in config.Characters:
        if char_name == c:
            bpy.data.collections[c].hide_viewport = False
            bpy.data.collections[c].hide_render = False
            if Select:
               for child in bpy.data.collections[c].children:
                  for obj in child.objects:
                     obj.select_set(True)
        else:
            bpy.data.collections[c].hide_viewport = True
            bpy.data.collections[c].hide_render = True


def HexToRGB(hex):
   string = hex.lstrip('#')
   rgb255 = tuple( int(string[i:i+2], 16) for i in (0,2,4) )
   rgb = tuple( (float(x) /255) for x in rgb255)
   return rgb
      


#-----------------------------------------------------------------------------------



if __name__ == '__main__':
   print("okay")