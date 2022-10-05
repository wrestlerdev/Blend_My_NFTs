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
"ShirtCropTank" : ["01-UT"],
"ShirtCropTankBack" : ["01-UT", "20-BP", "14-N"],
"ShirtCropTankNeck" : ["01-UT", "14-N", "11-HL", "17-EL"],
"ShirtCrop" : ["01-UT", "03-FA"],
"ShirtCropNeck" : ["01-UppreTorso", "03-FA", "14-N", "11-HL", "17-EL"],
"ShirtMidTank" : ["01-UT", "02-MT"],
"ShirtMidTankNeck" : ["01-UT", "02-MT", "14-N", "11-HL", "17-EL"],
"ShirtMidTankBack" : ["01-UT", "02-MT", "14-N", "11-HL", "20-BP", "17-EL"],
"ShirtMid" : ["01-UT", "02-MT", "03-FA"],
"ShirtMidNeck" : ["01-UT", "02-MT", "03-FA", "14-N", "11-HL", "17-EL"],
"ShirtMidBack" : ["01-UT", "02-MT", "03-FA", "14-N", "11-HL", "17-EL", "20-BP"],
"ShirtLongTank" : ["01-UT", "02-MT", "06-PTK"],
"ShirtLongTankNeck" : ["01-UT", "02-MT", "06-PTK","14-N", "11-HL", "17-EL"],
"ShirtLongTankBack" : ["01-UT", "02-MT", "06-PTK","14-N", "11-HL", "20-BP", "17-EL"],
"ShirtLong" : ["01-UT", "02-MT", "06-PTK", "03-FA"],
"ShirtLongNeck" : ["01-UT", "02-MT", "06-PTK", "03-FA","14-N", "11-HL", "17-EL"],
"ShirtLongHead": ["01-UT", "02-MT", "06-PTK", "03-FA","14-N", "11-HL", "12-HS", "18-ES", "17-EL"],
"ShirtLongBack" : ["01-UT", "02-MT", "03-FA", "06-PTK", "14-N", "11-HL", "20-BP", "17-EL"],

"PantsShort" : ["07-PTN"],
"PantsShortThick" : ["06-PTK", "07-PTN"],
"PantsShortHigh" : ["06-PTK", "07-PTN", "02-MT"],
"PantsMid" : ["07-PTN", "08-C"],
"PantsMidThick" : ["06-PTK", "07-PTN", "08-C"],
"PantsMidHigh" : ["06-PTK", "07-PTN", "08-C", "02-MT"],
"PantsLong" : ["07-PTN", "08-C", "09-A"],
"PantsLongThick" : ["06-PTK", "07-PTN", "08-C", "09-A"],
"PantsLongHigh" : ["06-PTK", "07-PTN", "08-C", "09-A", "02-MT"],

"OutfitLong" : ["01-UT", "02-MT", "06-PTK", "07-PTN", "03-FA", "14-N", "08-C", "09-A","17-EL"],
"OutfitLongTank" : ["01-UT", "02-MT", "06-PTK", "07-PTN", "14-N", "08-C", "09-A", "17-EL"],
"OutfitMid" : ["01-UT", "02-MT", "06-PTK", "07-PTN", "03-FA", "14-N", "08-C", "17-EL"],
"OutfitMidTank" : ["01-UT", "02-MT", "06-PTK", "07-PTN", "14-N", "08-C", "17-EL"],
"OutfitShort" : ["01-UT", "02-MT", "06-PTK", "07-PTN", "03-FA", "14-N", "17-EL"],
"OutfitShortTank" : ["01-UT", "02-MT", "06-PTK", "07-PTN", "14-N", "17-EL"],

"Forearm" : ["03-FA"],
"HandShort" : ["05-H", "04-W"],
"GlovesShort" : ["05-H", "04-W"],
"HandLong" : ["03-FA", "05-H", "04-W"],
"GlovesLong" : ["03-FA", "05-H", "04-W"],

"FeetLong" : ["08-C", "09-A", "10-F"],
"FeetMid" : ["09-A", "10-F"],
"FeetShort" : ["10-F"],
"FeetShortNone" : ["10-F"],
"Calf" : ["08-C"],
"CalfLong" : ["08-C", "09-A"],

"Neck" : ["14-N", "17-EL"],
"HairShort" : ["12-HS"],
"HairShortFront" : ["12-HS", "15-MH"],
"HairMid" : ["11-HL", "14-N", "12-HS", "18-ES", "17-EL"],
"HairMidFront" : ["11-HL", "14-N", "12-HS", "15-MH", "18-ES", "17-EL"],
"HairLong" : ["11-HL", "14-N", "12-HS", "18-ES", "20-BP", "17-EL"],

"HeadFull" : ["14-N", "15-MH", "16-LH", "18-ES", "17-EL"],
"HeadExtraEar" : ["17-EL", "18-ES"],
"HeadExtra" : [],

"FaceMid" : ["15-MH"],
"FaceMidNeutral" : ["15-MH", "19-EX"],
"FaceLower" : ["16-LH"],
"FaceFull" : ["15-MH", "16-LH"],
"EarringsShort" : ["18-ES"], 
"EarringsLong" : ["18-ES", "17-EL"],

"Backpack" : ["20-BP"],
"BackpackHigh" : ["14-N", "20-BP"],

"Expression" : ["19-EX"],
"ExpressionLower" : ["16-LH", "19-EX"],
"ExpressionLowerNone" : ["16-LH", "19-EX"],
"ExpressionUpper" : ["15-MH", "19-EX"],
"ExpressionFull" : ["16-LH", "15-MH", "19-EX"],

"Background" : ["22-BG"],

"TattooMiddleTorso": ["02-MT"],
"TattooForearm": ["03-FA"],
"TattooCalf": ["08-C"],
"TattooFeet": ["10-F"],
"TattooNeck": ["14-N"]

}
  

def RandomizeFullCharacter(maxNFTs, save_path):
    index = bpy.context.scene.my_tool.CurrentBatchIndex
    batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(index), "_NFTRecord_{}.json".format(index))

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
                if attribute[3:] == "HA": 
                    hair_collection = bpy.data.collections[hair_coll_name + '_' + character]
                    typeChoosen, typeIndex, varientChoosen, varientIndex = PickWeightedAccessoryTypeAndVariant(hierarchy[attribute], hair_collection)
                else:
                    typeChoosen, typeIndex = PickWeightedAttributeType(hierarchy[attribute])
                    varientChoosen, varientIndex = PickWeightedTypeVarient(hierarchy[attribute][typeChoosen])

                textureChoosen, textureIndex = PickWeightedTextureVarient(hierarchy[attribute][typeChoosen][varientChoosen])

                if (attribute[3:] == 'HS' or attribute[3:] == 'HL') and not varientChoosen.endswith("Null"):
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
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(index), "_NFTRecord_{}.json".format(index))

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
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(index), "_NFTRecord_{}.json".format(index))

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
                type_rarity_List_Of_i.append(float(type_rarity))

    if type_number_List_Of_i:
        typeChosen = random.choices(type_number_List_Of_i, weights=type_rarity_List_Of_i, k=1)
        type = typeChosen[0]
        type_index = list(hierarchy[att_name].keys()).index(type)
    elif not pointer_name == 'inputHA':
        return "0-0-0"

    number_List_Of_i = []
    rarity_List_Of_i = []
    max_attempts = 10

    if pointer_name == 'inputHA':
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

    null_var_rarity = bpy.data.collections["HA_HANull_000_Null"]['rarity']
    number_List_Of_i.append("00-HANull_HA_HANull_000_Null")
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