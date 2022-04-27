# Purpose:
# This file sorts the NFT DNA from NFTRecord.json and exports it to a given number of Batch#.json files set by nftsPerBatch
# in config.py.

from doctest import master
import bpy
import os
import json
import random
import shutil

def SaveNFT(DNASetToAdd, NFTDict, single_batch_save_path, batch_index, master_record_save_path):
    single_record_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{:03d}".format(batch_index), "_NFTRecord_{:03d}.json".format(batch_index))

    DataDictionary = json.load(open(single_record_path))
    single_i = int(DataDictionary["numNFTsGenerated"])
    hierarchy = DataDictionary["hierarchy"]
    
    MasterDictionary = json.load(open(master_record_save_path))
    totalDNAList = MasterDictionary["DNAList"]

    uniqueDNASetToAdd = []
    for nft in DNASetToAdd:
        if nft not in totalDNAList:
            singleNFT = {}
            singleNFT["DNAList"] = nft 
            singleNFT["CharacterItems"] = NFTDict[nft]

            singleNFTObject = json.dumps(singleNFT, indent=1, ensure_ascii=True)
            if not os.path.exists(os.path.join(single_batch_save_path, "NFT_{:04d}".format(single_i + 1))):
                os.mkdir(os.path.join(single_batch_save_path, "NFT_{:04d}".format(single_i + 1)))
            with open(os.path.join(single_batch_save_path, "NFT_{:04d}".format(single_i + 1), ("Batch_{:03d}_NFT_{:04d}.json".format(batch_index, single_i + 1))), "w") as outfile:
                outfile.write(singleNFTObject)
            single_i += 1
            uniqueDNASetToAdd.append(nft)

    if uniqueDNASetToAdd:
        UpdateNFTRecord(uniqueDNASetToAdd, DataDictionary, single_record_path, master_record_save_path)
        return True
    else:
        print("ERROR: This NFT(s) already exists")
        return False

def UpdateNFTRecord(DNASetToAdd, DataDictionary, single_record_path, master_record_save_path):
    print("This should updated record.json with new nft DNA and number")

    updatedMasterDictionary = {}
    MasterDictionary = json.load(open(master_record_save_path))
    updatedMasterDictionary["numNFTsGenerated"] = int(MasterDictionary["numNFTsGenerated"]) + len(DNASetToAdd)
    totalDNASet = MasterDictionary["DNAList"]

    currentNFTNumber = DataDictionary["numNFTsGenerated"]
    currentDNASet = DataDictionary["DNAList"]

    updatedDataDictionary = {}
    updatedDataDictionary["numNFTsGenerated"] = int(currentNFTNumber) + len(DNASetToAdd)
    updatedDataDictionary["hierarchy"] = DataDictionary["hierarchy"]
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
        return False

    updatedDictionary = {}
    updatedDictionary["hierarchy"] = DataDictionary["hierarchy"]
    updatedDictionary["numNFTsGenerated"] = DataDictionary["numNFTsGenerated"]


    DNAList = DataDictionary["DNAList"]
    oldDNA = DNAList[nft_index - 1]
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



def DeleteNFT(DNAToDelete, save_path, batch_index, master_record_save_path):
    NFTRecord_save_path = os.path.join(save_path, "_NFTRecord_{:03d}.json".format(batch_index))
    DataDictionary = json.load(open(NFTRecord_save_path))
    MasterDictionary = json.load(open(master_record_save_path))

    updatedDictionary = {}
    updatedDictionary["numNFTsGenerated"] = DataDictionary["numNFTsGenerated"] - 1

    updatedMasterDictionary = {}
    updatedMasterDictionary["numNFTsGenerated"] = MasterDictionary["numNFTsGenerated"] - 1

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
                print("Success update {}".format(NFTRecord_save_path))
            UpdateSingleNFTFileIndex(DNAToDelete, DNA_index, save_path, batch_index)

            totalDNAList = MasterDictionary["DNAList"]
            totalDNAList.remove(DNAToDelete)
            updatedMasterDictionary["DNAList"] = totalDNAList

            ledger = json.dumps(updatedMasterDictionary, indent=1, ensure_ascii=True)
            with open(master_record_save_path, 'w') as outfile:
                outfile.write(ledger + '\n')
                print("Success update {}".format(updatedMasterDictionary))
        except:
            print("Failed to update .json file")

    else:
        print("smth went wrong :^(")
    return DNA_index


def UpdateSingleNFTFileIndex(DNAToDelete, DNA_index, save_path, batch_index):
    total_nfts = len(os.listdir(save_path)) - 1 # TODO
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


def CreateSlotsFolderHierarchy(save_path):
    input_path = os.path.join(save_path, "INPUT")

    texture_path = os.path.join(input_path, "Textures")
    if not os.path.exists(texture_path):
        os.makedirs(texture_path)

    slots_path = os.path.join(input_path, "Slots")
    if os.path.exists(slots_path):
        try:
            shutil.rmtree(slots_path)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))

    os.makedirs(slots_path)

    batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(1), "_NFTRecord_{:03d}.json".format(1))
    DataDictionary = json.load(open(NFTRecord_save_path))
    hierarchy = DataDictionary["hierarchy"]



    h_keys = list(hierarchy.keys())
    for attribute in h_keys:
        att_path = os.path.join(slots_path, attribute)
        os.makedirs(att_path)
        for type in list(hierarchy[attribute].keys()):
            type_path = os.path.join(att_path, type)
            os.makedirs(type_path)
            for variant in list(hierarchy[attribute][type].keys()):
                variant_path = os.path.join(type_path, variant)
                os.makedirs(variant_path)
                os.makedirs(variant_path + "\Textures")
    return

def SearchForTexturesAndCreateDuplicates(save_path):
    slots_path = os.path.join(save_path, "INPUT")
    slots_path = os.path.join(slots_path, "Slots")
    
    for slot in os.listdir(slots_path):
        type_path = os.path.join(slots_path, slot)
        for type in os.listdir(type_path):
            varient_path = os.path.join(type_path, type)
            for varient in os.listdir(varient_path):
                texture_path = os.path.join(varient_path, varient)
                texture_path = os.path.join(texture_path, "Textures")
                
                for col in bpy.data.collections[varient].children:
                
                    for obj in col.objects:
                        bpy.data.objects.remove(obj, do_unlink=True)
                        
                    bpy.data.collections.remove(col)

                for texture in os.listdir(texture_path):
                    print(texture)
                    print(varient)
                    collection = bpy.data.collections.new(varient + texture)
                    bpy.data.collections[varient].children.link(collection)
                    for child in bpy.data.collections[varient].objects:
                        print(child.name)
                        ob = bpy.data.objects[child.name].copy()
                        collection.objects.link(ob)

                        material_slots = ob.material_slots
                        for m in material_slots:
                            #material = m.material
                            material = bpy.data.materials['Master']
                            material.use_nodes = True
                            matcopy = material.copy()
                            m.material = matcopy
                            #m.material = bpy.data.materials['Test_02']
                            # get the nodes
                            

                            for node in material.node_tree.nodes:
                                if (node.label == "Diffuse"):
                                    texture_set = os.path.join(texture_path, texture)
                                    for tex in os.listdir(texture_set):
                                        if "_D_" in tex:
                                            file = file = os.path.join(texture_set, tex)
                                            file = file.replace('\\', '/')
                                            newImage = bpy.data.images.load(file, check_existing=True)
                                            node.image = newImage


                        # textureFiles = os.listdir(textureSetPath)
                        # file = os.path.join(textureSetPath, textureFiles[0])
                        # file = file.replace('\\', '/')
                        # print(textureFiles[0])

                        





def SaveBlenderFile():
    print("This should save blender file")
    #bpy.ops.wm.save_as_mainfile(filepath=batch_json_save_path+".blend")

if __name__ == '__main__':
    SaveNFT()
