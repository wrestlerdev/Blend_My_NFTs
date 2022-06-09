# Purpose:
# This file takes a given Batch created by DNA_Generator.py and tells blender to render the image or export a 3D model to
# the NFT_Output folder.

from doctest import master
from re import L
import bpy
import os
import time
import json
import importlib
import shutil
from datetime import datetime
import subprocess

from . import Previewer
importlib.reload(Previewer)

from . import metaData
importlib.reload(metaData)

enableGeneration = False
colorList = []
generationType = None

class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR


def stripColorFromName(name):
   return "_".join(name.split("_")[:-1])
   
def getBatchData(batchToGenerate, batch_json_save_path):
    """
    Retrieves a given batches data determined by renderBatch in config.py
    """

    file_name = os.path.join(batch_json_save_path, "Batch{}.json".format(batchToGenerate))
    batch = json.load(open(file_name))
    
    NFTs_in_Batch = batch["NFTs_in_Batch"]
    hierarchy = batch["hierarchy"]
    BatchDNAList = batch["BatchDNAList"]

    return NFTs_in_Batch, hierarchy, BatchDNAList

def render_and_save_NFTs(nftName, maxNFTs, batchToGenerate, batch_json_save_path, nftBatch_save_path, enableImages,
                                      imageFileFormat, enableAnimations, animationFileFormat, enableModelsBlender,
                                      modelFileFormat
                                      ):
    """
    Renders the NFT DNA in a Batch#.json, where # is renderBatch in config.py. Turns off the viewport camera and
    the render camera for all items in hierarchy.
    """

    NFTs_in_Batch, hierarchy, BatchDNAList = getBatchData(batchToGenerate, batch_json_save_path)

    time_start_1 = time.time()

    x = 1
    for a in BatchDNAList:
        for i in hierarchy:
            for j in hierarchy[i]:
                if enableGeneration:
                    """
                     Remove Color code so blender recognises the collection
                    """
                    j = stripColorFromName(j)
                bpy.data.collections[j].hide_render = True
                bpy.data.collections[j].hide_viewport = True

        def match_DNA_to_Variant(a):
            """
            Matches each DNA number separated by "-" to its attribute, then its variant.
            """

            listAttributes = list(hierarchy.keys())
            listDnaDecunstructed = a.split('-')
            dnaDictionary = {}

            for i, j in zip(listAttributes, listDnaDecunstructed):
                dnaDictionary[i] = j

            for x in dnaDictionary:
                for k in hierarchy[x]:
                    kNum = hierarchy[x][k]["number"]
                    if kNum == dnaDictionary[x]:
                        dnaDictionary.update({x: k})
            return dnaDictionary

        dnaDictionary = match_DNA_to_Variant(a)
        name = nftName + "_" + str(x)

        print(f"\n{bcolors.OK}|---Generating NFT {x}/{NFTs_in_Batch} ---|{bcolors.RESET}")
        print(f"DNA attribute list:\n{dnaDictionary}\nDNA Code:{a}")

        for c in dnaDictionary:
            collection = dnaDictionary[c]
            if not enableGeneration:
                bpy.data.collections[collection].hide_render = False
                bpy.data.collections[collection].hide_viewport = False

        time_start_2 = time.time()

        batchFolder = os.path.join(nftBatch_save_path, "Batch" + str(batchToGenerate))

        imagePath = os.path.join(batchFolder, "Images", name)
        animationPath = os.path.join(batchFolder, "Animations", name)
        modelPath = os.path.join(batchFolder, "Models", name)

        imageFolder = os.path.join(batchFolder, "Images")
        animationFolder = os.path.join(batchFolder, "Animations")
        modelFolder = os.path.join(batchFolder, "Models")
        metaDataFolder = os.path.join(batchFolder, "BMNFT_metaData")

        # Material handling:
        if enableGeneration:
            for c in dnaDictionary:
                collection = dnaDictionary[c]
                if stripColorFromName(collection) in colorList:
                    colorVal = int(collection.rsplit("_", 1)[1])-1
                    collection = stripColorFromName(collection)
                    bpy.data.collections[collection].hide_render = False
                    bpy.data.collections[collection].hide_viewport = False
                    if generationType == 'color':
                        for activeObject in bpy.data.collections[collection].all_objects: 
                            mat = bpy.data.materials.new("PKHG")
                            mat.diffuse_color = colorList[collection][colorVal]
                            activeObject.active_material = mat
                    if generationType == 'material':
                        for activeObject in bpy.data.collections[collection].all_objects: 
                            activeObject.material_slots[0].material = bpy.data.materials[colorList[collection][colorVal]]
                else:
                    collection = stripColorFromName(collection)
                    bpy.data.collections[collection].hide_render = False
                    bpy.data.collections[collection].hide_viewport = False


        if enableImages:
            print(f"{bcolors.OK}Rendering Image{bcolors.RESET}")

            if not os.path.exists(imageFolder):
                os.makedirs(imageFolder)

            bpy.context.scene.render.filepath = imagePath
            bpy.context.scene.render.image_settings.file_format = imageFileFormat
            bpy.ops.render.render(write_still=True)

        if enableAnimations:
            print(f"{bcolors.OK}Rendering Animation{bcolors.RESET}")
            if not os.path.exists(animationFolder):
                os.makedirs(animationFolder)

            bpy.context.scene.render.filepath = animationPath

            if animationFileFormat == 'MP4':
                bpy.context.scene.render.image_settings.file_format = "FFMPEG"

                bpy.context.scene.render.ffmpeg.format = 'MPEG4'
                bpy.context.scene.render.ffmpeg.codec = 'H264'
                bpy.ops.render.render(animation=True)

            else:
                bpy.context.scene.render.image_settings.file_format = animationFileFormat
                bpy.ops.render.render(animation=True)

        if enableModelsBlender:
            print(f"{bcolors.OK}Generating 3D Model{bcolors.RESET}")
            if not os.path.exists(modelFolder):
                os.makedirs(modelFolder)

            for i in dnaDictionary:
                coll = dnaDictionary[i]

                for obj in bpy.data.collections[coll].all_objects:
                    obj.select_set(True)

            for obj in bpy.data.collections['Script_Ignore'].all_objects:
                obj.select_set(True)

            if modelFileFormat == 'GLB':
                bpy.ops.export_scene.gltf(filepath=f"{modelPath}.glb",
                                          check_existing=True,
                                          export_format='GLB',
                                          use_selection=True)
            if modelFileFormat == 'GLTF_SEPARATE':
                bpy.ops.export_scene.gltf(filepath=f"{modelPath}",
                                          check_existing=True,
                                          export_format='GLTF_SEPARATE',
                                          use_selection=True)
            if modelFileFormat == 'GLTF_EMBEDDED':
                bpy.ops.export_scene.gltf(filepath=f"{modelPath}.gltf",
                                          check_existing=True,
                                          export_format='GLTF_EMBEDDED',
                                          use_selection=True)
            elif modelFileFormat == 'FBX':
                bpy.ops.export_scene.fbx(filepath=f"{modelPath}.fbx",
                                         check_existing=True,
                                         use_selection=True)
            elif modelFileFormat == 'OBJ':
                bpy.ops.export_scene.obj(filepath=f"{modelPath}.obj",
                                         check_existing=True,
                                         use_selection=True)
            elif modelFileFormat == 'X3D':
                bpy.ops.export_scene.x3d(filepath=f"{modelPath}.x3d",
                                         check_existing=True,
                                         use_selection=True)
            elif modelFileFormat == 'STL':
                bpy.ops.export_mesh.stl(filepath=f"{modelPath}.stl",
                                        check_existing=True,
                                        use_selection=True)
            elif modelFileFormat == 'VOX':
                bpy.ops.export_vox.some_data(filepath=f"{modelPath}.vox")

        if not os.path.exists(metaDataFolder):
            os.makedirs(metaDataFolder)

        metaDataDict = {"name": name, "NFT_DNA": a, "NFT_Variants": dnaDictionary}

        jsonMetaData = json.dumps(metaDataDict, indent=1, ensure_ascii=True)

        with open(os.path.join(metaDataFolder, "Data_" + name + ".json"), 'w') as outfile:
            outfile.write(jsonMetaData + '\n')

        print("Completed {} render in ".format(name) + "%.4f seconds" % (time.time() - time_start_2))
        x += 1

    for a in BatchDNAList:
        for i in hierarchy:
            for j in hierarchy[i]:
                if enableGeneration:
                    j = stripColorFromName(j)
                bpy.data.collections[j].hide_render = False
                bpy.data.collections[j].hide_viewport = False

    print(f"\nAll NFTs successfully generated and sent to {nftBatch_save_path}")
    print("Completed all renders in Batch{}.json in ".format(batchToGenerate) + "%.4f seconds" % (time.time() - time_start_1) + "\n")




# -------------------------------- Custom render --------------------------------------
def create_blender_saves(batch_path, batch_num, nft_range):
    

    print(os.listdir(batch_path))
    for i in range(nft_range[0], nft_range[1] + 1):
        file_name = "Batch_{:03d}_NFT_{:04d}.json".format(batch_num, i)
        folder_name = "NFT_{:04d}".format(i)
        folder_path = os.path.join(batch_path, folder_name)
        json_path = os.path.join(folder_path, file_name)
        print(json_path)

        NFTDict = json.load(open(json_path))
        Previewer.show_nft_from_dna(NFTDict["DNAList"], NFTDict["CharacterItems"], True)
        select_hierarchy(bpy.data.collections["Rendering"])
        bpy.data.objects["CameraStill"].select_set(True)
        bpy.data.objects["CameraVideo"].select_set(True)
        blend_name = "Batch_{:03d}_NFT_{:04d}.blend".format(batch_num, i)
        blend_save  = os.path.join(batch_path, "NFT_{:04d}".format(i), blend_name)
        bpy.ops.save_selected.save(filepath=blend_save)
        python_path = os.path.join(bpy.context.scene.my_tool.separateExportPath, "Exporter.py")
        
        blenderExecutable = bpy.app.binary_path
        blenderFolder = blenderExecutable.rpartition("\\")[0] + "\\"
        blenderFolder = '"' + blenderFolder + '"'
        folder_path = folder_path.replace('\\', '/')

        batch_file_path = os.path.join(bpy.context.scene.my_tool.separateExportPath, "ExportBatchSingle.bat")
        batch_script_path = batch_file_path + " " + blenderFolder + " " + blend_save + " " + python_path + " " +  folder_path 
        
        os.system(batch_script_path)
    
def select_hierarchy(parent_col):
    # Go over all the objects in the hierarchy like @zeffi suggested:
    def get_child_names(obj):
        for child in obj.children:
            if child.children:
                get_child_names(child)
            for obj in child.objects:
                obj.select_set(True)       
    get_child_names(parent_col)

def render_nft_batch_custom(save_path, batch_num, file_formats, nft_range, transparency=False):
    folder = os.path.join(save_path, "OUTPUT")
    master_record_path = os.path.join(folder, "_NFTRecord.json")
    MasterDictionary = json.load(open(master_record_path))
    totalDNAList = MasterDictionary["DNAList"]

    if not os.path.exists(folder):
        os.makedirs(folder)

    batch_path = os.path.join(save_path, "OUTPUT", "Batch_{:03d}".format(batch_num))

    for i in range(nft_range[0], nft_range[1] + 1):
        file_name = "Batch_{:03d}_NFT_{:04d}.json".format(batch_num, i)
        json_path = os.path.join(batch_path, "NFT_{:04d}".format(i), file_name)

        for file_format in file_formats:
            if file_format in ['PNG', 'JPEG']:
                camera_name = "CameraStill"
                if bpy.data.objects.get(camera_name) is not None:
                    bpy.context.scene.camera = bpy.data.objects[camera_name]
                else:
                    print("Cannot find camera of name 'CameraStill', will continue with current camera")
                if transparency:
                    color_mode = 'RGBA'
                else:
                    color_mode = 'RGB'
                start_time = time.time()
                nft_name, render_passed = render_nft_single_custom(batch_path, batch_num, i, file_format, color_mode, totalDNAList)
                time_taken = time.time() - start_time
                print(f"{bcolors.OK}Time taken: {bcolors.RESET}" + "{:.2f}".format(time_taken))
                file_type = 'IMAGES'
                send_to_export_log(batch_path, batch_num, json_path, nft_name, file_type, file_format, time_taken, file_name, render_passed)

            elif file_format in ['MP4']:
                camera_name = "CameraVideo"
                if bpy.data.objects.get(camera_name) is not None:
                    bpy.context.scene.camera = bpy.data.objects[camera_name]
                else:
                    print("Cannot find camera of name 'CameraVideo', will continue with current camera")
                start_time = time.time()
                nft_name, render_passed = render_nft_single_video(batch_path, batch_num, i, file_format, totalDNAList)
                time_taken = time.time() - start_time
                print((f"{bcolors.OK}Time taken: {bcolors.RESET}") + "{:.2f}".format(time_taken))
                file_type = 'ANIMATIONS'
                send_to_export_log(batch_path, batch_num, json_path, nft_name, file_type, file_format, time_taken, file_name, render_passed)

            elif file_format in ['FBX', 'GLB']:
                start_time = time.time()
                nft_name, render_passed = render_nft_single_model(batch_path, batch_num, i, file_format, totalDNAList)
                time_taken = time.time() - start_time
                print((f"{bcolors.OK}Time taken: {bcolors.RESET}") + "{:.2f}".format(time_taken))
                file_type = '3DMODELS'
                send_to_export_log(batch_path, batch_num, json_path, nft_name, file_type, file_format, time_taken, file_name, render_passed)
    print((f"{bcolors.OK}Render Finished :^){bcolors.RESET}"))
    return




def render_nft_single_custom(batch_path, batch_num, nft_num, image_file_format, color_mode, totalDNAList):
    file_name = "Batch_{:03d}_NFT_{:04d}.json".format(batch_num, nft_num)
    json_path = os.path.join(batch_path, "NFT_{:04d}".format(nft_num), file_name)
    SingleDict = json.load(open(json_path))

    DNA = SingleDict["DNAList"]
    NFTDict = SingleDict["CharacterItems"]
    total_index = totalDNAList.index(DNA) + 1
    print(f"{bcolors.OK}Rendering Image: {bcolors.RESET}" + str(total_index) + " (File: {})".format(file_name))
    nft_name = file_name[:-len(".json")]

    image_path = os.path.join(batch_path, "NFT_{:04d}".format(nft_num), nft_name)
    Previewer.show_nft_from_dna(DNA, NFTDict)

    bpy.context.scene.render.filepath = image_path
    bpy.context.scene.render.image_settings.file_format = image_file_format
    bpy.context.scene.render.image_settings.color_mode = color_mode
    try:
        bpy.ops.render.render(write_still=True)
        return nft_name, True
    except:
        print((f"{bcolors.ERROR}Render Failed{bcolors.RESET}"))
        return nft_name, False



def render_nft_single_video(batch_path, batch_num, nft_num, file_format, totalDNAList):
    file_name = "Batch_{:03d}_NFT_{:04d}.json".format(batch_num, nft_num)
    json_path = os.path.join(batch_path, "NFT_{:04d}".format(nft_num), file_name)

    SingleDict = json.load(open(json_path))
    DNA = SingleDict["DNAList"]
    NFTDict = SingleDict["CharacterItems"]
    total_index = totalDNAList.index(DNA) + 1
    print(f"{bcolors.OK}Rendering Video: {bcolors.RESET}" + str(total_index) + " (File: {})".format(file_name))

    nft_name = file_name[:-len(".json")] + ".mp4"
    Previewer.show_nft_from_dna(DNA, NFTDict)

    video_path = os.path.join(batch_path, "NFT_{:04d}".format(nft_num), nft_name)
    bpy.context.scene.render.filepath = video_path

    if file_format == 'MP4':
        bpy.context.scene.render.image_settings.file_format = "FFMPEG"
        bpy.context.scene.render.ffmpeg.format = 'MPEG4'
        bpy.context.scene.render.ffmpeg.codec = 'H264'
        try:
            bpy.ops.render.render(animation=True)
            print("FINISHED VIDEO RENDER")
            return nft_name, True
        except:
            print((f"{bcolors.ERROR}Render Failed{bcolors.RESET}"))
            return nft_name, False


def render_nft_single_model(batch_path, batch_num, nft_num, file_format, totalDNAList):
    file_name = "Batch_{:03d}_NFT_{:04d}.json".format(batch_num, nft_num)
    json_path = os.path.join(batch_path, "NFT_{:04d}".format(nft_num), file_name)
    SingleDict = json.load(open(json_path))
    dnaDictionary = SingleDict["CharacterItems"]

    DNA = SingleDict["DNAList"]
    NFTDict = SingleDict["CharacterItems"]
    total_index = totalDNAList.index(DNA) + 1
    print(f"{bcolors.OK}Generating 3D Model: {bcolors.RESET}" + str(total_index) + " (File: {})".format(file_name))

    nft_name = file_name[:-len(".json")]
    modelPath = os.path.join(batch_path, "NFT_{:04d}".format(nft_num), nft_name)

    Previewer.show_nft_from_dna(DNA, NFTDict)

    for i in dnaDictionary:
        if dnaDictionary[i] != 'Null':
            coll = list(dnaDictionary[i].keys())[0]
        else:
            slot_coll = bpy.data.collections[i]
            if slot_coll.children:
                type_coll = slot_coll.children[0]
                if type_coll.children:
                    var_coll = type_coll.children[0]
                    coll = var_coll.name
                else:
                    coll = type_coll.name
            else:
                coll = slot_coll.name
        for obj in bpy.data.collections[coll].all_objects:
             obj.select_set(True)

    char_variant = DNA.partition(',')[0]
    for obj in bpy.data.collections[char_variant].all_objects:
        obj.select_set(True)

    try:
        if file_format == 'GLB':
            bpy.ops.export_scene.gltf(filepath=f"{modelPath}.glb",
                                        check_existing=True,
                                        export_format='GLB',
                                        use_selection=True)
        if file_format == 'GLTF_SEPARATE':
            bpy.ops.export_scene.gltf(filepath=f"{modelPath}",
                                        check_existing=True,
                                        export_format='GLTF_SEPARATE',
                                        use_selection=True)
        if file_format == 'GLTF_EMBEDDED':
            bpy.ops.export_scene.gltf(filepath=f"{modelPath}.gltf",
                                        check_existing=True,
                                        export_format='GLTF_EMBEDDED',
                                        use_selection=True)
        elif file_format == 'FBX':
            bpy.ops.export_scene.fbx(filepath=f"{modelPath}.fbx",
                                        check_existing=True,
                                        use_selection=True)
        elif file_format == 'OBJ':
            bpy.ops.export_scene.obj(filepath=f"{modelPath}.obj",
                                        check_existing=True,
                                        use_selection=True)
        elif file_format == 'X3D':
            bpy.ops.export_scene.x3d(filepath=f"{modelPath}.x3d",
                                        check_existing=True,
                                        use_selection=True)
        elif file_format == 'STL':
            bpy.ops.export_mesh.stl(filepath=f"{modelPath}.stl",
                                    check_existing=True,
                                    use_selection=True)
        elif file_format == 'VOX':
            bpy.ops.export_vox.some_data(filepath=f"{modelPath}.vox")
        return nft_name, True

    except:
        print((f"{bcolors.ERROR}Render Failed{bcolors.RESET}"))
        return nft_name, False



# ----------------------------------- Export Logs --------------------------------------------

def send_to_export_log(batch_path, batch_num, record_name, nft_name, file_type, file_format, render_time, key, render_sucess):
    Log, log_name = return_export_log_data(batch_path, batch_num, file_type)
    log_path = os.path.join(batch_path, log_name)
    logged_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    Log[key] = {'nft_number': nft_name, 'finished': logged_time, 
                'time_taken': "{:.2f} seconds".format(render_time), 'file_format': file_format,
                'has_succeeded': render_sucess}
    try:
        log = json.dumps(Log, indent=1, ensure_ascii=True)
        with open(log_path, 'w') as outfile:
            outfile.write(log + '\n')
    except:
        print(f"{bcolors.ERROR} ERROR:\nCould not export data to {log_path}\n {bcolors.RESET}")
    return


 
def return_export_log_data(batch_path, batch_num, file_format):
    log_name = "LOG_Batch_{:03d}_{}.json".format(batch_num, file_format)
    path = os.path.join(batch_path, log_name)
    if os.path.exists(path):
        log = json.load(open(path))
        return log, log_name
    else:
        return {}, log_name


# ---------------------------- Exporting out record data to local directory -------------------------------------------

def clear_all_export_data(record_path, local_output_path): # clear all nft, record, render data from export dir
    if not os.path.exists(local_output_path):
        return
    if record_path == local_output_path:
        return
    
    for dir in os.listdir(local_output_path):
        new_path = os.path.join(local_output_path, dir)
        if os.path.isdir(new_path):
            shutil.rmtree(new_path)
        else:
            os.remove(new_path)
    return


def export_record_data(record_batch_root, local_batch_root): # copy all record data to export dir
                                                            # keep any currently existing render data in export dir unless NFT count < render index
    if record_batch_root == local_batch_root:
        return False
    # if os.path.exists(local_batch_root):
    #     shutil.rmtree(local_batch_root)
    # clear_all_export_data(record_batch_root, local_batch_root) # CHECK THIS
    recurse_copy_data('', record_batch_root, local_batch_root)
    # recurse_delete_data('', record_batch_root, local_batch_root)
    
    src_batchscript_path = os.path.join(bpy.context.scene.my_tool.root_dir, "ExportBatchSingle.bat")
    dst_batscript_path = os.path.join(bpy.context.scene.my_tool.separateExportPath, "ExportBatchSingle.bat")
    shutil.copy(src_batchscript_path, dst_batscript_path)

    src_pyscript_path = os.path.join(bpy.context.scene.my_tool.root_dir, "Exporter.py")
    dst_pyscript_path = os.path.join(bpy.context.scene.my_tool.separateExportPath, "Exporter.py")
    shutil.copy(src_pyscript_path, dst_pyscript_path)
    return True


def recurse_copy_data(batch_path, record_batch_root, local_batch_root): # copies only json files
    local_path = os.path.join(local_batch_root, batch_path)
    record_path = os.path.join(record_batch_root, batch_path)

    for dir in os.listdir(record_path):
        new_record_path = os.path.join(record_path, dir)
        if os.path.isdir(new_record_path):
            new_dir = os.path.join(local_path, dir)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            new_batch_path = os.path.join(batch_path, dir)
            recurse_copy_data(new_batch_path, record_batch_root, local_batch_root)
        else:
            new_local_path = os.path.join(local_path, dir)
            if str(new_local_path).lower().endswith('.json'):
                shutil.copy(new_record_path, new_local_path)
            else:
                print("Would not copy {}".format(new_local_path))
    return


def recurse_delete_data(batch_path, record_batch_root, local_batch_root): # delete nfts that exist in local but don't exist in record folder
    local_path = os.path.join(local_batch_root, batch_path)               # leaves rendered outputs
    record_path = os.path.join(record_batch_root, batch_path)

    for dir in os.listdir(local_path):
        new_record_path = os.path.join(record_path, dir)
        if os.path.exists(new_record_path):
            if os.path.isdir(new_record_path):
                new_batch_path = os.path.join(batch_path, dir)
                recurse_delete_data(new_batch_path, record_batch_root, local_batch_root)
        else:
            new_local_path = os.path.join(local_path, dir)
            if os.path.isdir(new_local_path):
                shutil.rmtree(new_local_path)
            else:
                if str(new_local_path).lower().endswith('.json'):
                    os.remove(new_local_path)
                    print(new_local_path)


# -----------------------------------------------------------------

def save_metadata_file(path, nft_name, batch_num, nft_num, DNA):
    nft_path = os.path.join(path, nft_name)
    metadata = metaData.returnERC721MetaDataCustom(nft_name, DNA)

    metaDataObj = json.dumps(metadata, indent=1, ensure_ascii=True)
    with open(os.path.join(path, "ERC721_{}_{}.json".format(batch_num, nft_num)), "w") as outfile:
            outfile.write(metaDataObj)



def save_all_metadata_files(output_path):
    count = 0
    record_path = os.path.join(output_path,"_NFTRecord.json")
    total_record = json.load(open(record_path))
    total_DNA = total_record["DNAList"]

    for dir in os.listdir(output_path):
        batch_path = os.path.join(output_path, dir)
        if os.path.isdir(batch_path):
            for nft_dir in os.listdir(batch_path):
                nft_path = os.path.join(batch_path, nft_dir)
                if os.path.isdir(nft_path):
                    for nft_data in os.listdir(nft_path):
                        if nft_data.endswith(".json") and nft_data.startswith('Batch'):
                            batch_index = nft_data.split('_')[1]
                            nft_index = nft_data.split('_')[3]
                            nft_index = nft_index.split('.')[0]
                            nft_record = os.path.join(nft_path, nft_data)
                            single_record = json.load(open(nft_record))
                            DNA = single_record["DNAList"]
                            name_prefix = str(bpy.context.scene.my_tool.renderPrefix)
                            index = total_DNA.index(DNA) + 1
                            nft_name = name_prefix + "{:04d}".format(index)
                            save_metadata_file(nft_path, nft_name, batch_index, nft_index, DNA)
                            count += 1
    print("{} metadata files have been created".format(count))
    return



# ------------------------------- Refactor Exports ---------------------------

def refactor_all_batches(batches_path, master_record_path):
    DNAList = []
    emptyDict = {}
    emptyDict["DNAList"] = DNAList
    emptydata = json.dumps(emptyDict, indent=1, ensure_ascii=True)
    with open(master_record_path, 'w') as outfile:
        outfile.write(emptydata + '\n')

    batches = len(next(os.walk(batches_path))[1])

    for i in range(batches):
        batch_path = os.path.join(batches_path, "Batch_{:03d}".format(i + 1))
        refactor_single_batch(batch_path, i+1, master_record_path)
    return


def refactor_single_batch(batch_path, batch_index, master_record_path):
    master_record = json.load(open(master_record_path))
    DNAList = master_record["DNAList"]
    nfts = len(next(os.walk(batch_path))[1])

    for i in range(nfts):
        nft_path = os.path.join(batch_path, "NFT_{:04d}".format(i + 1))
        default_prefix = "Batch_{:03d}_NFT_{:04d}".format(batch_index, i + 1)
        metadata_prefix = "ERC721_{:03d}_{:04d}".format(batch_index, i + 1)

        for dir in os.listdir(nft_path): # checking if files have been renamed
            prefix, suffix = dir.split('.')
            if suffix != 'json':
                if prefix != default_prefix:
                    if prefix != metadata_prefix:
                        break
                    else:
                        prefix = default_prefix
                else:
                    prefix = default_prefix
        
        DNA = refactor_single_nft(nft_path, default_prefix, prefix, DNAList)
    if DNA:
        DNAList.append(DNA)

    master_record["DNAList"] = DNAList
    master_record_data = json.dumps(master_record, indent=1, ensure_ascii=True)
    with open(master_record_path, 'w') as outfile:
        outfile.write(master_record_data + '\n')
    return


def refactor_single_nft(folder_path, default_prefix, prefix, DNAList):
    # will rename export files and add new export names to json file info
    single_record = json.load(open(os.path.join(folder_path, default_prefix + '.json')))
    DNA = single_record["DNAList"]
    if not DNA in DNAList:
        DNAList.append(DNA)
        index = len(DNAList) - 1
        is_new = True
    else:
        index = DNAList.index(DNA)
        is_new = False

    files = os.listdir(folder_path)
    for old_file in files:
        if prefix in old_file:
            current_prefix = prefix
            suffix = old_file.split('.')[-1]
        else: # if file has already been refactored previously
            current_prefix, suffix = old_file.split('.')

        new_prefix = bpy.context.scene.my_tool.renderPrefix
        new_file_name = new_prefix + "{:04d}".format(index) + '.' + suffix
        old_path = os.path.join(folder_path, old_file)
        new_path = os.path.join(folder_path, new_file_name)            
        if suffix == "json":
            if current_prefix == default_prefix:
                record_path = os.path.join(old_path)
                save_filename_to_record(record_path, new_file_name)
            else:
                metadata_path = os.path.join(old_path)
                change_nftname_in_metadata(metadata_path, new_file_name)
        else:
            os.rename(old_path, new_path)
    
    return DNA if is_new else None


def save_filename_to_record(nftrecord_path, new_name):
    new_name = new_name.split('.')[0]
    if os.path.exists(nftrecord_path):
        record = json.load(open(nftrecord_path))
        record["filename"] = new_name

        recordObj = json.dumps(record, indent=1, ensure_ascii=True)
        with open(nftrecord_path, "w") as outfile:
                outfile.write(recordObj)
    return


def change_nftname_in_metadata(metadata_path, new_name):
    new_name = new_name.split('.')[0]
    if os.path.exists(metadata_path):
        data = json.load(open(metadata_path))
        data["name"] = new_name

        dataObj = json.dumps(data, indent=1, ensure_ascii=True)
        with open(metadata_path, "w") as outfile:
                outfile.write(dataObj)

    return


if __name__ == '__main__':
    render_and_save_NFTs()
