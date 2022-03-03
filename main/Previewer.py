# Purpose:
# This file generates NFT DNA based on a .blend file scene structure and exports NFTRecord.json.

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

class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR


time_start = time.time()


def create_preview_nft(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity):
   print("wow")
   # DNA_Generator.generateNFT_DNA(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity)
   """
   Returns batchDataDictionary containing the number of NFT combinations, hierarchy, and the DNAList.
   """

   listAllCollections, attributeCollections, attributeCollections1, hierarchy, possibleCombinations = DNA_Generator.returnData(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity)

   print(f"NFT Combinations: {possibleCombinations}\n")
   print(f"Generating {maxNFTs} combinations of DNA.\n")

   DataDictionary = {}
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

      for i in range(maxNFTs):
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
      DNAList = DNA_Generator.Rarity_Sorter.sortRarityWeights(hierarchy, listOptionVariant, DNAList, nftName, maxNFTs, nftsPerBatch, save_path, enableRarity)
      print(DNAList[0])

   # Data stored in batchDataDictionary:
   # DataDictionary["numNFTsGenerated"] = len(DNAList)
   # DataDictionary["hierarchy"] = hierarchy
   # DataDictionary["DNAList"] = DNAList

   return DNAList

if __name__ == '__main__':
   print("okay")