# Purpose:
# This file generates the Outfit DNA based on a rule set

import bpy
import os
import json
import random
import importlib
import time
from datetime import datetime

from . import ColorGen
importlib.reload(ColorGen)

from . import config


# A list for each caterogry of clothing that states what slots it will fil
ItemUsedBodySlot = {
"ShirtCropSleeveless" : ["01-UpperTorso"],
"ShirtCropSleevelessBack" : ["01-UpperTorso", "20-Backpack", "14-Neck"],
"ShirtCropSleevelessNeck" : ["01-UpperTorso", "14-Neck", "11-HairLong", "17-EarringsLong"],
"ShirtCrop" : ["01-UpperTorso", "03-ForeArms"],
"ShirtCropNeck" : ["01-UppreTorso", "03-ForeArms", "14-Neck", "11-HairLong", "17-EarringsLong"],
"ShirtMidSleeveless" : ["01-UpperTorso", "02-MiddleTorso"],
"ShirtMidSleevelessNeck" : ["01-UpperTorso", "02-MiddleTorso", "14-Neck", "11-HairLong", "17-EarringsLong"],
"ShirtMidSleevelessNeckBack" : ["01-UpperTorso", "02-MiddleTorso", "14-Neck", "11-HairLong", "20-Backpack", "17-EarringsLong"],
"ShirtMid" : ["01-UpperTorso", "02-MiddleTorso", "03-ForeArms"],
"ShirtMidNeck" : ["01-UpperTorso", "02-MiddleTorso", "03-ForeArms", "14-Neck", "11-HairLong", "17-EarringsLong"],
"ShirtMidNeckBack" : ["01-UpperTorso", "02-MiddleTorso", "03-ForeArms", "14-Neck", "11-HairLong", "17-EarringsLong", "20-Backpack"],
"ShirtLongSleeveless" : ["01-UpperTorso", "02-MiddleTorso", "06-PelvisThick"],
"ShirtLongSleevelessNeck" : ["01-UpperTorso", "02-MiddleTorso", "06-PelvisThick","14-Neck", "11-HairLong", "17-EarringsLong"],
"ShirtLongSleevelessNeckBack" : ["01-UpperTorso", "02-MiddleTorso", "06-PelvisThick","14-Neck", "11-HairLong", "20-Backpack", "17-EarringsLong"],
"ShirtLong" : ["01-UpperTorso", "02-MiddleTorso", "06-PelvisThick", "03-ForeArms"],
"ShirtLongNeck" : ["01-UpperTorso", "02-MiddleTorso", "06-PelvisThick", "03-ForeArms","14-Neck", "11-HairLong", "17-EarringsLong"],
"ShirtMidHead": ["01-UpperTorso", "02-MiddleTorso", "06-PelvisThick", "03-ForeArms","14-Neck", "11-HairLong", "12-HairShort", "18-Earrings", "17-EarringsLong"],

"PantsShort" : ["07-PelvisThin"],
"PantsShortThick" : ["06-PelvisThick", "07-PelvisThin"],
"PantsShortHigh" : ["06-PelvisThick", "07-PelvisThin", "02-MiddleTorso"],
"PantsMid" : ["07-PelvisThin", "08-Calf"],
"PantsMidThick" : ["06-PelvisThick", "07-PelvisThin", "08-Calf"],
"PantsMidHigh" : ["06-PelvisThick", "07-PelvisThin", "08-Calf", "02-MiddleTorso"],
"PantsLong" : ["07-PelvisThin", "08-Calf", "09-Ankle"],
"PantsLongThick" : ["06-PelvisThick", "07-PelvisThin", "08-Calf", "09-Ankle"],
"PantsLongHigh" : ["06-PelvisThick", "07-PelvisThin", "08-Calf", "09-Ankle", "02-MiddleTorso"],

"OutfitLong" : ["01-UpperTorso", "02-MiddleTorso", "06-PelvisThick", "07-PelvisThin", "03-ForeArms", "14-Neck", "08-Calf", "09-Ankle","17-EarringsLong"],
"OutfitLongSleeveless" : ["01-UpperTorso", "02-MiddleTorso", "06-PelvisThick", "07-PelvisThin", "14-Neck", "08-Calf", "09-Ankle", "17-EarringsLong"],
"OutfitMid" : ["01-UpperTorso", "02-MiddleTorso", "06-PelvisThick", "07-PelvisThin", "03-ForeArms", "14-Neck", "08-Calf", "17-EarringsLong"],
"OutfitMidSleeveless" : ["01-UpperTorso", "02-MiddleTorso", "06-PelvisThick", "07-PelvisThin", "14-Neck", "08-Calf", "17-EarringsLong"],
"OutfitShort" : ["01-UpperTorso", "02-MiddleTorso", "06-PelvisThick", "07-PelvisThin", "03-ForeArms", "14-Neck", "17-EarringsLong"],
"OutfitShortSleeveless" : ["01-UpperTorso", "02-MiddleTorso", "06-PelvisThick", "07-PelvisThin", "14-Neck", "17-EarringsLong"],

"Forearm" : ["03-ForeArms"],
"HandsShort" : ["05-Hands", "04-Wrists"],
"GlovesShort" : ["05-Hands", "04-Wrists"],
"HandsLong" : ["03-ForeArms", "05-Hands", "04-Wrists"],
"GlovesLong" : ["03-ForeArms", "05-Hands", "04-Wrists"],

"FeetLong" : ["08-Calf", "09-Ankle", "10-Feet"],
"FeetMid" : ["09-Ankle", "10-Feet"],
"FeetShort" : ["10-Feet"],
"FeetShortNone" : ["10-Feet"],
"Calf" : ["08-Calf"],
"CalfLong" : ["08-Calf", "09-Ankle"],

"Neck" : ["14-Neck", "17-EarringsLong"],
"HairShort" : ["12-HairShort"],
"HairShortFront" : ["12-HairShort", "15-MiddleHead"],
"HairMid" : ["11-HairLong", "14-Neck", "12-HairShort", "18-Earrings", "17-EarringsLong"],
"HairLong" : ["11-HairLong", "14-Neck", "12-HairShort", "18-Earrings", "20-Backpack", "17-EarringsLong"],

"HeadFull" : ["11-HairLong", "14-Neck", "12-HairShort", "15-MiddleHead", "16-LowerHead", "18-Earrings", "17-EarringsLong"],
"HeadExtraEar" : ["17-EarringsLong", "18-Earrings"],
"HeadExtra" : [],

"FaceMid" : ["15-MiddleHead"],
"FaceMidNeutral" : ["15-MiddleHead", "19-Expression"],
"FaceLower" : ["16-LowerHead"],
"FaceFull" : ["15-MiddleHead", "16-LowerHead"],
"EarringsShort" : ["18-Earrings"], 
"EarringsLong" : ["18-Earrings", "17-EarringsLong"],

"Backpack" : ["20-Backpack"],
"BackpackHigh" : ["14-Neck", "20-Backpack"],

"Expression" : ["19-Expression"],
"ExpressionLower" : ["16-LowerHead", "19-Expression"],
"ExpressionLowerNone" : ["16-LowerHead", "19-Expression"],
"ExpressionUpper" : ["15-MiddleHead", "19-Expression"],
"ExpressionFull" : ["16-LowerHead", "15-MiddleHead", "19-Expression"],

"Background" : ["22-Background"],

"TattooMiddleTorso": ["02-MiddleTorso"],
"TattooForearm": ["03-ForeArms"],
"TattooCalf": ["08-Calf"],
"TattooFeet": ["10-Feet"],
"TattooNeck": ["14-Neck"]

}
  

def RandomizeFullCharacter(maxNFTs, save_path):
    index = bpy.context.scene.my_tool.CurrentBatchIndex
    batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(index), "_NFTRecord_{:03d}.json".format(index))

    DataDictionary = json.load(open(NFTRecord_save_path))

    hierarchy = DataDictionary["hierarchy"]
    DNAList = DataDictionary["DNAList"]

    exsistingDNASet = set(DNAList)
    NFTDict = {}
    DNASet = set()
    numberToGen = int(maxNFTs)

    allowFailedAttempts = 50
    currentFailedAttempts = 0
    while numberToGen > 0: 
        SingleDNA = ["0"] * len(list(hierarchy.keys()))
        ItemsUsed = {}

        attributeskeys = list(hierarchy.keys())
        attributevalues = list(hierarchy.values())
        attributeUsedDict = dict.fromkeys(attributeskeys, False)

        character = PickCharacter()
        element = PickElement()
        style = PickCharacterElementalStyle(element)

        hair_coll_name = ''
        for attribute in attributeskeys:
            #Check if current attribute we are looking at has already been used
            if(attributeUsedDict.get(attribute)):
                #If it has populate will null varibales and move to next             
                typeChoosen = list(hierarchy[attribute])[0]
                varientChoosen = list(hierarchy[attribute][typeChoosen].keys())[0]

                typeIndex = 0
                varientIndex = 0
                textureIndex = 0
                textureChoosen = None
            else:
                #Check if current attribute is an accessory for hair
                if attribute[3:].startswith("Accessories"): 
                    hair_collection = bpy.data.collections[hair_coll_name + '_' + character]
                    typeChoosen, typeIndex, varientChoosen, varientIndex = PickWeightedAccessoryTypeAndVariant(hierarchy[attribute], hair_collection)
                else:
                    typeChoosen, typeIndex = PickWeightedAttributeType(hierarchy[attribute])
                    varientChoosen, varientIndex = PickWeightedTypeVarient(hierarchy[attribute][typeChoosen])

                textureChoosen, textureIndex = PickWeightedTextureVarient(hierarchy[attribute][typeChoosen][varientChoosen])

                if attribute[3:].startswith('Hair') and not varientChoosen.endswith("Null"):
                    hair_coll_name = varientChoosen

                #if both type and varient index are 0 a NULL collection was choosen
                if typeIndex == 0 and varientIndex == 0:
                    SingleDNA[list(hierarchy.keys()).index(attribute)] = "0-0-0"
                else:
                    ItemClothingGenre = hierarchy[attribute][typeChoosen][varientChoosen]["item_type"][3:]
                    #loop through all slots that selected item will take up
                    if ItemClothingGenre in ItemUsedBodySlot:
                        UsedUpSlotArray = ItemUsedBodySlot.get(ItemClothingGenre)
                    else: 
                        UsedUpSlotArray = []
                    #Update used slot array to reflect new used up slots
                    if UsedUpSlotArray:
                        for i in ItemUsedBodySlot.get(ItemClothingGenre):
                            SlotUpdateValue = {i : True}
                            attributeUsedDict.update(SlotUpdateValue)
                

            VarientDict = {}
            current_entry = {}
            variant_name = varientChoosen.split('_')[-1]

            if variant_name in ["Null", 'Nulll']:
                VarientDict = 'Null'
                SingleDNA[list(hierarchy.keys()).index(attribute)] = "0-0-0"
            else:
                color_key = setColorKeyData(attribute, typeChoosen, element)

                SingleDNA[list(hierarchy.keys()).index(attribute)] = "-".join([str(typeIndex), str(varientIndex), str(textureIndex), str(color_key)])

                #Check rarity of current texture set
                if hierarchy[attribute][typeChoosen][varientChoosen]["textureSets"]:
                    texture_rarity = hierarchy[attribute][typeChoosen][varientChoosen]["textureSets"][textureChoosen]
                else:
                    texture_rarity = 0

                current_entry["item_attribute"] = attribute
                current_entry["item_type"] = typeChoosen
                current_entry["item_variant"] = variant_name
                current_entry["item_texture"] = textureChoosen
                current_entry["item_index"] = hierarchy[attribute][typeChoosen][varientChoosen]["item_index"]
                current_entry["type_rarity"] = hierarchy[attribute][typeChoosen][varientChoosen]["type_rarity"]
                current_entry["variant_rarity"] = hierarchy[attribute][typeChoosen][varientChoosen]["variant_rarity"]
                current_entry["texture_rarity"] = texture_rarity
                current_entry["color_key"] = color_key
                VarientDict[varientChoosen] = current_entry

            ItemsUsed[attribute] = VarientDict
            
        #Format DNA        
        SingleDNA.insert(0, character)
        SingleDNA.insert(1, element)
        SingleDNA.insert(2, style)

        formattedDNA = ','.join(SingleDNA)
        if formattedDNA not in DNASet and formattedDNA not in exsistingDNASet:
            DNASet.add(formattedDNA)
            NFTDict[formattedDNA] = ItemsUsed
            numberToGen -= 1
        else:
            currentFailedAttempts += 1
            if currentFailedAttempts > allowFailedAttempts:
                break

    for m in bpy.data.materials: # purge all unused materials for now
        if m.users == 0 and m.name != 'MasterV01':
            bpy.data.materials.remove(m)

    return list(DNASet), NFTDict
    
def setColorKeyData(Attribute, typeChoosen, element):
    #Set color keys
    if typeChoosen[3:] in config.EmptyTypes:
        color_key = 'Empty'
    elif typeChoosen[3:].startswith("Tattoo"):
        color_key = 'Black'
    elif element != 'None-None':
        color_key = 'Element'
    else:
        color_key, color_choice = ColorGen.PickOutfitColors(Attribute)

    return color_key

def PickCharacterElementalStyle(element):
    if element == 'None-None':
        style = ColorGen.SetUpCharacterStyle()
    else:
        style = 'Elemental'
    bpy.context.scene.my_tool.currentGeneratorStyle = style
    return style

# ------------------------------------------------------

#Chooses a random teture set to use for mesh based on rarity ratings 
def GetRandomSingleTexture(att_name, variant_coll):
    index = bpy.context.scene.my_tool.CurrentBatchIndex
    batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(index), "_NFTRecord_{:03d}.json".format(index))

    DataDictionary = json.load(open(NFTRecord_save_path))
    hierarchy = DataDictionary["hierarchy"]

    number_List_Of_i = []
    rarity_List_Of_i = []

    #Find item and loop through all available textures sets on that item
    att_index = list(hierarchy.keys()).index(att_name)
    inputDNA = bpy.context.scene.my_tool.inputDNA
    dna_split = inputDNA.split(',')
    old_dna_strand = dna_split[att_index + 3] # .pop(0)
    old_texture_index = old_dna_strand.split('-')[2]
    variant = variant_coll.name
    for type in hierarchy[att_name].keys():
        if variant in hierarchy[att_name][type].keys():
            item_info = hierarchy[att_name][type][variant]
            texture_info = item_info["textureSets"]
            for tex in texture_info.keys():
                rarity = texture_info[tex]
                #for each texture set if its rarity is above 0 add it into possible list
                if rarity > 0.0:
                    rarity_List_Of_i.append(float(rarity))
                    number_List_Of_i.append(tex)
            break

    #Choose texture
    max_attempts = 10
    if number_List_Of_i:
        if len(number_List_Of_i) == 1:
            print("There's only one texture set")
            textureChosen = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)
        else:
            for i in range(max_attempts):
                textureChosen = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)
                index = str(list(texture_info.keys()).index(textureChosen[0]))
                if index != old_texture_index:
                    break
        return textureChosen[0], list(texture_info.keys()).index(textureChosen[0])
    elif texture_info:
        return list(texture_info.keys())[0], 0
    else: # set has none
        return None, 0


# Chooses a random mesh to use for slot based on rarity ratings
def GetRandomSingleMesh(att_name):
    pointer_name = "input" + att_name[3:]
    last_variant = bpy.context.scene.my_tool[pointer_name].name if bpy.context.scene.my_tool[pointer_name] else ''
    index = bpy.context.scene.my_tool.CurrentBatchIndex
    batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(index), "_NFTRecord_{:03d}.json".format(index))

    DataDictionary = json.load(open(NFTRecord_save_path))
    hierarchy = DataDictionary["hierarchy"]
    type_number_List_Of_i = []
    type_rarity_List_Of_i = []

    for type in hierarchy[att_name].keys():
        if hierarchy[att_name][type].keys():
            first_variant = list(hierarchy[att_name][type].keys())[0]
            type_rarity = hierarchy[att_name][type][first_variant]["type_rarity"]
            if type_rarity and not type.endswith('Null'):
                type_number_List_Of_i.append(type)
                type_rarity_List_Of_i.append(int(type_rarity))

    if type_number_List_Of_i:
        typeChosen = random.choices(type_number_List_Of_i, weights=type_rarity_List_Of_i, k=1)
        type = typeChosen[0]
        type_index = list(hierarchy[att_name].keys()).index(type)
    elif not pointer_name == 'inputAccessories':
        return "0-0-0"

    number_List_Of_i = []
    rarity_List_Of_i = []
    max_attempts = 10

    if pointer_name == 'inputAccessories':
        for type in hierarchy[att_name].keys():
            if hierarchy[att_name][type].keys() and not type.endswith('Null'):
                for variant in hierarchy[att_name][type]:
                    rarity = hierarchy[att_name][type][variant]["variant_rarity"]
                    if rarity:
                        rarity_List_Of_i.append(float(rarity))
                        number_List_Of_i.append(type + '_' + variant)

        if number_List_Of_i:
            for i in range(max_attempts):
                chosen = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)
                typeChosen, dash, variantChosen = chosen[0].partition('_')
                if variantChosen != last_variant:
                    break
            type_index = list(hierarchy[att_name].keys()).index(typeChosen)
            variant_index = list(hierarchy[att_name][typeChosen].keys()).index(variantChosen)
        else:
            return "0-0-0"

    else:
        for variant in hierarchy[att_name][type]:
            rarity = hierarchy[att_name][type][variant]["variant_rarity"]
            if rarity:
                rarity_List_Of_i.append(float(rarity))
                number_List_Of_i.append(variant)

        if number_List_Of_i:
            for i in range(max_attempts):
                variantChosen = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)[0]
                if variantChosen != last_variant:
                    break
            variant_index = list(hierarchy[att_name][type].keys()).index(variantChosen)
        else:
            return "0-0-0"

    texture, texture_index = GetRandomSingleTexture(att_name, bpy.data.collections[variantChosen])
    dna_strand = '-'.join([str(type_index), str(variant_index), str(texture_index)])
    return dna_strand



# ------------------------------------------------------
#Chooses a random head accessory based on what the current haor style supports and rarity rating

def PickWeightedAccessoryTypeAndVariant(AttributeTypes, hair_coll=''):
    number_List_Of_i = []
    rarity_List_Of_i = []

    null_var_rarity = bpy.data.collections["Accessories_AccessoriesNull_000_Null"]['rarity']
    number_List_Of_i.append("00-AccessoriesNull_Accessories_AccessoriesNull_000_Null")
    rarity_List_Of_i.append(null_var_rarity)

    for type in AttributeTypes:
        if AttributeTypes[type].keys():
            for variant in AttributeTypes[type].keys():
                variant_name = variant.rpartition('_')[2]

                for obj in hair_coll.objects:
                    if obj.type == 'MESH':
                        if hasattr(obj.data, "shape_keys") and obj.data.shape_keys != None:
                            for shape_key in obj.data.shape_keys.key_blocks:
                                if shape_key.name.lower() == variant_name.lower():
                                    number_List_Of_i.append(type + '_' + variant)
                                    rarity = bpy.data.collections[variant]['rarity'] # this doesn't take type into consideration atm
                                    rarity_List_Of_i.append(rarity)

    chosen = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)
    typeChosen, dash, variantChosen = chosen[0].partition('_')
    typeIndex = list(AttributeTypes.keys()).index(typeChosen)
    variantIndex = list(AttributeTypes[typeChosen].keys()).index(variantChosen)

    return typeChosen, typeIndex, variantChosen, variantIndex


def PickWeightedAttributeType(AttributeTypes):
    number_List_Of_i = []
    rarity_List_Of_i = []

    for attributetype in AttributeTypes:
        if AttributeTypes[attributetype].keys(): # BETA_1.0
            first_variant = list(AttributeTypes[attributetype].keys())[0]
            if list(AttributeTypes[attributetype][first_variant].keys()): # BETA_1.0
                rarity = float(AttributeTypes[attributetype][first_variant]["type_rarity"])
                if rarity > 0.0:
                    number_List_Of_i.append(attributetype)
                    rarity_List_Of_i.append(float(rarity))

    if len(number_List_Of_i) > 0:
        typeChoosen = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)          
        return typeChoosen[0], list(AttributeTypes.keys()).index(typeChoosen[0])
    else:
        first_attribute = list(AttributeTypes.keys())[0]
        print("no type attributes had rarity > 0, so chose first type attribute: {}".format(first_attribute))
        return first_attribute, 0



def PickWeightedTypeVarient(Varients):
    number_List_Of_i = []
    rarity_List_Of_i = []

    for varient in Varients:
        rarity = float(Varients[varient]["variant_rarity"])
        if rarity > 0.0:
            number_List_Of_i.append(varient)
            rarity_List_Of_i.append(float(rarity))

    if len(number_List_Of_i) > 0:
        variantChoosen = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)  
        return variantChoosen[0], list(Varients.keys()).index(variantChoosen[0])
    else:
        first_variant = list(Varients.keys())[0]
        print("no variant attributes had rarity > 0, so chose first variant attribute: {}".format(first_variant))
        return first_variant, 0



def PickWeightedTextureVarient(VariantInfo):
    number_List_Of_i = []
    rarity_List_Of_i = []

    for texture in VariantInfo['textureSets'].keys():
        rarity = float(VariantInfo['textureSets'][texture])
        if rarity > 0.0:
            number_List_Of_i.append(texture)
            rarity_List_Of_i.append(float(rarity))

    if len(number_List_Of_i) > 0:
        textureChoosen = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)
        return textureChoosen[0], list(VariantInfo['textureSets'].keys()).index(textureChoosen[0])
    else:
        if len(VariantInfo["textureSets"].keys()) > 0:
            first_texture = list(VariantInfo["textureSets"].keys())[0]
            print("no texture attributes had rarity > 0, so chose first texture attribute: {}".format(first_texture))
            return first_texture, 0
        else:
            print("no texture attributes, so chose None")
            return None, 0

 
def PickCharacter():
    if bpy.context.scene.my_tool.isCharacterLocked:
        inputDNA = bpy.context.scene.my_tool.inputDNA
        DNASplit = inputDNA.split(',')
        char = DNASplit[0]
    else:
        char = random.choice(config.Characters)
    return char


def PickElement():
    if not bpy.context.scene.my_tool.isElementStyleLocked:
        regular_prob = bpy.context.scene.my_tool.NonElementalProbability
        full_prob = bpy.context.scene.my_tool.FullElementalProbability
        outfit_prob = bpy.context.scene.my_tool.OutfitElementalProbability

        rand_elements = []
        weights_elements = []

        if regular_prob:
            rand_elements.append("None")
            weights_elements.append(regular_prob)
        if full_prob:
            rand_elements.append("All")
            weights_elements.append(full_prob)
        if full_prob:
            rand_elements.append("Outfit")
            weights_elements.append(outfit_prob)

        if not rand_elements:
            rand_elements.append("None")
            weights_elements.append(100)
        chosen_style = random.choices(rand_elements, weights=weights_elements, k=1)[0]
    else:
        chosen_style = bpy.context.scene.my_tool.elementStyle

    if chosen_style == 'None':
        return 'None-None'
    
    if not bpy.context.scene.my_tool.isElementLocked:
        rand_options = []
        weights_options = []
        for e in config.Elements:
            rand_options.append(e)
            weights_options.append(1)
        chosen_element = random.choices(rand_options, weights=weights_options, k=1)[0]
    else:
        chosen_element = bpy.context.scene.my_tool.element

    return chosen_style + '-' + chosen_element


if __name__ == '__main__':
    RandomizeFullCharacter()