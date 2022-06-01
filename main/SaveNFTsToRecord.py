# Purpose:
# This file sorts the NFT DNA from NFTRecord.json and exports it to a given number of Batch#.json files set by nftsPerBatch
# in config.py.

import bpy
import os
import json
import shutil
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


def delete_hierarchy(parent_col):
    # Go over all the objects in the hierarchy like @zeffi suggested:
    def get_child_names(obj):
        for child in obj.children:
            if child.name != "Script_Ignore":
                if child.children:
                    get_child_names(child)
                for obj in child.objects:
                    bpy.data.objects.remove(obj, do_unlink=True)       
                bpy.data.collections.remove(child)
    get_child_names(parent_col)


def CreateSlotsFolderHierarchy(save_path):
    #Clears scene and delets all hirachy except for ignore folder
    delete_hierarchy(bpy.context.scene.collection)
    bpy.ops.outliner.orphans_purge()

    slots_path = CheckAndFormatPath(save_path, "INPUT/SLOTS")
    if(slots_path != ""):
        for slot in os.listdir(slots_path):
            type_path = CheckAndFormatPath(slots_path, slot)
            if type_path != "":
                #Create slot type collection and link to scene
                slot_coll = bpy.data.collections.new(slot)
                bpy.context.scene.collection.children.link(slot_coll)

                #Set Up NUll texture slot
                slot_col_type = bpy.data.collections.new("00-" + slot.partition('-')[2] + "Null" )
                slot_coll.children.link(slot_col_type)
                slot_col_var = bpy.data.collections.new(slot.partition('-')[2] + "_" + slot_col_type.name.partition('-')[2] + "_000_" + "Null" )
                slot_col_type.children.link(slot_col_var)
                
                tex_object = bpy.context.scene.objects["BLANK"].copy()
                tex_object.data = bpy.context.scene.objects["BLANK"].data.copy()
                tex_object.hide_viewport = True
                tex_object.hide_render = True
                slot_col_type.objects.link(tex_object)
                characterCollectionDict = {}
                for char in config.Characters:
                    varient_coll_char = bpy.data.collections.new(slot.partition('-')[2] + "_" + slot_col_type.name.partition('-')[2]+ "_000_" + "Null_"  + char)
                    characterCollectionDict[char] = varient_coll_char
                    new_object = bpy.context.scene.objects["BLANK"].copy()
                    new_object.data = bpy.context.scene.objects["BLANK"].data.copy()                                                
                    varient_coll_char.objects.link(new_object)
                    varient_coll_char.hide_viewport = True
                    varient_coll_char.hide_render = True
                    #new_object.material_slots[0].material = tex_object.material_slots[0].material
                    slot_col_var.children.link(varient_coll_char)
                    
                # varient_coll_texture = bpy.data.collections.new(slot.partition('-')[2] + "_" + slot_col_type.name.partition('-')[2] + "_000_" + "Null_" +  "A000")
                # slot_col_var.children.link(varient_coll_texture)
                # for char in config.Characters:
                #     char_tex_col = characterCollectionDict[char].copy()
                #     char_tex_col.name = varient_coll_texture.name + "_" + char 
                #     varient_coll_texture.children.link(char_tex_col)

                # for char in config.Characters:
                #     bpy.data.collections.remove(characterCollectionDict[char])



                #Move on to types and varients if they exsist
                for type in os.listdir(type_path):                
                    varient_path = CheckAndFormatPath(type_path, type)
                    if varient_path != "":
                        #create varient collection and link to slot
                        type_coll = bpy.data.collections.new(type)
                        slot_coll.children.link(type_coll)
                        for varient in os.listdir(varient_path):             
                            item_path = CheckAndFormatPath(varient_path, varient)
                            if item_path != "":
                                print(varient)
                                varient_coll = bpy.data.collections.new(varient)
                                varient_coll.hide_viewport = True
                                varient_coll.hide_render = True
                                type_coll.children.link(varient_coll)

                                for file in os.listdir(item_path):
                                    if file.rpartition('.')[2] == "blend":
                                        directory = os.path.join(item_path, file, "Collection")
                                        directory = directory.replace('\\', '/')
                                        characterCollectionDict = {}
                                        for char in config.Characters:
                                            varient_coll_char = bpy.data.collections.new(varient + "_" + char)
                                            varient_coll.children.link(varient_coll_char)
                                            characterCollectionDict[char] = varient_coll_char
                                            varient_coll_char.hide_viewport = True
                                            varient_coll_char.hide_render = True
                                        file_path = ""
                                        file_path = os.path.join(directory, "Item")
                                        file_path = file_path.replace('\\', '/') 
                                        #bpy.ops.wm.append(filepath='//EMPIRE/Empire/INTERACTIVE_PROJECTS/SOUL_AETHER/3D_PRODUCTION/SLOTS/01-Uppertorso/CropTops/Uppertorso_Croptops_beltedCrop_001/uppertorso_crop01_001.blend/Collection/Import', directory='//EMPIRE/Empire/INTERACTIVE_PROJECTS/SOUL_AETHER/3D_PRODUCTION/SLOTS/01-Uppertorso/CropTops/Uppertorso_Croptops_beltedCrop_001/uppertorso_crop01_001.blend/Collection/', filename="Import")
                                        tempHolder = bpy.data.collections.new("tempHolder")
                                        bpy.context.scene.collection.children.link(tempHolder)
                                        layer_collection = bpy.context.view_layer.layer_collection.children[tempHolder.name]
                                        bpy.context.view_layer.active_layer_collection = layer_collection

                                        bpy.ops.wm.append(filepath=file_path, directory=directory, filename="Item", active_collection=True, autoselect=True )

                                        if len(bpy.context.selected_objects) > 0:
                                            #goes through the temp holder collection created and finds children imported and unlink objs from them
                                            for obj in bpy.context.selected_objects:
                                                if obj.type == "ARMATURE":
                                                    bpy.data.objects.remove(obj, do_unlink=True)

                                        for item in tempHolder.children:
                                            if item.name == "Item":
                                                for char in item.children:
                                                    print(char.name)
                                                    for obj in char.objects:
                                                        print(obj.name)
                                                        for c in config.Characters:
                                                            if char.name.partition(".")[0] == c:
                                                                print(c)
                                                                characterCollectionDict[c].objects.link(obj)
                                                                obj.hide_viewport = True
                                                                obj.hide_render =  True
                                                                if obj.modifiers:
                                                                    for mod in obj.modifiers:
                                                                        if mod.type == 'SUBSURF':
                                                                            print(obj.name)
                                                                            mod.show_viewport = False

                                        texture_path = CheckAndFormatPath(item_path, "Textures")
                                        if(texture_path != ""):
                                            index = 0
                                            for texture_set in os.listdir(texture_path):
                                                set_path = CheckAndFormatPath(texture_path, texture_set)
                                                if(set_path != ""):
                                                    tex_object = bpy.context.scene.objects["BLANK"].copy()
                                                    tex_object.data = bpy.context.scene.objects["BLANK"].data.copy()
                                                    tex_object.name = varient + "_" + texture_set
                                                    varient_coll.objects.link(tex_object)
                                                    SetUpObjectMaterialsAndTextures(tex_object, set_path, characterCollectionDict) 
                                                    #Remove base children objects used as a way to easily copy to texture varients
                                                    # for char in config.Characters:                                     
                                                    #     for childObj in characterCollectionDict[char].objects: 
                                                    #         for i in range(0, len(tex_object.material_slots)):
                                                    #             if childObj.material_slots[i]: 
                                                    #                 print("Material SHould exsists")                                                                 
                                                    #                 childObj.material_slots[i].material = tex_object.material_slots[i].material
                                                    #             else:
                                                    #                 childObj.data.materials.append(tex_object.material_slots[i].material)
                                                    #                 print("NO MATWRIAL SLOT TO EDIT SO ADDING ONE")
                                                    tex_object.hide_viewport = True
                                                    tex_object.hide_render = True
                                                    index += 1
                                            for child_col in tempHolder.children:
                                                for child_obj in child_col.objects:
                                                    child_col.objects.unlink(child_obj)
                                                bpy.data.collections.remove(child_col)                                    
                                            bpy.data.collections.remove(tempHolder)
                                            bpy.ops.outliner.orphans_purge() 

                                        else:
                                            print("No Textures" + varient)
                                            for child_col in tempHolder.children:
                                                for child_obj in child_col.objects:
                                                    child_col.objects.unlink(child_obj)
                                                bpy.data.collections.remove(child_col)                                    
                                            bpy.data.collections.remove(tempHolder)
                                            bpy.ops.outliner.orphans_purge()

                                        


    # color_path = CheckAndFormatPath(set_path, "ColorInfo.json")
    # if(color_path != ""):
    #     ColorInfo = json.load(open(color_path))
    #     availableSets = list(ColorInfo.values())[0]
        
    #     for color_tex_varient in availableSets:
    #         print(color_tex_varient)
    #         varient_texture_set = bpy.data.collections.new(varient + "_" + texture_set + color_tex_varient)
    #         global_color_path = CheckAndFormatPath(save_path, "INPUT/GlobalColorList.json")
    #         globalColorInfo = json.load(open(global_color_path))
    #         print(globalColorInfo[color_tex_varient])
    #         #varient_texture_set["color_style"] = ColorInfo[color_tex_varient]["ComonName"]
    #         varient_texture_set["color_style"] = globalColorInfo[color_tex_varient]["ComonName"]
    #         varient_texture_set["color_primary"] = globalColorInfo[color_tex_varient]["R"]
    #         varient_texture_set["color_secondary"] =  globalColorInfo[color_tex_varient]["G"]
    #         varient_texture_set["color_tertiary"] = globalColorInfo[color_tex_varient]["B"]
    #         varient_coll.children.link(varient_texture_set)
    #         for char in list(characterCollectionDict.keys()):
    #             col = bpy.data.collections.new(varient + "_" + texture_set + color_tex_varient + "_" + char)
    #             varient_texture_set.children.link(col)

    return

def SetUpObjectMaterialsAndTextures(obj, texture_path, characterCol): 
    materialSets = next(os.walk(texture_path))[1] 
    if len(materialSets) > 0:
        mats = set()
        for char in config.Characters:                                     
            for childObj in characterCol[char].objects: 
                for i in range(0, len(childObj.material_slots)):
                    if childObj.material_slots[i]:                                                                  
                        if childObj.material_slots[i].material not in mats:
                            mats.add(childObj.material_slots[i].material)
        matfolderlink = {}
        for mat in mats:
            for matset in materialSets:
                if matset.partition("_")[0] == mat.name.partition("_")[0]:
                    matfolderlink[mat.name] = matset
        i = 0
        for m in matfolderlink.keys():         
            if i >= len(obj.material_slots):
                result = [s for s in os.listdir(texture_path) if "_O." in s]
                if result != []:
                    material = bpy.data.materials['MasterTransparentV01']
                else:
                    material = bpy.data.materials['MasterV01']
                tempcopy = material.copy()
                tempcopy.name = m
                # bpy.data.objects[obj.name].select_set(True)
                # bpy.ops.object.material_slot_add()
                # bpy.ops.material.new()
                # obj.material_slots[i].link = 'OBJECT'
                # #bpy.ops.object.material_slot_remove()
                # bpy.data.objects[obj.name].select_set(False)
                obj.data.materials.append(None)
                #obj.material_slots[i].link = 'OBJECT'
                obj.material_slots[i].material = tempcopy
                tempcopy.name = m
                #obj.data.materials.pop(index = i) 
            else:
                print("Slot Exists")
                result = [s for s in os.listdir(texture_path) if "_O." in s]
                if result != []:
                    material = bpy.data.materials['MasterTransparentV01']
                else:
                    material = bpy.data.materials['MasterV01']
                tempcopy = material.copy()
                tempcopy.name = m
                #obj.material_slots[i].link = 'OBJECT'
                obj.material_slots[i].material = tempcopy
                tempcopy.name = m     
    
            # material = bpy.data.materials['MasterV01']
            # material.use_nodes = True
            # matcopy = material.copy()
            # matcopy.name = m
            LinkImagesToNodes(tempcopy, os.path.join(texture_path, matfolderlink[m]))
            i += 1
    else:
        material_slots = obj.material_slots
        for m in material_slots:
            #material = m.material
            #m.link = 'OBJECT' 
            result = [s for s in os.listdir(texture_path) if "_O." in s]
            if result != []:
                material = bpy.data.materials['MasterTransparentV01']
            else:
                material = bpy.data.materials['MasterV01']
            material.use_nodes = True
            matcopy = material.copy()
            m.material = matcopy
            LinkImagesToNodes(matcopy, texture_path)
    
    
    # for i in reversed(range(0, len(obj.material_slots))):
    #     if obj.material_slots[i].link != 'OBJECT':
    #         print("Deleting: " + str(i))
    #         obj.material_slots[i].link = 'OBJECT'
    #         #obj.data.materials.pop(index = i)
    

def LinkImagesToNodes(matcopy, texture_path):
        # get the nodes
        
        for tex in os.listdir(texture_path):      
            mapType = tex.rpartition("_")[2]
            print(mapType)
            mapType = mapType.partition(".")[0]
            print('TEXTURE IS: ' + mapType)
            if "D" == mapType:
                file = os.path.join(texture_path, tex)
                file = file.replace('/', '\\')
                newImage = bpy.data.images.load(file, check_existing=False)
                matcopy.node_tree.nodes["DiffuseNode"].image = newImage
                matcopy.node_tree.nodes["DiffuseMix"].outputs["Value"].default_value = 1

            if "N" == mapType:
                file = os.path.join(texture_path, tex)
                file = file.replace('/', '\\')
                newImage = bpy.data.images.load(file, check_existing=False)
                matcopy.node_tree.nodes["NormalNode"].image = newImage
                matcopy.node_tree.nodes["NormalNode"].image.colorspace_settings.name = 'Raw'
                matcopy.node_tree.nodes["NormalMix"].outputs["Value"].default_value = 1
            if "ID" == mapType:
                file = os.path.join(texture_path, tex)
                file = file.replace('/', '\\')
                newImage = bpy.data.images.load(file, check_existing=False)
                matcopy.node_tree.nodes["ColorIDNode"].image = newImage
                matcopy.node_tree.nodes["ColorIDNode"].image.colorspace_settings.name = 'Linear'
                matcopy.node_tree.nodes["ColorID_RGBMix"].outputs["Value"].default_value = 1

            if "M" == mapType:
                file = os.path.join(texture_path, tex)
                file = file.replace('/', '\\')
                newImage = bpy.data.images.load(file, check_existing=False)
                matcopy.node_tree.nodes["MetallicNode"].image = newImage
                matcopy.node_tree.nodes["MetallicNode"].image.colorspace_settings.name = 'Linear'
                matcopy.node_tree.nodes["MetallicMix"].outputs["Value"].default_value = 1

            if "R" == mapType:
                file = os.path.join(texture_path, tex)
                file = file.replace('/', '\\')
                newImage = bpy.data.images.load(file, check_existing=False)
                matcopy.node_tree.nodes["RoughnessNode"].image = newImage
                matcopy.node_tree.nodes["RoughnessNode"].image.colorspace_settings.name = 'Linear'
                matcopy.node_tree.nodes["RoughnessMix"].outputs["Value"].default_value = 1

            if "E" == mapType:
                file = file = os.path.join(texture_path, tex)
                file = file.replace('/', '\\')
                newImage = bpy.data.images.load(file, check_existing=False)
                matcopy.node_tree.nodes["EmissiveNode"].image = newImage 
                matcopy.node_tree.nodes["EmissiveMix"].outputs["Value"].default_value = 1

            if "O" == mapType:
                file = file = os.path.join(texture_path, tex)
                file = file.replace('/', '\\')
                newImage = bpy.data.images.load(file, check_existing=False)
                matcopy.node_tree.nodes["OpacityNode"].image = newImage 
                matcopy.node_tree.nodes["OpacityNode"].image.colorspace_settings.name = 'Linear'
                matcopy.node_tree.nodes["OpacityMix"].outputs["Value"].default_value = 1
            # if node.label == "RTint":
            #     node.outputs["Color"].default_value = parent["color_primary"]


def CheckAndFormatPath(path, pathTojoin = ""):
    if pathTojoin != "" :
        path = os.path.join(path, pathTojoin)

    new_path = path.replace('\\', '/')

    if not os.path.exists(new_path):
        return ""

    return new_path


# def SearchForMeshesAndCreateCharacterDuplicates(record_save_path):
#     DataDictionary = json.load(open(record_save_path))
#     hierarchy = DataDictionary["hierarchy"]

#     slots = list(hierarchy.keys())
#     for slot in slots:
#         types = list(hierarchy[slot].keys())
#         for type in types:
#             variants = list(hierarchy[slot][type].keys())
#             for variant in variants:
#                 kae_variant = variant + "_" + config.Characters[0]
#                 if bpy.data.collections.get(kae_variant) is None:
#                     original_meshes = bpy.data.collections[variant].objects
#                     for character in config.Characters:
#                         char_coll_name = variant + '_' + character
#                         char_coll = bpy.data.collections.new(char_coll_name)
#                         bpy.data.collections[variant].children.link(char_coll)
#                         print(original_meshes)
#                         for mesh in original_meshes:
#                             new_mesh = bpy.data.objects[mesh.name].copy()
#                             char_coll.objects.link(new_mesh)
#                             mat_slots = new_mesh.material_slots
#                             for m in mat_slots:
#                                 material = bpy.data.materials['MasterV01']
#                                 material.use_nodes = True
#                     for og_mesh in original_meshes:
#                         og_mesh.hide_render = True
#                         og_mesh.hide_viewport = True
#     return


# def SearchForTexturesAndCreateDuplicates(save_path):
#     slots_path = os.path.join(save_path, "INPUT")
#     slots_path = os.path.join(slots_path, "Slots")
    
#     for slot in os.listdir(slots_path):
#         type_path = os.path.join(slots_path, slot)
#         for type in os.listdir(type_path):
#             varient_path = os.path.join(type_path, type)
#             for varient in os.listdir(varient_path):
#                 texture_path = os.path.join(varient_path, varient)
#                 texture_path = os.path.join(texture_path, "Textures")
                
#                 Kae = None
#                 Nef = None
#                 Rem =  None

#                 for col in bpy.data.collections[varient].children:
#                     name = col.name.rpartition('_')[2]
#                     if name in config.Characters:
#                         if name == "Kae": 
#                             Kae =  col
#                         elif name == "Nef":
#                             Nef = col
#                         elif name == "Rem":
#                             Rem = col
#                     else:                    
#                         for obj in col.objects:
#                             bpy.data.objects.remove(obj, do_unlink=True)
#                         bpy.data.collections.remove(col)

#                 for texture in os.listdir(texture_path):
#                     print(texture)
#                     print(varient)
#                     splitName = varient.rpartition('_')
#                     texture_collection_name = splitName[0] + texture + splitName[1] + splitName[2]
#                     collection = bpy.data.collections.new(texture_collection_name)
#                     bpy.data.collections[varient].children.link(collection)
#                     texture_set = os.path.join(texture_path, texture)
#                     for character in config.Characters:
#                         if bpy.data.collections.get(varient + "_" + character ) != None:
#                             DuplicateChildrenMaterials(bpy.data.collections[varient + "_" + character ], collection, texture_set)


# def DuplicateChildrenMaterials(originalCollection, newParentCollection, texture_set):
#     collection = bpy.data.collections.new(newParentCollection.name + originalCollection.name.rpartition('_')[1] + originalCollection.name.rpartition('_')[2] )
#     bpy.data.collections[newParentCollection.name].children.link(collection)
#     for child in originalCollection.objects:
#         print(child.name)
#         ob = bpy.data.objects[child.name].copy()
#         collection.objects.link(ob)

#         material_slots = ob.material_slots
#         for m in material_slots:
#             #material = m.material
#             material = bpy.data.materials['MasterV01']
#             material.use_nodes = True
#             matcopy = material.copy()
#             m.material = matcopy
#             #m.material = bpy.data.materials['Test_02']
#             # get the nodes
            
#             for node in material.node_tree.nodes:
#                 if (node.label == "Diffuse"):
#                     for tex in os.listdir(texture_set):
#                         if "_D_" in tex:
#                             file = file = os.path.join(texture_set, tex)
#                             print(file)
#                             file = file.replace('\\', '/')
#                             print(file)
#                             newImage = bpy.data.images.load(file, check_existing=True)
#                             node.image = newImage
#                         elif "_N_" in tex:
#                             file = file = os.path.join(texture_set, tex)
#                             file = file.replace('\\', '/')
#                             newImage = bpy.data.images.load(file, check_existing=True)
#                             node.image = newImage




def SaveBlenderFile():
    print("This should save blender file")
    #bpy.ops.wm.save_as_mainfile(filepath=batch_json_save_path+".blend")

if __name__ == '__main__':
    SaveNFT()
