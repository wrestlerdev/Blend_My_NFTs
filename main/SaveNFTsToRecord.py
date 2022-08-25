# Purpose:
# This file sorts the NFT DNA from NFTRecord.json and exports it to a given number of Batch#.json files set by nftsPerBatch
# in config.py.

import bpy
import os
import json
import shutil
import bmesh
from . import config


def SaveNFT(DNASetToAdd, NFTDict, single_batch_save_path, batch_index, master_record_save_path):
    single_record_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{:03d}".format(batch_index), "_NFTRecord_{:03d}.json".format(batch_index))

    DataDictionary = json.load(open(single_record_path))
    single_i = int(DataDictionary["numNFTsGenerated"])
    
    MasterDictionary = json.load(open(master_record_save_path))
    totalDNAList = MasterDictionary["DNAList"]

    character_count = [0] * len(config.Characters)

    uniqueDNASetToAdd = []
    for nft in DNASetToAdd:
        if nft not in totalDNAList:
            singleNFT = {}
            singleNFT["CharacterItems"] = NFTDict[nft]
            singleNFT["DNAList"] = nft

            singleNFTObject = json.dumps(singleNFT, indent=1, ensure_ascii=True)
            if not os.path.exists(os.path.join(single_batch_save_path, "NFT_{:04d}".format(single_i + 1))):
                os.mkdir(os.path.join(single_batch_save_path, "NFT_{:04d}".format(single_i + 1)))
            with open(os.path.join(single_batch_save_path, "NFT_{:04d}".format(single_i + 1), ("Batch_{:03d}_NFT_{:04d}.json".format(batch_index, single_i + 1))), "w") as outfile:
                outfile.write(singleNFTObject)
            single_i += 1
            uniqueDNASetToAdd.append(nft)
            character = nft.partition(",")[0]
            char_index = config.Characters.index(character)
            character_count[char_index] += 1


    if uniqueDNASetToAdd:
        UpdateNFTRecord(uniqueDNASetToAdd, character_count, DataDictionary, single_record_path, master_record_save_path)
        print("{} NFTs have been saved (ノಠ vಠ)ノ彡( {}o)". format(len(uniqueDNASetToAdd), "o°"*len(uniqueDNASetToAdd)))
        return True
    else:
        print("ERROR: This NFT(s) already exists")
        return False


def UpdateNFTRecord(DNASetToAdd, CharacterCount, DataDictionary, single_record_path, master_record_save_path):
    print("This should updated record.json with new nft DNA and number")

    updatedMasterDictionary = {}
    MasterDictionary = json.load(open(master_record_save_path))
    updatedMasterDictionary["numNFTsGenerated"] = int(MasterDictionary["numNFTsGenerated"]) + len(DNASetToAdd)
    totalDNASet = MasterDictionary["DNAList"]

    numMasterCharDict = {}
    numSingleCharDict = {}

    # updatedMasterDictionary["numCharacters"] = newNumMasterCharDict

    currentNFTNumber = DataDictionary["numNFTsGenerated"]
    currentDNASet = DataDictionary["DNAList"]

    updatedDataDictionary = {}
    updatedDataDictionary["numNFTsGenerated"] = int(currentNFTNumber) + len(DNASetToAdd)
    updatedDataDictionary["hierarchy"] = DataDictionary["hierarchy"]

    numMasterCharDict = MasterDictionary["numCharacters"]
    numSingleCharDict = DataDictionary["numCharacters"]

    newNumMasterCharDict = {}
    newNumSingleCharDict = {}

    for i in range(len(CharacterCount)):
        character = config.Characters[i]
        newNumMasterCharDict[character] = numMasterCharDict[character] + CharacterCount[i]
        newNumSingleCharDict[character] = numSingleCharDict[character] + CharacterCount[i]

    updatedDataDictionary["numCharacters"] = newNumSingleCharDict
    updatedMasterDictionary["numCharacters"] = newNumMasterCharDict

    for dna in DNASetToAdd:
        currentDNASet.append(dna)
        totalDNASet.append(dna)
    updatedDataDictionary["DNAList"] = currentDNASet
    updatedMasterDictionary["DNAList"] = totalDNASet

    try:
      ledger = json.dumps(updatedDataDictionary, indent=1, ensure_ascii=True)
      with open(single_record_path, 'w') as outfile:
        outfile.write(ledger + '\n')
        print("Success update {}". format(single_record_path))
    except:
        print("Failed to update {}". format(single_record_path))

    try:
      ledger = json.dumps(updatedMasterDictionary, indent=1, ensure_ascii=True)
      with open(master_record_save_path, 'w') as outfile:
        outfile.write(ledger + '\n')
        print("Success update {}". format(master_record_save_path))
    except:
        print("Failed to update {}". format(master_record_save_path))



def OverrideNFT(DNAToAdd, NFTDict, batch_save_path, batch_index, nft_index, master_record_save_path):
    single_record_save_path = os.path.join(batch_save_path, "_NFTRecord_{:03d}.json".format(batch_index))
    DataDictionary = json.load(open(single_record_save_path))
    MasterDictionary = json.load(open(master_record_save_path))

    updatedMasterDictionary = {}
    totalDNAList = MasterDictionary["DNAList"]
    updatedMasterDictionary["numNFTsGenerated"] = MasterDictionary["numNFTsGenerated"]

    if DNAToAdd in totalDNAList:
        oldDNA_index = totalDNAList.index(DNAToAdd)
        newDNA_index = nft_index -1
        if oldDNA_index != newDNA_index: # if nft exists but isnt current index (for if colours have been adjusted)
            return False

    updatedDictionary = {}
    updatedDictionary["hierarchy"] = DataDictionary["hierarchy"]
    updatedDictionary["numNFTsGenerated"] = DataDictionary["numNFTsGenerated"]

    newSingleCharDict = DataDictionary["numCharacters"]
    newMasterCharDict = MasterDictionary["numCharacters"]

    DNAList = DataDictionary["DNAList"]

    oldDNA = DNAList[nft_index - 1]
    old_char = oldDNA.partition(',')[0]
    new_char = DNAToAdd.partition(',')[0]

    newMasterCharDict[old_char] = newMasterCharDict[old_char] - 1
    newMasterCharDict[new_char] = newMasterCharDict[new_char] + 1
    newSingleCharDict[old_char] = newSingleCharDict[old_char] - 1
    newSingleCharDict[new_char] = newSingleCharDict[new_char] + 1

    updatedMasterDictionary["numCharacters"] = newMasterCharDict
    updatedDictionary["numCharacters"] = newSingleCharDict

    DNAList[nft_index - 1] = DNAToAdd
    updatedDictionary["DNAList"] = DNAList

    oldDNAIndex = totalDNAList.index(oldDNA)
    totalDNAList[oldDNAIndex] = DNAToAdd
    updatedMasterDictionary["DNAList"] = totalDNAList

    try:
      ledger = json.dumps(updatedDictionary, indent=1, ensure_ascii=True)
      with open(single_record_save_path, 'w') as outfile:
        outfile.write(ledger + '\n')
        print("Success update {}".format(single_record_save_path))
    except:
        print("Failed to update {}".format(single_record_save_path))

    singleNFT = {}
    singleNFT["DNAList"] = DNAToAdd
    singleNFT["CharacterItems"] = NFTDict[DNAToAdd]
    singleNFTObject = json.dumps(singleNFT, indent=1, ensure_ascii=True)
    with open(os.path.join(batch_save_path, "NFT_{:04d}".format(nft_index), ("Batch_{:03d}_NFT_{:04d}.json".format(batch_index, nft_index))), "w") as outfile:
        outfile.write(singleNFTObject)

    updatedMasterObject = json.dumps(updatedMasterDictionary, indent=1, ensure_ascii=True)
    with open(master_record_save_path, "w") as outfile:
        outfile.write(updatedMasterObject)

    return True


def DeleteNFTsinRange(start, end, TotalDNA, save_path, batch_index, master_record_save_path):
    if start > end or start > len(TotalDNA):
        print(f"{config.bcolors.ERROR}This is not a valid range. Nothing was deleted{config.bcolors.RESET}")
        return

    if end > len(TotalDNA):
        end = len(TotalDNA)
        print(f"{config.bcolors.WARNING}This is out of range. New range deleted is {start} ~ {end}{config.bcolors.RESET}")

    for index in range(end, start - 1, -1):
        DNA = TotalDNA[index - 1]
        DeleteNFT(DNA, save_path, batch_index, master_record_save_path)

    print(f"{config.bcolors.OK}NFTs from {start} ~ {end} (total {end - start + 1}) deleted{config.bcolors.RESET}")
    return


def DeleteAllNFTs(TotalDNA, save_path, batch_index, master_record_save_path):
    for index in range(len(TotalDNA), 0, -1):
        DNA = TotalDNA[index - 1]
        DeleteNFT(DNA, save_path, batch_index, master_record_save_path)
    return


def DeleteNFT(DNAToDelete, save_path, batch_index, master_record_save_path):
    NFTRecord_save_path = os.path.join(save_path, "_NFTRecord_{:03d}.json".format(batch_index))
    DataDictionary = json.load(open(NFTRecord_save_path))
    MasterDictionary = json.load(open(master_record_save_path))

    updatedDictionary = {}
    updatedDictionary["numNFTsGenerated"] = DataDictionary["numNFTsGenerated"] - 1
    updatedDictionary["hierarchy"] = DataDictionary["hierarchy"]
    updatedMasterDictionary = {}
    updatedMasterDictionary["numNFTsGenerated"] = MasterDictionary["numNFTsGenerated"] - 1

    newSingleCharDict = DataDictionary["numCharacters"]
    newMasterCharDict = MasterDictionary["numCharacters"]

    old_char = DNAToDelete.partition(',')[0]
    newMasterCharDict[old_char] = int(newMasterCharDict[old_char]) - 1
    newSingleCharDict[old_char] = int(newSingleCharDict[old_char]) - 1
    updatedMasterDictionary["numCharacters"] = newMasterCharDict
    updatedDictionary["numCharacters"] = newSingleCharDict

    DNAList = DataDictionary["DNAList"]
    if DNAToDelete in DNAList:
        DNA_index = DNAList.index(DNAToDelete) + 1
        DNAList.remove(DNAToDelete)
        updatedDictionary["DNAList"] = DNAList

        try:
            ledger = json.dumps(updatedDictionary, indent=1, ensure_ascii=True)
            with open(NFTRecord_save_path, 'w') as outfile:
                outfile.write(ledger + '\n')
                print("Success update {}".format(NFTRecord_save_path))
            UpdateSingleNFTFileIndex(DNA_index, save_path, batch_index)

            totalDNAList = MasterDictionary["DNAList"]
            totalDNAList.remove(DNAToDelete)
            updatedMasterDictionary["DNAList"] = totalDNAList

            ledger = json.dumps(updatedMasterDictionary, indent=1, ensure_ascii=True)
            with open(master_record_save_path, 'w') as outfile:
                outfile.write(ledger + '\n')
                print("Success update {}".format(master_record_save_path))
        except:
            print("Failed to update {}".format(master_record_save_path))

    else:
        print("smth went wrong :^(")
    return DNA_index


def UpdateSingleNFTFileIndex(DNA_index, save_path, batch_index): 
    total_nfts = len(next(os.walk(save_path))[1])
    nft_save_path = os.path.join(save_path, "NFT_{:04d}".format(DNA_index))
    shutil.rmtree(nft_save_path)
    for i in range(DNA_index + 1, total_nfts + 1): # nfts from records should not be deleted after rendering starts
        old_nft_save_path = os.path.join(save_path, "NFT_{:04d}".format(i), "Batch_{:03d}_NFT_{:04d}.json".format( batch_index, i))
        new_nft_save_path = os.path.join(save_path, "NFT_{:04d}".format(i-1), "Batch_{:03d}_NFT_{:04d}.json".format( batch_index, i-1))
        new_folder_path = os.path.join(save_path, "NFT_{:04d}".format(i-1))

        os.mkdir(new_folder_path)
        
        os.rename(old_nft_save_path, new_nft_save_path)

        shutil.rmtree(os.path.join(save_path, "NFT_{:04d}".format(i)))
    return


# def delete_hierarchy(parent_col):
#     # Go over all the objects in the hierarchy like @zeffi suggested:
#     def get_child_names(obj):
#         for child in obj.children:
#             if child.name != "Script_Ignore":
#                 if child.children:
#                     get_child_names(child)
#                 for obj in child.objects:
#                     bpy.data.objects.remove(obj, do_unlink=True)       
#                 bpy.data.collections.remove(child)
#     get_child_names(parent_col)



def count_all_items_in_batch(batches_path, batch_nums, save_path):
    counter = {}
    has_init = False
    characters = 0
    for index in range(batch_nums[1], batch_nums[0]-1, -1):
        batch_path = os.path.join(batches_path, "Batch_{:03d}".format(index))
        if os.path.exists(batch_path):
            if not has_init:
                record_path = os.path.join(batch_path, "_NFTRecord_{:03d}.json".format(index))
                record = json.load(open(record_path))
                hierarchy = record["hierarchy"]
                for slot in hierarchy.keys():
                    for type in hierarchy[slot].keys():
                        for var in hierarchy[slot][type].keys():
                            for tex in hierarchy[slot][type][var]["textureSets"]:
                                var_name = tex.split('_')[3] + ' ' + tex.split('_')[4]
                                counter[var_name] = {}
                                counter[var_name]["count"] = 0
                                counter[var_name]["full_name"] = tex
                has_init = True

            for dir in os.listdir(batch_path):
                folder_dir = os.path.join(batch_path, dir)
                if os.path.isdir(folder_dir):
                    json_path = os.path.join(folder_dir, "Batch_{:03d}_{}.json".format(index, dir))
                    single_nft_json = json.load(open(json_path))
                    char_items = single_nft_json["CharacterItems"]
                    characters += 1
                    for slot in char_items.keys():
                        item_info = char_items[slot]
                        if item_info != "Null":
                            item = item_info[list(item_info)[0]]["item_texture"]

                            if item:
                                variant_name = item.split('_')[3] + ' ' + item.split('_')[4]
                                counter[variant_name]["count"] = counter[variant_name]["count"] + 1
                            else:
                                print(f"{config.bcolors.ERROR}THIS ITEM ({list(item_info)[0]}) IS MISSING TEXTURE SETS{config.bcolors.RESET}")

            
    counter_sorted = {k: v for k, v in sorted(counter.items(), key=lambda item: -item[1]["count"])}

    counter_info = {}
    counter_info["Total Characters"] = characters
    counter_info["Items"] = counter_sorted

    counter_obj = json.dumps(counter_info, indent=1, ensure_ascii=True)
    with open(save_path, "w") as outfile:
        outfile.write(counter_obj)

    return


def SaveBlenderFile():
    print("This should save blender file")
    #bpy.ops.wm.save_as_mainfile(filepath=batch_json_save_path+".blend")

if __name__ == '__main__':
    SaveNFT()
