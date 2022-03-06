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

def GenerateOutfit(hierarchy):
    DNASet = set()

    #Create a dictionary based on current top level collections in scene that should relate to slots. Set them to be populated false
    BodySlotKeys = list(hierarchy)
    BodySlotsDict = dict.fromkeys(BodySlotKeys, False)   


    for slot in BodySlotKeys:
        print(slot)
        if BodySlotsDict.get(slot):
            print("Slot Full")
        else:
            print("Slot Empty")
            
            BodySlotChildren = list(hierarchy.get(slot))
            ItemIndexChoosen = random.randrange(0, len(BodySlotChildren))
            ItemChoosen = list(BodySlotChildren)[ItemIndexChoosen]
            
            #Get item metadata from object 
            ItemMetaData = hierarchy.get(slot).get(ItemChoosen)
            ItemClothingGenre = ItemMetaData["clothingGenre"]
            
            #loop through all slots that selected item will take up
            UsedUpSlotArray = ItemUsedBodySlot.get(ItemClothingGenre)
            if UsedUpSlotArray:
                for i in ItemUsedBodySlot.get(ItemClothingGenre):
                    print("Item is in array")
                    SlotUpdateValue = {i : True}
                    BodySlotsDict.update(SlotUpdateValue)
 
            bpy.data.collections.get(ItemChoosen).hide_viewport = False
            
            


 
if __name__ == '__main__':
    GenerateOutfit()