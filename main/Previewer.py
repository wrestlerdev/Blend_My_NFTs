# Purpose:
# This file generates NFT DNA based on a .blend file scene structure and exports NFTRecord.json.

import collections
import bpy
import os
import json
from . import config

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




def show_nft_from_dna(DNA, NFTDict): # goes through collection hiearchy based on index to hide/show DNA
   hierarchy = get_hierarchy_ordered()
   print(NFTDict)
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
   show_character(character)

   for key in keys:
      for itemKey in NFTDict[key]:
         if(NFTDict[key] != "Null"):
            print("----------------------")
            print(NFTDict[key])
            print(NFTDict[key][itemKey])
            itemDictionary = NFTDict[key][itemKey]
            color_key = itemDictionary["color_key"] 

            variant_children = bpy.data.collections[list(NFTDict[key])[0]].children

            if variant_children:
               for child in variant_children:
                  if child.name.split('_')[-1] == character:
                     meshes = child.objects
                     child.hide_viewport = False
                     child.hide_render = False
                     for obj in meshes: # Should we re hide the object meshes?
                        obj.hide_viewport = False
                        obj.hide_render = False

                     set_armature_for_meshes(character, meshes)
                     texture_mesh = bpy.data.objects[itemDictionary["item_texture"]]

                     resolution = '_' + bpy.context.scene.my_tool.textureSize
                     if resolution == '_4k':
                        resolution = 4096
                     else:
                        resolution = list(config.texture_suffixes.keys())[list(config.texture_suffixes.values()).index(resolution)]
                     set_texture_on_mesh(variant, meshes, texture_mesh, resolution)
            attr = bpy.data.collections.get(itemDictionary["item_attribute"])
            attr.hide_viewport = False
            attr.hide_render = False

            type = bpy.data.collections[itemDictionary["item_type"]]
            type.hide_viewport = False
            type.hide_render = False

            varient = bpy.data.collections[list(NFTDict[key])[0]]
            varient.hide_viewport = False
            varient.hide_render = False
   newTempDict = {}
   newTempDict["DNAList"] = DNA
   newTempDict["CharacterItems"] = NFTDict
   SaveTempDNADict(newTempDict)
            

def SaveTempDNADict(TempNFTDict):
   save_path = os.getcwd()
   file_name = os.path.join(save_path, "NFT_Temp.json")
   print(TempNFTDict)
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

def set_texture_on_mesh(variant, meshes, texture_mesh, resolution):
   suffix = config.texture_suffixes[resolution]
   # if suffix == '':
   #    print("this should be 4k okay")
   for child in meshes:
      #for i in range(0, len(child.material_slots)):  # CHECK THIS ADD TO PREVIEWER
      for i in range(0, 1):  # CHECK THIS ADD TO PREVIEWER
         mat = texture_mesh.material_slots[i].material
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
                              mat.node_tree.nodes["EmissiveMix"].outputs["Value"].default_value = 1
                     # else:
                        # print("Texture image within this node is not named properly (e.g. missing _N)")
                  # else:
                     # print("This node ({}) doesn't have an image".format(n.name))
                     # then should it look for an image?
         child.material_slots[i].material = texture_mesh.material_slots[i].material #Check this - update to loop through all material slots
   return


def get_new_texture_name(node, suffix):
   types = ['_E', '_ID', '_M', '_N', '_R', '_D']
   for _type in types:
      filepath, partition, filename = node.image.filepath.rpartition('\\')
      if _type in filename:
         filesplit = filename.split(_type)
         file_suffix, f, file_type = filesplit[1].rpartition('.')
         if file_suffix == suffix:
            # print(filepath)
            # print("then this should be the same texture?")
            return filename, node.image.filepath, _type
         else:
            # print("this is a different texture?")
            new_path = filepath + partition
            new_texture = filesplit[0] + _type + suffix + '.' + file_type 
            new_texture_path = new_path + new_texture

            return new_texture, new_texture_path, _type
   # print(filepath)
   return None



#------------------------------------------------------------------------------------

def get_null_dna(character="Kae"):
   hierarchy = get_hierarchy_unordered()
   DNASplit = [character]
   for slot in list(hierarchy.keys()):
      null_strand = '0-0-0'
      DNASplit.append(null_strand)
      # DNASplit.append(null_strand)
   DNA = ','.join(DNASplit)
   return DNA

#  ----------------------------------------------------------------------------------



def set_from_collection(slot_coll, variant_name): # hide all in coll and show given variant based on name
   v_name_split = variant_name.split('_')[-1]
   is_texture = any(not char.isdigit() for char in v_name_split)

   if not is_texture:
      variant_child = bpy.data.collections[variant_name].children[0]
      texture_name = variant_child.name

   else: # get variant name by stripping out texture/color
      texture_name = variant_name
      variant_split = variant_name.split('_')
      variant_split = variant_split[:-1]
      variant_name = '_'.join(variant_split)

   new_dna_strand = ''
   type_index = 0
   variant_index = 0
   texture_index = 0

   lastDNA = bpy.context.scene.my_tool.lastDNA
   DNAString = lastDNA.split(",")
   character = DNAString.pop(0)
   style = DNAString.pop(0)

   for type_coll in slot_coll.children: # get type,variant,texture index by going through collection hierarchy
      if variant_name in type_coll.children:
         var_coll = bpy.data.collections[variant_name]
         tex_coll = bpy.data.collections[texture_name]

         type_list = list(type_coll.children)
         var_list = list(var_coll.children)
         variant_index = type_list.index(var_coll)
         texture_index = var_list.index(tex_coll) # TODO HOW TO GET TEXTURE INDEX NOW

         dna_string = [str(type_index), str(variant_index), str(texture_index)]
         new_dna_strand = '-'.join(dna_string)
         break # CHECK THIS
      else:
         type_index += 1
         # stop putting a break here lmao
   
   if new_dna_strand != '': # true if indices were found previously
      for type_coll in slot_coll.children:
         for variant_coll in type_coll.children: # hide all
            variant_coll.hide_render = True
            variant_coll.hide_viewport = True
            for texture_coll in variant_coll.children:
               texture_coll.hide_render = True
               texture_coll.hide_viewport = True

      var_coll.hide_render = False
      var_coll.hide_viewport = False
      tex_coll.hide_render = False
      tex_coll.hide_viewport = False

      if tex_coll.children:
         for child in tex_coll.children:
            if child.name.split('_')[-1] == character:
               meshes = child.objects
               child.hide_viewport = False
               child.hide_render = False
            else:
               child.hide_viewport = True
               child.hide_render = True
      else:
         meshes = bpy.data.collections.get(texture_name).objects # if character texture variant doesnt exist
         # mesh set armature?

   return new_dna_strand # return dna strand or empty string if not valid



def pointers_have_updated(slots_key, Slots): # this is called from init properties if pointerproperty updates
   last_key = slots_key.replace("input", "last")
   coll_name, label = Slots[slots_key]
   if bpy.context.scene.my_tool.get(slots_key) is not None: # pointer has been filled

      new_dnastrand = set_from_collection(bpy.data.collections[coll_name], bpy.context.scene.my_tool.get(slots_key).name)
      if new_dnastrand != '' and not(bpy.context.scene.my_tool.get(slots_key).hide_viewport): # if is from correct collection
         dna_string = update_DNA_with_strand(new_dnastrand, coll_name)
         
         bpy.context.scene.my_tool[last_key] = bpy.context.scene.my_tool.get(slots_key)
         bpy.context.scene.my_tool.lastDNA = dna_string
         bpy.context.scene.my_tool.inputDNA = dna_string
      else:
         print("is not valid || clear")
         bpy.context.scene.my_tool[slots_key] = None
         bpy.context.scene.my_tool[slots_key] = bpy.context.scene.my_tool.get(last_key)
   else:
      last_variant = bpy.context.scene.my_tool.get(last_key)
      last_type = last_variant.name.split('_')[1]
      if last_type not in ['Null', 'Nulll']: # gets null variant then fills pointer with it
         coll = bpy.data.collections[coll_name]
         null_type_coll = coll.children[0]
         null_var_coll = null_type_coll.children[0]
         new_dnastrand = set_from_collection(coll, null_var_coll.name)
         if new_dnastrand != '':
            dna_string = update_DNA_with_strand(new_dnastrand, coll_name)

            bpy.context.scene.my_tool[slots_key] = null_var_coll
            bpy.context.scene.my_tool[last_key] = null_var_coll
            bpy.context.scene.my_tool.lastDNA = dna_string

      else: # will refill pointer with null
         bpy.context.scene.my_tool[slots_key] = bpy.context.scene.my_tool.get(last_key)



def update_DNA_with_strand(new_dnastrand, coll_name):
   dna_string = bpy.context.scene.my_tool.inputDNA
   hierarchy = get_hierarchy_ordered()
   coll_index = list(hierarchy.keys()).index(coll_name)
   DNA = dna_string.split(',') 
   DNA[coll_index + 1] = str(new_dnastrand)
   dna_string = ','.join(DNA)
   return dna_string



def dnastring_has_updated(DNA, lastDNA): # called from inputdna update, check if user has updated dna manually
   # if DNA != lastDNA:
   #    DNA = DNA.replace('"', '')
   #    show_nft_from_dna(DNA)
   #    bpy.context.scene.my_tool.lastDNA = DNA
   #    bpy.context.scene.my_tool.inputDNA = DNA
   #    fill_pointers_from_dna(DNA, DNA)
      # try:
      #    show_nft_from_dna(DNA)
      #    bpy.context.scene.my_tool.lastDNA = DNA
      #    bpy.context.scene.my_tool.inputDNA = DNA
      #    fill_pointers_from_dna(DNA, DNA)
      # except:
      #    print("this is not a valid dna string")
   return



def fill_pointers_from_dna(DNA, Slots): # fill all pointer properties with variants
   return
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
      variant = list(atttype[1].items())[int(variant_index)]
      texture = list(variant[1].items())[int(texture_index)][0]

      coll_name = slot[0][3:len(slot[0])] # CHECK THIS FOR NEW HIERARCHY
      last_coll_name = "last" + str(coll_name)
      input_coll_name = "input" + str(coll_name)
      bpy.context.scene.my_tool[last_coll_name] = bpy.data.collections[texture]
      bpy.context.scene.my_tool[input_coll_name] = bpy.data.collections[texture]
   return



#  ----------------------------------------------------------------------------------



def create_item_dict(DNA): # make dict from DNA to save to file
   ohierarchy = get_hierarchy_ordered()
   coll_keys = list(ohierarchy.keys())
   uhierarchy = get_hierarchy_unordered()
   # print(uhierarchy)
   DNAString = DNA.split(",")
   character = DNAString.pop(0)
   style = DNAString.pop(0)

   item_dict = {}

   for strand in range(len(DNAString)):
      if DNAString[strand] == '0-0-0':
         item_dict[coll_keys[strand]] = "Null"
      else:
         DNASplit = DNAString[strand].split('-')
         atttype_index = DNASplit[0]
         variant_index = DNASplit[1]
         texture_index = int(DNASplit[2])

         slot = list(ohierarchy.items())[strand]

         atttype = list(slot[1].items())[int(atttype_index)]
         if len(list(atttype[1].items())) <= int(variant_index):
            print(atttype[0]) # TODO  KEEP WORKING ON THIS AFTER OUTFITGEN
            #print(len(list(atttype[1].items())))
            #print(variant_index)
         if len(list(atttype[1].items())) > 0: # else?
            print(list(atttype[1].items())[int(variant_index)])

            variant = list(atttype[1].items())[int(variant_index)]
            textures = uhierarchy[slot[0]][atttype[0]][variant[0]]["item_texture"]
            texture = list(textures.keys())[texture_index] if len(textures) > 0 else None
            
            texturevariant_dict = {}
            coll_index = coll_keys[strand]
            uh_info = uhierarchy[coll_index][atttype[0]][variant[0]] # add color info too here
            uh_info["Style"] = style
            uh_info["TextureSet"] = texture

            texturevariant_dict[variant[0]] = uh_info
            item_dict[coll_keys[strand]] = texturevariant_dict
   nft_dict = {}
   nft_dict[DNA] = item_dict
   return nft_dict



def set_armature_for_meshes(character, meshes):
   armature_name = "armature_" + str(character).lower()
   if bpy.data.objects.get(armature_name) is not None:
      for mesh in meshes:
         if mesh.modifiers:
               for mod in mesh.modifiers:
                  if mod.type == 'ARMATURE':
                     mod.object = bpy.data.objects[armature_name]
         else:
            mod = mesh.modifiers.new(name='armature', type='ARMATURE')
            mod.object = bpy.data.objects[armature_name]
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


def show_character(char_name):
   for c in config.Characters:
        if char_name == c:
            bpy.data.collections[c].hide_viewport = False
            bpy.data.collections[c].hide_render = False
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