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
LongShirtSlots = ["01-UpperTorso", "02-MiddleTorso", "03-LForeArm", "05-RForeArm"]
RSleaveSlots = ["06-RWrist", "07-Hands"]
PantsSlots = ["09-PelvisThin", "10-Calf", "11-Ankle"]
ShoesHighSlots = ["10-Calf", "11-Ankle", "12-Feet"]
ShoesMiddleSlots = ["11-Ankle", "12-Feet"]
ShortPantsSlot = ["09-PelvisThin", "10-Calf"]
LongCoatsSlot = ["01-UpperTorso", "02-MiddleTorso", "03-LForeArm", "05-RForeArm", "08-PelvisThick", "13-Neck"]
VestHoodiesSlot = ["01-UpperTorso", "02-MiddleTorso", "13-Neck", "18-BackPack"]
ThickShortsSlot = ["08-PelvisThick", "09-PelvisThin"]
# A dictionary which can be called to find what slots to fill when using certian items
ItemUsedBodySlot = {
    "Coats": CoatSlots, 
    "LongShirts": LongShirtSlots, 
    "RSleave": RSleaveSlots,  
    "Pants": PantsSlots, 
    "ShortPants": ShortPantsSlot, 
    "ShoesHigh" : ShoesHighSlots, 
    "ShoesMiddle" : ShoesMiddleSlots,
    "LongCoats" : LongCoatsSlot,
    "ThickShorts" : ThickShortsSlot,
    "VestHoodie" : VestHoodiesSlot
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

    

    BodySlotKeys = list(hierarchy)
    BodySlotsDict = dict.fromkeys(BodySlotKeys, False) 

    SingleDNA = CurrentDNA.split("-")
    
    for i in range(len(list(hierarchy)) ):
        #Get the name of the body slot
        currentSlot = list(hierarchy)[i]

        #find index of child we want to get body slot using current DNA
        index = int(SingleDNA[i])
        index -= 1 

        #get the name of that item
        itemArray = list(hierarchy.get(currentSlot))
        item = itemArray[index]

    #Get DNA strand index we want to modify
    #print( list(hierarchy.keys()).index(slot) )

    #Get item that is currently used
    currentChildIndex = int(SingleDNA[list(hierarchy.keys()).index(slot)]) -1
    BodySlotChildren = list(hierarchy.get(slot))
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