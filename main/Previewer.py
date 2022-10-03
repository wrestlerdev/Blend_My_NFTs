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


def show_nft_from_dna(DNA, NFTDict, Select = False): # goes through collection hiearchy based on index to hide/show DNA
   # Select = if visible objects should be selected (for export)
   bpy.ops.object.select_all(action='DESELECT')
   
   hierarchy = get_hierarchy_ordered()
   for attribute in hierarchy: # hide all variants in scene
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
                        # obj.hide_viewport = True
                        # obj.hide_render = True
                        if obj.field != None:
                           obj.field.apply_to_location = False
                           obj.field.apply_to_rotation = False

   keys = list(NFTDict.keys())
   DNAString = DNA.split(",")
   character = DNAString.pop(0)
   element = DNAString.pop(0)
   style = DNAString.pop(0)
   reset_shape_keys(character)
   show_character(character, Select)
   set_material_element(element)
   # image_nodes = ["MT" , "FA", "C", "F", "N"] # tattoo slots
   # for image_node in image_nodes:
   #    add_texture_to_tattoos(character, image_node, texture='clear')
   hair_coll = ''

   for key in keys:
      for itemKey in NFTDict[key]: # goes through each attribute in the NFTDict
         if(NFTDict[key] != "Null"):
            itemDictionary = NFTDict[key][itemKey]
            color_key = itemDictionary["color_key"] 
            variant_name =  list(NFTDict[key])[0]
            variant_children = bpy.data.collections[variant_name].children

            attr = bpy.data.collections.get(itemDictionary["item_attribute"])
            attr.hide_viewport = False
            attr.hide_render = False
            type = bpy.data.collections[itemDictionary["item_type"]]
            type.hide_viewport = False
            type.hide_render = False
            varient = bpy.data.collections[variant_name]
            varient.hide_viewport = False
            varient.hide_render = False

            if variant_children: # hide all in character variant collections
               for child in variant_children:
                  if child.name.split('_')[-1] == character:
                     meshes = child.objects
                     child.hide_viewport = False
                     child.hide_render = False
                     for obj in meshes: # Should we re-hide the object meshes?
                        obj.hide_viewport = False
                        obj.hide_render = False
                        if obj.field != None:
                           obj.field.apply_to_location = True
                           obj.field.apply_to_rotation = True
                        if Select:
                           obj.select_set(True)
                     set_armature_for_meshes(character, meshes)

                     texture_mesh = bpy.data.objects[itemDictionary["item_texture"]]
                     resolution = '_' + bpy.context.scene.my_tool.textureSize
                     if resolution == '_4k':
                           resolution = 4096
                     else:
                        resolution = list(config.texture_suffixes.keys())[list(config.texture_suffixes.values()).index(resolution)]
                        set_texture_on_mesh(varient, meshes, texture_mesh, color_key, resolution, [attr.name, type.name, varient.name])

            if type.name[3:].startswith('Expression'):
               variant_name = varient.name.rpartition('_')[2]
               set_shape_keys(character, variant_name)

            elif type.name[3:].startswith('Backpack'):
               config.custom_print(type.name[3:])
               RaycastPackpack(type.name[3:], character, NFTDict)

            elif type.name[3:].startswith('Feet'):
               config.custom_print(type.name[3:])
               SnapFeetToFloor(type.name[3:], character, NFTDict)

            elif (attr.name[3:] == 'HS' or attr.name[3:] == 'HL') and varient:
               hair_coll = bpy.data.collections[varient.name + '_' + character]
               reset_hair_shape_key(hair_coll)

            elif attr.name[3:] == 'HA':
               char_var_coll = bpy.data.collections[varient.name + '_' + character]
               print(char_var_coll)
               set_hair_accessory_shape_keys(char_var_coll, hair_coll)

            turn_on_tattoo(element, color_key)    

   newTempDict = {}
   newTempDict["DNAList"] = DNA
   newTempDict["CharacterItems"] = NFTDict
   SaveTempDNADict(newTempDict)
   bpy.context.scene.my_tool.lastDNA = DNA
   bpy.context.scene.my_tool.inputDNA = DNA
   if not Select:
      fill_pointers_from_dna(DNA)


def set_material_element(element):
   mixers = ["OutfitElementMixer", "SkinElementMixer", "FullBodyElementMixer", "TattooElementMixer"]
   element_style, element_type = element.split('-')

   if element_style == 'None': # set up element style within nodes
      for mixer in mixers:
         node_tree = bpy.data.node_groups[mixer]
         node_tree.nodes["ElementalMix"].outputs["Value"].default_value = 0
         element_node = node_tree.nodes["ElementPicker"]
         element_node.node_tree = bpy.data.node_groups["EmptyElement"]
         node_tree.links.new(node_tree.nodes["ElementalMixShader"].inputs[2], element_node.outputs[0])
         node_tree.links.new(element_node.inputs[0], node_tree.nodes["Group Input"].outputs["Normal"])

      node_tree = bpy.data.node_groups["TattooElementMixer"]
      node_tree.nodes["ElementalMix"].outputs["Value"].default_value = 0

   elif element_style == 'All':
      for mixer in mixers:
         node_tree = bpy.data.node_groups[mixer]
         node_tree.nodes["ElementalMix"].outputs["Value"].default_value = 1
         element_node = node_tree.nodes["ElementPicker"]
         element_node.node_tree = bpy.data.node_groups[element_type]
         node_tree.links.new(node_tree.nodes["ElementalMixShader"].inputs[2], element_node.outputs[0])
         node_tree.links.new(element_node.inputs[0], node_tree.nodes["Group Input"].outputs["Normal"])

      node_tree = bpy.data.node_groups["TattooElementMixer"]
      node_tree.nodes["ElementalMix"].outputs["Value"].default_value = 0


   elif element_style == 'Outfit':
      for mixer in ["OutfitElementMixer", "TattooElementMixer"]:
         node_tree = bpy.data.node_groups[mixer]
         node_tree.nodes["ElementalMix"].outputs["Value"].default_value = 1
         element_node = node_tree.nodes["ElementPicker"]
         element_node.node_tree = bpy.data.node_groups[element_type]
         node_tree.links.new(node_tree.nodes["ElementalMixShader"].inputs[2], element_node.outputs[0])
         node_tree.links.new(element_node.inputs[0], node_tree.nodes["Group Input"].outputs["Normal"])

      for mixer in ["FullBodyElementMixer", "SkinElementMixer"]:
         node_tree = bpy.data.node_groups[mixer]
         node_tree.nodes["ElementalMix"].outputs["Value"].default_value = 0
         element_node = node_tree.nodes["ElementPicker"]
         element_node.node_tree = bpy.data.node_groups["EmptyElement"]
         node_tree.links.new(node_tree.nodes["ElementalMixShader"].inputs[2], element_node.outputs[0])
         node_tree.links.new(element_node.inputs[0], node_tree.nodes["Group Input"].outputs["Normal"])
   return

# -----------------------------------------------------

def SnapFeetToFloor(shoetype, character, NFTDict): # moving character based on shoe height
   if shoetype == "FeetLong":
      shoes = list(NFTDict["08-C"].keys())[0]
   elif shoetype == "FeetMid":
      shoes = list(NFTDict["09-A"].keys())[0]
   else:
      shoes = list(NFTDict["10-F"].keys())[0]

   shoesObj = shoes + "_" + character
   objects = bpy.data.collections[shoesObj].objects
   characterHeight = 1.4
   platformHeight = 0.3
   if len(objects) > 0:
      cb = objects[0]
      depsgraph = bpy.context.evaluated_depsgraph_get()
      object_evaluated = cb.evaluated_get(depsgraph)
      #bbox_corners = [cb.matrix_world @ Vector(corner) for corner in cb.bound_box]
      bbox_corners = object_evaluated.matrix_world @ Vector(object_evaluated.bound_box[0])

      offset = platformHeight - bbox_corners.z  #orginal character feet heigh, different of shoe, new base height
      #bpy.ops.object.empty_add(location = bbox_corners)
   else:
      offset = platformHeight - characterHeight
      #apply inverse of this z height to armature
   rig_name = character + '_Rig'
   character_coll = bpy.data.collections[rig_name]
   for obj in character_coll.objects:
      if obj.type == 'ARMATURE':
         name = "root"
         pb = obj.pose.bones.get(name) # None if no bone named name
         pb.location = (0, 0, offset)
         config.custom_print("Moving: " + str(rig_name) + " Bone found: " + str(pb) + " Offset adjust: " + str(offset))


def RaycastPackpack(backpackType, character, NFTDict):
   if NFTDict["01-UT"] == 'Null':
      config.custom_print("There is no UPPER TORSO item for backpack to raycast against", '', config.bcolors.ERROR)
      return
   torsoObj = list(NFTDict["01-UT"].keys())[0]
   torsoObj = torsoObj + "_" + character
   objects = bpy.data.collections[torsoObj].objects
   if len(objects) > 0:
      for cb in objects:
         #cb = objects[0]
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
            config.custom_print("Hit at " + str(mw @ loc) + " (local)")
            config.custom_print(dst.matrix_world.to_translation())
            
            dir = (mw @ loc) - dst.matrix_world.to_translation()
            dist = dir.magnitude
            null_loc.location = Vector([0,2,0])
            null_loc.location.z -= dist

            if backpackType == "BackpackHigh":
               backpack = list(NFTDict["14-N"].keys())[0]
            else:
               backpack = list(NFTDict["20-BP"].keys())[0]
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
            return
         else:
            config.custom_print("No HIT")

# --------------------------------------------------------------

def SaveTempDNADict(TempNFTDict):
   save_path = os.getcwd()
   file_name = os.path.join(save_path, "NFT_Temp.json")
   try:
      ledger = json.dumps(TempNFTDict, indent=1, ensure_ascii=True)
      with open(file_name, 'w') as outfile:
         outfile.write(ledger + '\n')
         config.custom_print("Success: updated " + str(file_name), col=config.bcolors.OK)
   except:
      config.custom_print("Failed to update " + str(file_name), col=config.bcolors.ERROR)

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
   DNA = bpy.context.scene.my_tool.inputDNA
   NewDict = {}

   DNAString = DNA.split(',')
   character = DNAString.pop(0)
   element = DNAString.pop(0)
   style = DNAString.pop(0)
   if not ColorGen.DoesStyleExist(style):
      config.custom_print("This ({}) is not a valid color style, setting style to Random".format(style), '', config.bcolors.ERROR)
      style = 'Random'
   show_character(character)
   ohierarchy = get_hierarchy_ordered()

   ItemsUsed = {}
   for i in range(len(DNAString)):
      VarientDict = {}
      DNASplit = DNAString[i].split('-')
      atttype_index = DNASplit[0]
      variant_index = DNASplit[1]
      texture_index = DNASplit[2]

      attribute = list(ohierarchy.items())[i]
      if int(atttype_index) >= len(attribute[1].items()):
         DNAString[i] = "0-0-0"
         ItemsUsed[attribute[0]] = 'Null'
         config.custom_print("This is not valid for {}, setting slot to null".format(attribute[0]), '', config.bcolors.ERROR)
         continue

      type = list(attribute[1].items())[int(atttype_index)]
      if int(variant_index) >= len(type[1].items()):
         DNAString[i] = "0-0-0"
         ItemsUsed[attribute[0]] = 'Null'
         config.custom_print("This is not valid for {}, setting slot to null".format(attribute[0]), '', config.bcolors.ERROR)
         continue
      
      variant = list(type[1].items())[int(variant_index)][0]
      variant_name = variant.rpartition('_')[2]
      item_index = variant.split('_')[-2]
      
      if len(list(bpy.data.collections[variant].objects)) > 0:
         if int(texture_index) >= len(bpy.data.collections[variant].objects):
            DNAString[i] = "0-0-0"
            ItemsUsed[attribute[0]] = 'Null'
            config.custom_print("This is not valid for {}, setting slot to null".format(attribute[0]), '', config.bcolors.ERROR)
            continue
         else:
            last_texture = list(bpy.data.collections[variant].objects)[int(texture_index)].name
      else:
         last_texture = None

      if variant_name == 'Null':
         VarientDict = 'Null'
      else:
         current_entry = {}
         current_entry["item_attribute"] = attribute[0]
         current_entry["item_type"] = type[0]
         current_entry["item_variant"] = variant_name
         current_entry["item_texture"] = last_texture
         current_entry["item_index"] = item_index
         current_entry["texture_index"] = int(texture_index)
         current_entry["type_rarity"] = bpy.data.collections[type[0]]['rarity']
         current_entry["variant_rarity"] = bpy.data.collections[variant]['rarity']
         current_entry["texture_rarity"] = ohierarchy[attribute[0]][type[0]][variant]["textureSets"][last_texture]
         color_key = DNASplit[3]
         current_entry["color_key"] = color_key
         VarientDict[variant] = current_entry
      ItemsUsed[attribute[0]] = VarientDict

   DNAString = [character, element, style] + DNAString
   DNA = ','.join(DNAString)

   NewDict["DNAList"] = DNA
   NewDict["CharacterItems"] = ItemsUsed
   SaveTempDNADict(NewDict)
   show_nft_from_dna(DNA, ItemsUsed)
   return

# -----------------------------------------------------

def set_shape_keys(character, variant_name):
   rig_name = character + '_Rig'
   character_coll = bpy.data.collections[rig_name]
   for obj in character_coll.objects:
      if obj.type == 'ARMATURE':
         if bpy.data.actions.find(variant_name + "_" + character.lower() + '_action') > -1:
            obj.animation_data.action = bpy.data.actions[variant_name + "_" + character.lower() + '_action']
      if obj.type == 'MESH':
         if hasattr(obj.data, "shape_keys") and obj.data.shape_keys != None:
            for shape_key in obj.data.shape_keys.key_blocks:
               if variant_name in shape_key.name:
                  shape_key.value = 1
   return


def reset_shape_keys(character):
   rig_name = character + "_Rig"
   character_coll = bpy.data.collections[rig_name]
   for obj in character_coll.objects:
      if obj.type == 'ARMATURE':
         obj.animation_data.action = None
         name = "root"
         pb = obj.pose.bones.get(name) # None if no bone named name
         pb.location = (0, 0, 0)
      if obj.type == 'MESH':
         if hasattr(obj.data, "shape_keys") and obj.data.shape_keys != None:
            for shape_key in obj.data.shape_keys.key_blocks:
               if shape_key.name != 'Basis':
                  shape_key.value = 0
   return 


def reset_hair_shape_key(coll):
   for obj in coll.objects:
      if obj.type == 'MESH':
         if hasattr(obj.data, "shape_keys") and obj.data.shape_keys != None:
            for shape_key in obj.data.shape_keys.key_blocks:
               if shape_key.name != 'Basis':
                  shape_key.value = 0
   return


def set_hair_accessory_shape_keys(variant_coll, hair_coll):
   variant_name = variant_coll.name.split('_')[3]
   for obj in hair_coll.objects: # set blend shape on hair
      if obj.type == 'MESH':
         if hasattr(obj.data, "shape_keys") and obj.data.shape_keys != None:
               for shape_key in obj.data.shape_keys.key_blocks:
                  if shape_key.name.lower() == variant_name.lower():
                     shape_key.value = 1
   
   hair_name = hair_coll.name.split('_')[3]
   for obj in variant_coll.objects: # set blend shape on accessory
      if obj.type == 'MESH':
         if hasattr(obj.data, "shape_keys") and obj.data.shape_keys != None:
               for shape_key in obj.data.shape_keys.key_blocks:
                  if shape_key.name.lower() == hair_name.lower():
                     shape_key.value = 1
                  else:
                     shape_key.value = 0
   return

# -----------------------------------------------------

def set_texture_on_mesh(varient, meshes, texture_mesh, color_key, resolution, slot_pathing):
   suffix = config.texture_suffixes[resolution]
   for child in meshes:
      for childMatSlot in child.material_slots:
         # if config.LoggingEnabled: print("!--------------------------------!")
         # if config.LoggingEnabled: print("Child Name: " + child.name  + " || Child Mat" + childMatSlot.name)
         for textureMatSlot in texture_mesh.material_slots:
            # if config.LoggingEnabled: print("Texture Mat: " + textureMatSlot.name)
            childMatName = childMatSlot.material.name.partition('.')[0] # sometimes materials ending in .003 etc don't match up
            textureMatName = textureMatSlot.material.name.partition('.')[0]
            if textureMatName in childMatName or len(texture_mesh.material_slots) == 1 :
               # if config.LoggingEnabled: print("Child Name: " + childMatSlot.material.name + " || Texture Name: " + textureMatSlot.material.name)
               mat = textureMatSlot.material
               if mat.use_nodes:
                  for n in mat.node_tree.nodes:
                     if n.type == 'TEX_IMAGE':
                        if n.image is not None:
                           texture_info = get_new_texture_name(n, suffix, texture_mesh, slot_pathing, childMatSlot.name)
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
                                 elif _type == '_I':
                                    newImage = bpy.data.images.load(file, check_existing=False)
                                    mat.node_tree.nodes["IntensityNode"].image = newImage 
                                    mat.node_tree.nodes["IntensityNode"].image.colorspace_settings.name = 'Linear'
                                    mat.node_tree.nodes["IntensityMix"].outputs["Value"].default_value = 1

                     elif n.type == 'RGB' and color_key != 'Element':
                        GlobalColorList = OpenGlobalColorList()
                        colorChoice = GlobalColorList[color_key]
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
               childMatSlot.material = textureMatSlot.material #Check this - update to loop through all material slots
   return


def get_new_texture_name(node, suffix, texture_mesh, slot_pathing, material_name):
   types = ['_E', '_ID', '_M', '_N', '_R', '_D', '_O']
   for _type in types:
      filepath, partition, filename = node.image.filepath.rpartition('\\')
      if (_type + '.') in filename or (_type + '_') in filename:
         # filesplit = filename.split(_type)
         filesplit = filename.rpartition(_type)
         file_suffix, f, file_type = filesplit[2].rpartition('.')
         if file_suffix == suffix:
            # config.custom_print("then this should be the same texture?")
            return None
         else:
            # config.custom_print("this is a different texture?")
            texture_set = texture_mesh.name.rpartition('_')[2]
            slots_folder_path = os.path.join(bpy.context.scene.my_tool.root_dir, 'INPUT', 'SLOTS')
            variant_split = slot_pathing[2].split('_')
            variant_folder = variant_split[2] + '_' + variant_split[3]
            variant_folder_path = os.path.join(slots_folder_path, slot_pathing[0], slot_pathing[1], variant_folder)
            texture_folder_path = os.path.join(variant_folder_path, "Textures", texture_set)
            if len(next(os.walk(texture_folder_path))[1]) > 0: # if there's multiple sets
               if '.' in material_name:
                  material_name = material_name.split('.')[0]
               texture_folder_path = os.path.join(texture_folder_path, material_name)

            new_texture_end = _type + suffix + '.' + file_type
            original_texture_end = _type + '.' + file_type
            original_texture = None
            new_path = filepath + partition

            for t in os.listdir(texture_folder_path): # look within current texture set folder
               if t.endswith(new_texture_end): # image with correct suffix is found
                  new_texture = t
                  new_texture_path = new_path + new_texture
                  return new_texture, new_texture_path, _type
               elif t.endswith(original_texture_end): # returns 4k if proper size texture doesn't exist
                  texture_split = t.split('_')
                  original_texture_path = new_path + t
                  original_texture = t, original_texture_path, _type
            if original_texture: # if correct size texture isn't found but 4k texture is found, return it
               texture = texture_split[0] + '_' + texture_split[1] + _type + suffix
               config.custom_print("Texture ({}) could not be found, falling back to 4k texture.".format(texture), col=config.bcolors.ERROR)
               config.custom_print("\tPlease down-res textures to speed up previewer :<", col=config.bcolors.WARNING)
               return original_texture

         if texture_set != config.fallback_texture_set_name: # if texture doesn't exist in current texture set, try find it within the first ('A') texture set
            original_texture_folder_path = os.path.join(variant_folder_path, "Textures", config.fallback_texture_set_name)
            for t in os.listdir(original_texture_folder_path):
               if t.endswith(new_texture_end):
                  new_texture = t
                  new_texture_path = new_path + new_texture
                  return new_texture, new_texture_path, _type
               elif t.endswith(original_texture_end): # returns 4k if proper size texture doesn't exist
                  texture_split = t.split('_')
                  original_texture_path = new_path + t
                  original_texture = t, original_texture_path, _type
         if original_texture:
            texture = texture_split[0] + '_' + texture_split[1] + _type + suffix
            config.custom_print("Texture ({}) could not be found, falling back to 4k texture.".format(texture), col=config.bcolors.ERROR)
            config.custom_print("\tPlease down-res textures to speed up previewer :<", col=config.bcolors.WARNING)
            return original_texture
   return None

#  ----------------------------------------------------------------------------------

def get_new_dna_strand(slot_coll, variant_name, color_key='', texture_index=0): # get new dna strand from variant name
   new_dna_strand = ''
   type_index = 0
   variant_index = 0

   for type_coll in slot_coll.children: # get type, variant, texture index by going through collection hierarchy
      if variant_name in type_coll.children.keys():
         var_coll = bpy.data.collections[variant_name]

         type_list = list(type_coll.children)
         variant_index = type_list.index(var_coll)

         if type_coll.name[3:] in config.EmptyTypes:
            dna_string = [str(type_index), str(variant_index), str(texture_index), 'Empty']
         elif type_coll.name[3:].startswith('Tattoo'):
            dna_string = [str(type_index), str(variant_index), str(texture_index), 'Black']
         elif color_key:
            dna_string = [str(type_index), str(variant_index), str(texture_index), color_key]
         else:
            dna_string = [str(type_index), str(variant_index), str(texture_index)]
         new_dna_strand = '-'.join(dna_string)
         break
      else:
         type_index += 1
   return new_dna_strand # return dna strand or empty string if not valid


#  ----------------------------------------------------------------------------------


def elements_updated(): # called from UI
   NFTDict = LoadTempDNADict()
   DNA = NFTDict["DNAList"]
   DNASplit = DNA.split(',')
   element = DNASplit[1] # .pop
   last_ele_style, last_ele = element.split('-')

   if (bpy.context.scene.my_tool.element == last_ele  or last_ele_style == 'None') and \
               bpy.context.scene.my_tool.elementStyle == last_ele_style:
      return

   if bpy.context.scene.my_tool.elementStyle == 'None':
      new_element = 'None-None'
   else:
      new_element = bpy.context.scene.my_tool.elementStyle + '-' + bpy.context.scene.my_tool.element
   DNASplit[1] = new_element
   new_DNA = ','.join(DNASplit)

   if new_element != 'None-None':
      dna_string, CharacterItems = randomize_color_style(element=new_element, dna_string=new_DNA)
   else:
      dna_string, CharacterItems = randomize_color_style(dna_string=new_DNA)
   show_nft_from_dna(dna_string, CharacterItems)
   return


def general_pointer_updated(): # called from UI
   if bpy.context.scene.my_tool.inputGeneral is not None:
      inputted_item = bpy.context.scene.my_tool.inputGeneral
      item = inputted_item.name
      try:
         att_name, type_name, i, var_name = item.split('_')
      except:
         config.custom_print("Wrong type of collection", col=config.bcolors.ERROR)
         bpy.context.scene.my_tool.inputGeneral = None
         return
      input_name = 'input' + att_name
      att_coll = bpy.data.collections[config.Slots[input_name][0]]
      for types in att_coll.children:
         if types.name.endswith(type_name):
            for vars in types.children:
               split_variant_name = vars.name.rpartition('_')[2]
               if split_variant_name == var_name:
                  pointers_have_updated(input_name, vars.name)
                  break
      bpy.context.scene.my_tool.inputGeneral = None
   return


def pointers_have_updated(slots_key, variant_name=''): # this is called from init properties if pointerproperty updates
   last_key = slots_key.replace("input", "last")
   coll_name, label = config.Slots[slots_key]

   if variant_name != '': # if called from general pointer
      new_dnastrand = get_new_dna_strand(bpy.data.collections[coll_name], variant_name)
      if new_dnastrand != '': # if is from correct collection
         dna_string, CharacterItems = update_DNA_with_strand(coll_name, new_dnastrand)
         bpy.context.scene.my_tool[last_key] = bpy.data.collections[variant_name]
         show_nft_from_dna(dna_string, CharacterItems)
      else: # clear pointer or fill with last collection as new collection is not a valid input
         config.custom_print("is not valid || clear", col=config.bcolors.WARNING)
         last_type = variant_name.rpartition('_')[2]
         if last_type not in ['Null', 'Nulll']:
            bpy.context.scene.my_tool[slots_key] = bpy.context.scene.my_tool[last_key]
         else:
            bpy.context.scene.my_tool[slots_key] = None

   elif bpy.context.scene.my_tool.get(slots_key) is not None: # pointer has been filled in UI
      new_dnastrand = get_new_dna_strand(bpy.data.collections[coll_name], bpy.context.scene.my_tool.get(slots_key).name)
      if new_dnastrand != '': # if is from correct collection
         dna_string, CharacterItems = update_DNA_with_strand(coll_name, new_dnastrand)
         bpy.context.scene.my_tool[last_key] = bpy.context.scene.my_tool.get(slots_key)
         show_nft_from_dna(dna_string, CharacterItems)
      else: # clear pointer or fill with last collection as new collection is not a valid input
         config.custom_print("is not valid || clear", col=config.bcolors.WARNING)
         last_type = bpy.context.scene.my_tool[last_key].name.rpartition('_')[2]
         if last_type not in ['Null', 'Nulll']:
            bpy.context.scene.my_tool[slots_key] = bpy.context.scene.my_tool[last_key]
         else:
            bpy.context.scene.my_tool[slots_key] = None

   else: # pointer has been cleared so remove item from nft
      last_variant = bpy.context.scene.my_tool.get(last_key)
      last_type = last_variant.name.split('_')[1]
      if last_type not in ['Null', 'Nulll']: # gets null variant then fills pointer with it
         coll = bpy.data.collections[coll_name]
         null_var_coll = get_null_variant_collection(coll)
         new_dnastrand = get_new_dna_strand(coll, null_var_coll.name)
         if new_dnastrand != '':
            dna_string, CharacterItems = update_DNA_with_strand(coll_name, new_dnastrand)
            bpy.context.scene.my_tool[slots_key] = None
            bpy.context.scene.my_tool[last_key] = null_var_coll
            show_nft_from_dna(dna_string, CharacterItems)
      else: # will refill pointer with null
         bpy.context.scene.my_tool[slots_key] = bpy.context.scene.my_tool.get(last_key)

#  ----------------------------------------------------------------------------------

def get_null_variant_collection(att_coll): # if slot has been cleared, fill with relevant empty variant e.g. BareF if F is cleared
   def check_collections(info, atts):
      should_fill = True
      for i in range(len(atts)):
         input_name = "input" + atts[i][3:]
         current_variant = bpy.context.scene.my_tool[input_name]
         if current_variant:
            current_type = current_variant.name.split('_')[1]
            if current_type.startswith(info[0]) and not current_type.endswith(info[1]):
               should_fill = False
               break
      if should_fill:
         feet_coll = bpy.data.collections[atts[-1]]
         for type_coll in feet_coll.children:
            if type_coll.name.endswith("None"):
               var_coll = type_coll.children[0]
               if att_coll.name == feet_coll.name:
                  return var_coll
               else:
                  new_dnastrand = get_new_dna_strand(feet_coll, var_coll.name)
                  dna_string, CharacterItems = update_DNA_with_strand(feet_coll.name, new_dnastrand)
                  newTempDict = {}
                  newTempDict["DNAList"] = dna_string
                  newTempDict["CharacterItems"] = CharacterItems
                  SaveTempDNADict(newTempDict)
                  return att_coll.children[0].children[0]
      return att_coll.children[0].children[0]

   head_info = ["Head", "HeadShortNone"]
   head_atts = ["14-N", "16-LH", "15-MH", "18-ES"]
   feet_info = ["F", "FShortNone"]
   feet_atts = ["08-C", "09-A", "10-F"]

   if att_coll.name in head_atts: # should this account for the hoodie :(, can't differentiate between head and hair types atm
      return check_collections(head_info, head_atts)
   elif att_coll.name in feet_atts:
      return check_collections(feet_info, feet_atts)
   return att_coll.children[0].children[0]


#  ----------------------------------------------------------------------------------

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
   DNA = dna_string.split(',') # .pop(0)
   old_strand = DNA[coll_index + 3]

   if dna_strand: # append old colour to new dna_string
      new_dnastrand = dna_strand
      if len(dna_strand.split('-')) < 4 and dna_strand != '0-0-0':
         dna_strand += ('-' + old_strand.rpartition('-')[2])
         new_dnasplit = dna_strand.split('-')
         if len(old_strand.split('-')) < 4:
            style = bpy.context.scene.my_tool.currentGeneratorStyle or "Random"
            if style != 'Elemental':
               new_colorkey, color_choice = ColorGen.PickOutfitColors(coll_name, style)
            else:
               new_colorkey = 'Element'
         else:
            new_colorkey = old_strand.rpartition('-')[2]
         new_dnasplit[-1] = new_colorkey
         new_dnastrand = '-'.join(new_dnasplit)
      else:
         new_colorkey = dna_strand.rpartition('-')[2]

   else: # randomize colour here
      new_split = DNA[coll_index + 3].split('-') # .pop
      max_attempts = 10
      old_colorkey = old_strand.split('-')[-1]
      for i in range(max_attempts):
         style = bpy.context.scene.my_tool.currentGeneratorStyle or "Random"
         new_colorkey, color_choice = ColorGen.PickOutfitColors(coll_name, style)
         if new_colorkey != old_colorkey:
            break
      new_split[-1] = new_colorkey
      new_dnastrand = '-'.join(new_split)

   if new_dnastrand == '0-0-0':
      DNA[coll_index + 3] = str(new_dnastrand) # .pop
      dna_string = ','.join(DNA)
      CharacterItems[coll_name] = "Null"
      return dna_string, CharacterItems

   # update NFTDict based on new dna strand
   type_index, var_index, tex_index, color_key = new_dnastrand.split('-')
   batch_index = bpy.context.scene.my_tool.CurrentBatchIndex # get data from batch record json
   nftrecord_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{}".format(batch_index), "_NFTRecord_{}.json".format(batch_index))
   batch_record = json.load(open(nftrecord_save_path))
   type_coll = bpy.data.collections[coll_name].children[int(type_index)] # find collection based on indices in new dna strand
   if type_coll.name[3:] in config.EmptyTypes: # override colours in strand if needed
      new_colorkey = 'Empty'
   elif type_coll.name[3:].startswith("Tattoo"):
      new_colorkey = 'Black'
   elif new_colorkey == 'Empty':
      style = bpy.context.scene.my_tool.currentGeneratorStyle or "Random"
      new_colorkey, color_choice = ColorGen.PickOutfitColors(coll_name, style)
   new_dnastrand = '-'.join([type_index, var_index, tex_index, new_colorkey])

   var_coll = type_coll.children[int(var_index)]
   DNA[coll_index + 3] = str(new_dnastrand) # .pop
   dna_string = ','.join(DNA)

   record_item = batch_record["hierarchy"][coll_name][type_coll.name][var_coll.name]
   new_tex = list(record_item['textureSets'].keys())[int(tex_index)]
   new_tex_rarity = record_item['textureSets'][new_tex]
   new_item = {}
   new_item["item_attribute"] = coll_name
   new_item["item_type"] = type_coll.name
   new_item["item_variant"] = var_coll.name.split('_')[3]
   new_item["item_texture"] = new_tex
   new_item["type_rarity"] = type_coll['rarity']
   new_item["variant_rarity"] = var_coll['rarity']
   new_item["texture_rarity"] = new_tex_rarity
   new_item["color_key"] = new_colorkey
   variant_dict = {}
   variant_dict[var_coll.name] = new_item
   CharacterItems[coll_name] = variant_dict
   return dna_string, CharacterItems


def randomize_color_style(new_style='', element='', dna_string=''):
   NFTDict = LoadTempDNADict()
   CharacterItems = NFTDict["CharacterItems"]
   if not dna_string:
      dna_string = NFTDict["DNAList"]
   DNASplit = dna_string.split(',') 

   if element:
      new_style = 'Elemental'
      bpy.context.scene.my_tool.currentGeneratorStyle = new_style
   elif not new_style: # get color style
      last_style = bpy.context.scene.my_tool.currentGeneratorStyle
      max_count = 10
      for i in range(max_count):
         new_style = ColorGen.SetUpCharacterStyle()
         if new_style != last_style:
            break
      bpy.context.scene.my_tool.currentGeneratorStyle = new_style

   DNASplit[2] = new_style # .pop(0)
   for coll_name in list(NFTDict["CharacterItems"].keys()): # update all existing items with new colours from chosen style
      if CharacterItems[coll_name] != 'Null': 
         index = list(NFTDict["CharacterItems"].keys()).index(coll_name)
         dna_strand = DNASplit[index + 3] # .pop

         type_index, var_index, tex_index, color_key = dna_strand.split('-')
         type_coll = bpy.data.collections[coll_name].children[int(type_index)]
         var_coll = type_coll.children[int(var_index)]

         if type_coll.name[3:] in config.EmptyTypes:
            new_key = 'Empty'
         elif type_coll.name[3:].startswith("Tattoo"):
            new_key = 'Black'
         elif element:
            new_key = 'Element'
         else:
            new_key, color_choice = ColorGen.PickOutfitColors(coll_name, new_style)
         new_item = CharacterItems[coll_name][var_coll.name]
         new_item["color_key"] = new_key
         new_dnastrand = dna_strand.split('-')
         new_dnastrand[-1] = new_key
         new_dnastring = '-'.join(new_dnastrand)
         DNASplit[index + 3] = new_dnastring # .pop

         dna_string = ','.join(DNASplit)
         variant_dict = {}
         variant_dict[var_coll.name] = new_item
         CharacterItems[coll_name] = variant_dict
   return dna_string, CharacterItems


def fill_pointers_from_dna(DNA): # fill all pointer properties with variants
   ohierarchy = get_hierarchy_ordered()
   DNAString = DNA.split(',')
   character = DNAString.pop(0)
   element = DNAString.pop(0)
   style = DNAString.pop(0)
   show_character(character)
   
   for i in range(len(DNAString)):
      DNASplit = DNAString[i].split('-')
      atttype_index = DNASplit[0]
      variant_index = DNASplit[1]
      slot = list(ohierarchy.items())[i]
      atttype = list(slot[1].items())[int(atttype_index)]
      variant = list(atttype[1].items())[int(variant_index)][0]

      slot_name = slot[0][3:len(slot[0])]
      last_slot_name = "last" + str(slot_name)
      input_slot_name = "input" + str(slot_name)
      if variant.split('_')[3] != 'Null': # fill input slot with current variant
         bpy.context.scene.my_tool[last_slot_name] = bpy.data.collections[variant]
         bpy.context.scene.my_tool[input_slot_name] = bpy.data.collections[variant]
      else:
         bpy.context.scene.my_tool[last_slot_name] = bpy.data.collections[variant]
         bpy.context.scene.my_tool[input_slot_name] = None

   ele_style, ele = element.split('-') # set element UI to current element
   if ele != bpy.context.scene.my_tool.element and ele_style != 'None':
      bpy.context.scene.my_tool.element = ele
   if ele_style != bpy.context.scene.my_tool.elementStyle:
      bpy.context.scene.my_tool.elementStyle = ele_style
   return


def set_texture_on_slot(coll_name, variant_name, texture_index):
   new_dnastrand = get_new_dna_strand(bpy.data.collections[coll_name], variant_name, texture_index=texture_index)
   if new_dnastrand != '': # if is from correct collection
      dna_string, CharacterItems = update_DNA_with_strand(coll_name, new_dnastrand)
      show_nft_from_dna(dna_string, CharacterItems)
      return True
   return False


#  -------------------------------------- TATTOOS --------------------------------------------

def get_texture_for_tattoo(att, type, variant, element):
   slots_folder_path = os.path.join(bpy.context.scene.my_tool.root_dir, 'INPUT', 'SLOTS')
   variant_split = variant.split('_')
   variant_folder = variant_split[2] + '_' + variant_split[3]
   variant_folder_path = os.path.join(slots_folder_path, att, type, variant_folder)
   texture_folder_path = os.path.join(variant_folder_path, "Textures", element)
   for dir in os.listdir(texture_folder_path):
      if "_T." in dir:
         texture_path = os.path.join(texture_folder_path, dir)
         return texture_path


def add_texture_to_tattoos(character, attr, texture):
   image_node_name = attr.split('-')[-1]
   skin_node_tree = bpy.data.materials['CharacterSkin_Master' + "_" + character].node_tree

   if texture == 'clear':
      skin_node_tree.nodes[image_node_name].image = None
   elif texture:
      newImage = bpy.data.images.load(texture, check_existing=False)
      skin_node_tree.nodes[image_node_name].image = newImage


def turn_on_tattoo(element, color=''):
   element_style, element_type = element.split('-')
   #link element mix to whether outfit elmental is on
   tattoo_node_tree = bpy.data.node_groups["Tattoo_Master"]
   elementalTattooMixer = tattoo_node_tree.nodes["ElementalTattoo"]
   if element_type == "None":
      elementalTattooMixer.outputs["Value"].default_value = 0
      elementalTattooMixer.outputs["Value"].default_value = bpy.data.node_groups["OutfitElementMixer"].nodes["ElementalMix"].outputs["Value"].default_value
      tattoo_node_tree.nodes["EmissionMultiplier"].outputs["Value"].default_value = 1
   elif element_style == "All":
      elementalTattooMixer.outputs["Value"].default_value = 0
      tattoo_node_tree.nodes["TattooColor"].outputs["Color"].default_value = [0.0,0.0,0.0, 1.0]
   elif element_style == "Outfit":
      elementalTattooMixer.outputs["Value"].default_value = 1

#--------------------------------------------------------------------------------------

def set_armature_for_meshes(character, meshes):
   armature_name = "armature_" + str(character).lower()
   if bpy.data.objects.get(armature_name) is not None:
      for mesh in meshes:
         if mesh.modifiers:
               for mod in mesh.modifiers:
                  if mod.type == 'ARMATURE':
                     mod.object = bpy.data.objects[armature_name]
   return


def set_subdiv_levels(meshes):
   for mesh in meshes:
            if mesh.modifiers:
                  for mod in mesh.modifiers:
                     if mod.type == 'SUBSURF':
                        mod.show_viewport = False
                        mod.show_render = True
                        mod.levels = mod.render_levels
   return

#---------------------------------------------------------------------------


def colorpicker_has_applied(): # load colour picker onto mesh in UI
   inputColorListSceneObject = bpy.context.scene.my_tool.inputColorListSceneObject
   tint_key = bpy.context.scene.my_tool.colorSetName
   if inputColorListSceneObject and tint_key:
      collection_name = inputColorListSceneObject.users_collection[0].name
      variant_name = collection_name.rpartition('_')[0]

      ColorList = ColorGen.OpenGlobalColorList()

      if tint_key in ColorList and inputColorListSceneObject:
         att_name = collection_name.partition('_')[0]
         slots_key = 'input' + att_name
         coll_name, label = config.Slots[slots_key]
         new_dnastrand = get_new_dna_strand(bpy.data.collections[coll_name], variant_name, color_key=tint_key)
         if new_dnastrand != '': # if is from correct collection
            dna_string, CharacterItems = update_DNA_with_strand(coll_name, new_dnastrand)
            show_nft_from_dna(dna_string, CharacterItems)
            return True
   return False



#---------------------------------------------------------------------------

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


def get_hierarchy_ordered(index=0):
   if not index:
         index = bpy.context.scene.my_tool.CurrentBatchIndex
   batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
   NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(index), "_NFTRecord_{}.json".format(index))
   if os.path.exists(NFTRecord_save_path):
      DataDictionary = json.load(open(NFTRecord_save_path), object_pairs_hook=collections.OrderedDict)
      hierarchy = DataDictionary["hierarchy"]
      return hierarchy
   return None


def get_hierarchy_unordered(index=0):
   if not index:
         index = bpy.context.scene.my_tool.CurrentBatchIndex
   batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
   NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(index), "_NFTRecord_{}.json".format(index))      
   if os.path.exists(NFTRecord_save_path):
      DataDictionary = json.load(open(NFTRecord_save_path))
      hierarchy = DataDictionary["hierarchy"]
      return hierarchy
   return None


def HexToRGB(hex):
   string = hex.lstrip('#')
   rgb255 = tuple( int(string[i:i+2], 16) for i in (0,2,4) )
   rgb = tuple( (float(x) /255) for x in rgb255)
   return rgb


#-----------------------------------------------------------------------------------



if __name__ == '__main__':
   print("okay")