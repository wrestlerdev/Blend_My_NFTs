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



# This defines a varible that tracks current populated slots on the body
'''
Interestly we could potentially fill this body slot dic with list(hierarchy). Returns top level collections in scene
'''

# A list for each caterogry of clothing that states what slots it will fil
CoatSlots = ["UpperTorso", "LowerTorso", "L_UpperArm", "L_ForeArm"]
PantsSlots = ["Pelvis", "Calf"]

# A dictionary which can be called to find what slots to fill

ItemUsedBodySlot = {"Coat": CoatSlots, "PantsLong": PantsSlots}

def GenerateOutfit(hierarchy):
    DNASet = set()

    #Create a dictionary based on current top level collections in scene that should relate to slots. Set them to be populated false
    BodySlotKeys = list(hierarchy)
    BodySlotsDict = dict.fromkeys(BodySlotKeys, False)   

    for i in hierarchy:
        #print(i)
        numChild = len(hierarchy[i])
        #print(hierarchy[i])
        possibleNums = list(range(1, numChild + 1))


    for slot in BodySlotKeys:
        if BodySlotsDict.get(slot):
            print("Slot Full")
        else:
            BodySlotChildren = list(hierarchy.get(slot))
            ItemChoosen = random.randrange(0, len(BodySlotChildren))
            print(ItemChoosen)

if __name__ == '__main__':
    GenerateOutfit()