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


import os
import importlib

# Import files from main directory:

importList = ['Batch_Sorter', 'Exporter', 'Batch_Refactorer', 'get_combinations', 'UIList', 'Previewer']

if bpy in locals():
        importlib.reload(Previewer)
        importlib.reload(Batch_Sorter)
        importlib.reload(Exporter)
        importlib.reload(Batch_Refactorer)
        importlib.reload(get_combinations)
        importlib.reload(UIList)
else:
    from .main import \
        Previewer, \
        Batch_Sorter, \
        Exporter, \
        Batch_Refactorer, \
        get_combinations

    from .ui_Lists import UIList


class WCUSTOM_PGT_SlotCollection(bpy.types.PropertyGroup):
    inputUpperTorso2: bpy.props.PointerProperty(name="Upper Torso Slot",type=bpy.types.Collection)

    

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

    inputUpperTorso: bpy.props.PointerProperty(name="Upper Torso Slot",type=bpy.types.Collection)
    inputLowerTorso: bpy.props.PointerProperty(name="Lower Torso Slot",type=bpy.types.Collection)
    # inputLForearm: bpy.props.PointerProperty(name="Left Forearm Slot",type=bpy.types.Collection)
    # inputRForearm: bpy.props.PointerProperty(name="Right Forearm Slot",type=bpy.types.Collection)
    # inputRWrist: bpy.props.PointerProperty(name="Right Wrist Slot",type=bpy.types.Collection)
    # inputLWrist: bpy.props.PointerProperty(name="Left Wrist Slot",type=bpy.types.Collection)
    inputHands: bpy.props.PointerProperty(name="Hands Slot",type=bpy.types.Collection)
    inputCalf: bpy.props.PointerProperty(name="Calf Slot",type=bpy.types.Collection)
    inputAnkle: bpy.props.PointerProperty(name="Ankle Slot",type=bpy.types.Collection)
    inputFeet: bpy.props.PointerProperty(name="Feet Slot",type=bpy.types.Collection)
    inputNeck: bpy.props.PointerProperty(name="Neck Slot",type=bpy.types.Collection)


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

    redraw_panel()

bpy.app.handlers.depsgraph_update_post.append(update_combinations)

# Main Operators:
class createData(bpy.types.Operator):
    bl_idname = 'create.data'
    bl_label = 'Create Data'
    bl_description = 'Creates NFT Data. Run after any changes were made to scene.'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        nftName = bpy.context.scene.my_tool.nftName
        maxNFTs = bpy.context.scene.my_tool.collectionSize
        nftsPerBatch = bpy.context.scene.my_tool.nftsPerBatch
        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        enableRarity = bpy.context.scene.my_tool.enableRarity

        Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        Previewer.DNA_Generator.send_To_Record_JSON(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity, Blend_My_NFTs_Output)
        Batch_Sorter.makeBatches(nftName, maxNFTs, nftsPerBatch, save_path, batch_json_save_path)
        return {"FINISHED"}

class exportNFTs(bpy.types.Operator):
    bl_idname = 'exporter.nfts'
    bl_label = 'Export NFTs'
    bl_description = 'Generate and export a given batch of NFTs.'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        nftName = bpy.context.scene.my_tool.nftName
        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        batchToGenerate = bpy.context.scene.my_tool.batchToGenerate
        maxNFTs = bpy.context.scene.my_tool.collectionSize

        Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        enableImages = bpy.context.scene.my_tool.imageBool
        imageFileFormat = bpy.context.scene.my_tool.imageEnum

        enableAnimations = bpy.context.scene.my_tool.animationBool
        animationFileFormat = bpy.context.scene.my_tool.animationEnum

        enableModelsBlender = bpy.context.scene.my_tool.modelBool
        modelFileFormat = bpy.context.scene.my_tool.modelEnum


        Exporter.render_and_save_NFTs(nftName, maxNFTs, batchToGenerate, batch_json_save_path, nftBatch_save_path, enableImages,
                                      imageFileFormat, enableAnimations, animationFileFormat, enableModelsBlender,
                                      modelFileFormat
                                      )
        return {"FINISHED"}

class refactor_Batches(bpy.types.Operator):
    """Refactor your Batches? This action cannot be undone."""
    bl_idname = 'refactor.batches'
    bl_label = 'Refactor your Batches?'
    bl_description = 'This action cannot be undone.'
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.report({'INFO'}, "Batches Refactored, MetaData created!")

        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)

        cardanoMetaDataBool = bpy.context.scene.my_tool.cardanoMetaDataBool
        solanaMetaDataBool = bpy.context.scene.my_tool.solanaMetaDataBool
        erc721MetaData = bpy.context.scene.my_tool.erc721MetaData

        Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)

        Batch_Refactorer.reformatNFTCollection(save_path, Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path,
                                               cardanoMetaDataBool, solanaMetaDataBool, erc721MetaData)
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

class randomizePreview(bpy.types.Operator):
    bl_idname = 'randomize.preview'
    bl_label = 'Randomize'
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
        DNA = Previewer.create_preview_nft(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity)
        bpy.context.scene.my_tool.inputDNA = DNA
        
        return {'FINISHED'}

class previewNFT(bpy.types.Operator):
    bl_idname = 'create.preview'
    bl_label = 'Create Preview'
    bl_description = 'Generates Test NFT'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        nftName = "temp"
        maxNFTs = bpy.context.scene.my_tool.collectionSize
        nftsPerBatch = 1
        save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
        enableRarity = bpy.context.scene.my_tool.enableRarity
        inputDNA = bpy.context.scene.my_tool.inputDNA
        if inputDNA == "":
            Previewer.create_preview_nft(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity)
        else:
            Previewer.show_nft_from_dna(inputDNA, nftName, maxNFTs, nftsPerBatch, save_path, enableRarity)
        # Blend_My_NFTs_Output, batch_json_save_path, nftBatch_save_path = make_directories(save_path)
        # DNA_Generator.send_To_Record_JSON(nftName, maxNFTs, nftsPerBatch, save_path, enableRarity, Blend_My_NFTs_Output)
        # Batch_Sorter.makeBatches(nftName, maxNFTs, nftsPerBatch, save_path, batch_json_save_path)
        return {"FINISHED"}

class randomizeModel(bpy.types.Operator):
    bl_idname = 'randomize.model'
    bl_label = 'Randomize Model'
    bl_options = {"REGISTER", "UNDO"}
    # collection: bpy.props.CollectionProperty(type=BMNFTS_PGT_MyProperties)
    collection_name: bpy.props.StringProperty(default="")
    # coll_text: bpy.context.scene.my_tool.inputUpperTorso
    # var: bpy.props.PointerProperty(name="Upper Torso Slot",type=bpy.types.Collection)


    def setSlot(self, string, scene_slot):
        self.collection_name = string

    def execute(self, context):
        if self.collection_name != "":
            print("wow")
            rand_model_coll = Previewer.get_random_from_collection(bpy.data.collections[self.collection_name])
            if self.collection_name == "AUpperTorso":
                # bpy.context.scene.my_tool.inputUpperTorso = bpy.data.collections[self.collection_name]
                bpy.context.scene.my_tool.inputUpperTorso = rand_model_coll
            elif self.collection_name == "ILowerTorso":
                bpy.context.scene.my_tool.inputLowerTorso = rand_model_coll
            elif self.collection_name == "HHands":
                bpy.context.scene.my_tool.inputHands = rand_model_coll
            elif self.collection_name == "JCalf":
                bpy.context.scene.my_tool.inputCalf = rand_model_coll
            elif self.collection_name == "KAnkle":
                bpy.context.scene.my_tool.inputAnkle = rand_model_coll
            elif self.collection_name == "LFeet":
                bpy.context.scene.my_tool.inputFeet = rand_model_coll
            elif self.collection_name == "MNeck":
                bpy.context.scene.my_tool.inputNeck = rand_model_coll
            # colls2 = {'AUpperTorso': bpy.context.scene.my_tool.inputUpperTorso,'ILowerTorso': bpy.context.scene.my_tool.inputLowerTorso}
            # coll1 = colls2.get(self.collection_name, 'default')
            # coll1 = bpy.data.collections[self.collection_name]
            # print(coll1)
        
        return {'FINISHED'}

class randomizeColor(bpy.types.Operator):
    bl_idname = 'randomize.color'
    bl_label = 'Randomize Color/Texture'
    bl_options = {"REGISTER", "UNDO"}
    collection_name: bpy.props.StringProperty(default="")

    def execute(self, context):
        if self.collection_name != "":
            print("wow")
            # if self.collection_name == "AUpperTorso":
            #     bpy.context.scene.my_tool.inputUpperTorso = bpy.data.collections[self.collection_name]
            # elif self.collection_name == "ILowerTorso":
            #     bpy.context.scene.my_tool.inputLowerTorso = bpy.data.collections[self.collection_name]
            # elif self.collection_name == "HHands":
            #     bpy.context.scene.my_tool.inputHands = bpy.data.collections[self.collection_name]
            # elif self.collection_name == "JCalf":
            #     bpy.context.scene.my_tool.inputCalf = bpy.data.collections[self.collection_name]
            # elif self.collection_name == "KAnkle":
            #     bpy.context.scene.my_tool.inputAnkle = bpy.data.collections[self.collection_name]
            # elif self.collection_name == "LFeet":
            #     bpy.context.scene.my_tool.inputFeet = bpy.data.collections[self.collection_name]
            # elif self.collection_name == "MNeck":
            #     bpy.context.scene.my_tool.inputNeck = bpy.data.collections[self.collection_name]
        
        return {'FINISHED'}


# Create Data Panel:
class BMNFTS_PT_CreateData(bpy.types.Panel):
    bl_label = "Create NFT Data"
    bl_idname = "BMNFTS_PT_CreateData"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.label(text=f"Maximum Number Of NFTs: {combinations}")

        row = layout.row()
        layout.label(text="")

        row = layout.row()
        row.prop(mytool, "nftName")

        row = layout.row()
        row.prop(mytool, "collectionSize")

        row = layout.row()
        row.prop(mytool, "nftsPerBatch")

        row = layout.row()
        row.prop(mytool, "save_path")

        row = layout.row()
        row.prop(mytool, "enableRarity")

        row = layout.row()
        self.layout.operator("create.data", icon='DISCLOSURE_TRI_RIGHT', text="Create Data")

class WCUSTOM_PT_PreviewNFTs(bpy.types.Panel):
    bl_label = "Preview NFT"
    bl_idname = "WCUSTOM_PT_PreviewNFTs"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    Slots = (("inputUpperTorso", "AUpperTorso", "Upper Torso Slot"), 
        ("inputLowerTorso", "ILowerTorso", "Lower Torso Slot"),
        ("inputHands", "HHands", "Hands Slot"),
        ("inputCalf", "JCalf", "Calf Slot"),
        ("inputAnkle", "KAnkle", "Ankle Slot"),
        ("inputFeet", "LFeet", "Feet Slot"),
        ("inputNeck", "MNeck", "Neck Slot"),)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.prop(mytool, "inputDNA")
        row.operator(randomizePreview.bl_idname, text=randomizePreview.bl_label)
        row = layout.row()
        layout.label(text="wah")

        row = layout.row()

        # previewNFT
        self.layout.operator(previewNFT.bl_idname, text=previewNFT.bl_label)

        for name in self.Slots:
            layout.row().label(text=name[2])
            row = layout.row()
            row.prop(mytool, name[0], text="")
            row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).collection_name = name[1]
            row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label)


        # layout.row().label(text="hm")
        # row = layout.row()
        # row.prop(mytool, "inputUpperTorso", text="")
        # row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).collection_name = "AUpperTorso"

        # layout.row().label(text="hm")
        # row = layout.row()
        # row.prop(mytool, "inputLowerTorso", text="")
        # row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).collection_name = "ILowerTorso"

        # row = layout.row()
        # row.prop(mytool, "inputHands", text="")
        # row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).collection_name = "HHands"

        # row = layout.row()
        # row.prop(mytool, "inputCalf", text="")
        # row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).collection_name = "JCalf"

        # row = layout.row()
        # row.prop(mytool, "inputAnkle", text="")
        # row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).collection_name = "KAnkle"

        # row = layout.row()
        # row.prop(mytool, "inputFeet", text="")
        # row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).collection_name = "LFeet"

        # row = layout.row()
        # row.prop(mytool, "inputNeck", text="")
        # row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).collection_name = "MNeck"

        # row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).var = coll
        # row.operator(randomizeModel.bl_idname, text=randomizeModel.bl_label).var = '3'
        # self.layout.operator(randomizeModel.bl_idname).var = '2'

# Generate NFTs Panel:
class BMNFTS_PT_GenerateNFTs(bpy.types.Panel):
    bl_label = "Generate NFTs"
    bl_idname = "BMNFTS_PT_GenerateNFTs"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.prop(mytool, "imageBool")
        if  bpy.context.scene.my_tool.imageBool == True:
            row.prop(mytool, "imageEnum")

        row = layout.row()
        row.prop(mytool, "animationBool")
        if  bpy.context.scene.my_tool.animationBool == True:
            row.prop(mytool, "animationEnum")

        row = layout.row()
        row.prop(mytool, "modelBool")
        if  bpy.context.scene.my_tool.modelBool == True:
            row.prop(mytool, "modelEnum")

        row = layout.row()
        row.prop(mytool, "batchToGenerate")

        row = layout.row()
        self.layout.operator("exporter.nfts", icon='RENDER_RESULT', text="Generate NFTs")

# Refactor Batches & create MetaData Panel:
class BMNFTS_PT_Refactor(bpy.types.Panel):
    bl_label = "Refactor Batches & create MetaData"
    bl_idname = "BMNFTS_PT_Refactor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        layout.label(text="Meta Data format:")

        row = layout.row()
        row.prop(mytool, "cardanoMetaDataBool")
        row.prop(mytool, "solanaMetaDataBool")
        row.prop(mytool, "erc721MetaData")
        self.layout.operator("refactor.batches", icon='FOLDER_REDIRECT', text="Refactor Batches & create MetaData")

# Documentation Panel:
class BMNFTS_PT_Documentation(bpy.types.Panel):
    bl_label = "Documentation"
    bl_idname = "BMNFTS_PT_Documentation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blend_My_NFTs'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.operator("wm.url_open", text="Documentation",
                     icon='URL').url = "https://github.com/torrinworx/Blend_My_NFTs"

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


def redraw_panel():
    try:
        bpy.utils.unregister_class(BMNFTS_PT_CreateData)
    except:
        pass
    bpy.utils.register_class(BMNFTS_PT_CreateData)


# Register and Unregister classes from Blender:
classes = (
    BMNFTS_PGT_MyProperties,
    BMNFTS_PT_CreateData,
    WCUSTOM_PT_PreviewNFTs,
    BMNFTS_PT_GenerateNFTs,
    BMNFTS_PT_Refactor,
    BMNFTS_PT_Documentation,


    # Other panels:

    # BMNFTS_PT_LOGIC_Panel,
    # BMNFTS_PT_MATERIALS_Panel,
    # BMNFTS_PT_API_Panel,
    randomizeModel,
    randomizeColor,
    createData,
    exportNFTs,
    refactor_Batches,
    randomizePreview,
    previewNFT,

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
