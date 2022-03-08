# Purpose:
# This file generates the Outfit DNA based on a rule set

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
CoatSlots = ["AUpperTorso", "MNeck"]
PantsSlots = ["ILowerTorso", "JCalf", "KAnkle"]
ShoesHighSlots = ["JCalf", "KAnkle", "LFeet"]
ShoesMiddleSlots = ["KAnkle", "LFeet"]

# A dictionary which can be called to find what slots to fill when using certian items
ItemUsedBodySlot = {"Coats": CoatSlots, "Pants": PantsSlots, "ShoesHigh" : ShoesHighSlots, "ShoesMiddle" : ShoesMiddleSlots}

def GenerateOutfit(hierarchy, maxNFTs):
    DNASet = set()
    numberToGen = maxNFTs

    allowFailedAttempts = 50
    currentFailedAttempts = 0
    while numberToGen > 0: 

        SingleDNA = []

        #Create a dictionary based on current top level collections in scene that should relate to slots. Set them to be populated false
        BodySlotKeys = list(hierarchy)
        BodySlotsDict = dict.fromkeys(BodySlotKeys, False)   


        for slot in BodySlotKeys:
            if BodySlotsDict.get(slot):
                SingleDNA.append("1")
            else:
                BodySlotChildren = list(hierarchy.get(slot))
                ItemIndexChoosen = PickWeightedDNAStrand(hierarchy.get(slot))
                ItemChoosen = list(BodySlotChildren)[ItemIndexChoosen]


                
                #Get item metadata from object 
                ItemMetaData = hierarchy.get(slot).get(ItemChoosen)
                ItemIndex = ItemMetaData["number"]
                SingleDNA.append(str(ItemIndex))
                ItemClothingGenre = ItemMetaData["clothingGenre"]
                
                #loop through all slots that selected item will take up
                UsedUpSlotArray = ItemUsedBodySlot.get(ItemClothingGenre)
                if UsedUpSlotArray:
                    for i in ItemUsedBodySlot.get(ItemClothingGenre):
                        SlotUpdateValue = {i : True}
                        BodySlotsDict.update(SlotUpdateValue)
    
                bpy.data.collections.get(ItemChoosen).hide_viewport = False

        formattedDNA = '-'.join(SingleDNA)
        if formattedDNA not in DNASet:
            print("ADDING DNA TO SET")
            DNASet.add(formattedDNA)
            numberToGen -= 1
        else:
            print("ALL READY IN SET")
            currentFailedAttempts += 1
            if currentFailedAttempts > allowFailedAttempts:
                break
            
    print(DNASet)
    return list(DNASet)
            
def PickWeightedDNAStrand(BodySlotChildren):
    number_List_Of_i = []
    rarity_List_Of_i = []
    ifZeroBool = None

    for k in BodySlotChildren:
        number = BodySlotChildren[k]["number"]
        number_List_Of_i.append(number)

        rarity = BodySlotChildren[k]["rarity"]
        rarity_List_Of_i.append(float(rarity))

    for x in rarity_List_Of_i:
        if x == 0:
            ifZeroBool = True
        elif x != 0:
            ifZeroBool = False

    if ifZeroBool == True:
        variantByNum = random.choices(number_List_Of_i, k=1)
    elif ifZeroBool == False:
        variantByNum = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)          
    
    print(int(variantByNum[0])-1)
    return (int(variantByNum[0]) -1)

 
if __name__ == '__main__':
    GenerateOutfit()