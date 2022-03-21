# Purpose:
# 

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



def read_DNAList_from_file(index):
    Blend_My_NFTs_Output = os.path.join("Blend_My_NFTs Output", "NFT_Data")
    NFTRecord_save_path = os.path.join(Blend_My_NFTs_Output, "NFTRecord.json")
    DataDictionary = json.load(open(NFTRecord_save_path))
    DNAList = DataDictionary["DNAList"]

    if index < len(DNAList):
        DNA = DNAList[index]
        return len(DNAList), DNA
    else:
        return len(DNAList), ''

def get_total_DNA():
    Blend_My_NFTs_Output = os.path.join("Blend_My_NFTs Output", "NFT_Data")
    NFTRecord_save_path = os.path.join(Blend_My_NFTs_Output, "NFTRecord.json")
    DataDictionary = json.load(open(NFTRecord_save_path))
    DNAList = DataDictionary["DNAList"]
    return len(DNAList)


def load_number_has_updated():

    return