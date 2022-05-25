bl_info = {
    "name": "Blend_My_NFTs",
    "author": "Torrin Leonard, This Cozy Studio Inc",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D",
    "description": "Blend_My_NFTs UI Edition",
    "category": "Development",
}

# Import handling:

import bpy
from bpy.app.handlers import persistent
from rna_prop_ui import PropertyPanel
import time

# import json

import os
import importlib
from .main import config

# Import files from main directory:

importList = ['TextureEditor', 'Batch_Sorter', 'DNA_Generator', 'Exporter', 'Batch_Refactorer', 'get_combinations', 'SaveNFTsToRecord', 'UIList', 'LoadNFT']

if bpy in locals():
        importlib.reload(LoadNFT)
        importlib.reload(DNA_Generator)
        importlib.reload(Batch_Sorter)
        importlib.reload(Exporter)
        importlib.reload(Batch_Refactorer)
        importlib.reload(get_combinations)
        importlib.reload(SaveNFTsToRecord)
        importlib.reload(UIList)
        importlib.reload(TextureEditor)
else:
    from .main import \
        LoadNFT, \
        DNA_Generator, \
        Batch_Sorter, \
        Exporter, \
        Batch_Refactorer, \
        SaveNFTsToRecord, \
        get_combinations, \
        TextureEditor

    from .ui_Lists import UIList

Slots = {"inputUpperTorso": ("01-UpperTorso", "Upper Torso Slot"),
    "inputMiddleTorso": ("02-MiddleTorso", "Mid Torso Slot"),
    "inputLForeArm": ("03-LForeArm", "Left Forearm Slot"),
    "inputLWrist": ("04-LWrist", "Left Wrist Slot"),
    "inputRForeArm": ("05-RForeArm", "Right Forearm Slot"),
    "inputRWrist": ("06-RWrist", "Right Wrist Slot"),
    "inputHands": ("07-Hands", "Hands Slot"),
    "inputPelvisThick": ("08-PelvisThick", "Pelvis Thick Slot"),
    "inputPelvisThin": ("09-PelvisThin", "Pelvis Thin Slot"),
    "inputCalf": ("10-Calf", "Calf Slot"),
    "inputAnkle": ("11-Ankle", "Ankle Slot"),
    "inputFeet": ("12-Feet", "Feet Slot"),
    "inputNeck": ("13-Neck", "Neck Slot"),
    "inputLowerHead": ("14-LowerHead", "Lower Head Slot"),
    "inputMiddleHead": ("15-MiddleHead", "Mid Head Slot"),
    "inputEarings": ("16-Earings", "Earrings Slot"),
    "inputUpperHead": ("17-UpperHead", "Upper Head Slot"),
    "inputBackPack": ("18-BackPack", "Backpack Slot"),
    "inputBackground": ("19-Background", "Background Slot")}
    

# User input Property Group:
class BMNFTS_PGT_MyProperties(bpy.types.PropertyGroup):

    # Main BMNFTS Panel properties: 
    
    nftName: bpy.props.StringProperty(name="NFT Name")

    collectionSize: bpy.props.IntProperty(name="NFT Collection Size", default=1, min=1)  # max=(combinations - offset)
    nftsPerBatch: bpy.props.IntProperty(name="NFTs Per Batch", default=1, min=1)  # max=(combinations - offset)
    batchToGenerate: bpy.props.IntProperty(name="Batch To Generate", default=1, min=1)  # max=(collectionSize / nftsPerBatch)
    


    save_path: bpy.props.StringProperty(
                        name="Save Path",
                        description="Save path for NFT files",
                        default="",
                        maxlen=1024,
                        subtype="DIR_PATH"
    )

    enableRarity: bpy.props.BoolProperty(name="Enable Rarity")

    imageBool: bpy.props.BoolProperty(name="Image")
    imageEnum: bpy.props.EnumProperty(
        name="Image File Format", 
        description="Select Image file format", 
        items=[
            ('PNG', ".PNG", "Export NFT as PNG"),
            ('JPEG', ".JPEG", "Export NFT as JPEG")
        ]
    )
    
    animationBool: bpy.props.BoolProperty(name="Animation")
    animationEnum: bpy.props.EnumProperty(
        name="Animation File Format", 
        description="Select Animation file format", 
        items=[
            ('AVI_JPEG', '.avi (AVI_JPEG)', 'Export NFT as AVI_JPEG'),
            ('AVI_RAW', '.avi (AVI_RAW)', 'Export NFT as AVI_RAW'),
            ('FFMPEG', '.mkv (FFMPEG)', 'Export NFT as FFMPEG'),
            ('MP4', '.mp4', 'Export NFT as .mp4')
        ]
    )


    modelBool: bpy.props.BoolProperty(name="3D Model")
    modelEnum: bpy.props.EnumProperty(
        name="3D Model File Format", 
        description="Select 3D Model file format", 
        items=[
            ('GLB', '.glb', 'Export NFT as .glb'),
            # ('GLTF_SEPARATE', '.gltf + .bin + textures', 'Export NFT as .gltf with separated textures in .bin + textures.'),
            # ('GLTF_EMBEDDED', '.gltf', 'Export NFT as embedded .gltf file that contains textures.'),
            ('FBX', '.fbx', 'Export NFT as .fbx'),
            # ('OBJ', '.obj', 'Export NFT as .obj'),
            # ('X3D', '.x3d', 'Export NFT as .x3d'),
            # ('STL', '.stl', 'Export NFT as .stl'),
            # ('VOX', '.vox (Experimental)', 'Export NFT as .vox, requires the voxwriter add on: https://github.com/Spyduck/voxwriter')
        ]
    )


    cardanoMetaDataBool: bpy.props.BoolProperty(name="Cardano Cip")
    solanaMetaDataBool: bpy.props.BoolProperty(name="Solana Metaplex")
    erc721MetaData: bpy.props.BoolProperty(name="ERC721")

    # API Panel properties:
    apiKey: bpy.props.StringProperty(name="API Key", subtype='PASSWORD')



    # Custom properties

    textureSize: bpy.props.EnumProperty(
            name='textuuuuuuuuures',
            description="texture",
            items=[
                ('4k', '4k', '4096x4096'),
                # ('2k', '2k', '2048x2048'),
                ('1k', '1k', '1024x1024')
                # ('512', '512', '512x512')
            ]
        )

    isCharacterLocked: bpy.props.BoolProperty(name="Lock Character", default=False)

    separateExportPath: bpy.props.StringProperty(name="Directory")
    renderPrefix: bpy.props.StringProperty(name="Output Prefix:", default="SAE #")

    renderFullBatch: bpy.props.BoolProperty(name= "Render Full Batch", default=True)
    renderSectionSize: bpy.props.IntProperty(name= "Section Size", default=1, min=1, max=9999)
    renderSectionIndex: bpy.props.IntProperty(name= "Section Index", default=1, min=1, max=9999)
    rangeBool: bpy.props.BoolProperty(name="Use Sections", default=True)
    BatchRenderIndex: bpy.props.IntProperty(name= "Batch To Render", default=1, min=1, max=10)
    PNGTransparency: bpy.props.BoolProperty(name= 'Transparency', default=True)

    batch_json_save_path: bpy.props.StringProperty(name="Batch Save Path")
    root_dir: bpy.props.StringProperty(name="Root Directory")

    maxNFTs: bpy.props.IntProperty(name="Max NFTs to Generate",default=1, min=1, max=9999)
    loadNFTIndex: bpy.props.IntProperty(name="Number to Load:", min=1, max=9999, default=1)
    CurrentBatchIndex : bpy.props.IntProperty(name="Current Batch", min=1, max=10, default=1)

    BatchSliderIndex : bpy.props.IntProperty(name="Batch", min=1, max=10, default=1, update=lambda s,c:LoadNFT.batch_property_updated())
    lastBatchSliderIndex: bpy.props.IntProperty(default=1)

    lastDNA: bpy.props.StringProperty(name="lastDNA") # for checks if dna string field is edited by user
    inputDNA: bpy.props.StringProperty(name="DNA", update=lambda s,c: Exporter.Previewer.dnastring_has_updated(bpy.context.scene.my_tool.inputDNA,bpy.context.scene.my_tool.lastDNA))

    inputUpperTorso: bpy.props.PointerProperty(name="Upper Torso Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputUpperTorso",Slots))
    inputMiddleTorso: bpy.props.PointerProperty(name="",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputMiddleTorso",Slots))
    inputLForeArm: bpy.props.PointerProperty(name="",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputLForeArm",Slots))
    inputLWrist: bpy.props.PointerProperty(name="Left Wrist Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputLWrist",Slots))
    inputRForeArm: bpy.props.PointerProperty(name="",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputRForeArm",Slots))
    inputRWrist: bpy.props.PointerProperty(name="Right Wrist Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputRWrist",Slots))
    inputPelvisThick: bpy.props.PointerProperty(name="Lower Torso Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputPelvisThick",Slots))
    inputPelvisThin: bpy.props.PointerProperty(name="Lower Torso Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputPelvisThin",Slots))
    inputHands: bpy.props.PointerProperty(name="Hands Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputHands",Slots))
    inputCalf: bpy.props.PointerProperty(name="Calf Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputCalf",Slots))
    inputAnkle: bpy.props.PointerProperty(name="Ankle Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputAnkle",Slots))
    inputFeet: bpy.props.PointerProperty(name="Feet Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputFeet",Slots))
    inputNeck: bpy.props.PointerProperty(name="Neck Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputNeck",Slots))
    inputLowerHead: bpy.props.PointerProperty(name="",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputLowerHead",Slots))
    inputMiddleHead: bpy.props.PointerProperty(name="",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputMiddleHead",Slots))
    inputEarings: bpy.props.PointerProperty(name="",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputEarings",Slots))
    inputUpperHead: bpy.props.PointerProperty(name="t",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputUpperHead",Slots))
    inputBackPack: bpy.props.PointerProperty(name="",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputBackPack",Slots))
    inputBackground: bpy.props.PointerProperty(name="",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputBackground",Slots))

    lastUpperTorso: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastMiddleTorso: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastLForeArm: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastLWrist: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastRForeArm: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastRWrist: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastPelvisThick: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastPelvisThin: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastHands: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastCalf: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastAnkle: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastFeet: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastNeck: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastLowerHead: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastMiddleHead: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastEarings: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastUpperHead: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastBackPack: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastBackground: bpy.props.PointerProperty(name="",type=bpy.types.Collection)

    colourStyleIndex: bpy.props.StringProperty(default="1", 
                                update=lambda s,c:DNA_Generator.Outfit_Generator.ColorGen.colourindex_has_been_updated("colourStyleIndex", "lastStyleIndex"))
    lastStyleIndex: bpy.props.IntProperty(default=1, min=0,max=999)

    textureSetIndex: bpy.props.StringProperty(default="A",
                                update=lambda s,c:DNA_Generator.Outfit_Generator.ColorGen.textureindex_has_been_updated("textureSetIndex", "lastSetIndex"))
    lastSetIndex: bpy.props.StringProperty(default="A")

    RTint: bpy.props.FloatVectorProperty(name="R Tint", subtype="COLOR", default=(1.0,0.0,0.0,1.0), size=4, min=0.0, max=1)
    GTint: bpy.props.FloatVectorProperty(name="G Tint", subtype="COLOR", default=(0.0,1.0,0.0,1.0), size=4, min=0.0, max=1)
    BTint: bpy.props.FloatVectorProperty(name="B Tint", subtype="COLOR", default=(0.0,0.0,1.0,1.0), size=4, min=0.0, max=1)

    colorStyleName: bpy.props.StringProperty(name="Colour Style Name", default="wah")

canRefactor = False

def make_directories(save_path):
    Blend_My_NFTs_Output = os.path.join(save_path, "Blend_My_NFTs Output")
    batch_json_save_path = os.path.join(Blend_My_NFTs_Output, "OUTPUT")

    if not os.path.exists(Blend_My_NFTs_Output):
        os.makedirs(Blend_My_NFTs_Output)
    if not os.path.exists(batch_json_save_path):
        os.makedirs(batch_json_save_path)

    return Blend_My_NFTs_Output, batch_json_save_path

# Update NFT count:
combinations: int = 0
offset: int = 0

@persistent
def update_combinations(dummy1, dummy2):
    global combinations
    global offset

    #combinations = (get_combinations.get_combinations_from_scene()) - offset

    # redraw_panel()

#bpy.app.handlers.depsgraph_update_post.append(update_combinations)




# ------------------------------- Operators ---------------------------------------------

class initializeRecord(bpy.types.Operator):
    bl_idname = 'create.record'
    bl_label = 'Reinitialize'
    bl_description = "This will reinitialize the entire NFT ledger. Are you sure?"
    bl_options = {"REGISTER", "INTERNAL"}


    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bpy.context.scene.my_tool.root_dir == '':
            save_path = os.path.abspath(bpy.context.scene.my_tool.save_path)
        elif not os.path.exists(bpy.context.scene.my_tool.root_dir):
            self.report({"ERROR"}, "Failed: The root directory folder does not exist")
            save_path = bpy.context.scene.my_tool.root_dir
            return {'FINISHED'}
        else:
            save_path = bpy.context.scene.my_tool.root_dir
        print(save_path)
        Blend_My_NFTs_Output, output_save_path = make_directories(save_path)

        first_nftrecord_save_path = os.path.join(output_save_path, "Batch_{:03d}".format(1), "_NFTRecord_{:03d}.json".format(1))
        master_nftrecord_save_path = os.path.join(output_save_path, "_NFTRecord.json")

        bpy.context.scene.my_tool.batch_json_save_path = output_save_path
        bpy.context.scene.my_tool.loadNFTIndex = 1
        bpy.context.scene.my_tool.BatchSliderIndex = 1

        original_hierarchy = Exporter.Previewer.get_hierarchy_unordered(1)
        LoadNFT.init_batch(output_save_path)
        if original_hierarchy != None:
            DNA_Generator.save_rarity_To_Record(original_hierarchy, first_nftrecord_save_path)
        else:
            DNA_Generator.send_To_Record_JSON(first_nftrecord_save_path)
        DNA_Generator.set_up_master_Record(master_nftrecord_save_path)
        LoadNFT.update_current_batch(1, output_save_path)
        LoadNFT.update_collection_rarity_property(first_nftrecord_save_path)
        return {'FINISHED'}



#-------------------------


class randomizePreview(bpy.types.Operator):
    bl_idname = 'randomize.preview'
    bl_label = 'Randomize All'
    bl_description = "Create and generate random combination"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        maxNFTs = bpy.context.scene.my_tool.collectionSize
        save_path = bpy.path.abspath(bpy.context.scene.my_tool.root_dir)
        # some randomize dna code here
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
        DNA = DNA_Generator.Outfit_Generator.RandomizeFullCharacter(maxNFTs, save_path)[0][0]
        Exporter.Previewer.show_nft_from_dna(DNA)
        bpy.context.scene.my_tool.lastDNA = DNA
        bpy.context.scene.my_tool.inputDNA = DNA
        return {'FINISHED'}


# class randomizeModel(bpy.types.Operator):
#     bl_idname = 'randomize.model'
#     bl_label = 'Randomize Model'
#     bl_description = "Randomize model of current slot"
#     bl_options = {"REGISTER", "UNDO"}
#     collection_name: bpy.props.StringProperty(default="")

#     def execute(self, context):
#         if self.collection_name != "":
#             if self.collection_name in bpy.context.scene.my_tool:
#                 LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
#                 inputDNA = bpy.context.scene.my_tool.inputDNA
#                 save_path = ''
#                 bpy.context.scene.my_tool.inputDNA = DNA_Generator.Outfit_Generator.RandomizeSingleDNAStrandMesh(self.collection_name,inputDNA,save_path)
#         return {'FINISHED'}


# class randomizeColor(bpy.types.Operator):
#     bl_idname = 'randomize.color'
#     bl_label = 'Randomize Color/Texture'
#     bl_description = "Randomize color of current slot"
#     bl_options = {"REGISTER", "UNDO"}
#     collection_name: bpy.props.StringProperty(default="")

#     def execute(self, context):
#         if self.collection_name != "":
#             LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
#             inputDNA = bpy.context.scene.my_tool.inputDNA
#             inputSlot = self.collection_name
#             slotCollection = Slots[inputSlot][0]
#             save_path = ''
#             DNA = DNA_Generator.Outfit_Generator.RandomizeSingleDNAStrandColor(inputSlot, slotCollection, inputDNA,save_path)
#             bpy.context.scene.my_tool.inputDNA = DNA
#         return {'FINISHED'}


class clearSlots(bpy.types.Operator):
    bl_idname = 'clear.slots'
    bl_label = 'Clear All Slots'
    bl_description = 'Set all slots to Null'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
        lastDNA = bpy.context.scene.my_tool.inputDNA
        DNASplit = lastDNA.split(',')
        character = DNASplit.pop(0)
        DNA = Exporter.Previewer.get_null_dna(character)
        print(DNA)
        bpy.context.scene.my_tool.inputDNA = DNA
        return {'FINISHED'}


#-------------------------


class saveNewNFT(bpy.types.Operator):
    bl_idname = 'save.nft'
    bl_label = 'Save as New NFT'
    bl_description = "Save current preview as a new NFT"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
        DNASet = {str(context.scene.my_tool.inputDNA)}

        batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
        NFTDict = Exporter.Previewer.create_item_dict(context.scene.my_tool.inputDNA)
        index = int(bpy.context.scene.my_tool.CurrentBatchIndex)

        master_save_path = os.path.join(batch_json_save_path, "_NFTRecord.json")
        nft_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(index))
        if not SaveNFTsToRecord.SaveNFT(DNASet, NFTDict, nft_save_path, index, master_save_path):
            self.report({"ERROR"}, "This NFT already exists")

        numGenerated = LoadNFT.get_total_DNA()
        bpy.context.scene.my_tool.loadNFTIndex = numGenerated    
        return {'FINISHED'}



class createBatch(bpy.types.Operator):
    bl_idname = 'create.batch'
    bl_label = "Create NFTs"
    bl_description = "Create multiple random NFTs"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
        index = bpy.context.scene.my_tool.CurrentBatchIndex
        master_record_save_path = os.path.join(batch_json_save_path, "_NFTRecord.json")
        nft_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(index))
        DNASet, NFTDict = DNA_Generator.Outfit_Generator.RandomizeFullCharacter(bpy.context.scene.my_tool.maxNFTs, nft_save_path)
        if not SaveNFTsToRecord.SaveNFT(DNASet, NFTDict, nft_save_path, index, master_record_save_path):
            self.report({"ERROR"}, "These NFTs already exist")

        numGenerated = LoadNFT.get_total_DNA()
        bpy.context.scene.my_tool.loadNFTIndex = numGenerated
        DNA = DNASet[len(DNASet) - 1] # show last DNA created

        Exporter.Previewer.show_nft_from_dna(DNA)
        bpy.context.scene.my_tool.lastDNA = DNA
        bpy.context.scene.my_tool.inputDNA = DNA
        Exporter.Previewer.fill_pointers_from_dna(DNA, Slots)
        return {'FINISHED'}



#-------------------------



class loadNFT(bpy.types.Operator):
    bl_idname = 'load.nft'
    bl_label = "Load NFT"
    bl_description = "Load NFT from index based on slider"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
        loadNFTIndex = bpy.context.scene.my_tool.loadNFTIndex
        batch_index = bpy.context.scene.my_tool.CurrentBatchIndex
        TotalDNA, DNA = LoadNFT.read_DNAList_from_file(batch_index, loadNFTIndex)
        nft_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{:03d}".format(batch_index))
        if TotalDNA > 0 and DNA != '':
            Exporter.Previewer.show_nft_from_dna(DNA)
            bpy.context.scene.my_tool.lastDNA = DNA
            bpy.context.scene.my_tool.inputDNA = DNA
            Exporter.Previewer.fill_pointers_from_dna(DNA, Slots)
        else:
            self.report({"ERROR"}, "This is not a valid number (%d), as there are only %d NFTs saved" %(loadNFTIndex, TotalDNA))

        return {'FINISHED'}


class loadNextNFT(bpy.types.Operator):
    bl_idname = 'next.nft'
    bl_label = "Load Next"
    bl_description = 'Load Next NFT based on slider'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
        batch_index = bpy.context.scene.my_tool.CurrentBatchIndex
        nft_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{:03d}".format(batch_index))

        nftnum = len(next(os.walk(nft_save_path))[1])
        print(nftnum)
        if  nftnum > 0 and bpy.context.scene.my_tool.loadNFTIndex < nftnum:
            bpy.context.scene.my_tool.loadNFTIndex = bpy.context.scene.my_tool.loadNFTIndex + 1
            loadNFTIndex = bpy.context.scene.my_tool.loadNFTIndex
            TotalDNA, DNA = LoadNFT.read_DNAList_from_file(batch_index, loadNFTIndex)

            Exporter.Previewer.show_nft_from_dna(DNA)
            bpy.context.scene.my_tool.lastDNA = DNA
            bpy.context.scene.my_tool.inputDNA = DNA
            Exporter.Previewer.fill_pointers_from_dna(DNA, Slots)
        return {'FINISHED'}


class loadPrevNFT(bpy.types.Operator):
    bl_idname = 'prev.nft'
    bl_label = "Load Previous"
    bl_description = 'Load Previous NFT based on slider'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
        batch_index = bpy.context.scene.my_tool.CurrentBatchIndex
        nft_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{:03d}".format(batch_index))
        if len(os.listdir(nft_save_path)) > 1 :
            bpy.context.scene.my_tool.loadNFTIndex = bpy.context.scene.my_tool.loadNFTIndex - 1
            loadNFTIndex = bpy.context.scene.my_tool.loadNFTIndex
            TotalDNA, DNA = LoadNFT.read_DNAList_from_file(batch_index, loadNFTIndex)

            Exporter.Previewer.show_nft_from_dna(DNA)
            bpy.context.scene.my_tool.lastDNA = DNA
            bpy.context.scene.my_tool.inputDNA = DNA
            Exporter.Previewer.fill_pointers_from_dna(DNA, Slots)
        return {'FINISHED'}


#-------------------------------

class saveCurrentNFT(bpy.types.Operator):
    bl_idname = 'save.currentnft'
    bl_label = 'Save NFT'
    bl_description = "This action cannot be undone. Are you sure?"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
        DNA = context.scene.my_tool.inputDNA

        batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
        NFTDict = Exporter.Previewer.create_item_dict(DNA)
        index = bpy.context.scene.my_tool.CurrentBatchIndex
        loadNFTIndex = bpy.context.scene.my_tool.loadNFTIndex

        master_record_save_path = os.path.join(batch_json_save_path, "_NFTRecord.json")
        nft_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(index))
        if not SaveNFTsToRecord.OverrideNFT(DNA, NFTDict, nft_save_path, index, loadNFTIndex, master_record_save_path):
            self.report({"ERROR"}, "This NFT already exists probably")
        return {'FINISHED'}



class deleteNFT(bpy.types.Operator):
    bl_idname = 'delete.nft'
    bl_label = 'Delete NFT'
    bl_description = "This will override an NFT and cannot be undone. Are you sure?"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
        batch_index = bpy.context.scene.my_tool.CurrentBatchIndex
        nft_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{:03d}".format(batch_index))
        loadNFTIndex = bpy.context.scene.my_tool.loadNFTIndex
        TotalDNA, DNA = LoadNFT.read_DNAList_from_file(batch_index, loadNFTIndex)
        master_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "_NFTRecord.json")
        
        if TotalDNA > 0 and DNA != '':
            deleted_index = SaveNFTsToRecord.DeleteNFT(DNA, nft_save_path, batch_index, master_save_path)
            new_index = min(deleted_index, TotalDNA - 1)
            TotalDNA, DNA = LoadNFT.read_DNAList_from_file(batch_index, new_index)

            bpy.context.scene.my_tool.loadNFTIndex = new_index
            Exporter.Previewer.show_nft_from_dna(DNA)
            bpy.context.scene.my_tool.lastDNA = DNA
            bpy.context.scene.my_tool.inputDNA = DNA
            Exporter.Previewer.fill_pointers_from_dna(DNA, Slots)
        else:
            self.report({"ERROR"}, "This is not a valid number (%d), as there are only %d NFTs saved" %(loadNFTIndex, TotalDNA))
        return {'FINISHED'}



class deleteAllNFTs(bpy.types.Operator):
    bl_idname = 'delete.allnfts'
    bl_label = 'Delete All NFTs'
    bl_description = "This will delete all NFTS from the current Batch. u sure bud?"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self,context):
        batch_index = int(bpy.context.scene.my_tool.CurrentBatchIndex)
        nft_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{:03d}".format(batch_index))
        TotalDNA = LoadNFT.get_all_DNA_from_batch(batch_index)
        master_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "_NFTRecord.json")


        if len(TotalDNA) > 0:
            SaveNFTsToRecord.DeleteAllNFTs(TotalDNA, nft_save_path, batch_index, master_save_path)
        else:
            print(">:^(")
        return {'FINISHED'}

#-------------------------------


class loadBatch(bpy.types.Operator):
    bl_idname = 'load.batch'
    bl_label = "Load Batch"
    bl_description = "Load Batch data based on slider index"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        index = bpy.context.scene.my_tool.BatchSliderIndex
        LoadNFT.check_if_paths_exist(index)
        batch_path = bpy.context.scene.my_tool.batch_json_save_path
        if len(next(os.walk(batch_path))[1]) < index:
            self.report({"ERROR"}, "This is not a valid batch" )
            return {'FINISHED'}

        try:
            LoadNFT.update_current_batch(index, batch_path)
            NFTRecord_save_path = os.path.join(batch_path, "Batch_{:03d}".format(index), "_NFTRecord_{:03d}.json".format(index))
            LoadNFT.update_collection_rarity_property(NFTRecord_save_path)

            bpy.context.scene.my_tool.loadNFTIndex = 1
            TotalDNA, DNA = LoadNFT.read_DNAList_from_file(index, 1)
            if DNA != '':
                Exporter.Previewer.show_nft_from_dna(DNA)
                bpy.context.scene.my_tool.lastDNA = DNA
                bpy.context.scene.my_tool.inputDNA = DNA
                Exporter.Previewer.fill_pointers_from_dna(DNA, Slots)
        except:
            self.report({"ERROR"}, "This is not a valid batch" )
        print(bpy.context.scene.my_tool.BatchSliderIndex)
        return {'FINISHED'}



class saveBatch(bpy.types.Operator):
    bl_idname = 'save.batch'
    bl_label = "Save Batch"
    bl_description = "Save and overwrite current Batch data to the current Batch"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
        batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
        index = bpy.context.scene.my_tool.BatchSliderIndex
        LoadNFT.update_current_batch(index, batch_json_save_path)

        NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(index), "_NFTRecord_{:03d}.json".format(index))
        DNA_Generator.send_To_Record_JSON(NFTRecord_save_path)

        # LoadNFT.save_collection_rarity_property(index, NFTRecord_save_path, batch_json_save_path)
        LoadNFT.update_collection_rarity_property(NFTRecord_save_path)
        return {'FINISHED'}



class saveNewBatch(bpy.types.Operator):
    bl_idname = 'save.newbatch'
    bl_label = "Save as New Batch"
    bl_description = "Save current Batch data to a new Batch"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)

        batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
        index = len(os.listdir(batch_json_save_path))
        
        LoadNFT.update_current_batch(index, batch_json_save_path)

        NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(index), "_NFTRecord_{:03d}.json".format(index))
        DNA_Generator.send_To_Record_JSON(NFTRecord_save_path)
        # LoadNFT.save_collection_rarity_property(index, NFTRecord_save_path, batch_json_save_path)
        LoadNFT.update_collection_rarity_property(NFTRecord_save_path)

        bpy.context.scene.my_tool.BatchSliderIndex = index
        return {'FINISHED'}



class resetBatch(bpy.types.Operator):
    bl_idname = 'reset.batch'
    bl_label = "Reset Batch"
    bl_description = "This will reset the Batch at index. This cannot be undone"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        batch_index = bpy.context.scene.my_tool.BatchSliderIndex
        LoadNFT.check_if_paths_exist(batch_index)
        batch_path = bpy.context.scene.my_tool.batch_json_save_path
        total_batches = len(os.listdir(batch_path)) - 1

        if batch_index > total_batches:
            self.report({"ERROR"}, "Failed: Invalid batch to reset")
            return {'FINISHED'}

        nftrecord_path = os.path.join(batch_path, "Batch_{:03d}".format(batch_index), "_NFTRecord_{:03d}.json".format(batch_index))
        DNA_Generator.create_default_rarity_Record(nftrecord_path)
        LoadNFT.update_collection_rarity_property(nftrecord_path)
        return {'FINISHED'}

#----------------------------------------------------------------


class swapCharacter(bpy.types.Operator):
    bl_idname = 'change.char'
    bl_label = "Choose"
    bl_options = {"REGISTER", "UNDO"}
    character_name: bpy.props.StringProperty(default="Kae")
    bl_description = "Change current preview to"

    def execute(self, context):
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
        DNA = bpy.context.scene.my_tool.inputDNA
        DNAString = DNA.split(',')
        DNAString[0] = self.character_name
        DNA = ','.join(DNAString)
        bpy.context.scene.my_tool.inputDNA = DNA
        return {'FINISHED'}



class chooseRootFolder(bpy.types.Operator):
    bl_idname = 'choose.root'
    bl_label = 'Choose Root Folder'
    bl_description = "Choose root folder for all inputs and outputs"
    bl_options = {"REGISTER", "UNDO"}
    filepath: bpy.props.StringProperty(subtype='FILE_PATH', default='')
    filter_glob: bpy.props.StringProperty(default ='',options = {'HIDDEN'})

    # @classmethod
    # def poll(cls, context):
    #     return context.object is not None

    def execute(self, context):
        print(self.filepath)
        bpy.context.scene.my_tool.root_dir = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = ""
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class loadDirectory(bpy.types.Operator):
    bl_idname = 'load.dir'
    bl_label = 'Create/Load Directory'
    bl_description = "Load all data from Root Directory or create new folder for data if none exists"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        path = bpy.context.scene.my_tool.root_dir
        if path != '':
            if os.path.exists(path):
                save_path = path
            else:
                print("oh no")
                return {'FINISHED'}
        else:
            print("is empty")
            save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)

        Blend_My_NFTs_Output, batch_json_save_path = make_directories(save_path)
        batch_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(1))
        NFTRecord_save_path = os.path.join(batch_path, "_NFTRecord_{:03d}.json".format(1))
        master_nftrecord_save_path = os.path.join(batch_json_save_path, "_NFTRecord.json")
        bpy.context.scene.my_tool.batch_json_save_path = batch_json_save_path

        bpy.context.scene.my_tool.CurrentBatchIndex = 1
        bpy.context.scene.my_tool.loadNFTIndex = 1
        bpy.context.scene.my_tool.BatchSliderIndex = 1
        if os.path.exists(batch_path) and os.path.exists(NFTRecord_save_path):
            LoadNFT.update_collection_rarity_property(NFTRecord_save_path)
        else:
            LoadNFT.init_batch(batch_json_save_path)
            DNA_Generator.send_To_Record_JSON(NFTRecord_save_path)
            DNA_Generator.set_up_master_Record(master_nftrecord_save_path)
            LoadNFT.update_current_batch(1, batch_json_save_path)
            LoadNFT.update_collection_rarity_property(NFTRecord_save_path)
            
        return {'FINISHED'}
        


class createSlotFolders(bpy.types.Operator):
    bl_idname = 'create.slotfolers'
    bl_label = 'Create Slot Folders (TEMP)'
    bl_description = 'This will override the current folder which cannot be undone. Are you sure?'
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


    def execute(self, context):
        folder_dir = os.path.join(bpy.context.scene.my_tool.root_dir, "Blend_My_NFTs Output")
        SaveNFTsToRecord.CreateSlotsFolderHierarchy(bpy.context.scene.my_tool.root_dir)

        return {'FINISHED'}

class organizeScene(bpy.types.Operator):
    bl_idname = 'create.organizescene'
    bl_label = 'Organize Scene'
    bl_description = 'This will look through all folders for textures and create model copies for each. Are you sure...Punk?'
    bl_options = {"REGISTER", "UNDO"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


    def execute(self, context):
        # folder_dir = os.path.join(bpy.context.scene.my_tool.root_dir, "Blend_My_NFTs Output")
        # SaveNFTsToRecord.SearchForTexturesAndCreateDuplicates(folder_dir)
        original_hierarchy = Exporter.Previewer.get_hierarchy_ordered(1)
        DNA_Generator.save_rarity_To_Record(original_hierarchy)
        return {'FINISHED'}


class createCharacterCollections(bpy.types.Operator):
    bl_idname = 'create.charcolls'
    bl_label = 'Organize Character Collections'
    bl_description = 'This will look through all folders for textures and create model copies for each. Are you sure...Punk?'
    bl_options = {"REGISTER", "UNDO"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


    def execute(self, context):
        folder_dir = os.path.join(bpy.context.scene.my_tool.root_dir, "Blend_My_NFTs Output")
        record_path = os.path.join(folder_dir, "OUTPUT", "Batch_{:03d}".format(1), "_NFTRecord_{:03d}.json".format(1))
        SaveNFTsToRecord.SearchForMeshesAndCreateCharacterDuplicates(record_path)
        return {'FINISHED'}
       


#----------------------------------------------------------------


class renderBatch(bpy.types.Operator):
    bl_idname = "render.batch"
    bl_label = "Render Batch"
    bl_description = "Render out batch"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
        render_batch_num = bpy.context.scene.my_tool.BatchRenderIndex
        export_path = os.path.abspath(bpy.context.scene.my_tool.separateExportPath)
        export_path = os.path.join(export_path, "Blend_My_NFTs Output")
        batch_path = os.path.join(export_path, "OUTPUT", "Batch_{:03d}".format(render_batch_num))
        record_path = os.path.join(batch_path, "_NFTRecord_{:03d}.json".format(render_batch_num))

        if os.path.exists(record_path):
            bpy.context.scene.render.engine = 'BLENDER_EEVEE'
            
            imageEnum = bpy.context.scene.my_tool.imageEnum
            imageBool = bpy.context.scene.my_tool.imageBool
            animationBool = bpy.context.scene.my_tool.animationBool
            modelBool = bpy.context.scene.my_tool.modelBool
            modelEnum = bpy.context.scene.my_tool.modelEnum
            if imageEnum == 'PNG':
                transparency = bpy.context.scene.my_tool.PNGTransparency
            else:
                transparency = False
            batch_count = len(next(os.walk(batch_path))[1])
            range = []
            if not bpy.context.scene.my_tool.renderFullBatch:
                if bpy.context.scene.my_tool.rangeBool:
                    size = bpy.context.scene.my_tool.renderSectionSize
                    index = bpy.context.scene.my_tool.renderSectionIndex
                    range_start = size * (index - 1) + 1
                    range_end = min(size * (index), batch_count)
                    if range_start <= batch_count:
                        range = [range_start, range_end]
                else:
                    range_start = bpy.context.scene.my_tool.renderSectionIndex
                    range_end = min(bpy.context.scene.my_tool.renderSectionSize, batch_count)
                    if range_start <= batch_count and range_end >= range_start:
                        range = [range_start, range_end]
            else:
                range = [1, batch_count]

            file_formats = []
            if imageBool:
                file_formats.append(imageEnum)
            if animationBool:
                file_formats.append("MP4")
            if modelBool:
                file_formats.append(modelEnum)

            if file_formats:
                if range:
                    Exporter.render_nft_batch_custom(export_path, render_batch_num, file_formats, range, transparency)
                else:
                    self.report({"ERROR"}, "Failed: Invalid range")
            else:
                self.report({"ERROR"}, "Failed: No output render types selected :(")
        else:
            self.report({"ERROR"}, "Failed: This Batch does not exist")
        return {'FINISHED'}



class chooseExportFolder(bpy.types.Operator):
    bl_idname = 'choose.export'
    bl_label = 'Choose Export Folder'
    bl_description = "Choose folder for all NFT and render data"
    bl_options = {"REGISTER", "UNDO"}
    filepath: bpy.props.StringProperty(subtype='FILE_PATH', default='')
    filter_glob: bpy.props.StringProperty(default ='',options = {'HIDDEN'})

    # @classmethod
    # def poll(cls, context):
    #     return context.object is not None

    def execute(self, context):
        print(self.filepath)
        bpy.context.scene.my_tool.separateExportPath = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = ""
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}



class moveDataToLocal(bpy.types.Operator):
    bl_idname = 'move.datalocal'
    bl_label = "Copy Record Data"
    bl_description = "this will overwrite files, u sure?"
    bl_options = {'REGISTER', 'UNDO'}

    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        bath_path_end = os.path.join("Blend_My_NFTs Output", "OUTPUT")
        record_save_path = os.path.join(os.path.abspath(bpy.context.scene.my_tool.root_dir), bath_path_end)
        local_save_path = os.path.join(os.path.abspath(bpy.context.scene.my_tool.separateExportPath), bath_path_end)

        success = Exporter.export_record_data(record_save_path, local_save_path)
        if not success:
            self.report({"ERROR"}, "Failed: pls choose a different folder from the root folder")
        return {'FINISHED'}


# --------------------------------------------------------------

class exportMetadata(bpy.types.Operator):
    bl_idname = 'export.metadata'
    bl_label = 'Export ERC721 Metadata'
    bl_description = 'Export out metadata for all NFTs'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bacth_path_end = os.path.join("Blend_My_NFTs Output", "OUTPUT")
        path = os.path.join(os.path.abspath(bpy.context.scene.my_tool.separateExportPath), bacth_path_end)
        Exporter.save_all_metadata_files(path)
        return {'FINISHED'}



class refactorExports(bpy.types.Operator):
    bl_idname = 'refactor.exports'
    bl_label = 'Refactor All Exports'
    bl_description = "Rename all exports"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        export_dir = bpy.context.scene.my_tool.separateExportPath
        batches_path = os.path.join(export_dir, "Blend_My_NFTs Output", "OUTPUT")
        render_record_path = os.path.join(batches_path, "_RenderRecord.json")
        Exporter.refactor_all_batches(batches_path, render_record_path)

        return {'FINISHED'}


class confirmRefactor(bpy.types.Operator):
    bl_idname = 'confirm.refactor'
    bl_label = 'Have all renders been finalized?'
    bl_description = "Are you super super duper sure?"
    bl_options = {'REGISTER', 'UNDO'}
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        global canRefactor
        canRefactor = True
        return {'FINISHED'}

#----------------------------------------------------------------

class purgeData(bpy.types.Operator):
    bl_idname = 'purge.datas'
    bl_label = 'Purge Data?'
    bl_description = 'This will purge mesh, material and collection data'
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        objs = [o for o in bpy.data.objects if not o.users_scene]
        bpy.data.batch_remove(objs)

        mats = [m for m in bpy.data.materials if m.users == 0 and m.name != 'MasterV01']
        bpy.data.batch_remove(mats)

        colls = [c for c in bpy.data.collections if c.users == 0]
        bpy.data.batch_remove(colls)
        return {'FINISHED'}




# -------------------------------------------------------------

class addNewColourStyle(bpy.types.Operator):
    bl_idname = 'add.colorstyle'
    bl_label = 'Save New Colour Style'
    bl_description = 'Append new colour style to colour list'
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        print(">:3c")
        self.report({'INFO'}, '>:3c')
        return {'FINISHED'}

class updateColourStyle(bpy.types.Operator):
    bl_idname = 'update.colorstyle'
    bl_label = 'Update Colour Style'
    bl_description = 'This will overwrite the current colour style, are you sure?'
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        save_path = os.path.abspath(bpy.context.scene.my_tool.save_path)
        DNA_Generator.Outfit_Generator.ColorGen.SetUpCharacterStyle("//EMPIRE/Empire/INTERACTIVE_PROJECTS/SOUL_AETHER/3D_PRODUCTION/", "Kae")
        DNA_Generator.Outfit_Generator.ColorGen.PickOutfitColors("//EMPIRE/Empire/INTERACTIVE_PROJECTS/SOUL_AETHER/3D_PRODUCTION/", "not", [])
        return {'FINISHED'}


class deleteColourStyle(bpy.types.Operator):
    bl_idname = 'delete.colorstyle'
    bl_label = 'Delete Colour Style'
    bl_description = 'This cannot be undone, are you sure?'
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        image_path = os.path.abspath("T_cellMain_N.png")
        im = Image.open(image_path)
        return {'FINISHED'}


class nextColorStyle(bpy.types.Operator):
    bl_idname = 'next.colorstyle'
    bl_label = 'Next Style'
    bl_description = 'Next colour style'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        DNA_Generator.Outfit_Generator.ColorGen.add_to_colourindex(1)
        return {'FINISHED'}


class prevColorStyle(bpy.types.Operator):
    bl_idname = 'prev.colorstyle'
    bl_label = 'Prev Style'
    bl_description = 'Next colour style'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        DNA_Generator.Outfit_Generator.ColorGen.add_to_colourindex(-1)
        return {'FINISHED'}


class nextTextureSet(bpy.types.Operator):
    bl_idname = 'next.textureset'
    bl_label = 'Next Set'
    bl_description = 'Next texture set'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        DNA_Generator.Outfit_Generator.ColorGen.add_to_textureindex(1)
        return {'FINISHED'}


class prevTextureSet(bpy.types.Operator):
    bl_idname = 'prev.textureset'
    bl_label = 'Prev Set'
    bl_description = 'Prev ctexture set'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        DNA_Generator.Outfit_Generator.ColorGen.add_to_textureindex(-1)
        return {'FINISHED'}



# --------------------------------- Textures ---------------------------------------------


class downresTextures(bpy.types.Operator):
    bl_idname = 'downres.textures'
    bl_label = 'Create Down-res Textures'
    bl_description = 'Create Down-res Textures'
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        input_path = os.path.join(bpy.context.scene.my_tool.root_dir, 'INPUT')
        resolutions = [1024]
        TextureEditor.create_downres_textures(input_path, resolutions)
        return {'FINISHED'}


class renameAllOriginalTextures(bpy.types.Operator):
    bl_idname = 'rename.textures'
    bl_label = 'Rename All Textures'
    bl_description = "This can't be undone okay!!!!!!"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        input_path = os.path.join(bpy.context.scene.my_tool.root_dir, 'INPUT')
        TextureEditor.rename_all_original_textures(input_path)
        return {'FINISHED'}

# ------------------------------- Panels ----------------------------------------------

#Create Preview Panel

class WCUSTOM_PT_FCreateData(bpy.types.Panel):
    bl_label = "Create NFTs and Data"
    bl_idname = "WCUSTOM_PT_FCreateData"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GENERATION'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        scene = context.scene
        mytool = scene.my_tool





class WCUSTOM_PT_PreviewNFTs(bpy.types.Panel):
    bl_label = "Create NFTs"
    bl_idname = "WCUSTOM_PT_PreviewNFTs"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GENERATION'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.prop(mytool, "inputDNA")
        row.operator(randomizePreview.bl_idname, text=randomizePreview.bl_label)

        # row = layout.separator(factor=0.0)
        row = layout.row()
        row.prop(mytool, "maxNFTs")
        row.operator(createBatch.bl_idname, text=createBatch.bl_label)

        row = layout.separator()
        box = layout.box()
        row = box.row()
        row.operator(saveCurrentNFT.bl_idname, text=saveCurrentNFT.bl_label)
        row.operator(saveNewNFT.bl_idname, text=saveNewNFT.bl_label)


       

# class WCUSTOM_PT_NFTSlots(bpy.types.Panel):
#     bl_label = "Customize Slots"
#     bl_idname = "WCUSTOM_PT_NFTSlots"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'GENERATION'

#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool

#         for name in Slots:
#             layout.row().label(text=Slots[name][1])
#             row = layout.row()
#             row.prop(mytool, name, text="")
#             row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).collection_name = name
#             row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label).collection_name = name


class WCUSTOM_PT_ParentSlots(bpy.types.Panel):
    bl_label = "All Slots"
    bl_idname = "WCUSTOM_PT_ParentSlots"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GENERATION'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        row = layout.row()
        for char in config.Characters:
            inputDNA = bpy.context.scene.my_tool.inputDNA
            DNASplit = inputDNA.split(',')
            if char == DNASplit[0]:
                row.operator(swapCharacter.bl_idname, text=char, emboss=False).character_name = char
            else:
                row.operator(swapCharacter.bl_idname, text=char).character_name = char

        row = layout.row()
        row.prop(mytool, "isCharacterLocked", toggle=1, expand=True)

        box = layout.box()
        row = box.row()
        row.prop(mytool, "textureSize", expand=True)




# class WCUSTOM_PT_TorsoSlots(bpy.types.Panel):
#     bl_label = "Torso Slots"
#     bl_idname = "WCUSTOM_PT_TorsoSlots"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'GENERATION'
#     bl_parent_id = 'WCUSTOM_PT_ParentSlots'

#     slots = {"inputUpperTorso": ("MOD_CLOTH"),
#     "inputMiddleTorso": ("MOD_CLOTH"),
#     "inputBackPack": ("CON_ARMATURE")}
    
#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool
#         for name in self.slots:
#             row = layout.row()
#             row.label(text=Slots[name][1], icon=self.slots[name])
#             row.prop(mytool, name, text="")
#             row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).collection_name = name
#             row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label).collection_name = name

# class WCUSTOM_PT_ArmSlots(bpy.types.Panel):
#     bl_label = "Arms Slots"
#     bl_idname = "WCUSTOM_PT_ArmSlots"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'GENERATION'
#     bl_parent_id = 'WCUSTOM_PT_ParentSlots'

#     slots = {
#     "inputRForeArm": ("LOOP_FORWARDS"),
#     "inputLForeArm": ("LOOP_BACK"),
#     "inputRWrist": ("FORWARD"),
#     "inputLWrist": ("BACK"),
#     "inputHands": ("VIEW_PAN"),}
    
#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool
#         for name in self.slots:
#             row = layout.row()
#             row.label(text=Slots[name][1], icon=self.slots[name])
#             row.prop(mytool, name, text="")
#             row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).collection_name = name
#             row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label).collection_name = name

# class WCUSTOM_PT_LegSlots(bpy.types.Panel):
#     bl_label = "Leg Slots"
#     bl_idname = "WCUSTOM_PT_LegSlots"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'GENERATION'
#     bl_parent_id = 'WCUSTOM_PT_ParentSlots'

#     slots = {
#     "inputPelvisThick": ("OUTLINER_OB_ARMATURE"),
#     "inputPelvisThin": ("HANDLE_ALIGNED"),
#     "inputCalf": ("LINCURVE"),
#     "inputAnkle": ("LINCURVE"),
#     "inputFeet": ("MOD_DYNAMICPAINT"),}
    
#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool
#         for name in self.slots:
#             row = layout.row()
#             row.label(text=Slots[name][1], icon=self.slots[name])
#             row.prop(mytool, name, text="")
#             row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).collection_name = name
#             row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label).collection_name = name

# class WCUSTOM_PT_HeadSlots(bpy.types.Panel):
#     bl_label = "Head Slots"
#     bl_idname = "WCUSTOM_PT_HeadSlots"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'GENERATION'
#     bl_parent_id = 'WCUSTOM_PT_ParentSlots'

#     slots = {
#     "inputUpperHead": ("MESH_CONE"),
#     "inputMiddleHead": ("HIDE_OFF"),
#     "inputLowerHead": ("USER"),
#     "inputEarings": ("PMARKER_ACT"),
#     "inputNeck": ("NODE_INSERT_OFF"),}
    
#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool
#         for name in self.slots:
#             row = layout.row()
#             row.label(text=Slots[name][1], icon=self.slots[name])
#             row.prop(mytool, name, text="")
#             row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).collection_name = name
#             row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label).collection_name = name

# class WCUSTOM_PT_OtherSlots(bpy.types.Panel):
#     bl_label = "Other Slots"
#     bl_idname = "WCUSTOM_PT_OtherSlots"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'GENERATION'
#     bl_parent_id = 'WCUSTOM_PT_ParentSlots'
#     slots = {"inputBackground": ("NODE_TEXTURE")}
    
#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool
#         for name in self.slots:
#             row = layout.row()
#             row.label(text=Slots[name][1], icon=self.slots[name])
#             row.prop(mytool, name, text="")
#             row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).collection_name = name
#             row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label).collection_name = name


#-----------------------------------------------------------------------

class WCUSTOM_PT_ELoadFromFile(bpy.types.Panel):
    bl_label = "Load from File"
    bl_idname = "WCUSTOM_PT_ELoadFromFile"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GENERATION'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        index = int(bpy.context.scene.my_tool.CurrentBatchIndex)
        nft_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{:03d}".format(index))

        if os.path.exists(nft_save_path):
            row.label(text="Current Generated: " + str(len(next(os.walk(nft_save_path))[1])))
        else:
            print()
        row = layout.row()
        row.prop(mytool, "loadNFTIndex")
        row.operator(loadNFT.bl_idname, text=loadNFT.bl_label)
        
        row = layout.row()
        row.operator(loadPrevNFT.bl_idname, text=loadPrevNFT.bl_label)
        row.operator(loadNextNFT.bl_idname, text=loadNextNFT.bl_label)

        row = layout.row()
        row.operator(deleteNFT.bl_idname, text=deleteNFT.bl_label, emboss=False)
        row.operator(deleteAllNFTs.bl_idname, text=deleteAllNFTs.bl_label, emboss=False)
        return


class GU_PT_collection_custom_properties(bpy.types.Panel, PropertyPanel):
    _context_path = "collection"
    _property_type = bpy.types.Collection
    bl_label = "Custom Properties"
    bl_idname = "GU_PT_collection_custom_properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "collection"


class WCUSTOM_PT_EditBatch(bpy.types.Panel):
    bl_label = "Batch Editor"
    bl_idname = "WCUSTOM_PT_EditRarity"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GENERATION'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        row = layout.row()
        if os.path.exists(bpy.context.scene.my_tool.batch_json_save_path):
            batch_path = bpy.context.scene.my_tool.batch_json_save_path
            row.label(text="Current Batch: {} / {}".format(bpy.context.scene.my_tool.CurrentBatchIndex, len(os.listdir(batch_path)) - 1))
        else:
            # row.label(text="Current Batch: {}".format(bpy.context.scene.my_tool.CurrentBatchIndex))
            row.label(text="Please create or load directory")

        row = layout.row()
        row.prop(mytool, "BatchSliderIndex")

        row.operator(loadBatch.bl_idname, text=loadBatch.bl_label)
        row = layout.row()
        row.operator(saveBatch.bl_idname, text=saveBatch.bl_label)
        row.operator(saveNewBatch.bl_idname, text=saveNewBatch.bl_label)
        row = layout.row()
        row.operator(resetBatch.bl_idname, text=resetBatch.bl_label, emboss=False)



class WCUSTOM_PT_ARootDirectory(bpy.types.Panel):
    bl_label = "Root Directory"
    bl_idname = "WCUSTOM_PT_ARootDirectory"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GENERATION'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        output_path = os.path.abspath(os.path.join(mytool.batch_json_save_path, '..\..'))
        row = layout.row()
        
        if output_path != os.path.abspath(mytool.root_dir):
            row.operator(initializeRecord.bl_idname, text=initializeRecord.bl_label, emboss=False)
        else:
            row.operator(initializeRecord.bl_idname, text=initializeRecord.bl_label)

        box = layout.box()
        row = box.row()
        row.prop(mytool, "root_dir",text='')
        row.operator(chooseRootFolder.bl_idname, text=chooseRootFolder.bl_label)

        row = layout.row()
        row.label(text="Current loaded directory:")
        row = layout.row()
        row.label(text=output_path)

        row = layout.row()
        row.operator(loadDirectory.bl_idname, text=loadDirectory.bl_label)

        row = layout.row()
        row.operator(createSlotFolders.bl_idname, text=createSlotFolders.bl_label)

        # row = layout.row()
        row.operator(downresTextures.bl_idname, text=downresTextures.bl_label)


#-----------------------------------------------------------------------

class WCUSTOM_PT_OutputSettings(bpy.types.Panel):
    bl_label = "Export Settings"
    bl_idname = "WCUSTOM_PT_OutputSettings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EXPORTING'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.prop(mytool, "separateExportPath")
        row.operator(chooseExportFolder.bl_idname, text=chooseExportFolder.bl_label)

        row = layout.row()
        row.operator(moveDataToLocal.bl_idname, text=moveDataToLocal.bl_label)
        export_path = os.path.join(mytool.separateExportPath, "Blend_My_NFTs Output", "OUTPUT")



class WCUSTOM_PT_Render(bpy.types.Panel):
    bl_label = "Render NFTs"
    bl_idname = "WCUSTOM_PT_Render"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EXPORTING'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        export_path = os.path.join(mytool.separateExportPath, "Blend_My_NFTs Output", "OUTPUT")
        if os.path.exists(export_path) and bpy.context.scene.my_tool.root_dir != bpy.context.scene.my_tool.separateExportPath:
            batches_path = os.path.join(bpy.context.scene.my_tool.separateExportPath, "Blend_My_NFTs Output", "OUTPUT")
            batch_path = os.path.join(batches_path, "Batch_{:03d}".format(mytool.BatchRenderIndex))
            box = layout.box()
            boxbox = box.box()
            row = boxbox.row()
            row.label(text="WARNING:")
            row = box.row()
            row.label(text="Only render once all NFTs have been generated and finalized.")
            layout.separator()

            batch_count = len(os.listdir(batches_path)) - 1
            row = layout.row()
            row.label(text="Total Batches: {}".format(batch_count))            
            row = layout.row()
            row.prop(mytool, "BatchRenderIndex")

            row = layout.row()
            if os.path.exists(batch_path):
                batch_count = len(next(os.walk(batch_path))[1])
                row.label(text="Number in batch: {}".format(batch_count))
            else:
                batch_count = 0
                row.label(text="This batch doesn't exist")
            row.prop(mytool, "renderFullBatch",toggle=-1)
            layout.separator()

            if not bpy.context.scene.my_tool.renderFullBatch:
                row = layout.row()
                size = bpy.context.scene.my_tool.renderSectionSize
                index = bpy.context.scene.my_tool.renderSectionIndex
                
                if mytool.rangeBool:
                    range_start = size * (index - 1) + 1
                    range_end = min(size * (index), batch_count)
                else:
                    range_start = mytool.renderSectionIndex
                    range_end = min(mytool.renderSectionSize, batch_count)

                row = layout.row()
                row.prop(mytool, "rangeBool")

                if range_start > batch_count or range_start > range_end:
                    row.label(text="Render range: Out of range")
                else:
                    if mytool.rangeBool:
                        row.label(text="Render range: {} ~ {}".format(range_start, range_end))
                    else:
                        row.label(text="Render total: {}".format(range_end - range_start + 1))

                row = layout.row()
                if mytool.rangeBool:
                    row.prop(mytool, "renderSectionIndex")
                    row.prop(mytool, "renderSectionSize")
                else:
                    row.prop(mytool, "renderSectionIndex", text="Range Start")
                    row.prop(mytool, "renderSectionSize", text="Range End")

            row = layout.row()
            row.prop(mytool, "imageBool")
            row.prop(mytool, "animationBool")
            row.prop(mytool, "modelBool")
            if mytool.imageBool:
                row = layout.row()
                row.label(text="Image Type:")
                row.prop(mytool, "imageEnum", expand=True)
                row = layout.row()

                if(bpy.context.scene.my_tool.imageEnum == 'PNG'):
                    row.label(text="")
                    row.label(text="")
                    row.prop(mytool, "PNGTransparency",toggle=1)
                    row = layout.row()
            if mytool.modelBool:
                row = layout.row()
                row.label(text="Model Type:")
                row.prop(mytool, "modelEnum", expand=True)
                row = layout.row()

            layout.separator()
            box = layout.box()
            box.operator(renderBatch.bl_idname, text=renderBatch.bl_label)


#-------------------------------------------

class WCUSTOM_PT_CreateMetadata(bpy.types.Panel):
    bl_label = "Export Metadata"
    bl_idname = "WCUSTOM_PT_CreateMetadata"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EXPORTING'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()

        export_path = os.path.join(mytool.separateExportPath, "Blend_My_NFTs Output", "OUTPUT")
        if os.path.exists(export_path) and bpy.context.scene.my_tool.root_dir != bpy.context.scene.my_tool.separateExportPath:
            row.operator(exportMetadata.bl_idname, text=exportMetadata.bl_label, emboss=True)

#------------------------------------


class WCUSTOM_PT_RefactorExports(bpy.types.Panel):
    bl_label = "Refactor All Exports"
    bl_idname = "WCUSTOM_PT_RefactorExports"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EXPORTING'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool


        if canRefactor:
            export_path = os.path.join(mytool.separateExportPath, "Blend_My_NFTs Output", "OUTPUT")
            if os.path.exists(export_path) and bpy.context.scene.my_tool.root_dir != bpy.context.scene.my_tool.separateExportPath:

                row = layout.row()
                row.prop(mytool, "renderPrefix")

                row = layout.row()
                row.label(text="Output example:")
                row.label(text="{}0123.png".format(mytool.renderPrefix))
                row = layout.row()
                row.operator(refactorExports.bl_idname, text=refactorExports.bl_label)
        else:
            box = layout.box()
            row = box.row()
            row.label(text=confirmRefactor.bl_label)
            row = box.row()
            row.operator(confirmRefactor.bl_idname, text="Confirm")



#------------------------------------

class WCUSTOM_PT_Initialize(bpy.types.Panel):
    bl_label = "Render NFTs"
    bl_idname = "WCUSTOM_PT_Initialize"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SET UP'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        row = layout.row()
        row.label(text="Collections:")
        row = layout.row()
        
        row.operator(createSlotFolders.bl_idname, text=createSlotFolders.bl_label)

        row = layout.row()
        row.label(text="Textures:")

        row = layout.row()
        row.operator(renameAllOriginalTextures.bl_idname, text=renameAllOriginalTextures.bl_label)
        row = layout.row()
        row.operator(downresTextures.bl_idname, text=downresTextures.bl_label)


        row = layout.row()

        row.label(text="Clean up:")
        row = layout.row()
        row.operator(purgeData.bl_idname, text=purgeData.bl_label)




# --------------------------------------------------------

class WCUSTOM_PT_ArtistUI(bpy.types.Panel):
    bl_label ="Colour Panel"
    bl_idname = "WCUSTOM_PT_ArtistUI"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ARTIST'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        box = row.box()
        box.label(text="Some text here as instructions?")

        layout.separator()

        row = layout.row()
        row.operator(prevColorStyle.bl_idname, text=prevColorStyle.bl_label)
        row.prop(mytool, "colourStyleIndex", text='')
        row.operator(nextColorStyle.bl_idname, text=nextColorStyle.bl_label)

        row = layout.row()
        row.operator(prevTextureSet.bl_idname, text=prevTextureSet.bl_label)
        row.prop(mytool, "textureSetIndex", text='')
        row.operator(nextTextureSet.bl_idname, text=nextTextureSet.bl_label)

        layout.separator()

        box = layout.box()
        row = box.row()
        row.label(text="Color Style Name")
        row.prop(mytool, "colorStyleName", text="")

        layout.separator()

        row = layout.row()
        row.prop(mytool, "RTint", text="Red Tint")
        row = layout.row()
        row.prop(mytool, "GTint", text="Green Tint")
        row = layout.row()
        row.prop(mytool, "BTint", text="Blue Tint")

        layout.separator()
        box = layout.box()

        row = box.row()
        row.operator(updateColourStyle.bl_idname, text=updateColourStyle.bl_label)
        row.operator(addNewColourStyle.bl_idname, text=addNewColourStyle.bl_label)
        row = box.row()
        row.operator(deleteColourStyle.bl_idname, text=deleteColourStyle.bl_label, emboss=False)
        
# # Documentation Panel:
# class BMNFTS_PT_Documentation(bpy.types.Panel):
#     bl_label = "Documentation"
#     bl_idname = "BMNFTS_PT_Documentation"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Blend_My_NFTs'

#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool

#         row = layout.row()
#         row.operator("wm.url_open", text="Documentation",
#                      icon='URL').url = "https://github.com/torrinworx/Blend_My_NFTs"

classes = (
    #Panels

    BMNFTS_PGT_MyProperties,
    WCUSTOM_PT_Initialize,
    WCUSTOM_PT_ARootDirectory,
    WCUSTOM_PT_EditBatch,
    WCUSTOM_PT_ELoadFromFile,
    WCUSTOM_PT_PreviewNFTs,
    # WCUSTOM_PT_FCreateData,
    WCUSTOM_PT_ParentSlots,
    # WCUSTOM_PT_HeadSlots,
    # WCUSTOM_PT_TorsoSlots,
    # WCUSTOM_PT_ArmSlots,
    # WCUSTOM_PT_LegSlots,
    # WCUSTOM_PT_OtherSlots,
    GU_PT_collection_custom_properties,
    WCUSTOM_PT_OutputSettings,
    WCUSTOM_PT_Render,
    WCUSTOM_PT_CreateMetadata,
    WCUSTOM_PT_RefactorExports,
    WCUSTOM_PT_ArtistUI,
    # BMNFTS_PT_Documentation,


    # Operators:

    loadBatch,
    saveBatch,
    saveNewBatch,
    resetBatch,
    # randomizeModel,
    # randomizeColor,
    clearSlots,
    initializeRecord,
    randomizePreview,
    saveNewNFT,
    saveCurrentNFT,
    createBatch,
    loadNFT,
    loadPrevNFT,
    loadNextNFT,
    swapCharacter,
    chooseRootFolder,
    loadDirectory,
    deleteNFT,
    deleteAllNFTs,
    createSlotFolders,
    organizeScene,
    createCharacterCollections,
    renderBatch,
    chooseExportFolder,
    moveDataToLocal,
    purgeData,
    exportMetadata,
    addNewColourStyle,
    updateColourStyle,
    nextColorStyle,
    prevColorStyle,
    nextTextureSet,
    prevTextureSet,
    deleteColourStyle,
    confirmRefactor,
    refactorExports,

    downresTextures,
    renameAllOriginalTextures

)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=BMNFTS_PGT_MyProperties)

    # UIList1:

    # bpy.types.Scene.custom = bpy.props.CollectionProperty(type=UIList.CUSTOM_PG_objectCollection)
    # bpy.types.Scene.custom_index = bpy.props.IntProperty()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.my_tool

    # UIList 1:

    # del bpy.types.Scene.custom
    # del bpy.types.Scene.custom_index

if __name__ == '__main__':
    register()
