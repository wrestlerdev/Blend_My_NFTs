# Purpose:
# This file takes a given Batch created by DNA_Generator.py and tells blender to render the image or export a 3D model to
# the NFT_Output folder.

from re import L
import bpy
import os
import time
import json
import importlib
import shutil

from . import Previewer
importlib.reload(Previewer)

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



def render_nft_batch_custom(save_path, batch_num, file_formats, nft_range, transparency=False):
    folder = os.path.join(save_path, "OUTPUT")
    master_record_path = os.path.join(folder, "_NFTRecord.json")
    MasterDictionary = json.load(open(master_record_path))
    totalDNAList = MasterDictionary["DNAList"]

    if not os.path.exists(folder):
        os.makedirs(folder)

    batch_path = os.path.join(save_path, "OUTPUT", "Batch_{:03d}".format(batch_num))
    for file_format in file_formats:
        if file_format in ['PNG', 'JPEG']:
            camera_name = "CameraStill"
            if bpy.data.objects.get(camera_name) is not None:
                bpy.context.scene.camera = bpy.data.objects[camera_name]
            else:
                print("Cannot find camera of name 'CameraStill', will continue with current camera")
                if bpy.context.scene.camera is None:
                    print("Camera does not exist in scene, please make one :^(")
            for i in range(nft_range[0], nft_range[1] + 1):
                if transparency:
                    color_mode = 'RGBA'
                else:
                    color_mode = 'RGB'
                start_time = time.time()
                render_nft_single_custom(batch_path, batch_num, i, file_format, color_mode, totalDNAList)
                print(f"{bcolors.OK}Time taken: {bcolors.RESET}" + "{:.2f}".format(time.time() - start_time))


        elif file_format in ['MP4']:
            camera_name = "CameraVideo"
            if bpy.data.objects.get(camera_name) is not None:
                bpy.context.scene.camera = bpy.data.objects[camera_name]
            else:
                print("Cannot find camera of name 'CameraVideo', will continue with current camera")
                if bpy.context.scene.camera is None:
                    print("Camera does not exist in scene, please make one :^(")
            for i in range(nft_range[0], nft_range[1] + 1):
                start_time = time.time()
                render_nft_single_video(batch_path, batch_num, i, file_format, totalDNAList)
                print((f"{bcolors.OK}Time taken: {bcolors.RESET}") + "{:.2f}".format(time.time() - start_time))

        elif file_format in ['FBX', 'GLB']:
            for i in range(nft_range[0], nft_range[1] + 1):
                start_time = time.time()
                render_nft_single_model(batch_path, batch_num, i, file_format, totalDNAList)
                print((f"{bcolors.OK}Time taken: {bcolors.RESET}") + "{:.2f}".format(time.time() - start_time))

    print((f"{bcolors.OK}Render Finished :^){bcolors.RESET}"))
    return



def render_nft_single_custom(batch_path, batch_num, nft_num, image_file_format, color_mode, totalDNAList):
    file_name = "Batch_{:03d}_NFT_{:04d}.json".format(batch_num, nft_num)
    json_path = os.path.join(batch_path, "NFT_{:04d}".format(nft_num), file_name)
    SingleDict = json.load(open(json_path))

    DNA = SingleDict["DNAList"]
    total_index = totalDNAList.index(DNA) + 1
    print(f"{bcolors.OK}Rendering Image: {bcolors.RESET}" + str(total_index) + " (File: {})".format(file_name))
    name_prefix = str(bpy.context.scene.my_tool.renderPrefix)
    nft_name = name_prefix + "{:04d}".format(total_index)

    image_path = os.path.join(batch_path, "NFT_{:04d}".format(nft_num), nft_name)
    Previewer.show_nft_from_dna(DNA)

    bpy.context.scene.render.filepath = image_path
    bpy.context.scene.render.image_settings.file_format = image_file_format
    bpy.context.scene.render.image_settings.color_mode = color_mode
    bpy.ops.render.render(write_still=True)
    return



def render_nft_single_video(batch_path, batch_num, nft_num, file_format, totalDNAList):
    file_name = "Batch_{:03d}_NFT_{:04d}.json".format(batch_num, nft_num)
    json_path = os.path.join(batch_path, "NFT_{:04d}".format(nft_num), file_name)

    SingleDict = json.load(open(json_path))
    DNA = SingleDict["DNAList"]
    total_index = totalDNAList.index(DNA) + 1

    print(f"{bcolors.OK}Rendering Video: {bcolors.RESET}" + str(total_index) + " (File: {})".format(file_name))
    name_prefix = str(bpy.context.scene.my_tool.renderPrefix)
    nft_name = name_prefix + "{:04d}.mp4".format(total_index)
    Previewer.show_nft_from_dna(DNA)

    video_path = os.path.join(batch_path, "NFT_{:04d}".format(nft_num), nft_name)
    bpy.context.scene.render.filepath = video_path

    if file_format == 'MP4':
        bpy.context.scene.render.image_settings.file_format = "FFMPEG"
        bpy.context.scene.render.ffmpeg.format = 'MPEG4'
        bpy.context.scene.render.ffmpeg.codec = 'H264'
        bpy.ops.render.render(animation=True)
        print("FINISHED VIDEO RENDER")
    return


def render_nft_single_model(batch_path, batch_num, nft_num, file_format, totalDNAList):
    file_name = "Batch_{:03d}_NFT_{:04d}.json".format(batch_num, nft_num)
    json_path = os.path.join(batch_path, "NFT_{:04d}".format(nft_num), file_name)
    
    print(f"{bcolors.OK}Generating 3D Model{bcolors.RESET}")


    SingleDict = json.load(open(json_path))
    dnaDictionary = SingleDict["CharacterItems"]

    DNA = SingleDict["DNAList"]
    total_index = totalDNAList.index(DNA) + 1
    name_prefix = str(bpy.context.scene.my_tool.renderPrefix)
    nft_name = name_prefix + "{:04d}".format(total_index)
    modelPath = os.path.join(batch_path, "NFT_{:04d}".format(nft_num), nft_name)

    Previewer.show_nft_from_dna(DNA)
    # if not os.path.exists(modelFolder):
    #     os.makedirs(modelFolder)

    for i in dnaDictionary:
        coll = list(dnaDictionary[i].keys())[0]
        print(coll)
        for obj in bpy.data.collections[coll].all_objects:
             obj.select_set(True)

    char_variant = DNA.partition(',')[0]
    for obj in bpy.data.collections[char_variant].all_objects:
        obj.select_set(True)

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
    return


def clear_all_export_data(record_path, local_output_path):
    if not os.path.exists(local_output_path):
        return
    if os.path.abspath(record_path) == os.path.abspath(local_output_path):
        return
    
    for dir in os.listdir(local_output_path):
        new_path = os.path.join(local_output_path, dir)
        if os.path.isdir(new_path):
            shutil.rmtree(new_path)
        else:
            os.remove(new_path)
    return


def export_record_data(record_batch_root, local_batch_root):
    if os.path.abspath(record_batch_root) == os.path.abspath(local_batch_root):
        print("This is the same folder lol")
        return
    # if os.path.exists(local_batch_root):
    #     shutil.rmtree(local_batch_root)
    recurse_copy_data('', record_batch_root, local_batch_root)
    recurse_delete_data('', record_batch_root, local_batch_root)
    return


def recurse_copy_data(batch_path, record_batch_root, local_batch_root):
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


def recurse_delete_data(batch_path, record_batch_root, local_batch_root):   # delete nfts that exist in local but don't exist in record folder
    local_path = os.path.join(local_batch_root, batch_path)                 # leaves rendered outputs
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


if __name__ == '__main__':
    render_and_save_NFTs()
