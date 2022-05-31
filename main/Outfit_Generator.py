# Purpose:
# This file generates the Outfit DNA based on a rule set

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

from . import ColorGen
importlib.reload(ColorGen)

from . import config


# A list for each caterogry of clothing that states what slots it will fil
ItemUsedBodySlot = {
"ShirtCropSleeveless" : ["01-UpperTorso"],
"ShirtCropSleevelessNeck" : ["01-UpperTorso", "13-Neck"],
"ShirtCrop" : ["01-UpperTorso", "03-LForeArm", "05-RForeArm"],
"ShirtCropNeck" : ["01-UpperTorso", "03-LForeArm", "05-RForeArm", "13-Neck",  "18-Backpack"],
"ShirtMidSleeveless" : ["01-UpperTorso", "02-MiddleTorso"],
"ShirtMidSleevelessNeck" : ["01-UpperTorso", "02-MiddleTorso", "13-Neck"],
"ShirtMid" : ["01-UpperTorso", "02-MiddleTorso", "03-LForeArm", "05-RForeArm"],
"ShirtMidNeck" : ["01-UpperTorso", "02-MiddleTorso", "03-LForeArm", "05-RForeArm", "13-Neck", "18-Backpack"],
"ShirtLongSleeveless" : ["01-UpperTorso", "02-MiddleTorso", "08-PelvisThick"],
"ShirtLongSleevelessNeck" : ["01-UpperTorso", "02-MiddleTorso", "08-PelvisThick","13-Neck"],
"ShirtLong" : ["01-UpperTorso", "02-MiddleTorso", "08-PelvisThick", "03-LForeArm", "05-RForeArm"],
"ShirtLongNeck" : ["01-UpperTorso", "02-MiddleTorso", "08-PelvisThick", "03-LForeArm", "05-RForeArm","13-Neck", "18-Backpack"],
"ShirtMidHead": ["01-UpperTorso", "02-MiddleTorso", "08-PelvisThick", "03-LForeArm", "05-RForeArm","13-Neck", "17-UpperHead"],
"PantsShort" : ["09-PelvisThin"],
"PantsShortThick" : ["08-PelvisThick", "09-PelvisThin"],
"PantsShortHigh" : ["08-PelvisThick", "09-PelvisThin", "02-MiddleTorso"],
"PantsMid" : ["09-PelvisThin", "10-Calf"],
"PantsMidThick" : ["08-PelvisThick", "09-PelvisThin", "10-Calf"],
"PantsMidHigh" : ["08-PelvisThick", "09-PelvisThin", "10-Calf", "02-MiddleTorso"],
"PantsLong" : ["09-PelvisThin", "10-Calf", "11-Ankle"],
"PantsLongThick" : ["08-PelvisThick", "09-PelvisThin", "10-Calf", "11-Ankle"],
"PantsLongHigh" : ["08-PelvisThick", "09-PelvisThin", "10-Calf", "11-Ankle", "02-MiddleTorso"],
"OutfitLong" : ["01-UpperTorso", "02-MiddleTorso", "08-PelvisThick", "09-PelvisThin", "03-LForeArm", "05-RForeArm", "13-Neck", "18-Backpack", "10-Calf", "11-Ankle"],
"OutfitLongSleeveless" : ["01-UpperTorso", "02-MiddleTorso", "08-PelvisThick", "09-PelvisThin", "13-Neck", "18-Backpack", "10-Calf", "11-Ankle"],
"OutfitMid" : ["01-UpperTorso", "02-MiddleTorso", "08-PelvisThick", "09-PelvisThin", "03-LForeArm", "05-RForeArm", "13-Neck", "18-Backpack", "10-Calf"],
"OutfitMidSleeveless" : ["01-UpperTorso", "02-MiddleTorso", "08-PelvisThick", "09-PelvisThin", "13-Neck", "18-Backpack", "10-Calf"],
"OutfitShort" : ["01-UpperTorso", "02-MiddleTorso", "08-PelvisThick", "09-PelvisThin", "03-LForeArm", "05-RForeArm", "13-Neck", "18-Backpack"],
"OutfitShortSleeveless" : ["01-UpperTorso", "02-MiddleTorso", "08-PelvisThick", "09-PelvisThin", "13-Neck", "18-Backpack"],
"Forearm" : ["03-LForeArm", "05-RForeArm"],
"HandsShort" : ["07-Hands"],
"HandsLong" : ["05-RForeArm", "03-LForeArm", "07-Hands"],
"FeetLong" : ["10-Calf", "11-Ankle", "12-Feet"],
"FeetMid" : ["11-Ankle", "12-Feet"],
"FeetShort" : ["12-Feet"],
"Calf" : ["10-Calf"],
"Neck" : ["13-Neck"],
"HeadUpper" : ["17-UpperHead"],
"HeadUpperMid" : ["17-UpperHead", "13-Neck", "16-Earings"],
"HeadUpperLong" : ["17-UpperHead", "13-Neck", "18-Backpack", "16-Earings"],
"HeadMiddle" : ["15-MiddleHead"],
"HeadLower" : ["14-LowerHead"],
"FaceFull" : ["15-MiddleHead", "14-LowerHead"],
"HeadFull" : ["15-MiddleHead", "14-LowerHead", "13-Neck", "17-UpperHead", "16-Earings"],
"EaringShort" : ["16-Earings"], 
"EaringLong" : ["16-Earings", "13-Neck"], 
"Backpack" : ["18-Backpack"],
"BackpackHigh" : ["18-Backpack"],
"ThinPantsSlots" : ["09-PelvisThin", "10-Calf", "11-Ankle"],
"CoatSlots" : ["01-UpperTorso", "02-MiddleTorso", "08-PelvisThick", "03-LForeArm", "05-RForeArm", "13-Neck"],
"LongCoatsSlot" : ["01-UpperTorso", "02-MiddleTorso", "03-LForeArm", "05-RForeArm", "08-PelvisThick", "13-Neck"],
"VestHoodiesSlot" : ["01-UpperTorso", "02-MiddleTorso", "13-Neck", "18-Backpack"],
"CropShirtsSlot" : ["01-UpperTorso"],
"TShirtsSlot" : ["01-UpperTorso", "02-MiddleTorso"],
"LongShirtSlots" : ["01-UpperTorso", "02-MiddleTorso", "03-LForeArm", "05-RForeArm"],
"LSleaveSlots" : ["03-LForeArm", "04-LWrist", "07-Hands"],
"RSleaveSlots" : ["05-RForeArm", "06-RWrist", "07-Hands"],
"ThickPantsSlots" : ["08-PelvisThick", "09-PelvisThin", "10-Calf", "11-Ankle"],
"ThinPantsSlots" : ["09-PelvisThin", "10-Calf", "11-Ankle"],
"ShoesHighSlots" : ["10-Calf", "11-Ankle", "12-Feet"],
"ShoesMiddleSlots" : ["11-Ankle", "12-Feet"],
"ThickQuarterPantsSlot" : ["08-PelvisThick", "09-PelvisThin", "10-Calf"],
"ThinQuarterPantsSlot" : ["09-PelvisThin", "10-Calf"],
"ThickShortsSlot" : ["08-PelvisThick", "09-PelvisThin"],
"ThinShortsSlot" : ["09-PelvisThin"],
"NeckWearSlots" : ["13-Neck"],
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
        ColorGen.SetUpCharacterStyle()

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
                typeChoosen, typeIndex = PickWeightedAttributeType(hierarchy[attribute])
                varientChoosen, varientIndex = PickWeightedTypeVarient(hierarchy[attribute][typeChoosen])
                textureChoosen, textureIndex = PickWeightedTextureVarient(hierarchy[attribute][typeChoosen][varientChoosen])

                char_variants = bpy.data.collections.get(varientChoosen).children
                if char_variants:
                    for char_coll in char_variants:
                        char_name = char_coll.name.split('_')[-1]
                        if char_name == character:
                            chidlrenObjs = char_coll.objects
                else:
                    chidlrenObjs = bpy.data.collections.get(varientChoosen).objects # CHECK THIS
                    #for obj in chidlrenObjs:

                armature_name = "armature_" + str(character).lower()
                if bpy.data.objects.get(armature_name) is not None:
                    for obj in chidlrenObjs:
                        if obj.modifiers:
                            for mod in obj.modifiers:
                                if mod.type == 'ARMATURE':
                                    mod.object = bpy.data.objects[armature_name]
                        else:
                            mod = obj.modifiers.new(name='armature', type='ARMATURE')
                            mod.object = bpy.data.objects[armature_name]
                # else:
                    # print("Armature '{}' does not exist atm".format(armature_name)) # CHECK THIS
            

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
            textureIndex = 0
            if(len(bpy.data.collections.get(varientChoosen).objects) > 0):
                textureIndex = random.randrange(0, len(bpy.data.collections.get(varientChoosen).objects))
                textureVarient = bpy.data.collections.get(varientChoosen).objects[textureIndex]
                for child in chidlrenObjs:
                    child.material_slots[0].material = textureVarient.material_slots[0].material #Check this - update to loop through all material slots
            ColorGen.PickOutfitColors(attribute)
            SingleDNA[list(hierarchy.keys()).index(attribute)] = "-".join([str(typeIndex), str(varientIndex), str(textureIndex)])

            # SingleDNA[list(hierarchy.keys()).index(attribute)] = str(typeIndex) + "-" + str(varientIndex) + "-" + str(ColorGen.styleChoice) + "-" + str(ColorID[0]) + "-" + str(ColorID[1]) + "-" + str(ColorID[2])
            #SingleDNA[list(hierarchy.keys()).index(attribute)] = str(typeIndex) + "-" + str(varientIndex)
            VarientDict = {}
            current_entry = {}
            # current_entry = hierarchy[attribute][typeChoosen][varientChoosen]
            variant_name = varientChoosen.split('_')[-1]
            if variant_name in ["Null", 'Nulll']:
                VarientDict = 'Null'
            else:
                current_entry["item_attribute"] = attribute
                current_entry["item_type"] = typeChoosen
                current_entry["item_variant"] = variant_name
                current_entry["item_texture"] = textureChoosen
                current_entry["item_index"] = hierarchy[attribute][typeChoosen][varientChoosen]["item_index"]
                current_entry["texture_index"] = textureIndex
                current_entry["type_rarity"] = hierarchy[attribute][typeChoosen][varientChoosen]["type_rarity"]
                current_entry["variant_rarity"] = hierarchy[attribute][typeChoosen][varientChoosen]["variant_rarity"]
                if hierarchy[attribute][typeChoosen][varientChoosen]["textureSets"]:
                    texture_rarity = hierarchy[attribute][typeChoosen][varientChoosen]["textureSets"][textureChoosen]
                else:
                    texture_rarity = 0
                current_entry["texture_rarity"] = texture_rarity
                current_entry["color_style"] = ColorGen.styleKey
                current_entry["color_key"] = ColorGen.colorkey
                VarientDict[varientChoosen] = current_entry
            ItemsUsed[attribute] = VarientDict
            
                
        SingleDNA.insert(0, character)
        SingleDNA.insert(1, ColorGen.styleKey) # TODO add color style to dict too
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

    return list(DNASet), NFTDict
    




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



def PickWeightedTextureVarient(Textures):
    number_List_Of_i = []
    rarity_List_Of_i = []

    for texture in Textures['textureSets'].keys():
        rarity = float(Textures['textureSets'][texture])
        if rarity > 0.0:
            number_List_Of_i.append(texture)
            rarity_List_Of_i.append(float(rarity))

    if len(number_List_Of_i) > 0:
        textureChoosen = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)  
        return textureChoosen[0], list(Textures['textureSets'].keys()).index(textureChoosen[0])
    else:
        # first_texture = list(Textures['textureSets'].keys())[0] # TODO CHECK IF ANY TEXTURES EXIST?
        first_texture = None
        print("no texture attributes had rarity > 0, so chose first texture attribute: {}".format(first_texture))
        return first_texture, 0




 
def PickCharacter(default_char=''):
    if default_char == '':
        if bpy.context.scene.my_tool.isCharacterLocked:
            inputDNA = bpy.context.scene.my_tool.inputDNA
            DNASplit = inputDNA.split(',')
            char = DNASplit[0]
        else:
            char = random.choice(config.Characters)
    else:
        char = default_char
    return char





#ColorStyle-1-1-textureSet-ColorR-COlorG-ColorB

if __name__ == '__main__':
    RandomizeFullCharacter()