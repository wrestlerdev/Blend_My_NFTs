# Purpose:
# This file sorts the NFT DNA from NFTRecord.json and exports it to a given number of Batch#.json files set by nftsPerBatch
# in config.py.

import bpy
import os
import json
import random
import shutil

def SaveNFT(DNASetToAdd, NFTDict, batch_json_save_path, batch_index):
    NFTRecord_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{}".format(batch_index), "_NFTRecord{}.json".format(batch_index))

    DataDictionary = json.load(open(NFTRecord_save_path))
    i = int(DataDictionary["numNFTsGenerated"])
    hierarchy = DataDictionary["hierarchy"]
    
    for nft in DNASetToAdd:
        singleNFT = {}
        singleNFT["DNAList"] = nft 
        singleNFT["CharacterItems"] = NFTDict[nft]

        singleNFTObject = json.dumps(singleNFT, indent=1, ensure_ascii=True)
        with open(os.path.join(batch_json_save_path, ("NFT_Batch{}Num{}.json".format(batch_index, i + 1))), "w") as outfile:
            outfile.write(singleNFTObject)
        i += 1

    UpdateNFTRecord(DNASetToAdd, DataDictionary, NFTRecord_save_path)
        

def UpdateNFTRecord(DNASetToAdd, DataDictionary, NFTRecord_save_path):
    print("This should updated record.json with new nft DNA and number")

    currentNFTNumber = DataDictionary["numNFTsGenerated"]
    currentDNASet = DataDictionary["DNAList"]

    updatedDataDictionary = {}
    updatedDataDictionary["numNFTsGenerated"] = int(currentNFTNumber) + len(DNASetToAdd)
    updatedDataDictionary["hierarchy"] = DataDictionary["hierarchy"]
    for dna in DNASetToAdd:
        currentDNASet.append(dna)
    updatedDataDictionary["DNAList"] = currentDNASet

    try:
      ledger = json.dumps(updatedDataDictionary, indent=1, ensure_ascii=True)
      with open(NFTRecord_save_path, 'w') as outfile:
        outfile.write(ledger + '\n')
        print("Success update .json file")

    except:
        print("Failed to update .json file")


def OverrideNFT(DNAToAdd, NFTDict, batch_json_save_path, batch_index, nft_index):
    NFTRecord_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{}".format(batch_index), "_NFTRecord{}.json".format(batch_index))
    DataDictionary = json.load(open(NFTRecord_save_path))
    updatedDictionary = {}
    updatedDictionary["hierarchy"] = DataDictionary["hierarchy"]
    updatedDictionary["numNFTsGenerated"] = DataDictionary["numNFTsGenerated"]

    DNAList = DataDictionary["DNAList"]
    DNAList[nft_index - 1] = DNAToAdd
    updatedDictionary["DNAList"] = DNAList

    try:
      ledger = json.dumps(updatedDictionary, indent=1, ensure_ascii=True)
      with open(NFTRecord_save_path, 'w') as outfile:
        outfile.write(ledger + '\n')
        print("Success update .json file")
    except:
        print("Failed to update .json file")

    singleNFT = {}
    singleNFT["DNAList"] = DNAToAdd
    singleNFT["CharacterItems"] = NFTDict[DNAToAdd]

    singleNFTObject = json.dumps(singleNFT, indent=1, ensure_ascii=True)
    with open(os.path.join(batch_json_save_path, ("NFT_Batch{}Num{}.json".format(batch_index, nft_index))), "w") as outfile:
            outfile.write(singleNFTObject)



def DeleteNFT(DNAToDelete, save_path, batch_index):
    NFTRecord_save_path = os.path.join(save_path, "_NFTRecord{}.json".format(batch_index))
    DataDictionary = json.load(open(NFTRecord_save_path))

    updatedDictionary = {}
    updatedDictionary["numNFTsGenerated"] = DataDictionary["numNFTsGenerated"] - 1

    updatedDictionary["hierarchy"] = DataDictionary["hierarchy"]

    DNAList = DataDictionary["DNAList"]
    if DNAToDelete in DNAList:
        DNA_index = DNAList.index(DNAToDelete) + 1
        DNAList.remove(DNAToDelete)

        updatedDictionary["DNAList"] = DNAList

        try:
            ledger = json.dumps(updatedDictionary, indent=1, ensure_ascii=True)
            with open(NFTRecord_save_path, 'w') as outfile:
                outfile.write(ledger + '\n')
                print("Success update .json file")
            UpdateSingleNFTFiles(DNAToDelete, DNA_index, save_path, batch_index)
        except:
            print("Failed to update .json file")

    else:
        print("smth went wrong :^(")
    return DNA_index


def UpdateSingleNFTFiles(DNAToDelete, DNA_index, save_path, batch_index):
    total_nfts = len(os.listdir(save_path)) - 1 # TODO
    nft_save_path = os.path.join(save_path, "NFT_Batch{}Num{}.json".format(batch_index, DNA_index))
    os.remove(nft_save_path)

    for i in range(DNA_index + 1, total_nfts + 1):
        old_nft_save_path = os.path.join(save_path, "NFT_Batch{}Num{}.json".format(batch_index, i))
        new_nft_save_path = os.path.join(save_path, "NFT_Batch{}Num{}.json".format(batch_index, i-1))
        os.rename(old_nft_save_path, new_nft_save_path)
    return


def CreateSlotsFolderHierarchy(save_path):
    input_path = os.path.join(save_path, "INPUT")
    if os.path.exists(input_path):
        try:
            shutil.rmtree(input_path)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))

    os.makedirs(input_path)

    batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_1", "_NFTRecord1.json")
    DataDictionary = json.load(open(NFTRecord_save_path))
    hierarchy = DataDictionary["hierarchy"]

    h_keys = list(hierarchy.keys())
    for attribute in h_keys:
        att_path = os.path.join(input_path, attribute)
        os.makedirs(att_path)
        for type in list(hierarchy[attribute].keys()):
            type_path = os.path.join(att_path, type)
            os.makedirs(type_path)
            for variant in list(hierarchy[attribute][type].keys()):
                variant_path = os.path.join(type_path, variant)
                os.makedirs(variant_path)
    return


def SaveBlenderFile():
    print("This should save blender file")
    #bpy.ops.wm.save_as_mainfile(filepath=batch_json_save_path+".blend")

if __name__ == '__main__':
    SaveNFT()
