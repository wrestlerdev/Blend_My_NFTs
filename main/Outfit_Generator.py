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

"Background" : ["22-Background"]
}



#Color dict which uses a letter to definae style. 0 element is main color, all other elements are complemntary colors
# cols = {
#     "a" : [(0.00000, 0.04706, 0.03529), (0.64706, 0.41569, 0.21176), (0.84706, 0.81176, 0.78039), (0.84706, 0.65490, 0.58431), (0.54902,0.00784,0.00784)],
#     "b" : [(0.62745,0.76471,0.84706), (0.13333,0.35686,0.44706), (0.19608,0.24706,0.00392), (0.84706,0.46667,0.38039), (0.74902,0.26667,0.26667)],
#     "c" : [(0.31373,0.70588,0.74902), (0.84706,0.63922,0.01569), (0.74902,0.49020,0.01176), (0.74902,0.35686,0.01176), (0.64706,0.48235,0.33725)]
# }
cols = {
    "a" : [(0.0194444444444444,0.22,0.96),(0.569444444444444,0.16,0.96),(0.633333333333333,0.7,0.34),(0,0,0.68),(0,0,1),(0.611111111111111,0.38,0.03),(0.991666666666667,0.85,0.85),(0.111111111111111,0.13,0.99)],
    "b" : [(0.997222222222222,0.68,0.82),(0.569444444444444,0.16,0.96),(0.633333333333333,0.7,0.34),(0,0,0.68),(0,0,1),(0.611111111111111,0.43,0.03),(0.0194444444444444,0.27,0.98),(0.111111111111111,0.13,0.98)],
    "c" : [(0.0388888888888889,0.83,0.95),(0.402777777777778,0.81,0.35),(0.569444444444444,0.16,0.96),(0.633333333333333,0.7,0.34),(0,0,1),(0.611111111111111,0.43,0.03),(0.111111111111111,0.13,0.99),(0.0277777777777778,0.44,0.31)],
    "d" : [(0.119444444444444,0.1,0.96),(0.633333333333333,0.7,0.34),(0.933333333333333,0.56,0.38),(0.0222222222222222,0.45,0.31),(0,0,1),(0.611111111111111,0.38,0.03),(0.136111111111111,0.81,0.99),(0.0388888888888889,0.83,0.95)],
    "e" : [(0.130555555555556,0.69,0.98),(0.402777777777778,0.81,0.35),(0.633333333333333,0.7,0.34),(0,0,1),(0.611111111111111,0.38,0.03),(0.111111111111111,0.13,0.99)],
    "f" : [(0.433333333333333,0.99,0.47),(0.0388888888888889,0.83,0.95),(0.933333333333333,0.56,0.38),(0,0,1),(0.611111111111111,0.38,0.03),(0.136111111111111,0.81,0.99),(0.569444444444444,0.16,0.96)],
    "g" : [(0.563888888888889,0.15,0.93),(0.0194444444444444,0.27,0.98),(0.991666666666667,0.85,0.85),(0.0388888888888889,0.83,0.95),(0,0,1),(0.611111111111111,0.38,0.03),(0.633333333333333,0.7,0.34),(0.933333333333333,0.56,0.38)],
    "h" : [(0.580555555555556,0.76,0.45),(0.0194444444444444,0.27,0.98),(0.991666666666667,0.85,0.85),(0.136111111111111,0.81,0.99),(0,0,0.68),(0,0,1),(0.611111111111111,0.38,0.03),(0.569444444444444,0.16,0.96),(0.933333333333333,0.56,0.38)],
    "i" : [(0.925,0.39,0.45),(0.0388888888888889,0.83,0.95),(0,0,0.68),(0.433333333333333,0.99,0.47),(0,0,1),(0.611111111111111,0.38,0.03),(0.569444444444444,0.16,0.96),(0.633333333333333,0.7,0.34)],
    "j" : [(0.025,0.28,0.39),(0.111111111111111,0.13,0.99),(0,0,1),(0.611111111111111,0.38,0.03),(0.0388888888888889,0.83,0.95)],
    "k" : [(0.588888888888889,0.08,0.74),(0.0194444444444444,0.27,0.98),(0.991666666666667,0.85,0.85),(0.633333333333333,0.7,0.34),(0.933333333333333,0.56,0.38),(0,0,1),(0.611111111111111,0.38,0.03)],
    "l" : [(0,0,1), (0,0,1), (0.611111111111111,0.38,0.03), (0.611111111111111,0.38,0.03)],

}

haircols = [(0.66667,0.53333,0.40000), (0.87059,0.74510,0.60000), (0.14118,0.10980,0.06667), (0.30980,0.10196,0.00000), (0.60392,0.20000,0.00000) ]
skincols = [(0.310, 0.102, 0.000), (0.21403, 0.129142,0.019756), (0.227,0.062,0.0000), (0.841,0.431,0.195) ]

# A dictionary which can be called to find what slots to fill when using certian items


def setBodySlotsValue(ItemClothingGenre, ValueToSet):
    #loop through all slots that selected item will take up
    UsedUpSlotArray = ItemUsedBodySlot.get(ItemClothingGenre)
    if UsedUpSlotArray:
        for i in ItemUsedBodySlot.get(ItemClothingGenre):
            SlotUpdateValue = {i : True}
            #BodySlotsDict.update(SlotUpdateValue)   


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
        # bpy.ops.outliner.orphans_purge()
        # coll = bpy.data.collections.get("NFTHolder")
        # # if it doesn't exist create it
        # if coll is None:
        #     coll = bpy.data.collections.new("NFTHolder")
        #     bpy.data.collections["Script_Ignore"].children.link(coll)

        # for child in bpy.data.collections["NFTHolder"].children:
        #     for obj in child.objects:
        #         bpy.data.objects.remove(obj, do_unlink=True)
        #     bpy.data.collections.remove(child)

            

        SingleDNA = ["0"] * len(list(hierarchy.keys()))
        ItemsUsed = {}

        attributeskeys = list(hierarchy.keys())
        attributevalues = list(hierarchy.values())
        attributeUsedDict = dict.fromkeys(attributeskeys, False)

        character = PickCharacter()
        element = PickElement()
        style = ColorGen.SetUpCharacterStyle()
        bpy.context.scene.my_tool.currentGeneratorStyle = style

        # letterstyles = 'abcdefghijkl'
        # styleChoice = random.choice(letterstyles)
        # style = copy.deepcopy( cols[random.choice(styleChoice)] )
        # maincolor = (0.0, 0.0, 0.0)
        # secondarycolor = (0.0, 0.0, 0.0)
        # mainColorIndex = -1
        # SecondaryColorIndex = -1
        # if( random.random() > .05 ):
        #     mainColorIndex = 0
        #     maincolor = style.pop(mainColorIndex)
        #     SecondaryColorIndex = random.randrange(0, len(style))
        #     secondarycolor = style.pop(SecondaryColorIndex)
        # else:
        #     SecondaryColorIndex = 0
        #     secondarycolor = style.pop(SecondaryColorIndex)
        #     mainColorIndex = random.randrange(0, len(style))
        #     maincolor = style.pop(mainColorIndex)

        
        # for child in bpy.data.collections.get("Kae").objects:
        #     obj = bpy.data.objects[child.name]
        #     obj["TestColor"] = skincols[random.randrange(len(skincols))]
        #     obj["metallic"] = random.random()
        #     obj.hide_viewport = False
        
        hair_coll_name = ''
        for attribute in attributeskeys:
            if(attributeUsedDict.get(attribute)):
                SingleDNA[list(hierarchy.keys()).index(attribute)] = "0-0-0"
                
                typeChoosen = list(hierarchy[attribute])[0]
                typeIndex = 0
                varientChoosen = list(hierarchy[attribute][typeChoosen].keys())[0]
                varientIndex = 0
                if len(list(hierarchy[attribute][typeChoosen][varientChoosen]['textureSets'].keys())) > 0:
                    textureChoosen = list(hierarchy[attribute][typeChoosen][varientChoosen].keys())[0]
                else:
                    textureChoosen = None
                textureIndex = 0
            else:
                position = attributevalues.index(hierarchy[attribute])
                if attribute[3:].startswith("Accessories"): # for hair accessories
                    hair_collection = bpy.data.collections[hair_coll_name + '_' + character]
                    typeChoosen, typeIndex, varientChoosen, varientIndex = PickWeightedAccessoryTypeAndVariant(hierarchy[attribute], hair_collection)
                else:
                    typeChoosen, typeIndex = PickWeightedAttributeType(hierarchy[attribute])
                    varientChoosen, varientIndex = PickWeightedTypeVarient(hierarchy[attribute][typeChoosen])
                textureChoosen, textureIndex = PickWeightedTextureVarient(hierarchy[attribute][typeChoosen][varientChoosen])
                if attribute[3:].startswith('Hair') and not varientChoosen.endswith("Null"):
                    hair_coll_name = varientChoosen

                if typeIndex == 0 and varientIndex == 0:
                    SingleDNA[list(hierarchy.keys()).index(attribute)] = "0-0-0"
                else:
                    char_variants = bpy.data.collections.get(varientChoosen).children
                    if char_variants:
                        for char_coll in char_variants:
                            char_name = char_coll.name.split('_')[-1]
                            if char_name == character:
                                chidlrenObjs = char_coll.objects
                    else:
                        chidlrenObjs = bpy.data.collections.get(varientChoosen).objects # CHECK THIS
                        #for obj in chidlrenObjs:

                    ItemClothingGenre = hierarchy[attribute][typeChoosen][varientChoosen]["item_type"][3:]
                    #loop through all slots that selected item will take up
                    if ItemClothingGenre in ItemUsedBodySlot:
                        UsedUpSlotArray = ItemUsedBodySlot.get(ItemClothingGenre)
                    else: 
                        UsedUpSlotArray = []

                    if UsedUpSlotArray:
                        for i in ItemUsedBodySlot.get(ItemClothingGenre):
                            SlotUpdateValue = {i : True}
                            attributeUsedDict.update(SlotUpdateValue)


            if not (typeIndex == 0 and varientIndex == 0):
                if typeChoosen[3:] in config.EmptyTypes:
                    color_key = 'Empty'
                else:
                    color_key, color_choice = ColorGen.PickOutfitColors(attribute)
                SingleDNA[list(hierarchy.keys()).index(attribute)] = "-".join([str(typeIndex), str(varientIndex), str(textureIndex), str(color_key)])

            VarientDict = {}
            current_entry = {}
            variant_name = varientChoosen.split('_')[-1]
            if variant_name in ["Null", 'Nulll']:
                VarientDict = 'Null'
            else:
                current_entry["item_attribute"] = attribute
                current_entry["item_type"] = typeChoosen
                current_entry["item_variant"] = variant_name
                current_entry["item_texture"] = textureChoosen
                current_entry["item_index"] = hierarchy[attribute][typeChoosen][varientChoosen]["item_index"]
                current_entry["type_rarity"] = hierarchy[attribute][typeChoosen][varientChoosen]["type_rarity"]
                current_entry["variant_rarity"] = hierarchy[attribute][typeChoosen][varientChoosen]["variant_rarity"]
                if hierarchy[attribute][typeChoosen][varientChoosen]["textureSets"]:
                    texture_rarity = hierarchy[attribute][typeChoosen][varientChoosen]["textureSets"][textureChoosen]
                else:
                    texture_rarity = 0
                current_entry["texture_rarity"] = texture_rarity
                current_entry["color_key"] = color_key
                VarientDict[varientChoosen] = current_entry
            ItemsUsed[attribute] = VarientDict
            
                
        SingleDNA.insert(0, character)
        SingleDNA.insert(1, element)
        SingleDNA.insert(2, style)
        # SingleDNA.insert(1, ColorGen.styleKey)
        formattedDNA = ','.join(SingleDNA)
        if formattedDNA not in DNASet and formattedDNA not in exsistingDNASet:
            print("ADDING DNA TO SET")
            DNASet.add(formattedDNA)
            NFTDict[formattedDNA] = ItemsUsed
            numberToGen -= 1
        else:
            print("ALL READY IN SET")
            currentFailedAttempts += 1
            if currentFailedAttempts > allowFailedAttempts:
                break


    for m in bpy.data.materials: # purge all unused materials for now
        if m.users == 0 and m.name != 'MasterV01':
            bpy.data.materials.remove(m)

    print(DNASet)

    return list(DNASet), NFTDict
    


# ------------------------------------------------------


def GetRandomSingleTexture(att_name, variant_coll):
    index = bpy.context.scene.my_tool.CurrentBatchIndex
    batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(index), "_NFTRecord_{:03d}.json".format(index))

    DataDictionary = json.load(open(NFTRecord_save_path))
    hierarchy = DataDictionary["hierarchy"]

    number_List_Of_i = []
    rarity_List_Of_i = []

    att_index = list(hierarchy.keys()).index(att_name)
    inputDNA = bpy.context.scene.my_tool.inputDNA
    dna_split = inputDNA.split(',')
    old_dna_strand = dna_split[att_index + 2] # .pop(0)
    old_texture_index = old_dna_strand.split('-')[2]

    variant = variant_coll.name
    for type in hierarchy[att_name].keys():
        if variant in hierarchy[att_name][type].keys():
            item_info = hierarchy[att_name][type][variant]
            texture_info = item_info["textureSets"]
            for tex in texture_info.keys():
                rarity = texture_info[tex]
                if rarity > 0.0:
                    rarity_List_Of_i.append(float(rarity))
                    number_List_Of_i.append(tex)
            break

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
        # null_type = list(hierarchy[att_name].keys())[0]
        # null_variant = list(hierarchy[att_name][null_type].keys())[0]
        # print(null_variant)
        return "0-0-0"

    number_List_Of_i = []
    rarity_List_Of_i = []
    max_attempts = 10

    if pointer_name == 'inputAccessories':
        for type in hierarchy[att_name].keys():
            if hierarchy[att_name][type].keys() and not type.endswith('Null'):
                for variant in hierarchy[att_name][type]:
                    rarity = hierarchy[att_name][type][variant]["variant_rarity"]
                    print(variant)
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
        # rarity = attributetype.split("_")[1]
        
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
        # print(textureChoosen[0])
        # print(list(VariantInfo['textureSets'].keys()).index(textureChoosen[0]))
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
    # All || Skin || Outfit
    element_rarity = 10
    none_rarity = 100
    # elements = [("None", 100), ("Gold", 10), ("Bismuth", 10)]
    options = [("All", 10), ("Skin", 20), ("Outfit", 20)]

    rand_elements = ["None"]
    weights_elements = [none_rarity]
    for e in config.Elements:
        rand_elements.append(e)
        weights_elements.append(element_rarity)
    chosen = random.choices(rand_elements, weights=weights_elements, k=1)[0]
    if chosen == "None":
        return "None-None"

    rand_options = []
    weights_options = []
    for o in options:
        rand_options.append(o[0])
        weights_options.append(o[1])
    chosen_option = random.choices(rand_options, weights=weights_options, k=1)[0]
    
    return chosen_option + '-' + chosen
# ----------------------------------------------------------------------

count = 0

def count_all_rarities(batch_record_path, index):
    global count
    print("(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")
    json_name = os.path.join(batch_record_path, '_RarityCounter_{:03d}.json'.format(index))
    DataDictionary = json.load(open(os.path.join(batch_record_path, "_NFTRecord_{:03d}.json".format(index))))
    hierarchy = DataDictionary["hierarchy"]

    time_start = time.time()

    rarity_dict = {}
    for attribute in hierarchy.keys():
        rarity_dict[attribute] = {}
        rarity_dict[attribute]['absolute_rarity'] = 0.0
        for type in hierarchy[attribute].keys():
            rarity_dict[attribute][type] = {}
            rarity_dict[attribute][type]['absolute_rarity'] = 0.0
            rarity_dict[attribute][type]['relative_rarity'] = get_weighted_rarity(type, attribute)[0]
            for variant in hierarchy[attribute][type].keys():
                rarity_dict[attribute][type][variant] = {}
                rarity_dict[attribute][type][variant]['absolute_rarity'] = 0.0
                rarity_dict[attribute][type][variant]['relative_rarity'] = get_weighted_rarity(variant, type)[0]

    count = 0
    filled_slots = '0' * len(hierarchy.keys())
    rarity_dict = add_rarity_recurse(rarity_dict, 1, hierarchy, filled_slots, attribute='01-UpperTorso')

    logged_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    export_dict = {}
    export_dict["Date/Time Calculated"] = logged_time
    export_dict["Rarities"] = rarity_dict

    ledger = json.dumps(export_dict, indent=4, ensure_ascii=True)
    with open(json_name, 'w') as outfile:
        outfile.write(ledger + '\n')
    
    print(f"{config.bcolors.OK}Time taken to calculate rarity: {time.time() - time_start} seconds{config.bcolors.RESET}")
    print("Total number of possible combinations? {}".format(count))
    return


max_att = 20 # inclusive?

def add_rarity_recurse(rarity_dict, current_probability, hierarchy, filled_slots, attribute='', type='', branch_count=1):
    global count
    if attribute and filled_slots[int(attribute[:2]) - 1] == '1':
        null_type = bpy.data.collections[attribute].children[0]
        null_variant = null_type.children[0]
        rarity_dict[attribute]["absolute_rarity"] = rarity_dict[attribute]["absolute_rarity"] + current_probability
        rarity_dict[attribute][null_type.name]["absolute_rarity"] = rarity_dict[attribute][null_type.name]["absolute_rarity"] + current_probability 
        rarity_dict[attribute][null_type.name][null_variant.name]["absolute_rarity"] = rarity_dict[attribute][null_type.name][null_variant.name]["absolute_rarity"] + current_probability
        next_index = list(hierarchy.keys()).index(attribute) + 1
        if next_index != max_att:
        # if next_index != len(hierarchy.keys()):
            next_att = list(hierarchy.keys())[next_index]
            rarity_dict = add_rarity_recurse(rarity_dict, current_probability, hierarchy, filled_slots, attribute=next_att, branch_count=branch_count)
        else:
            count += branch_count
        return rarity_dict

    if not type: # this is a attribute
        percentage = 1.0
    else: # this is a type
        percentage = get_weighted_rarity(type, attribute)[0]

    new_probability = current_probability * percentage

    if new_probability == 0.0: # if 0 then it shouldn't need to go down branch?
        return rarity_dict
    
    if type:
        rarity_dict[attribute][type]["absolute_rarity"] = rarity_dict[attribute][type]["absolute_rarity"] + new_probability
        var_count = 0
        var_weight_total = 0
        for variant in rarity_dict[attribute][type].keys():
            if variant != "absolute_rarity" and variant != "relative_rarity":
                variant_percentage, var_weight_total = get_weighted_rarity(variant, type, var_weight_total)
                rarity_dict[attribute][type][variant]["absolute_rarity"] = rarity_dict[attribute][type][variant]["absolute_rarity"] + new_probability * variant_percentage
                if variant_percentage:
                    var_count += 1
        branch_count = branch_count * var_count

    else:
        rarity_dict[attribute]["absolute_rarity"] = rarity_dict[attribute]["absolute_rarity"] + new_probability

    if not type: # this is an attribute
        att_coll = bpy.data.collections[attribute]
        for coll in att_coll.children:
            rarity_dict = add_rarity_recurse(rarity_dict, new_probability, hierarchy, filled_slots, attribute=attribute, type=coll.name, branch_count=branch_count)
    else: # this is a type
        if 'Null' not in type and type[3:] in ItemUsedBodySlot:
            new_slots = ItemUsedBodySlot[type[3:]]
        else:
            new_slots = []

        if new_slots:
            for slot in new_slots:
                index = int(slot[:2]) - 1
                if filled_slots[index] == '0':
                    filled_slots = filled_slots[:index] + '1' + filled_slots[index+1:]

        next_index = (list(hierarchy.keys()).index(attribute)) + 1
        # if next_index != len(hierarchy.keys()):
        if next_index != max_att:
            next_att = list(hierarchy.keys())[next_index]
            rarity_dict = add_rarity_recurse(rarity_dict, new_probability, hierarchy, filled_slots, attribute=next_att, branch_count=branch_count)
        else:
            count += branch_count
    return rarity_dict



def get_weighted_rarity(current_name, parent_name, total = 0):
    # print(current_name)
    if not total:
        for coll in bpy.data.collections[parent_name].children:
            if coll.get('rarity') != None:
                total += coll.get('rarity')

    if total:
        current_coll = bpy.data.collections[current_name]
        if current_coll.get('rarity') != None:
            percentage = current_coll.get('rarity') / total
            return percentage, total
        else:
            return 0.0, total

    else: # CHECK GREEN NULL
        # print(current_coll.name)
        if len(bpy.data.collections[parent_name].children) == 1:
            return 1.0, total
        else: # CHECK THIS
            if 'Null' in current_coll.name:
                return 1.0, total
            else:
                return 0.0, total



if __name__ == '__main__':
    RandomizeFullCharacter()