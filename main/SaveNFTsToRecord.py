import bpy
import os
import json
import shutil
from . import config


def SaveNFTs(DNASetToAdd, NFTDict, single_batch_save_path, batch_index, master_record_save_path): 
    single_record_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{}".format(batch_index), "_NFTRecord_{}.json".format(batch_index))
    DataDictionary = json.load(open(single_record_path))
    single_i = int(DataDictionary["numNFTsGenerated"])
    MasterDictionary = json.load(open(master_record_save_path))
    totalDNAList = MasterDictionary["DNAList"]
    character_count = [0] * len(config.Characters)

    uniqueDNASetToAdd = []
    for nft in DNASetToAdd:
        if nft not in totalDNAList:
            singleNFT = {}
            if len(DNASetToAdd) == 1:
                singleNFT["Handmade"] = bpy.context.scene.my_tool.handmadeBool
            else:
                singleNFT["Handmade"] = False
            singleNFT["CharacterItems"] = NFTDict[nft]
            singleNFT["DNAList"] = nft
            singleNFTObject = json.dumps(singleNFT, indent=1, ensure_ascii=True)
            if not os.path.exists(os.path.join(single_batch_save_path, "NFT_{}".format(single_i + 1))):
                os.mkdir(os.path.join(single_batch_save_path, "NFT_{}".format(single_i + 1)))
            with open(os.path.join(single_batch_save_path, "NFT_{}".format(single_i + 1), ("Batch_{}_NFT_{}.json".format(batch_index, single_i + 1))), "w") as outfile:
                outfile.write(singleNFTObject)
            single_i += 1
            uniqueDNASetToAdd.append(nft)
            character = nft.partition(",")[0]
            char_index = config.Characters.index(character)
            character_count[char_index] += 1

    if uniqueDNASetToAdd:
        UpdateNFTRecord(uniqueDNASetToAdd, character_count, DataDictionary, single_record_path, master_record_save_path)
        config.custom_print(("{} NFTs have been saved (ノಠ vಠ)ノ彡( {}o)".format(len(uniqueDNASetToAdd), "o°"*len(uniqueDNASetToAdd))), col=config.bcolors.OK)
        return True
    else:
        config.custom_print("ERROR: This NFT(s) already exists", col=config.bcolors.ERROR)
        return False


def UpdateNFTRecord(DNASetToAdd, CharacterCount, DataDictionary, single_record_path, master_record_save_path): 
    # This should update record.json with new nft DNA and number
    # Also updates nft/character counts
    updatedMasterDictionary = {}
    MasterDictionary = json.load(open(master_record_save_path))
    updatedMasterDictionary["numNFTsGenerated"] = int(MasterDictionary["numNFTsGenerated"]) + len(DNASetToAdd)
    totalDNASet = MasterDictionary["DNAList"]

    numMasterCharDict = {}
    numSingleCharDict = {}

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
        config.custom_print("Success update {}".format(single_record_path), col=config.bcolors.OK)
    except:
        config.custom_print("Failed to update {}".format(single_record_path), col=config.bcolors.ERROR)

    try:
      ledger = json.dumps(updatedMasterDictionary, indent=1, ensure_ascii=True)
      with open(master_record_save_path, 'w') as outfile:
        outfile.write(ledger + '\n')
        config.custom_print("Success update {}".format(master_record_save_path), col=config.bcolors.OK)
    except:
        config.custom_print("Failed to update {}".format(master_record_save_path), col=config.bcolors.ERROR)



def OverrideNFT(DNAToAdd, NFTDict, batch_save_path, batch_index, nft_index, master_record_save_path): # save over existing nft
    single_record_save_path = os.path.join(batch_save_path, "_NFTRecord_{}.json".format(batch_index))
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
        config.custom_print("Success update {}".format(single_record_save_path), col=config.bcolors.OK)
    except:
        config.custom_print("Failed to update {}".format(single_record_save_path), col=config.bcolors.ERROR)
    singleNFT = {}
    singleNFT["DNAList"] = DNAToAdd
    singleNFT["CharacterItems"] = NFTDict[DNAToAdd]
    singleNFT["Handmade"] = bpy.context.scene.my_tool.handmadeBool
    singleNFTObject = json.dumps(singleNFT, indent=1, ensure_ascii=True)
    with open(os.path.join(batch_save_path, "NFT_{}".format(nft_index), ("Batch_{}_NFT_{}.json".format(batch_index, nft_index))), "w") as outfile:
        outfile.write(singleNFTObject)

    updatedMasterObject = json.dumps(updatedMasterDictionary, indent=1, ensure_ascii=True)
    with open(master_record_save_path, "w") as outfile:
        outfile.write(updatedMasterObject)
    return True


#------------------------------------------------------------


def DeleteNFTsinRange(start, end, TotalDNA, save_path, batch_index, master_record_save_path):
    if start > end or start > len(TotalDNA):
        config.custom_print("This is not a valid range. Nothing was deleted", col=config.bcolors.WARNING)
        return
    if end > len(TotalDNA):
        end = len(TotalDNA)
        config.custom_print("This is out of range. New range deleted is {} ~ {}".format(start, end), col=config.bcolors.WARNING)
    for index in range(end, start - 1, -1):
        DNA = TotalDNA[index - 1]
        DeleteNFT(DNA, save_path, batch_index, master_record_save_path)
    config.custom_print("NFTs from {} ~ {} (total {}) deleted".format(start, end, str(end - start + 1)), col=config.bcolors.OK)
    return


def DeleteAllNFTs(TotalDNA, save_path, batch_index, master_record_save_path):
    for index in range(len(TotalDNA), 0, -1):
        DNA = TotalDNA[index - 1]
        DeleteNFT(DNA, save_path, batch_index, master_record_save_path)
    return


def DeleteNFT(DNAToDelete, save_path, batch_index, master_record_save_path):
    NFTRecord_save_path = os.path.join(save_path, "_NFTRecord_{}.json".format(batch_index))
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
    if DNAToDelete in DNAList: # goes through each dna, deletes, updates indices, then goes to next dna
        DNA_index = DNAList.index(DNAToDelete) + 1
        DNAList.remove(DNAToDelete)
        updatedDictionary["DNAList"] = DNAList
        try:
            ledger = json.dumps(updatedDictionary, indent=1, ensure_ascii=True)
            with open(NFTRecord_save_path, 'w') as outfile:
                outfile.write(ledger + '\n')
                config.custom_print("Success update {}".format(NFTRecord_save_path))
            UpdateSingleNFTFileIndex(DNA_index, save_path, batch_index)

            totalDNAList = MasterDictionary["DNAList"]
            totalDNAList.remove(DNAToDelete)
            updatedMasterDictionary["DNAList"] = totalDNAList

            ledger = json.dumps(updatedMasterDictionary, indent=1, ensure_ascii=True)
            with open(master_record_save_path, 'w') as outfile:
                outfile.write(ledger + '\n')
                config.custom_print("Success update {}".format(master_record_save_path))
        except:
            config.custom_print("Failed to update {}".format(master_record_save_path))
    else:
        config.custom_print("smth went wrong :^(")
    return DNA_index


def UpdateSingleNFTFileIndex(DNA_index, save_path, batch_index): # updates index of nft files after deletion
    total_nfts = len(next(os.walk(save_path))[1])
    nft_save_path = os.path.join(save_path, "NFT_{}".format(DNA_index))
    shutil.rmtree(nft_save_path)
    for i in range(DNA_index + 1, total_nfts + 1): # nfts from records should not be deleted after rendering starts
        old_nft_save_path = os.path.join(save_path, "NFT_{}".format(i), "Batch_{}_NFT_{}.json".format( batch_index, i))
        new_nft_save_path = os.path.join(save_path, "NFT_{}".format(i-1), "Batch_{}_NFT_{}.json".format( batch_index, i-1))
        new_folder_path = os.path.join(save_path, "NFT_{}".format(i-1))

        os.mkdir(new_folder_path)
        os.rename(old_nft_save_path, new_nft_save_path)
        shutil.rmtree(os.path.join(save_path, "NFT_{}".format(i)))
    return



if __name__ == '__main__':
    SaveNFTs()
