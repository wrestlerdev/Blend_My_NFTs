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


# A list for each caterogry of clothing that states what slots it will fil
CoatSlots = ["01-UpperTorso", "02-MiddleTorso", "08-PelvisThick", "03-LForeArm", "05-RForeArm", "13-Neck"]
LongCoatsSlot = ["01-UpperTorso", "02-MiddleTorso", "03-LForeArm", "05-RForeArm", "08-PelvisThick", "13-Neck"]
VestHoodiesSlot = ["01-UpperTorso", "02-MiddleTorso", "13-Neck", "18-BackPack"]
CropShirtsSlot = ["01-UpperTorso"]
TShirtsSlot = ["01-UpperTorso", "02-MiddleTorso"]
LongShirtSlots = ["01-UpperTorso", "02-MiddleTorso", "03-LForeArm", "05-RForeArm"]
LSleaveSlots = ["03-LForeArm", "04-LWrist", "07-Hands"]
RSleaveSlots = ["05-RForeArm", "06-RWrist", "07-Hands"]
PantsSlots = ["09-PelvisThin", "10-Calf", "11-Ankle"]
ShoesHighSlots = ["10-Calf", "11-Ankle", "12-Feet"]
ShoesMiddleSlots = ["11-Ankle", "12-Feet"]
ShortPantsSlot = ["09-PelvisThin", "10-Calf"]
ThickShortsSlot = ["08-PelvisThick", "09-PelvisThin"]

cols = {
    "a" : [(0.00000, 0.04706, 0.03529), (0.64706, 0.41569, 0.21176), (0.84706, 0.81176, 0.78039), (0.84706, 0.65490, 0.58431), (0.54902,0.00784,0.00784)],
    "b" : [(0.62745,0.76471,0.84706), (0.13333,0.35686,0.44706), (0.19608,0.24706,0.00392), (0.84706,0.46667,0.38039), (0.74902,0.26667,0.26667)],
    "c" : [(0.31373,0.70588,0.74902), (0.84706,0.63922,0.01569), (0.74902,0.49020,0.01176), (0.74902,0.35686,0.01176), (0.64706,0.48235,0.33725)]
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
    "ThickShorts" : ThickShortsSlot, 
    "LSleave": LSleaveSlots,
    "RSleave": RSleaveSlots,  
    "Pants": PantsSlots, 
    "ShortPants": ShortPantsSlot, 
    "ShoesHigh" : ShoesHighSlots, 
    "ShoesMiddle" : ShoesMiddleSlots
}


def RandomizeSingleDNAStrand(slot, CurrentDNA, save_path):

    #go through entire DNA and populate diction of used body slots
    #Create a dictionary based on current top level collections in scene that should relate to slots. Set them to be populated false  

    #go to index of slot chosen
    #set body slots it populated to false
    #get a random weight item from children
    #check to see if its allowed with body slots 
    #if so choose that item, if not pick again

    Blend_My_NFTs_Output = os.path.join(save_path, "Blend_My_NFTs Output", "NFT_Data")
    NFTRecord_save_path = os.path.join(Blend_My_NFTs_Output, "NFTRecord.json")

    DataDictionary = json.load(open(NFTRecord_save_path))

    hierarchy = DataDictionary["hierarchy"]
    DNAList = DataDictionary["DNAList"]
    #print(CurrentDNA)

    
    #Build Dict
    attributeskeys = list(hierarchy.keys())
    attributevalues = list(hierarchy.values())
    attributeUsedDict = dict.fromkeys(attributeskeys, False)


    DNAString = CurrentDNA.split(",")
    for strand in range(len(DNAString)):

        atttype_index, variant_index = DNAString[strand].split('-')
        slot = list(hierarchy.items())[strand]

        atttype = list(slot[1].items())[int(atttype_index)]
        variant = list(atttype[1].items())[int(variant_index)][0]

        ItemClothingGenre = list(atttype[1].items())[int(variant_index)][1]["clothingGenre"]
        print(ItemClothingGenre)
               
        #loop through all slots that selected item will take up
        UsedUpSlotArray = ItemUsedBodySlot.get(ItemClothingGenre)
        if UsedUpSlotArray:
            for i in ItemUsedBodySlot.get(ItemClothingGenre):
                SlotUpdateValue = {i : True}
                attributeUsedDict.update(SlotUpdateValue)

    print(attributeUsedDict)
        
        # bpy.data.collections[variant].hide_viewport = False
        # bpy.data.collections[variant].hide_render = False
    
    # for i in range(len(list(hierarchy)) ):
    #     #Get the name of the body slot
    #     currentSlot = list(hierarchy)[i]

    #     #find index of child we want to get body slot using current DNA
    #     index = int(SingleDNA[i])
    #     index -= 1 

    #     #get the name of that item
    #     itemArray = list(hierarchy.get(currentSlot))
    #     item = itemArray[index]

    #Get DNA strand index we want to modify
    #print( list(hierarchy.keys()).index(slot) )

    #Get item that is currently used
    # currentChildIndex = int(SingleDNA[list(hierarchy.keys()).index(slot)]) -1
    # BodySlotChildren = list(hierarchy.get(slot))
    #print(list(BodySlotChildren)[currentChildIndex])

    
    # ItemIndexChoosen = PickWeightedDNAStrand(hierarchy.get(slot))
    # ItemChoosen = list(BodySlotChildren)[ItemIndexChoosen]
                    
    # #Get item metadata from object 
    # ItemMetaData = hierarchy.get(slot).get(ItemChoosen)
    # ItemIndex = ItemMetaData["number"]
    # SingleDNA[list(hierarchy.keys()).index(slot)] = ItemIndex
    # ItemClothingGenre = ItemMetaData["clothingGenre"]
                    
    # #loop through all slots that selected item will take up
    # UsedUpSlotArray = ItemUsedBodySlot.get(ItemClothingGenre)
    # if UsedUpSlotArray:
    #     for i in ItemUsedBodySlot.get(ItemClothingGenre):
    #         SlotUpdateValue = {i : True}
    #         #BodySlotsDict.update(SlotUpdateValue)           
    # #bpy.data.collections.get(ItemChoosen).hide_viewport = False

def setBodySlotsValue(ItemClothingGenre, ValueToSet):
    #loop through all slots that selected item will take up
    UsedUpSlotArray = ItemUsedBodySlot.get(ItemClothingGenre)
    if UsedUpSlotArray:
        for i in ItemUsedBodySlot.get(ItemClothingGenre):
            SlotUpdateValue = {i : True}
            #BodySlotsDict.update(SlotUpdateValue)   


def RandomizeFullCharacter(maxNFTs, save_path):

    Blend_My_NFTs_Output = os.path.join(save_path, "Blend_My_NFTs Output", "NFT_Data")
    NFTRecord_save_path = os.path.join(Blend_My_NFTs_Output, "NFTRecord.json")

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

        letterstyles = 'abc'
        style = copy.deepcopy( cols[random.choice(letterstyles)] )
        maincolor = (0.0, 0.0, 0.0)
        secondarycolor = (0.0, 0.0, 0.0)
        if( random.random() > .05 ):
            maincolor = style.pop(0)
            index = random.randrange(0, len(style))
            secondarycolor = style.pop(index)
        else:
            secondarycolor = style.pop(0)
            index = random.randrange(0, len(style))
            maincolor = style.pop(index)

        
        for child in bpy.data.collections.get("Kae").objects:
            obj = bpy.data.objects[child.name]
            obj["TestColor"] = skincols[random.randrange(len(skincols))]
            obj["metallic"] = random.random()
            obj.hide_viewport = False
        
         

        for attribute in attributeskeys:
            if(attributeUsedDict.get(attribute)):
                SingleDNA[list(hierarchy.keys()).index(attribute)] = "0-0"
                ItemsUsed[attribute] = "Null"
            else:
                position = attributevalues.index(hierarchy[attribute])
                typeChoosen, typeIndex = PickWeightedAttributeType(hierarchy[attribute])

                varientChoosen, varientIndex = PickWeightedTypeVarient(hierarchy[attribute][typeChoosen])
                # print(typeChoosen + " " +  varientChoosen)
                # print(typeIndex)
                # print(varientIndex)
                SingleDNA[list(hierarchy.keys()).index(attribute)] = str(typeIndex) + "-" + str(varientIndex)
                VarientDict = {}
                VarientDict[varientChoosen] = hierarchy[attribute][typeChoosen][varientChoosen]
                ItemsUsed[attribute] = VarientDict

                bpy.data.collections.get(varientChoosen).hide_viewport = False
                chidlrenObjs = bpy.data.collections.get(varientChoosen).objects

                col = (0.0, 0.0, 0.0)

                if(attribute == "01-UpperTorso"):
                    col =  maincolor
                elif(attribute == "08-PelvisThick" or attribute == "08-PelvisThick"):
                    col = secondarycolor
                elif(attribute == "17-UpperHead"):
                    col = haircols[random.randrange(0, len(haircols) ) ]
                else:  
                    col = style[random.randrange(0, len(style) ) ]
                    #col = (random.random(), random.random(), random.random())

                for child in chidlrenObjs:
                    ob = bpy.data.objects[child.name]
                    ob["TestColor"] = col

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
    
def PickWeightedAttributeType(AttributeTypes):
    number_List_Of_i = []
    rarity_List_Of_i = []
    ifZeroBool = None


    for attributetype in AttributeTypes:
        number_List_Of_i.append(attributetype)

        rarity = attributetype.split("_")[1]
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

 
if __name__ == '__main__':
    RandomizeFullCharacter()