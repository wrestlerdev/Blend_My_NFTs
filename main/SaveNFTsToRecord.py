# Purpose:
# This file sorts the NFT DNA from NFTRecord.json and exports it to a given number of Batch#.json files set by nftsPerBatch
# in config.py.

import bpy
import os
import json
import random


def SaveNFT(DNASetToAdd, save_path, batch_json_save_path):
    
    Blend_My_NFTs_Output = os.path.join(save_path, "Blend_My_NFTs Output", "NFT_Data")
    NFTRecord_save_path = os.path.join(Blend_My_NFTs_Output, "NFTRecord.json")

    DataDictionary = json.load(open(NFTRecord_save_path))
    i = int(DataDictionary["numNFTsGenerated"])
    hierarchy = DataDictionary["hierarchy"]

    for nft in DNASetToAdd:
        singleNFT = {}
        singleNFT["DNAList"] = nft 
        index = 0

        chracterItemDict = {}
        for char in nft.split('-'):
            varientArray = hierarchy.get( list(hierarchy)[index])

            '''
            Make list of all items character used
            '''
            chracterItemDict[list(hierarchy)[index]] = list(varientArray)[int(char) -1]
            index += 1

        singleNFT["CharacterItems"] = chracterItemDict

        singleNFTObject = json.dumps(singleNFT, indent=1, ensure_ascii=True)
        with open(os.path.join(batch_json_save_path, ("NFTNumber{}.json".format(i + 1))), "w") as outfile:
            outfile.write(singleNFTObject)
        i += 1
    UpdateNFTRecord(DNASetToAdd, save_path, DataDictionary, NFTRecord_save_path)
        

def UpdateNFTRecord(DNASetToAdd, save_path, DataDictionary, NFTRecord_save_path):
    print("This should updated record.json with new nft DNA and number")

    currentNFTNumber = DataDictionary["numNFTsGenerated"]
    currentDNASet = DataDictionary["DNAList"]

    updatedDataDictionary = {}
    updatedDataDictionary["numNFTsGenerated"] = int(currentNFTNumber) + len(DNASetToAdd)
    updatedDataDictionary["hierarchy"] = DataDictionary["hierarchy"]
    for dna in DNASetToAdd:
        currentDNASet.append(dna)
    updatedDataDictionary["DNAList"] = currentDNASet

    print(updatedDataDictionary)
    print(currentDNASet)

    try:
      ledger = json.dumps(updatedDataDictionary, indent=1, ensure_ascii=True)
      with open(NFTRecord_save_path, 'w') as outfile:
        outfile.write(ledger + '\n')
        print("Success update .json file")

    except:
        print("Failed to update .json file")




def SaveBlenderFile():
    print("This should save blender file")
    #bpy.ops.wm.save_as_mainfile(filepath=batch_json_save_path+".blend")

if __name__ == '__main__':
    SaveNFT()
