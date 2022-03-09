# Purpose:
# This file generates NFT DNA based on a .blend file scene structure and exports NFTRecord.json.

from venv import create
import bpy
import os
import re
import copy
import time
import json
import random
import importlib
from functools import partial

from . import DNA_Generator
importlib.reload(DNA_Generator)


enableGeneration = False
colorList = []
current_hierarchy = {}



class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR


time_start = time.time()

def show_NFT(DNA, hierarchy):


   print("DNA: " + str(DNA))
   dnaDictionary = {}
   listAttributes = list(hierarchy.keys())

   listDNADeconstructed = DNA.split('-')
   for i, j in zip(listAttributes, listDNADeconstructed): 
                dnaDictionary[i] = j

   for x in dnaDictionary: 
      for k in hierarchy[x]:
                    kNum = hierarchy[x][k]["number"]
                    if kNum == dnaDictionary[x]:
                        dnaDictionary.update({x: k})

      
   for c in dnaDictionary:
      # bpy.data.collections[c].hide_render = False
      # bpy.data.collections[c].hide_viewport = False
      print(dnaDictionary[c])
      objs = bpy.data.collections[c].children
      mesh_collection = bpy.data.collections[c].children[str(dnaDictionary[c])]

      for obj in objs:
         print(obj)
         if obj == mesh_collection:
            mesh_collection.hide_render = False
            mesh_collection.hide_viewport = False
         else:
            obj.hide_render = True
            obj.hide_viewport = True

      # for obj in mesh_collection.objects:
      #    print(obj)



def create_DNA(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity):
   print("wow")
   # DNA_Generator.generateNFT_DNA(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity)
   """
   Returns batchDataDictionary containing the number of NFT combinations, hierarchy, and the DNAList.
   """

   listAllCollections, attributeCollections, attributeCollections1, hierarchy, possibleCombinations = DNA_Generator.returnData(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity)

   print("Generating one preview NFT")
   print(f"NFT Combinations: {possibleCombinations}\n")

   listOptionVariant = []
   DNAList = []

   if not enableRarity:
      DNASet = set()

      for i in hierarchy:
         numChild = len(hierarchy[i])
         possibleNums = list(range(1, numChild + 1))
         listOptionVariant.append(possibleNums)

      def createDNARandom():
         dnaStr = ""
         dnaStrList = []

         for i in listOptionVariant:
            randomVariantNum = random.choices(i, k = 1)
            str1 = ''.join(str(e) for e in randomVariantNum)
            dnaStrList.append(str1)

         for i in dnaStrList:
            num = "-" + str(i)
            dnaStr += num

         dna = ''.join(dnaStr.split('-', 1))

         return str(dna)

      for i in range(1):
         dnaPushToList = partial(createDNARandom)

         DNASet |= {''.join([dnaPushToList()]) for _ in range(maxNFTs - len(DNASet))}

      DNAList = list(DNASet)

      possibleCombinations = maxNFTs

      if nftsPerBatch > maxNFTs:
         print(bcolors.WARNING + "\nWARNING:" + bcolors.RESET)
         print(f"The Max num of NFTs you chose is smaller than the NFTs Per Batch you set. Only {maxNFTs} were added to 1 batch")

   else:
      print(f"{bcolors.OK} Rarity is on. Weights listed in .blend will be taken into account {bcolors.RESET}")
      possibleCombinations = maxNFTs
      DNAList = DNA_Generator.Rarity_Sorter.sortRarityWeights(hierarchy, listOptionVariant, DNAList, nftName, 1, 1, save_path, enableRarity)
   
   current_hierarchy = hierarchy
   return DNAList[0], hierarchy



def create_preview_nft(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity):
   DNA, hierarchy = create_DNA(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity)
   global current_hierarchy
   current_hierarchy = hierarchy
   show_NFT(DNA, current_hierarchy)
   return DNA

def show_nft_from_dna(DNA, nftName, maxNFTs, nftsPerBatch, save_path, enableRarity):
   global current_hierarchy
   if len(current_hierarchy) == 0:
      randDNA, hierarchy = create_DNA(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity)
      current_hierarchy = hierarchy
   show_NFT(DNA, current_hierarchy)


#  ----------------------------------------------------------------------------------


def get_random_from_collection(coll): # doesn't respect weights or filled slots yet
                                       # should check if from right collection
   rand_int = random.randint(0,len(coll.children)-1)
   chosen_coll = coll.children[rand_int]
   for child in coll.children:
      child.hide_render = True
      child.hide_viewport = True
   chosen_coll.hide_render = False
   chosen_coll.hide_viewport = False
   return chosen_coll
 
if __name__ == '__main__':
   print("okay")