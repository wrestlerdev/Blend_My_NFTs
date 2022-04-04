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
from mathutils import Color

from . import ColorGen
importlib.reload(ColorGen)


# A list for each caterogry of clothing that states what slots it will fil
CoatSlots = ["01-UpperTorso", "02-MiddleTorso", "08-PelvisThick", "03-LForeArm", "05-RForeArm", "13-Neck"]
LongCoatsSlot = ["01-UpperTorso", "02-MiddleTorso", "03-LForeArm", "05-RForeArm", "08-PelvisThick", "13-Neck"]
VestHoodiesSlot = ["01-UpperTorso", "02-MiddleTorso", "13-Neck", "18-BackPack"]
CropShirtsSlot = ["01-UpperTorso"]
TShirtsSlot = ["01-UpperTorso", "02-MiddleTorso"]
LongShirtSlots = ["01-UpperTorso", "02-MiddleTorso", "03-LForeArm", "05-RForeArm"]
LSleaveSlots = ["03-LForeArm", "04-LWrist", "07-Hands"]
RSleaveSlots = ["05-RForeArm", "06-RWrist", "07-Hands"]
ThickPantsSlots = ["08-PelvisThick", "09-PelvisThin", "10-Calf", "11-Ankle"]
ThinPantsSlots = ["09-PelvisThin", "10-Calf", "11-Ankle"]
ShoesHighSlots = ["10-Calf", "11-Ankle", "12-Feet"]
ShoesMiddleSlots = ["11-Ankle", "12-Feet"]
ThickQuarterPantsSlot = ["08-PelvisThick", "09-PelvisThin", "10-Calf"]
ThinQuarterPantsSlot = ["09-PelvisThin", "10-Calf"]
ThickShortsSlot = ["08-PelvisThick", "09-PelvisThin"]
ThinShortsSlot = ["09-PelvisThin"]
NeckWearSlots = ["13-Neck"]

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
ItemUsedBodySlot = {
    "Coats": CoatSlots, 
    "LongShirts": LongShirtSlots,
    "LongCoats" : LongCoatsSlot,
    "VestHoodie" : VestHoodiesSlot,
    "CropShirts" : CropShirtsSlot,
    "TShirts" : TShirtsSlot,
    "Shorts" : ThinShortsSlot,
    "LSleave": LSleaveSlots,
    "RSleave": RSleaveSlots,  
    "ThickPants": ThickPantsSlots, 
    "ThickQuaterPants": ThickQuarterPantsSlot,
    "ThickShorts" : ThickShortsSlot,
    "ThinPants" : ThinPantsSlots,
    "ThinShorts" : ThinShortsSlot, 
    "ShoesHigh" : ShoesHighSlots, 
    "ShoesMiddle" : ShoesMiddleSlots,
    "NeckWear" : NeckWearSlots
}

def RandomizeSingleDNAStrandColor(inputSlot, slot_coll, CurrentDNA, save_path):
    NFTRecord_save_path = bpy.context.scene.my_tool.NFTRecord_save_path
    DataDictionary = json.load(open(NFTRecord_save_path))

    hierarchy = DataDictionary["hierarchy"]
    attributeskeys = list(hierarchy.keys())
    index = attributeskeys.index(slot_coll)

    DNAString = CurrentDNA.split(",")
    DNASplit = DNAString[index].split('-')

    newDNASplit = [DNASplit[0], DNASplit[1]]

    if not (newDNASplit[0] == 0 and newDNASplit[1] == 0): # if not null
        if len(DNASplit) > 2: # append color style
            newDNASplit.append(DNASplit[2])
        else:
            newDNASplit.append(get_style())


        slot = bpy.context.scene.my_tool[inputSlot]
        col = (random.random(), random.random(), random.random())
        print(slot.name)
        col = (random.random(), random.random(), random.random())

        chidlrenObjs = bpy.data.collections.get(slot.name).objects
        # hexCodes = ColorGen.PickOutfitColors(slot_coll, chidlrenObjs)
        for child in chidlrenObjs:
            obj = bpy.data.objects[child.name]
            obj["TestColor"] = col
            obj["R"] = col
            
            obj.hide_viewport = False
            hex = ColorGen.RGBtoHex((col))


            if len(DNASplit) > 2:
                newDNASplit.extend([hex, DNASplit[4], DNASplit[5]])
            else:
                newDNASplit.extend([hex, hex, hex])

        newDNAStrand = '-'.join(newDNASplit)
        newDNAString = copy.deepcopy(DNAString)
        newDNAString[index] = newDNAStrand
        newDNA = ','.join(newDNAString)
        print(newDNAStrand)
        return newDNA

    return CurrentDNA


def get_style(): # placeholder
    style = 'a'
    return style

def get_rando_color(): # placeholder
    return get_style(), '#FFFFFF', '#FFFFFF', '#FFFFFF'



def RandomizeSingleDNAStrandMesh(inputSlot, CurrentDNA, save_path):
    NFTRecord_save_path = bpy.context.scene.my_tool.NFTRecord_save_path

    DataDictionary = json.load(open(NFTRecord_save_path))
    RarityDictionary = json.load(open(bpy.context.scene.my_tool.Rarity_save_path))

    hierarchy = DataDictionary["hierarchy"]
    DNAList = DataDictionary["DNAList"]

    
    #Build Dict
    attributeskeys = list(hierarchy.keys())
    attributevalues = list(hierarchy.values())
    attributeUsedDict = dict.fromkeys(attributeskeys, False)

    attributes = {}
    indexToEdit = -1
    currentVarient = ''
    DNAString = CurrentDNA.split(",")
    for strand in range(len(DNAString)):
        
        DNASplit = DNAString[strand].split('-')
        atttype_index = DNASplit[0]
        variant_index = DNASplit[1]


        slot = list(hierarchy.items())[strand]

        atttype = list(slot[1].items())[int(atttype_index)]
        variant = list(atttype[1].items())[int(variant_index)][0]


        slotName = list(atttype[1].items())[int(variant_index)][1]["slotName"]
        formatedSlot = str(inputSlot).split("input", 2)[1]
        if(slotName != formatedSlot):
            #loop through all slots that selected item will take up
            ItemClothingGenre = list(atttype[1].items())[int(variant_index)][1]["clothingGenre"]
            UsedUpSlotArray = ItemUsedBodySlot.get(ItemClothingGenre)
            if UsedUpSlotArray:
                for i in ItemUsedBodySlot.get(ItemClothingGenre):
                    SlotUpdateValue = {i : True}
                    attributeUsedDict.update(SlotUpdateValue)
        else:
            attributes = slot
            indexToEdit =  strand
            currentVarient = variant
            if len(DNASplit) > 2:
                last_color = DNASplit[2:] # get last used colour from dna
            else:
                last_color = get_rando_color()

    attempts = 100
    while attempts > 0:
        typeChoosen, typeIndex = PickWeightedAttributeType(attributes[1], RarityDictionary[attributes[0]])
        varientChoosen, varientIndex = PickWeightedTypeVarient(attributes[1][typeChoosen])
        if(varientChoosen != currentVarient):
            willItemFit =  True
            ItemClothingGenre = hierarchy[attributes[0]][typeChoosen][varientChoosen]["clothingGenre"]
            UsedUpSlotArray = ItemUsedBodySlot.get(ItemClothingGenre)
            if UsedUpSlotArray:
                for i in UsedUpSlotArray:
                    if attributeUsedDict.get(i):
                        willItemFit = False
            if(willItemFit):       
                DNAStrand = [str(typeIndex), str(varientIndex)]
                if typeIndex != 0 or varientIndex != 0: # if is not a null block
                    DNAStrand += last_color
                newDNAString = '-'.join(DNAStrand)
                # DNAString[indexToEdit] = str(typeIndex) + '-' + str(varientIndex)
                DNAString[indexToEdit] = newDNAString
                FormattedDNA = ','.join(DNAString)
                bpy.data.collections[currentVarient].hide_viewport = True
                bpy.data.collections[varientChoosen].hide_viewport = False
                return FormattedDNA
        #print(currentVarient)
        attempts -= 1
    return CurrentDNA

def setBodySlotsValue(ItemClothingGenre, ValueToSet):
    #loop through all slots that selected item will take up
    UsedUpSlotArray = ItemUsedBodySlot.get(ItemClothingGenre)
    if UsedUpSlotArray:
        for i in ItemUsedBodySlot.get(ItemClothingGenre):
            SlotUpdateValue = {i : True}
            #BodySlotsDict.update(SlotUpdateValue)   


def RandomizeFullCharacter(maxNFTs, save_path):
    NFTRecord_save_path = bpy.context.scene.my_tool.NFTRecord_save_path
    RarityDictionary = json.load(open(bpy.context.scene.my_tool.Rarity_save_path))

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

        for attribute in hierarchy:
            for type in hierarchy[attribute]:
                for varient in hierarchy[attribute][type]:
                    bpy.data.collections.get(varient).hide_viewport = True

        
        SingleDNA = ["0"] * len(list(hierarchy.keys()))
        ItemsUsed = {}

        attributeskeys = list(hierarchy.keys())
        attributevalues = list(hierarchy.values())
        attributeUsedDict = dict.fromkeys(attributeskeys, False)

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
                SingleDNA[list(hierarchy.keys()).index(attribute)] = "0-0"
                
                typeChoosen = list(hierarchy[attribute])[0]
                ItemsUsed[attribute] = list( hierarchy[attribute][typeChoosen].values())[0]

            else:
                position = attributevalues.index(hierarchy[attribute])
                typeChoosen, typeIndex = PickWeightedAttributeType(hierarchy[attribute], RarityDictionary[attribute])
                varientChoosen, varientIndex = PickWeightedTypeVarient(hierarchy[attribute][typeChoosen])
                # print(typeChoosen + " " +  varientChoosen)
                # print(typeIndex)
                # print(varientIndex)


                bpy.data.collections.get(varientChoosen).hide_viewport = False
                chidlrenObjs = bpy.data.collections.get(varientChoosen).objects

                ColorID = ColorGen.PickOutfitColors(attribute, chidlrenObjs)

                SingleDNA[list(hierarchy.keys()).index(attribute)] = str(typeIndex) + "-" + str(varientIndex) + "-" + str(ColorGen.styleChoice) + "-" + str(ColorID[0]) + "-" + str(ColorID[1]) + "-" + str(ColorID[2])
                #SingleDNA[list(hierarchy.keys()).index(attribute)] = str(typeIndex) + "-" + str(varientIndex)
                VarientDict = {}
                VarientDict[varientChoosen] = hierarchy[attribute][typeChoosen][varientChoosen]
                ItemsUsed[attribute] = VarientDict

                ItemClothingGenre = hierarchy[attribute][typeChoosen][varientChoosen]["clothingGenre"]
                
                #loop through all slots that selected item will take up
                UsedUpSlotArray = ItemUsedBodySlot.get(ItemClothingGenre)
                if UsedUpSlotArray:
                    for i in ItemUsedBodySlot.get(ItemClothingGenre):
                        SlotUpdateValue = {i : True}
                        attributeUsedDict.update(SlotUpdateValue)
           
        formattedDNA = ','.join(SingleDNA)
        if formattedDNA not in DNASet and formattedDNA not in exsistingDNASet:
            print("ADDING DNA TO SET")
            print(formattedDNA)
            DNASet.add(formattedDNA)
            NFTDict[formattedDNA] = ItemsUsed
            numberToGen -= 1
        else:
            print("ALL READY IN SET")
            currentFailedAttempts += 1
            if currentFailedAttempts > allowFailedAttempts:
                break
    print(NFTDict)
    return list(DNASet), NFTDict
    
def PickWeightedAttributeType(AttributeTypes, TypesRarity):
    number_List_Of_i = []
    rarity_List_Of_i = []
    ifZeroBool = None


    for attributetype in AttributeTypes:
        number_List_Of_i.append(attributetype)

        # rarity = attributetype.split("_")[1]
        rarity = TypesRarity[attributetype]["type_rarity"]
        rarity_List_Of_i.append(float(rarity))

    for x in rarity_List_Of_i:
        if x == 0:
            ifZeroBool = True
        elif x != 0:
            ifZeroBool = False

    if ifZeroBool == True:
        typeChoosen = random.choices(number_List_Of_i, k=1)
    elif ifZeroBool == False:
        typeChoosen = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)          
    
    return typeChoosen[0], list(AttributeTypes.keys()).index(typeChoosen[0])



def PickWeightedTypeVarient(Varients):
    number_List_Of_i = []
    rarity_List_Of_i = []
    ifZeroBool = None
    
    for varient in Varients:
        number_List_Of_i.append(varient)

        rarity = Varients[varient]["rarity"]
        rarity_List_Of_i.append(float(rarity))

    for x in rarity_List_Of_i:
        if x == 0:
            ifZeroBool = True
        elif x != 0:
            ifZeroBool = False

    if ifZeroBool == True:
        variantChoosen = random.choices(number_List_Of_i, k=1)
    elif ifZeroBool == False:
        variantChoosen = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)          
    
    return variantChoosen[0], list(Varients.keys()).index(variantChoosen[0])

 
#ColorStyle-1-1-textureSet-ColorR-COlorG-ColorB

if __name__ == '__main__':
    RandomizeFullCharacter()