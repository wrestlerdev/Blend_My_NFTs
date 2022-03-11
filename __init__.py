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

from cgitb import text
from venv import create
import bpy
from bpy.app.handlers import persistent

# import json

import os
import importlib

# Import files from main directory:

importList = ['Batch_Sorter', 'DNA_Generator', 'Exporter', 'Batch_Refactorer', 'get_combinations', 'SaveNFTsToRecord', 'UIList', 'Previewer']

if bpy in locals():
        importlib.reload(Previewer)
        importlib.reload(DNA_Generator)
        importlib.reload(Batch_Sorter)
        importlib.reload(Exporter)
        importlib.reload(Batch_Refactorer)
        importlib.reload(get_combinations)
        importlib.reload(SaveNFTsToRecord)
        importlib.reload(UIList)
else:
    from .main import \
        Previewer, \
        DNA_Generator, \
        Batch_Sorter, \
        Exporter, \
        Batch_Refactorer, \
        SaveNFTsToRecord, \
        get_combinations

    from .ui_Lists import UIList

Slots = {"inputUpperTorso": ("AUpperTorso", "Upper Torso Slot"),
    "inputMiddleTorso": ("BMiddleTorso", "Mid Torso Slot"),
    "inputLForeArm": ("CLForeArm", "Left Forearm Slot"),
    "inputLWrist": ("DLWrist", "Left Wrist Slot"),
    "inputRForeArm": ("ERForeArm", "Right Forearm Slot"),
    "inputRWrist": ("FRWrist", "Right Wrist Slot"),
    "inputHands": ("HHands", "Hands Slot"),
    "inputLowerTorso": ("ILowerTorso", "Lower Torso Slot"),
    "inputCalf": ("JCalf", "Calf Slot"),
    "inputAnkle": ("KAnkle", "Ankle Slot"),
    "inputFeet": ("LFeet", "Feet Slot"),
    "inputNeck": ("MNeck", "Neck Slot"),
    "inputLowerHead": ("NLowerHead", "Lower Head Slot"),
    "inputMiddleHead": ("OMiddleHead", "Mid Head Slot"),
    "inputEarrings": ("PEarings", "Earrings Slot"),
    "inputUpperHead": ("QUpperHead", "UpperHead Slot"),
    "inputBackpack": ("RBackPack", "Backpack Slot")}
    

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
            ('GLTF_SEPARATE', '.gltf + .bin + textures', 'Export NFT as .gltf with separated textures in .bin + textures.'),
            ('GLTF_EMBEDDED', '.gltf', 'Export NFT as embedded .gltf file that contains textures.'),
            ('FBX', '.fbx', 'Export NFT as .fbx'),
            ('OBJ', '.obj', 'Export NFT as .obj'),
            ('X3D', '.x3d', 'Export NFT as .x3d'),
            ('STL', '.stl', 'Export NFT as .stl'),
            ('VOX', '.vox (Experimental)', 'Export NFT as .vox, requires the voxwriter add on: https://github.com/Spyduck/voxwriter')
        ]
    )

    cardanoMetaDataBool: bpy.props.BoolProperty(name="Cardano Cip")
    solanaMetaDataBool: bpy.props.BoolProperty(name="Solana Metaplex")
    erc721MetaData: bpy.props.BoolProperty(name="ERC721")

    # API Panel properties:
    apiKey: bpy.props.StringProperty(name="API Key", subtype='PASSWORD')




    # Custom properties

    inputDNA: bpy.props.StringProperty(name="DNA")

    inputUpperTorso: bpy.props.PointerProperty(name="Upper Torso Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputUpperTorso",Slots))
    inputMiddleTorso: bpy.props.PointerProperty(name="",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputMiddleTorso",Slots))
    inputLForeArm: bpy.props.PointerProperty(name="",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputLForeArm",Slots))
    inputLWrist: bpy.props.PointerProperty(name="Left Wrist Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputLWrist",Slots))
    inputRForeArm: bpy.props.PointerProperty(name="",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputRForeArm",Slots))
    inputRWrist: bpy.props.PointerProperty(name="Right Wrist Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputRWrist",Slots))
    inputLowerTorso: bpy.props.PointerProperty(name="Lower Torso Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputLowerTorso",Slots))
    inputHands: bpy.props.PointerProperty(name="Hands Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputHands",Slots))
    inputCalf: bpy.props.PointerProperty(name="Calf Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputCalf",Slots))
    inputAnkle: bpy.props.PointerProperty(name="Ankle Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputAnkle",Slots))
    inputFeet: bpy.props.PointerProperty(name="Feet Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputFeet",Slots))
    inputNeck: bpy.props.PointerProperty(name="Neck Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputNeck",Slots))
    inputLowerHead: bpy.props.PointerProperty(name="",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputLowerHead",Slots))
    inputMiddleHead: bpy.props.PointerProperty(name="",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputMiddleHead",Slots))
    inputEarrings: bpy.props.PointerProperty(name="",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputEarrings",Slots))
    inputUpperHead: bpy.props.PointerProperty(name="t",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputUpperHead",Slots))
    inputBackpack: bpy.props.PointerProperty(name="",type=bpy.types.Collection,
                                                update=lambda s,c: Previewer.collections_have_updated("inputBackpack",Slots))


def make_directories(save_path):
    Blend_My_NFTs_Output = os.path.join(save_path, "Blend_My_NFTs Output", "NFT_Data")
    batch_json_save_path = os.path.join(Blend_My_NFTs_Output, "Batch_Data")

    nftBatch_save_path = os.path.join(save_path, "Blend_My_NFTs Output", "Generated NFT Batches")

    if not os.path.exists(Blend_My_NFTs_Output):
        os.makedirs(Blend_My_NFTs_Output)
    if not os.path.exists(batch_json_save_path):
        os.makedirs(batch_json_save_path)
    if not os.path.exists(nftBatch_save_path):
        os.makedirs(nftBatch_save_path)
    return Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path

# Update NFT count:
combinations: int = 0
offset: int = 0

@persistent
def update_combinations(dummy1, dummy2):
    global combinations
    global offset

    combinations = (get_combinations.get_combinations_from_scene()) - offset

    # redraw_panel()

bpy.app.handlers.depsgraph_update_post.append(update_combinations)


batch_json_save_path = ""
DataDictionary = dict()
# ------------------------------- Operators ---------------------------------------------

class createNFTRecord(bpy.types.Operator):
    bl_idname = 'create.record'
    bl_label = 'Create NFT Record'
    bl_description = "This will reinitialize the entire NFT ledger. Are you sure?"
    bl_options = {"REGISTER", "INTERNAL"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        nftName = "temp"
        maxNFTs = bpy.context.scene.my_tool.collectionSize
        nftsPerBatch = 1
        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        enableRarity = bpy.context.scene.my_tool.enableRarity
        inputDNA = bpy.context.scene.my_tool.inputDNA


        global batch_json_save_path

        Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)
        DataDictionary = DNA_Generator.send_To_Record_JSON(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity, Blend_My_NFTs_Output, batch_json_save_path)

        return {'FINISHED'}


class randomizePreview(bpy.types.Operator):
    bl_idname = 'randomize.preview'
    bl_label = 'Randomize All'
    bl_description = "Create and generate random combination"
    bl_options = {"REGISTER", "UNDO"} # what do these mean btw lmao

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        nftName = "temp"
        maxNFTs = bpy.context.scene.my_tool.collectionSize
        nftsPerBatch = 1
        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        enableRarity = bpy.context.scene.my_tool.enableRarity
        # some randomize dna code here
        DNA = DNA_Generator.Outfit_Generator.RandomizeFullCharacter(maxNFTs, save_path)
        Previewer.fill_pointers_from_dna(DNA[0])
        bpy.context.scene.my_tool.inputDNA = DNA[0]
        return {'FINISHED'}


class previewNFT(bpy.types.Operator):
    bl_idname = 'create.preview'
    bl_label = 'Create Preview'
    bl_description = 'Generates Test NFT'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        maxNFTs = 1
        nftsPerBatch = 1
        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        inputDNA = bpy.context.scene.my_tool.inputDNA

        if inputDNA == "":
            DNASet = DNA_Generator.Outfit_Generator.RandomizeFullCharacter(maxNFTs, save_path)
            bpy.context.scene.my_tool.inputDNA = DNASet[0]
            Previewer.fill_pointers_from_dna(DNASet[0])
        else:
            print("generating from DNA")
            Previewer.show_nft_from_dna(inputDNA)
        return {"FINISHED"}


class randomizeModel(bpy.types.Operator):
    bl_idname = 'randomize.model'
    bl_label = 'Randomize Model'
    bl_options = {"REGISTER", "UNDO"}
    collection_name: bpy.props.StringProperty(default="")

    # def invoke(self, context, event):
    #     print("I HAVE BEEN INVOKED")
    #     print(event.type)
    #     return {'FINISHED'}

    def execute(self, context):

        if self.collection_name != "":
            if self.collection_name in bpy.context.scene.my_tool:
                
                # Blend_My_NFTs_Output = os.path.join(bpy.path.abspath(bpy.context.scene.my_tool.save_path), "Blend_My_NFTs Output", "NFT_Data")
                # NFTRecord_save_path = os.path.join(Blend_My_NFTs_Output, "NFTRecord.json")
                # DataDictionary = json.load(open(NFTRecord_save_path))
                # hierarchy = DataDictionary["hierarchy"]
                # DNAList = DataDictionary["DNAList"]
                # variant_index = Outfit_Generator.PickWeightedDNAStrand(hierarchy.get(slot))
                rand_variant = Previewer.get_random_from_collection(bpy.data.collections[Slots[self.collection_name][0]])
                Previewer.collections_have_updated(Slots[self.collection_name][0], Slots)
                bpy.context.scene.my_tool[str(self.collection_name)] = rand_variant
        return {'FINISHED'}

class randomizeColor(bpy.types.Operator):
    bl_idname = 'randomize.color'
    bl_label = 'Randomize Color/Texture'
    bl_options = {"REGISTER", "UNDO"}
    collection_name: bpy.props.StringProperty(default="")

    def execute(self, context):
        if self.collection_name != "":
            print("this should rando color sometime")
        
        return {'FINISHED'}

class saveNFT(bpy.types.Operator):
    bl_idname = 'save.nft'
    bl_label = 'Save Character'
    bl_options = {"REGISTER", "UNDO"}


    def execute(self, context):
        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        DNASet = set(context.scene.my_tool.inputDNA)
        SaveNFTsToRecord.SaveNFT(DNASet, save_path, batch_json_save_path)

# # Main Operators:
# class createData(bpy.types.Operator):
#     bl_idname = 'create.data'
#     bl_label = 'Create Data'
#     bl_description = 'Creates NFT Data. Run after any changes were made to scene.'
#     bl_options = {"REGISTER", "UNDO"}

#     def execute(self, context):

#         nftName = bpy.context.scene.my_tool.nftName
#         maxNFTs = bpy.context.scene.my_tool.collectionSize
#         nftsPerBatch = bpy.context.scene.my_tool.nftsPerBatch
#         save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
#         enableRarity = bpy.context.scene.my_tool.enableRarity

#         Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

#         Previewer.DNA_Generator.send_To_Record_JSON(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity, Blend_My_NFTs_Output)
#         Batch_Sorter.makeBatches(nftName, maxNFTs, nftsPerBatch, save_path, batch_json_save_path)
#         return {"FINISHED"}

# class exportNFTs(bpy.types.Operator):
#     bl_idname = 'exporter.nfts'
#     bl_label = 'Export NFTs'
#     bl_description = 'Generate and export a given batch of NFTs.'
#     bl_options = {"REGISTER", "UNDO"}

#     def execute(self, context):
#         nftName = bpy.context.scene.my_tool.nftName
#         save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
#         batchToGenerate = bpy.context.scene.my_tool.batchToGenerate
#         maxNFTs = bpy.context.scene.my_tool.collectionSize

#         Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

#         enableImages = bpy.context.scene.my_tool.imageBool
#         imageFileFormat = bpy.context.scene.my_tool.imageEnum

#         enableAnimations = bpy.context.scene.my_tool.animationBool
#         animationFileFormat = bpy.context.scene.my_tool.animationEnum

#         enableModelsBlender = bpy.context.scene.my_tool.modelBool
#         modelFileFormat = bpy.context.scene.my_tool.modelEnum


#         Exporter.render_and_save_NFTs(nftName, maxNFTs, batchToGenerate, batch_json_save_path, nftBatch_save_path, enableImages,
#                                       imageFileFormat, enableAnimations, animationFileFormat, enableModelsBlender,
#                                       modelFileFormat
#                                       )
#         return {"FINISHED"}

# class refactor_Batches(bpy.types.Operator):
#     """Refactor your Batches? This action cannot be undone."""
#     bl_idname = 'refactor.batches'
#     bl_label = 'Refactor your Batches?'
#     bl_description = 'This action cannot be undone.'
#     bl_options = {'REGISTER', 'INTERNAL'}

#     @classmethod
#     def poll(cls, context):
#         return True

#     def execute(self, context):
#         self.report({'INFO'}, "Batches Refactored, MetaData created!")

#         save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)

#         cardanoMetaDataBool = bpy.context.scene.my_tool.cardanoMetaDataBool
#         solanaMetaDataBool = bpy.context.scene.my_tool.solanaMetaDataBool
#         erc721MetaData = bpy.context.scene.my_tool.erc721MetaData

#         Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

#         Batch_Refactorer.reformatNFTCollection(save_path, Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path,
#                                                cardanoMetaDataBool, solanaMetaDataBool, erc721MetaData)
#         return {"FINISHED"}

#     def invoke(self, context, event):
#         return context.window_manager.invoke_confirm(self, event)




# ------------------------------- Panels ----------------------------------------------

#Create Preview Panel
class WCUSTOM_PT_PreviewNFTs(bpy.types.Panel):
    bl_label = "Preview NFT"
    bl_idname = "WCUSTOM_PT_PreviewNFTs"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.operator(createNFTRecord.bl_idname, text=createNFTRecord.bl_label)

        row = layout.row()
        row.label(text='')

        row = layout.row()
        row.prop(mytool, "inputDNA")
        row.operator(randomizePreview.bl_idname, text=randomizePreview.bl_label)

        row = layout.row()
        self.layout.operator(previewNFT.bl_idname, text=previewNFT.bl_label)

        row = layout.row()
        self.layout.operator(saveNFT.bl_idname, text=saveNFT.bl_label)

        row = layout.row()
        row.label(text='')

        for name in Slots:
            layout.row().label(text=Slots[name][1])
            row = layout.row()
            row.prop(mytool, name, text="")
            row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).collection_name = name
            row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label)

# # Create Data Panel:
# class BMNFTS_PT_CreateData(bpy.types.Panel):
#     bl_label = "Create NFT Data"
#     bl_idname = "BMNFTS_PT_CreateData"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Blend_My_NFTs'

#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool

#         layout.label(text=f"Maximum Number Of NFTs: {combinations}")

#         row = layout.row()
#         layout.label(text="")

#         row = layout.row()
#         row.prop(mytool, "nftName")

#         row = layout.row()
#         row.prop(mytool, "collectionSize")

#         row = layout.row()
#         row.prop(mytool, "nftsPerBatch")

#         row = layout.row()
#         row.prop(mytool, "save_path")

#         row = layout.row()
#         row.prop(mytool, "enableRarity")

#         row = layout.row()
#         self.layout.operator("create.data", icon='DISCLOSURE_TRI_RIGHT', text="Create Data")



# # Generate NFTs Panel:
# class BMNFTS_PT_GenerateNFTs(bpy.types.Panel):
#     bl_label = "Generate NFTs"
#     bl_idname = "BMNFTS_PT_GenerateNFTs"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Blend_My_NFTs'

#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool

#         row = layout.row()
#         row.prop(mytool, "imageBool")
#         if  bpy.context.scene.my_tool.imageBool == True:
#             row.prop(mytool, "imageEnum")

#         row = layout.row()
#         row.prop(mytool, "animationBool")
#         if  bpy.context.scene.my_tool.animationBool == True:
#             row.prop(mytool, "animationEnum")

#         row = layout.row()
#         row.prop(mytool, "modelBool")
#         if  bpy.context.scene.my_tool.modelBool == True:
#             row.prop(mytool, "modelEnum")

#         row = layout.row()
#         row.prop(mytool, "batchToGenerate")

#         row = layout.row()
#         self.layout.operator("exporter.nfts", icon='RENDER_RESULT', text="Generate NFTs")

# # Refactor Batches & create MetaData Panel:
# class BMNFTS_PT_Refactor(bpy.types.Panel):
#     bl_label = "Refactor Batches & create MetaData"
#     bl_idname = "BMNFTS_PT_Refactor"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Blend_My_NFTs'

#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool

#         row = layout.row()
#         layout.label(text="Meta Data format:")

#         row = layout.row()
#         row.prop(mytool, "cardanoMetaDataBool")
#         row.prop(mytool, "solanaMetaDataBool")
#         row.prop(mytool, "erc721MetaData")
#         self.layout.operator("refactor.batches", icon='FOLDER_REDIRECT', text="Refactor Batches & create MetaData")

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

# # Logic Panel:
# class BMNFTS_PT_LOGIC_Panel(bpy.types.Panel):
#     bl_label = "Logic"
#     bl_idname = "BMNFTS_PT_LOGIC_Panel"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Blend_My_NFTs'
#
#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool
#
# # Materials Panel:
#
# class BMNFTS_PT_MATERIALS_Panel(bpy.types.Panel):
#     bl_label = "Materials"
#     bl_idname = "BMNFTS_PT_MATERIALS_Panel"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Blend_My_NFTs'
#
#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool
#
# # API Panel:
# class BMNFTS_PT_API_Panel(bpy.types.Panel):
#     bl_label = "API"
#     bl_idname = "BMNFTS_PT_API_Panel"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Blend_My_NFTs'
#
#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool
#
#         row = layout.row()
#         row.prop(mytool, "apiKey")


# def redraw_panel():
#     try:
#         bpy.utils.unregister_class(BMNFTS_PT_CreateData)
#     except:
#         pass
#     bpy.utils.register_class(BMNFTS_PT_CreateData)


# Register and Unregister classes from Blender:
classes = (
    BMNFTS_PGT_MyProperties,
    # BMNFTS_PT_CreateData,
    WCUSTOM_PT_PreviewNFTs,
    # BMNFTS_PT_GenerateNFTs,
    # BMNFTS_PT_Refactor,
    # BMNFTS_PT_Documentation,


    # Other panels:

    # BMNFTS_PT_LOGIC_Panel,
    # BMNFTS_PT_MATERIALS_Panel,
    # BMNFTS_PT_API_Panel,
    randomizeModel,
    randomizeColor,
    createNFTRecord,
    # createData,
    # exportNFTs,
    # refactor_Batches,
    randomizePreview,
    previewNFT,
    saveNFT,
    # UIList 1:

    # UIList.CUSTOM_OT_actions,
    # UIList.CUSTOM_OT_addViewportSelection,
    # UIList.CUSTOM_OT_printItems,
    # UIList.CUSTOM_OT_clearList,
    # UIList.CUSTOM_OT_removeDuplicates,
    # UIList.CUSTOM_OT_selectItems,
    # UIList.CUSTOM_OT_deleteObject,
    # UIList.CUSTOM_UL_items,
    # UIList.CUSTOM_PT_objectList,
    # UIList.CUSTOM_PG_objectCollection,
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
