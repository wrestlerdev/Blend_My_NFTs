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
import json
import re

# Import files from main directory:

importList = ['TextureEditor', 'Scene_Setup', 'DNA_Generator', 'Exporter', 'SaveNFTsToRecord', 'UIList', 'LoadNFT']

if bpy in locals():
        importlib.reload(LoadNFT)
        importlib.reload(DNA_Generator)
        importlib.reload(Exporter)
        importlib.reload(SaveNFTsToRecord)
        importlib.reload(UIList)
        importlib.reload(Scene_Setup)
        importlib.reload(TextureEditor)
        importlib.reload(Rarity_Wrangler)
else:
    from .main import \
        LoadNFT, \
        DNA_Generator, \
        Exporter, \
        SaveNFTsToRecord, \
        TextureEditor, \
        Scene_Setup, \
        Rarity_Wrangler

    from .ui_Lists import UIList
    

# User input Property Group:
class BMNFTS_PGT_MyProperties(bpy.types.PropertyGroup):

    # Main BMNFTS Panel properties:   
    save_path: bpy.props.StringProperty(
                        name="Save Path",
                        description="Save path for NFT files",
                        default="",
                        maxlen=1024,
                        subtype="DIR_PATH"
    )

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

    gifBool: bpy.props.BoolProperty(name="GIF")


    # API Panel properties:


    # Custom properties

    elementStyle: bpy.props.EnumProperty(
            name='Elemental Type',
            description="Elemental Type (ﾉ◕ヮ◕)ﾉ*✲ﾟ*｡⋆",
            items=[
                ('None', 'None', 'None'),
                ('All', 'All', 'All'),
                # ('Skin', 'Skin', 'Skin'),
                ('Outfit', 'Outfit', 'Outfit')
            ],
            default='All',
            update=lambda s,c: Exporter.Previewer.elements_updated()
        )

    element: bpy.props.EnumProperty(
            name='Elemental Type',
            description="Elemental Type (ﾉ◕ヮ◕)ﾉ*✲ﾟ*｡⋆",
            items=[
                # ('Gold', 'Gold', 'Gold'),
                ('Acid', 'Acid', 'Acid'),
                ('Amalgum', 'Amalgum', 'Amalgum'),
                ('Antimony', 'Antimony', 'Antimony'),
                ('AquaFortis', 'AquaFortis', 'AquaFortis'),
                ('AquaRegia', 'AquaRegia', 'AquaRegia'),
                ('Arsenic', 'Arsenic', 'Arsenic'),
                ('Cobalt', 'Cobalt', 'Cobalt'),
                ('Copper', 'Copper', 'Copper'),
                ('Cinnabar', 'Cinnabar', 'Cinnabar'),
                ('Gold', 'Gold', 'Gold')   ,
                ('Bismuth', 'Bismuth', 'Bismuth'),
                ('Brimstone', 'Brimstone', 'Brimstone'),
                ('Iron', 'Iron', 'Iron'),
                ('Lead', 'Lead', 'Lead'),
                ('Phlogiston', 'Phlogiston', 'Phlogiston'),
                ('Platinum', 'Platinum', 'Platinum'),
                ('Phosphorus', 'Phosphorus', 'Phosphorus'),
                ('Manganese', 'Manganese', 'Manganese'),
                ('Magnesium', 'Magnesium', 'Magnesium'),
                ('Mercury', 'Mercury', 'Mercury'),
                ('Nickel', 'Nickel', 'Nickel'),
                ('Oxygen', 'Oxygen', 'Oxygen'),
                ('SalAmmoniac', 'SalAmmoniac', 'SalAmmoniac'),
                ('Salt', 'Salt', 'Salt'),
                ('Silver', 'Silver', 'Silver'),
                ('SpiritOfWine', 'SpiritOfWine', 'SpiritOfWine'),
                ('Sulphur', 'Sulphur', 'Sulphur'),
                ('Tin', 'Tin', 'Tin'),
                ('Vitriol', 'Vitriol', 'Vitriol'),
                ('Zinc', 'Zinc', 'Zinc')
            ],
            update=lambda s,c: Exporter.Previewer.elements_updated()
        )

    isElementLocked: bpy.props.BoolProperty(name='Lock Element', default=False)
    isElementStyleLocked: bpy.props.BoolProperty(name='Lock Style', default=False)
    NonElementalProbability: bpy.props.IntProperty(name='Regular', default=50, max=100, min=0)
    FullElementalProbability: bpy.props.IntProperty(name='All', default=0, max=100, min=0)
    OutfitElementalProbability: bpy.props.IntProperty(name='Outfit', default=0, max=100, min=0)

    renameSetFrom: bpy.props.StringProperty(name='Rename Set From')
    renameSetTo: bpy.props.StringProperty(name='Rename Set To')
    shouldForceDownres: bpy.props.BoolProperty(name='Force downres', default=False)

    searcherString: bpy.props.StringProperty(name="Variants to find:")

    textureSize: bpy.props.EnumProperty(
            name='textuuuuuuuuures',
            description="texture",
            items=[
                ('4k', '4k', '4096x4096'),
                # ('2k', '2k', '2048x2048'),
                ('1k', '1k', '1024x1024'),
                # ('512', '512', '512x512'),
                ('64', '64', '64x64')
            ]
        )

    handmadeBool: bpy.props.BoolProperty(name='Handmade NFT', default=False)
    handmadeLock: bpy.props.BoolProperty(name='Lock Handmade attribute', default=False)

    customGenerateString: bpy.props.StringProperty(name="Custom Generator String")

    customRenderRange: bpy.props.StringProperty(name="Custom Render Range", default='')
    customRenderRangeBool: bpy.props.BoolProperty(name="Custom Range", default=False)
    exportDimension: bpy.props.IntProperty(name="Dimensions", default=2048, min=64, max=4096)
    imageFrame: bpy.props.IntProperty(name="Image Frame", default=1)
    frameLength: bpy.props.FloatProperty(name="Animation Length", default=10.0)

    evalMinTime: bpy.props.FloatProperty(name='Evaluate Min Render Time', default=60)
    evalMaxTime: bpy.props.FloatProperty(name='Evaluate Max Render Time', default=600)
    evalFilePath: bpy.props.StringProperty(name='File Location')

    deleteStart: bpy.props.IntProperty(name="Start Range", default=1,min=1)
    deleteEnd: bpy.props.IntProperty(name="End Range", default=1,min=1)

    isCharacterLocked: bpy.props.BoolProperty(name="Lock Character", default=False)

    separateExportPath: bpy.props.StringProperty(name="Directory")
    renderPrefix: bpy.props.StringProperty(name="Output Prefix:", default="SAE #")

    renderFullBatch: bpy.props.BoolProperty(name= "Render Full Batch", default=True)
    renderMultiBatch: bpy.props.BoolProperty(name= "Render Multiple Batches", default=False)
    renderSectionSize: bpy.props.IntProperty(name= "Section Size", default=1, min=1, max=9999)
    renderSectionIndex: bpy.props.IntProperty(name= "Section Index", default=1, min=1, max=9999)
    rangeBool: bpy.props.BoolProperty(name="Use Sections", default=False)
    BatchRenderIndex: bpy.props.IntProperty(name= "Batch To Render", default=1, min=1, max=100)
    BatchRenderEndIndex: bpy.props.IntProperty(name= "Batch To Render To", default=1, min=1, max=100)
    PNGTransparency: bpy.props.BoolProperty(name= 'Transparency', default=True)

    batch_json_save_path: bpy.props.StringProperty(name="Batch Save Path")
    root_dir: bpy.props.StringProperty(name="Root Directory")

    maxNFTs: bpy.props.IntProperty(name="Max NFTs to Generate",default=1, min=1, max=9999)
    loadNFTIndex: bpy.props.IntProperty(name="Number to Load:", min=1, max=9999, default=1)
    CurrentBatchIndex : bpy.props.IntProperty(name="Current Batch", min=1, max=100, default=1)
    currentColorStyleKey : bpy.props.StringProperty(name="Color Style Key", default="N/A", update=lambda s,c:DNA_Generator.Outfit_Generator.ColorGen.UIColorKey_has_updated())

    BatchSliderIndex : bpy.props.IntProperty(name="Batch", min=1, max=100, default=1, update=lambda s,c:LoadNFT.batch_property_updated())
    lastBatchSliderIndex: bpy.props.IntProperty(default=1)

    lastDNA: bpy.props.StringProperty(name="lastDNA") # for checks if dna string field is edited by user
    inputDNA: bpy.props.StringProperty(name="DNA")


    inputUT: bpy.props.PointerProperty(name="Upper Torso Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputUT"))
    inputMT: bpy.props.PointerProperty(name="Middle Torso Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputMT"))
    inputFA: bpy.props.PointerProperty(name="Forearms Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputFA"))
    inputW: bpy.props.PointerProperty(name="Wrist Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputW"))
    inputPTK: bpy.props.PointerProperty(name="Lower Torso Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputPTK"))
    inputPTN: bpy.props.PointerProperty(name="Lower Torso Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputPTN"))
    inputH: bpy.props.PointerProperty(name="Hair Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputH"))
    inputC: bpy.props.PointerProperty(name="Calf Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputC"))
    inputA: bpy.props.PointerProperty(name="Ankle Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputA"))
    inputF: bpy.props.PointerProperty(name="Feet Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputF"))
    inputN: bpy.props.PointerProperty(name="Neck Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputN"))
    inputLH: bpy.props.PointerProperty(name="Lower Head Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputLH"))
    inputMH: bpy.props.PointerProperty(name="Middle Head Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputMH"))
    inputES: bpy.props.PointerProperty(name="Earrings Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputES"))
    inputEL: bpy.props.PointerProperty(name="Earrings Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputEL"))
    inputHS: bpy.props.PointerProperty(name="Hair Short Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputHS"))
    inputHL: bpy.props.PointerProperty(name="Hair Long Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputHL"))
    inputHA: bpy.props.PointerProperty(name="Accessories Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputHA"))
    inputBP: bpy.props.PointerProperty(name="Backpack Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputBP"))
    inputBG: bpy.props.PointerProperty(name="Background Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputBG"))
    inputEX: bpy.props.PointerProperty(name="Expression Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputEX"))
    inputENV: bpy.props.PointerProperty(name="Environment Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.pointers_have_updated("inputENV"))
    inputGeneral: bpy.props.PointerProperty(name="Any Slot",type=bpy.types.Collection,
                                                update=lambda s,c: Exporter.Previewer.general_pointer_updated())

    inputColorListSceneObject: bpy.props.PointerProperty(name="ColorListObject", type=bpy.types.Object)

    lastUT: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastMT: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastFA: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastHS: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastHL: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastW: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastPTK: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastPTN: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastH: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastC: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastA: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastF: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastN: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastLH: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastMH: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastES: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastEL: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastBP: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastBG: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastEX: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastENV: bpy.props.PointerProperty(name="",type=bpy.types.Collection)
    lastHA: bpy.props.PointerProperty(name="",type=bpy.types.Collection)

    colourStyleIndex: bpy.props.StringProperty(default="1", 
                                update=lambda s,c:DNA_Generator.Outfit_Generator.ColorGen.colourindex_has_been_updated("colourStyleIndex", "lastStyleIndex"))
    lastStyleIndex: bpy.props.IntProperty(default=1, min=0,max=999)

    textureSetIndex: bpy.props.StringProperty(default="A",
                                update=lambda s,c:DNA_Generator.Outfit_Generator.ColorGen.textureindex_has_been_updated("textureSetIndex", "lastSetIndex"))
    colorStyleColorListKey: bpy.props.StringProperty(default="001")
    lastSetIndex: bpy.props.StringProperty(default="A")

    RTint: bpy.props.FloatVectorProperty(name="R Tint", subtype="COLOR", default=(1.0,0.0,0.0,1.0), size=4, min=0.0, max=1,
                                        update=lambda s,c: DNA_Generator.Outfit_Generator.ColorGen.ColorHasbeenUpdated("RTint"))
    GTint: bpy.props.FloatVectorProperty(name="G Tint", subtype="COLOR", default=(0.0,1.0,0.0,1.0), size=4, min=0.0, max=1,
                                        update=lambda s,c: DNA_Generator.Outfit_Generator.ColorGen.ColorHasbeenUpdated("GTint"))
    BTint: bpy.props.FloatVectorProperty(name="B Tint", subtype="COLOR", default=(0.0,0.0,1.0,1.0), size=4, min=0.0, max=1,
                                        update=lambda s,c: DNA_Generator.Outfit_Generator.ColorGen.ColorHasbeenUpdated("BTint"))
    AlphaTint: bpy.props.FloatVectorProperty(name="A Tint", subtype="COLOR", default=(0.0,0.0,1.0,1.0), size=4, min=0.0, max=1,
                                        update=lambda s,c: DNA_Generator.Outfit_Generator.ColorGen.ColorHasbeenUpdated("AlphaTint"))
    WhiteTint: bpy.props.FloatVectorProperty(name="W Tint", subtype="COLOR", default=(0.0,0.0,1.0,1.0), size=4, min=0.0, max=1,
                                        update=lambda s,c: DNA_Generator.Outfit_Generator.ColorGen.ColorHasbeenUpdated("WhiteTint"))

    currentGeneratorStyle: bpy.props.StringProperty(name="Style", default='')
    colorStyleName : bpy.props.StringProperty(name="Colour Style Name", default="Ocean")
    colorStyleRarity: bpy.props.IntProperty(name= "Colour Style Rarity", default=50, min=0, soft_max=100,max=2000)
    colorSetName : bpy.props.StringProperty(name="Colour Set Name", default="000")

    RTintPreview: bpy.props.FloatVectorProperty(name="R Tint Preview", subtype="COLOR", default=(1.0,0.0,0.0,1.0), size=4, min=0.0, max=1)
    GTintPreview: bpy.props.FloatVectorProperty(name="G Tint Preview", subtype="COLOR", default=(0.0,1.0,0.0,1.0), size=4, min=0.0, max=1)
    BTintPreview: bpy.props.FloatVectorProperty(name="B Tint Preview", subtype="COLOR", default=(0.0,0.0,1.0,1.0), size=4, min=0.0, max=1)
    AlphaTintPreview: bpy.props.FloatVectorProperty(name="A Tint Preview", subtype="COLOR", default=(0.0,0.0,1.0,1.0), size=4, min=0.0, max=1)
    WhiteTintPreview: bpy.props.FloatVectorProperty(name="W Tint Preview", subtype="COLOR", default=(0.0,0.0,1.0,1.0), size=4, min=0.0, max=1)

canRefactor = False

def make_directories(save_path):
    Blend_My_NFTs_Output = os.path.join(save_path, "Blend_My_NFT")
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
            # save_path = os.path.abspath(bpy.context.scene.my_tool.save_path)
            save_path = bpy.context.scene.my_tool.save_path
        elif not os.path.exists(bpy.context.scene.my_tool.root_dir):
            self.report({"ERROR"}, "Failed: The root directory folder does not exist")
            save_path = bpy.context.scene.my_tool.root_dir
            return {'FINISHED'}
        else:
            save_path = bpy.context.scene.my_tool.root_dir
        print(save_path)
        Blend_My_NFTs_Output, output_save_path = make_directories(save_path)

        first_batch_path = os.path.join(output_save_path,  "Batch_{}".format(1))
        first_nftrecord_save_path = os.path.join(first_batch_path, "_NFTRecord_{}.json".format(1))
        master_nftrecord_save_path = os.path.join(output_save_path, "_NFTRecord.json")
        Rarity_save_path = os.path.join(first_batch_path, "_RarityCounter_{}.json".format(1))
        record_backup_save_path = os.path.join(bpy.context.scene.my_tool.root_dir, "_NFTRecord_{}_BACKUP.json".format(1))

        bpy.context.scene.my_tool.batch_json_save_path = output_save_path
        bpy.context.scene.my_tool.loadNFTIndex = 1
        bpy.context.scene.my_tool.BatchSliderIndex = 1

        original_hierarchy = Exporter.Previewer.get_hierarchy_unordered(1)
        LoadNFT.init_batch(output_save_path)
        if original_hierarchy != None or os.path.exists(record_backup_save_path):
            DNA_Generator.save_rarity_To_New_Record(original_hierarchy, first_nftrecord_save_path, record_backup_save_path)
        else:
            DNA_Generator.send_To_Record_JSON(first_nftrecord_save_path)
        DNA_Generator.set_up_master_Record(master_nftrecord_save_path)
        LoadNFT.update_current_batch(1, output_save_path)

        # DNA_Generator.Outfit_Generator.count_all_rarities(first_batch_path, 1)
        LoadNFT.update_collection_rarity_property(first_nftrecord_save_path)

        DNA_Generator.Outfit_Generator.ColorGen.create_batch_color(first_batch_path, 1, True)

        bpy.context.scene.my_tool.handmadeBool = False
        return {'FINISHED'}



#-----------------------------------------


class randomizePreview(bpy.types.Operator):
    bl_idname = 'randomize.preview'
    bl_label = 'Randomize All'
    bl_description = "Create and generate random combination"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        save_path = bpy.context.scene.my_tool.root_dir
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)

        DNA, NFTDict = DNA_Generator.Outfit_Generator.RandomizeFullCharacter(1, save_path)
        SingleDNA = DNA[0]
        SingleNFTDict = NFTDict[DNA[0]]
        Exporter.Previewer.show_nft_from_dna(SingleDNA, SingleNFTDict)

        if not bpy.context.scene.my_tool.handmadeLock:
            bpy.context.scene.my_tool.handmadeBool = False
        return {'FINISHED'}

class randomizeAllColor(bpy.types.Operator):
    bl_idname = 'randomize.allcolor'
    bl_label = 'Randomize Color Style'
    bl_description = "Randomize colour style"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if bpy.context.scene.my_tool.elementStyle == 'None':
            dna_string, CharacterItems = Exporter.Previewer.randomize_color_style()
            Exporter.Previewer.show_nft_from_dna(dna_string, CharacterItems)
        return {'FINISHED'}

class randomizeAllSets(bpy.types.Operator):
    bl_idname = 'randomize.colorsets'
    bl_label = 'Randomize Color Sets'
    bl_description = "Randomize colour sets"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if bpy.context.scene.my_tool.elementStyle == 'None':
            style = bpy.context.scene.my_tool.currentGeneratorStyle or "Random"
            dna_string, CharacterItems = Exporter.Previewer.randomize_color_style(style)
            Exporter.Previewer.show_nft_from_dna(dna_string, CharacterItems)
        return {'FINISHED'}


class randomizeColor(bpy.types.Operator):
    bl_idname = 'randomize.color'
    bl_label = 'Color'
    bl_description = "Randomize color of current slot"
    bl_options = {"REGISTER", "UNDO"}
    collection_name: bpy.props.StringProperty(default="")

    def execute(self, context):
        if self.collection_name != "":
            LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
            input_slot = self.collection_name
            slot_coll = config.Slots[input_slot][0]
            type = bpy.context.scene.my_tool[input_slot].name.split('_')[1]
            if type not in config.EmptyTypes and bpy.context.scene.my_tool.elementStyle == 'None':
                Exporter.Previewer.update_colour_random(slot_coll)
        return {'FINISHED'}


class randomizeTexture(bpy.types.Operator):
    bl_idname = 'texture.randomize'
    bl_label = 'Texture'
    bl_description = "Randomize texture of current slot"
    bl_options = {"REGISTER", "UNDO"}
    collection_name: bpy.props.StringProperty(default="")

    def execute(self, context):
        if self.collection_name != "":
            LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
            input_slot = self.collection_name
            slot_coll = config.Slots[input_slot][0]
            type = bpy.context.scene.my_tool[input_slot].name.split('_')[1]
            # if type not in config.EmptyTypes:
            attribute = config.Slots[self.collection_name][0]
            variant = bpy.context.scene.my_tool[self.collection_name]
            texture, index = DNA_Generator.Outfit_Generator.GetRandomSingleTexture(attribute, variant)

            Exporter.Previewer.set_texture_on_slot(slot_coll, variant.name, index)
        return {'FINISHED'}


class randomizeMesh(bpy.types.Operator):
    bl_idname = 'mesh.randomize'
    bl_label = 'Mesh'
    bl_description = "Randomize mesh of current slot"
    bl_options = {"REGISTER", "UNDO"}
    collection_name: bpy.props.StringProperty(default="")

    def execute(self, context):
        if self.collection_name != "":
            LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
            # if type not in config.EmptyTypes:
            attribute = config.Slots[self.collection_name][0]
            dna_strand = DNA_Generator.Outfit_Generator.GetRandomSingleMesh(attribute)
            dna_string, CharacterItems = Exporter.Previewer.update_DNA_with_strand(attribute, dna_strand)
            Exporter.Previewer.show_nft_from_dna(dna_string, CharacterItems)
        return {'FINISHED'}


#-----------------------------------------


class createBatch(bpy.types.Operator):
    bl_idname = 'create.batch'
    bl_label = "Create NFTs"
    bl_description = "Create multiple random NFTs"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.context.scene.my_tool.handmadeBool = False
        batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
        index = bpy.context.scene.my_tool.CurrentBatchIndex
        master_record_save_path = os.path.join(batch_json_save_path, "_NFTRecord.json")
        nft_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(index))
        DNASet, NFTDict = DNA_Generator.Outfit_Generator.RandomizeFullCharacter(bpy.context.scene.my_tool.maxNFTs, nft_save_path)
        if not SaveNFTsToRecord.SaveNFTs(DNASet, NFTDict, nft_save_path, index, master_record_save_path):
            self.report({"ERROR"}, "These NFTs already exist")

        numGenerated = LoadNFT.get_total_DNA()
        bpy.context.scene.my_tool.loadNFTIndex = numGenerated
        DNA = DNASet[len(DNASet) - 1] # show last DNA created
        print(NFTDict[DNA])
        Exporter.Previewer.show_nft_from_dna(DNA, NFTDict[DNA])
        return {'FINISHED'}


class createCustomBatch(bpy.types.Operator):
    bl_idname = 'create.custom'
    bl_label = 'Re-generate NFTs'
    bl_description = "Re-generate NFTs from custom range"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        bpy.context.scene.my_tool.handmadeBool = False
        string = bpy.context.scene.my_tool.customGenerateString
        string = string.replace(" ", "")
        string = string.rstrip(',')
        if string:
            nft_num = re.split(',', string)
            DNASet, NFTDict = DNA_Generator.Outfit_Generator.RandomizeFullCharacter(len(nft_num))

            batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
            master_record_save_path = os.path.join(batch_json_save_path, "_NFTRecord.json")
            index = bpy.context.scene.my_tool.CurrentBatchIndex
            for i in range(len(nft_num)):
                DNA = DNASet[i]
                nft_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(index))
                nft_index = int(nft_num[i])
                if not SaveNFTsToRecord.OverrideNFT(DNA, NFTDict, nft_save_path, index, nft_index, master_record_save_path):
                    config.custom_print("This ({}) nft already exists probably".format(DNA), '', config.bcolors.ERROR)
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
        TotalDNA, DNA, NFTDict = LoadNFT.read_DNAList_from_file(batch_index, loadNFTIndex)
        nft_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{}".format(batch_index))
        if TotalDNA > 0 and DNA != '':
            Exporter.Previewer.show_nft_from_dna(DNA, NFTDict)
        else:
            self.report({"ERROR"}, "This is not a valid number (%d), as there are only %d NFTs saved" %(loadNFTIndex, TotalDNA))

        if not bpy.context.scene.my_tool.handmadeLock:
            bpy.context.scene.my_tool.handmadeBool = False
        return {'FINISHED'}


class loadNextNFT(bpy.types.Operator):
    bl_idname = 'next.nft'
    bl_label = "Load Next"
    bl_description = 'Load Next NFT based on slider'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
        batch_index = bpy.context.scene.my_tool.CurrentBatchIndex
        nft_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{}".format(batch_index))

        nftnum = len(next(os.walk(nft_save_path))[1])
        if  nftnum > 0 and bpy.context.scene.my_tool.loadNFTIndex < nftnum:
            bpy.context.scene.my_tool.loadNFTIndex = bpy.context.scene.my_tool.loadNFTIndex + 1
            loadNFTIndex = bpy.context.scene.my_tool.loadNFTIndex
            TotalDNA, DNA, NFTDict = LoadNFT.read_DNAList_from_file(batch_index, loadNFTIndex)

            Exporter.Previewer.show_nft_from_dna(DNA, NFTDict)

        if not bpy.context.scene.my_tool.handmadeLock:
            bpy.context.scene.my_tool.handmadeBool = False
        return {'FINISHED'}


class loadPrevNFT(bpy.types.Operator):
    bl_idname = 'prev.nft'
    bl_label = "Load Previous"
    bl_description = 'Load Previous NFT based on slider'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
        batch_index = bpy.context.scene.my_tool.CurrentBatchIndex
        nft_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{}".format(batch_index))
        if len(os.listdir(nft_save_path)) > 1 :
            bpy.context.scene.my_tool.loadNFTIndex = bpy.context.scene.my_tool.loadNFTIndex - 1
            loadNFTIndex = bpy.context.scene.my_tool.loadNFTIndex
            TotalDNA, DNA, NFTDict = LoadNFT.read_DNAList_from_file(batch_index, loadNFTIndex)

            Exporter.Previewer.show_nft_from_dna(DNA, NFTDict)

        if not bpy.context.scene.my_tool.handmadeLock:
            bpy.context.scene.my_tool.handmadeBool = False
        return {'FINISHED'}


#-------------------------------


class saveNewNFT(bpy.types.Operator):
    bl_idname = 'save.nft'
    bl_label = 'Save as New NFT'
    bl_description = "Save current preview as a new NFT"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)
        DNASet = {context.scene.my_tool.inputDNA}

        batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
        NFTDicts = {}
        SingleNFTDict = Exporter.Previewer.LoadTempDNADict()
        NFTDicts[SingleNFTDict["DNAList"]] = SingleNFTDict["CharacterItems"]
        index = int(bpy.context.scene.my_tool.CurrentBatchIndex)

        master_save_path = os.path.join(batch_json_save_path, "_NFTRecord.json")
        nft_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(index))
        if not SaveNFTsToRecord.SaveNFTs(DNASet, NFTDicts, nft_save_path, index, master_save_path):
            self.report({"ERROR"}, "This NFT already exists")

        bpy.context.scene.my_tool.loadNFTIndex = LoadNFT.get_total_DNA()

        if not bpy.context.scene.my_tool.handmadeLock:
            bpy.context.scene.my_tool.handmadeBool = False
        return {'FINISHED'}



class saveCurrentNFT(bpy.types.Operator):
    bl_idname = 'save.currentnft'
    bl_label = 'Save NFT'
    bl_description = "This action cannot be undone. Are you sure?"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        LoadNFT.check_if_paths_exist(bpy.context.scene.my_tool.BatchSliderIndex)

        batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
        NFTDicts = {}
        SingleNFTDict = Exporter.Previewer.LoadTempDNADict()
        DNA = SingleNFTDict["DNAList"]
        NFTDicts[DNA] = SingleNFTDict["CharacterItems"]
        index = bpy.context.scene.my_tool.CurrentBatchIndex
        loadNFTIndex = bpy.context.scene.my_tool.loadNFTIndex

        master_record_save_path = os.path.join(batch_json_save_path, "_NFTRecord.json")
        nft_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(index))
        if not SaveNFTsToRecord.OverrideNFT(DNA, NFTDicts, nft_save_path, index, loadNFTIndex, master_record_save_path):
            self.report({"ERROR"}, "This NFT already exists probably")

        if not bpy.context.scene.my_tool.handmadeLock:
            bpy.context.scene.my_tool.handmadeBool = False
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
        nft_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{}".format(batch_index))
        loadNFTIndex = bpy.context.scene.my_tool.loadNFTIndex
        TotalDNA, DNA, Dict = LoadNFT.read_DNAList_from_file(batch_index, loadNFTIndex)
        master_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "_NFTRecord.json")
        
        if TotalDNA > 0 and DNA != '':
            deleted_index = SaveNFTsToRecord.DeleteNFT(DNA, nft_save_path, batch_index, master_save_path)
            new_index = min(deleted_index, TotalDNA - 1)
            TotalDNA, DNA, NFTDict = LoadNFT.read_DNAList_from_file(batch_index, new_index)

            bpy.context.scene.my_tool.loadNFTIndex = new_index
            Exporter.Previewer.show_nft_from_dna(DNA, NFTDict)
        else:
            self.report({"ERROR"}, "This is not a valid number (%d), as there are only %d NFTs saved" %(loadNFTIndex, TotalDNA))
        
        if not bpy.context.scene.my_tool.handmadeLock:
            bpy.context.scene.my_tool.handmadeBool = False
        return {'FINISHED'}


class deleteRangeNFT(bpy.types.Operator):
    bl_idname = 'delete.nftrnge'
    bl_label = 'Delete NFT in Range'
    bl_description = "This delete NFTs and cannot be undone. Are you sure?"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        start_range = bpy.context.scene.my_tool.deleteStart
        end_range = bpy.context.scene.my_tool.deleteEnd

        batch_index = int(bpy.context.scene.my_tool.CurrentBatchIndex)
        nft_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{}".format(batch_index))
        TotalDNA = LoadNFT.get_all_DNA_from_batch(batch_index)
        master_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "_NFTRecord.json")

        SaveNFTsToRecord.DeleteNFTsinRange(start_range, end_range, TotalDNA, nft_save_path, batch_index, master_save_path)
        
        if not bpy.context.scene.my_tool.handmadeLock:
            bpy.context.scene.my_tool.handmadeBool = False
        return {'FINISHED'}



class deleteAllNFTs(bpy.types.Operator):
    bl_idname = 'delete.allnfts'
    bl_label = 'Delete ALL NFTs in Batch'
    bl_description = "This will delete all NFTS from the current Batch. u sure bud?"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self,context):
        batch_index = int(bpy.context.scene.my_tool.CurrentBatchIndex)
        nft_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{}".format(batch_index))
        TotalDNA = LoadNFT.get_all_DNA_from_batch(batch_index)
        master_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "_NFTRecord.json")

        if len(TotalDNA) > 0:
            SaveNFTsToRecord.DeleteAllNFTs(TotalDNA, nft_save_path, batch_index, master_save_path)
        else:
            print(">:^(")
        
        if not bpy.context.scene.my_tool.handmadeLock:
            bpy.context.scene.my_tool.handmadeBool = False
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

        LoadNFT.update_current_batch(index, batch_path)
        batch_save_path = os.path.join(batch_path, "Batch_{}".format(index))
        NFTRecord_save_path = os.path.join(batch_save_path, "_NFTRecord_{}.json".format(index))
        Rarity_save_path = os.path.join(batch_save_path, "_RarityCounter_{}.json".format(index))
        LoadNFT.update_collection_rarity_property(NFTRecord_save_path)

        bpy.context.scene.my_tool.loadNFTIndex = 1
        TotalDNA, DNA, NFTDict = LoadNFT.read_DNAList_from_file(index, 1)
        if DNA != '':
            Exporter.Previewer.show_nft_from_dna(DNA, NFTDict)

        print(bpy.context.scene.my_tool.BatchSliderIndex)
        rarity_dict = DNA_Generator.Outfit_Generator.ColorGen.OpenBatchColorRarity(index)
        if bpy.context.scene.my_tool.colorStyleName in rarity_dict:
            bpy.context.scene.my_tool.colorStyleRarity = rarity_dict[bpy.context.scene.my_tool.colorStyleName]
        else:
            bpy.context.scene.my_tool.colorStyleRarity = 0

        if not bpy.context.scene.my_tool.handmadeLock:
            bpy.context.scene.my_tool.handmadeBool = False
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

        batch_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(index))
        NFTRecord_save_path = os.path.join(batch_save_path, "_NFTRecord_{}.json".format(index))
        Rarity_save_path = os.path.join(batch_save_path, "_RarityCounter_{}.json".format(index))
        DNA_Generator.save_new_rarity_Record(NFTRecord_save_path)
        if index == 1:
            record_backup_save_path = os.path.join(bpy.context.scene.my_tool.root_dir, "_NFTRecord_{}_BACKUP.json".format(index))
            DNA_Generator.send_To_Record_JSON(record_backup_save_path)

        nftrecord_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{}".format(index))

        # Rarity_Wrangler.count_all_rarities(batch_save_path, index)
        # LoadNFT.update_collection_rarity_property(NFTRecord_save_path, Rarity_save_path)
        LoadNFT.update_collection_rarity_property(NFTRecord_save_path)

        if not bpy.context.scene.my_tool.handmadeLock:
            bpy.context.scene.my_tool.handmadeBool = False
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
        index = len(next(os.walk(batch_json_save_path))[1]) + 1
        
        LoadNFT.update_current_batch(index, batch_json_save_path)

        current_batch_save_path = os.path.join(batch_json_save_path, "Batch_{}".format(index))
        NFTRecord_save_path = os.path.join(current_batch_save_path, "_NFTRecord_{}.json".format(index))
        Rarity_save_path = os.path.join(current_batch_save_path, "_RarityCounter_{}.json".format(index))
        DNA_Generator.send_To_Record_JSON(NFTRecord_save_path)

        bpy.context.scene.my_tool.BatchSliderIndex = index
        DNA_Generator.Outfit_Generator.ColorGen.create_batch_color(current_batch_save_path, index, True)
        # DNA_Generator.Outfit_Generator.count_all_rarities(current_batch_save_path, index)
        LoadNFT.update_collection_rarity_property(NFTRecord_save_path)

        if not bpy.context.scene.my_tool.handmadeLock:
            bpy.context.scene.my_tool.handmadeBool = False
        return {'FINISHED'}



class resetBatch(bpy.types.Operator):
    bl_idname = 'reset.batch'
    bl_label = "Reset Rarity in Batch"
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

        current_batch_save_path = os.path.join(batch_path, "Batch_{}".format(batch_index))
        nftrecord_path = os.path.join(current_batch_save_path, "_NFTRecord_{}.json".format(batch_index))
        Rarity_save_path = os.path.join(current_batch_save_path, "_RarityCounter_{}.json".format(batch_index))

        DNA_Generator.reset_rarity_Record(nftrecord_path)
        DNA_Generator.Outfit_Generator.ColorGen.create_batch_color(current_batch_save_path, batch_index, True)

        # DNA_Generator.Outfit_Generator.count_all_rarities(current_batch_save_path, batch_index)
        LoadNFT.update_collection_rarity_property(nftrecord_path)

        if not bpy.context.scene.my_tool.handmadeLock:
            bpy.context.scene.my_tool.handmadeBool = False
        return {'FINISHED'}


class updateBatch(bpy.types.Operator):
    bl_idname = 'update.batch'
    bl_label = "Update Batch"
    bl_description = "Update batch to include new items"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        batch_index = bpy.context.scene.my_tool.BatchSliderIndex
        LoadNFT.check_if_paths_exist(batch_index)
        batch_path = bpy.context.scene.my_tool.batch_json_save_path
        total_batches = len(os.listdir(batch_path)) - 1
        
        if batch_index > total_batches:
            self.report({"ERROR"}, "Failed: Not a valid batch")
            return {'FINISHED'}

        batch_save_path = os.path.join(batch_path, "Batch_{}".format(batch_index))
        NFTRecord_save_path = os.path.join(batch_save_path, "_NFTRecord_{}.json".format(batch_index))
        Rarity_save_path = os.path.join(batch_save_path, "_RarityCounter_{}.json".format(batch_index))

        LoadNFT.update_batch_items(batch_index, NFTRecord_save_path)
        if batch_index == 1:
            record_backup_save_path = os.path.join(bpy.context.scene.my_tool.root_dir, "_NFTRecord_{}_BACKUP.json".format(batch_index))
            LoadNFT.update_batch_items(batch_index, record_backup_save_path)

        # DNA_Generator.Outfit_Generator.count_all_rarities(batch_save_path, batch_index)
        LoadNFT.update_collection_rarity_property(NFTRecord_save_path)

        if not bpy.context.scene.my_tool.handmadeLock:
            bpy.context.scene.my_tool.handmadeBool = False
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
        NFTDict = Exporter.Previewer.LoadTempDNADict()
        DNA = NFTDict["DNAList"]
        DNAString = DNA.split(',')
        DNAString[0] = self.character_name
        DNA = ','.join(DNAString)
        Exporter.Previewer.show_nft_from_dna(DNA, NFTDict["CharacterItems"])
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
            # save_path = bpy.path.abspath(bpy.context.scene.my_tool.save_path)
            save_path = bpy.context.scene.my_tool.save_path

        Blend_My_NFTs_Output, batch_json_save_path = make_directories(save_path)
        batch_path = os.path.join(batch_json_save_path, "Batch_{}".format(1))
        NFTRecord_save_path = os.path.join(batch_path, "_NFTRecord_{}.json".format(1))
        master_nftrecord_save_path = os.path.join(batch_json_save_path, "_NFTRecord.json")
        Rarity_save_path = os.path.join(batch_path, "_RarityCounter_{}.json".format(1))

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
            # DNA_Generator.Outfit_Generator.count_all_rarities(batch_path, 1)
            LoadNFT.update_collection_rarity_property(NFTRecord_save_path)
            
        if not bpy.context.scene.my_tool.handmadeLock:
            bpy.context.scene.my_tool.handmadeBool = False
        return {'FINISHED'}
        


class createSlotFolders(bpy.types.Operator):
    bl_idname = 'create.slotfolers'
    bl_label = 'Import All Collections'
    bl_description = 'This will override the current folder which cannot be undone. Are you sure?'
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


    def execute(self, context):
        Scene_Setup.CreateSlotsFolderHierarchy(bpy.context.scene.my_tool.root_dir)
        return {'FINISHED'}


class createCharacterCollections(bpy.types.Operator): # OLD
    bl_idname = 'create.charcolls'
    bl_label = 'Organize Character Collections'
    bl_description = 'This will look through all folders for textures and create model copies for each. Are you sure...Punk?'
    bl_options = {"REGISTER", "UNDO"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


    def execute(self, context):
        folder_dir = os.path.join(bpy.context.scene.my_tool.root_dir, "Blend_My_NFT")
        record_path = os.path.join(folder_dir, "OUTPUT", "Batch_{}".format(1), "_NFTRecord_{}.json".format(1))
        Scene_Setup.SearchForMeshesAndCreateCharacterDuplicates(record_path)
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
        # export_path = os.path.abspath(bpy.context.scene.my_tool.separateExportPath)
        export_path = bpy.context.scene.my_tool.separateExportPath
        export_path = os.path.join(export_path, "Blend_My_NFT")
        batch_path = os.path.join(export_path, "OUTPUT", "Batch_{}".format(render_batch_num))
        record_path = os.path.join(batch_path, "_NFTRecord_{}.json".format(render_batch_num))

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

class createBlenderSave(bpy.types.Operator):
    bl_idname = "createblendersave.batch"
    bl_label = "Render"
    bl_description = "Create Blender Saves and Render"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        render_batch_num = bpy.context.scene.my_tool.BatchRenderIndex
        # export_path = os.path.abspath(bpy.context.scene.my_tool.separateExportPath)
        export_path = bpy.context.scene.my_tool.separateExportPath
        export_path = os.path.join(export_path, "Blend_My_NFT")
        batch_path = os.path.join(export_path, "OUTPUT", "Batch_{}".format(render_batch_num))
        record_path = os.path.join(batch_path, "_NFTRecord_{}.json".format(render_batch_num))

        range_start = bpy.context.scene.my_tool.renderSectionIndex
        batch_count = len(next(os.walk(batch_path))[1])
        ranges = []
        if bpy.context.scene.my_tool.renderMultiBatch and bpy.context.scene.my_tool.renderFullBatch:
            batch_end = max(bpy.context.scene.my_tool.BatchRenderEndIndex, bpy.context.scene.my_tool.BatchRenderIndex)
            for i in range( bpy.context.scene.my_tool.BatchRenderIndex, batch_end + 1):
                batch_path = os.path.join(export_path, "OUTPUT", "Batch_{}".format(i))
                batch_count = len(next(os.walk(batch_path))[1])
                ranges = [[1, batch_count]]
                for range_ in ranges:
                    passed = Exporter.create_blender_saves(batch_path, render_batch_num, range_)
                    if passed:
                        print("SAVE NEW BLENDER SCENES: " + batch_path)
                if not ranges:
                    print("Something went wrong for batch {} :(".format(i))
        else:
            if not bpy.context.scene.my_tool.renderFullBatch:
                if bpy.context.scene.my_tool.customRenderRangeBool:
                    ranges = Exporter.get_custom_range()
                elif bpy.context.scene.my_tool.rangeBool:
                    size = bpy.context.scene.my_tool.renderSectionSize
                    index = bpy.context.scene.my_tool.renderSectionIndex
                    range_start = size * (index - 1) + 1
                    range_end = min(size * (index), batch_count)
                    if range_start <= batch_count:
                        ranges = [[range_start, range_end]]
                else:
                    range_start = bpy.context.scene.my_tool.renderSectionIndex
                    range_end = min(bpy.context.scene.my_tool.renderSectionSize, batch_count)
                    if range_start <= batch_count and range_end >= range_start:
                        ranges = [[range_start, range_end]]
            else:
                ranges = [[1, batch_count]]

            for range_ in ranges:
                passed = Exporter.create_blender_saves(batch_path, render_batch_num, range_)
                if passed:
                    print("SAVE NEW BLENDER SCENES: " + batch_path)
            if not ranges:
                print("Custom render string is empty or not valid so nothing was rendered :(")

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
        bath_path_end = os.path.join("Blend_My_NFT", "OUTPUT")
        record_save_path = os.path.join(bpy.context.scene.my_tool.root_dir, bath_path_end)
        local_save_path = os.path.join(bpy.context.scene.my_tool.separateExportPath, bath_path_end)

        bpy.context.scene.my_tool.BatchRenderIndex = bpy.context.scene.my_tool.CurrentBatchIndex
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
        bacth_path_end = os.path.join("Blend_My_NFT", "OUTPUT")
        # path = os.path.join(os.path.abspath(bpy.context.scene.my_tool.separateExportPath), bacth_path_end)
        path = os.path.join(bpy.context.scene.my_tool.separateExportPath, bacth_path_end)
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
        root_dir = bpy.context.scene.my_tool.root_dir
        batches_path = os.path.join(export_dir, "Blend_My_NFT", "OUTPUT")
        render_record_path = os.path.join(root_dir, "_RenderRecord.json")
        look_up_path = os.path.join(root_dir, "_RenderLookUp.json")
        # render_record_path = os.path.join(batches_path, "_NFTRecord.json")
        Exporter.refactor_all_batches(batches_path, render_record_path, look_up_path)
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


class chooseLogPath(bpy.types.Operator):
    bl_idname = 'choose.log'
    bl_label = 'Choose Log Path'
    bl_description = "Choose log to evaluate"
    bl_options = {"REGISTER", "UNDO"}
    filepath: bpy.props.StringProperty(subtype='FILE_PATH', default='')
    filter_glob: bpy.props.StringProperty(default ='*.json',options = {'HIDDEN'})

    def execute(self, context):
        print(self.filepath)
        bpy.context.scene.my_tool.evalFilePath = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = ""
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class evaluateExportLog(bpy.types.Operator):
    bl_idname = 'eval.logs'
    bl_label = 'Evaluate Export Log'
    bl_description = 'Evaluate Export Log'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        path = bpy.context.scene.my_tool.evalFilePath
        min_sec = bpy.context.scene.my_tool.evalMinTime
        max_sec = bpy.context.scene.my_tool.evalMaxTime
        Exporter.evaluate_export_log(path, min_sec, max_sec)
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



# ---------------------------- Colours ---------------------------------


class addNewColourStyle(bpy.types.Operator):
    bl_idname = 'add.colorstyle'
    bl_label = 'Save New Style'
    bl_description = 'Append new colour style to colour list'
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        if DNA_Generator.Outfit_Generator.ColorGen.DoesStyleExist():
            return context.window_manager.invoke_confirm(self, event)
        else:
            return self.execute(context)

    def execute(self, context):
        if DNA_Generator.Outfit_Generator.ColorGen.DoesStyleExist():
            print("This colour style already  ໒(⊙ᴗ⊙)७✎▤")
        else:
            print("New colour style has been added ໒(⊙ᴗ⊙)७✎▤")
            self.report({'INFO'}, '໒(⊙ᴗ⊙)७✎▤')
            DNA_Generator.Outfit_Generator.ColorGen.SaveNewColorStyle()
        return {'FINISHED'}


class updateColourStyle(bpy.types.Operator):
    bl_idname = 'update.colorstyle'
    bl_label = 'Add Color Set To Style'
    bl_description = 'This will overwrite the current colour style, are you sure?'
    bl_options = {'REGISTER', 'UNDO'}
    icon = 'SORT_ASC'

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        save_path = bpy.context.scene.my_tool.save_path
        DNA_Generator.Outfit_Generator.ColorGen.AddColorSetToStyle()
        return {'FINISHED'}


class deleteColourStyle(bpy.types.Operator):
    bl_idname = 'delete.colorstyle'
    bl_label = 'Delete Colour Style'
    bl_description = 'This cannot be undone, are you sure?'
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        DNA_Generator.Outfit_Generator.ColorGen.DeleteGlobalColor(bpy.context.scene.my_tool.colorStyleName, bpy.context.scene.my_tool.root_dir)
        return {'FINISHED'}


class nextColorStyle(bpy.types.Operator):
    bl_idname = 'next.colorstyle'
    bl_label = 'Next Style'
    bl_description = 'Next colour style'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        DNA_Generator.Outfit_Generator.ColorGen.NextStyle(1)
        return {'FINISHED'}


class prevColorStyle(bpy.types.Operator):
    bl_idname = 'prev.colorstyle'
    bl_label = 'Prev Style'
    bl_description = 'Previous colour Style'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        DNA_Generator.Outfit_Generator.ColorGen.NextStyle(-1)
        return {'FINISHED'}


class nextGlobalColorSet(bpy.types.Operator):
    bl_idname = 'next.globalcolorset'
    bl_label = 'Next Global Color Set'
    bl_description = 'Next Global Color Set'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        color_key = DNA_Generator.Outfit_Generator.ColorGen.NextGlobalColorSet(1)
        Exporter.Previewer.colorpicker_has_applied()
        return {'FINISHED'}


class prevGlobalColorSet(bpy.types.Operator):
    bl_idname = 'prev.globalcolorset'
    bl_label = 'Prev Global Color Set'
    bl_description = 'Previous Global Color Set'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        color_key = DNA_Generator.Outfit_Generator.ColorGen.NextGlobalColorSet(-1)
        Exporter.Previewer.colorpicker_has_applied()
        return {'FINISHED'}

class addGlobalColorSet(bpy.types.Operator):
    bl_idname = 'add.globalcolorset'
    bl_label = 'Add / Update Global Color Set'
    bl_description = 'Add / Update Global Color Set'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        DNA_Generator.Outfit_Generator.ColorGen.AddNewGlobalColorSet()
        Exporter.Previewer.colorpicker_has_applied()
        return {'FINISHED'}

class loadGlobalColorSet(bpy.types.Operator):
    bl_idname = 'load.globalcolorset'
    bl_label = 'Load Color Set'
    bl_description = 'Load Global Color Set'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        success = DNA_Generator.Outfit_Generator.ColorGen.LoadColorSet()
        if success:
            Exporter.Previewer.colorpicker_has_applied()
        else:
            self.report({"ERROR"}, "Failed: This color set does not exist")
        return {'FINISHED'}

class deleteGlobalColorSet(bpy.types.Operator):
    bl_idname = 'delete.globalcolorset'
    bl_label = 'Delete Global Color Set'
    bl_description = 'Delete Global Color Set'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        DNA_Generator.Outfit_Generator.ColorGen.DeleteGlobalColorSet()
        return {'FINISHED'}

class nextStyleColorSet(bpy.types.Operator):
    bl_idname = 'next.stylecolorset'
    bl_label = 'Next Set'
    bl_description = 'Next Set from Style'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        DNA_Generator.Outfit_Generator.ColorGen.NextStyleColor(1)
        return {'FINISHED'}

class prevStyleColorSet(bpy.types.Operator):
    bl_idname = 'prev.stylecolorset'
    bl_label = 'Prev Set'
    bl_description = 'Prev Set from Style'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        DNA_Generator.Outfit_Generator.ColorGen.NextStyleColor(-1)
        return {'FINISHED'}


class saveStyleRarity(bpy.types.Operator):
    bl_idname = 'stylerarity.save'
    bl_label = 'Save Style Rarity'
    bl_description = 'Save Rarity for Style'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        DNA_Generator.Outfit_Generator.ColorGen.UpdateStyleRarity()
        return {'FINISHED'}
# -------------------------------------------------------------------------------------


class colourCopyUp(bpy.types.Operator):
    bl_idname = 'colour.copyup'
    bl_label = 'Copy Colour Up'
    bl_description = "This can't be undone okay!!!!!!"
    bl_options = {'REGISTER', 'UNDO'}
    icon = 'SORT_DESC'

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        return {'FINISHED'}


class colourCopyDown(bpy.types.Operator):
    bl_idname = 'colour.copydown'
    bl_label = 'Copy Colour Down'
    bl_description = 'Copy Colour Down'
    bl_options = {'REGISTER', 'UNDO'}
    icon = 'SORT_ASC'

    def execute(self, context):
        DNA_Generator.Outfit_Generator.ColorGen.copy_colour_down()
        Exporter.Previewer.colorpicker_has_applied()
        return {'FINISHED'}


class loadColorOnMesh(bpy.types.Operator):
    bl_idname = 'load.meshcol'
    bl_label = 'Force Load Tint'
    bl_description = 'Load Tint onto mesh'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        DNA_Generator.Outfit_Generator.ColorGen.ColorHasbeenUpdated("woo")
        Exporter.Previewer.colorpicker_has_applied()
        return {'FINISHED'}


class deleteColorStyle(bpy.types.Operator):
    bl_idname = 'delete.colstyle'
    bl_label = 'Delete Style'
    bl_description = 'This cannot be undone, are you sure?'
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        DNA_Generator.Outfit_Generator.ColorGen.DeleteGlobalColorStyle()
        return {'FINISHED'}


class deleteColorSet(bpy.types.Operator):
    bl_idname = 'delete.colset'
    bl_label = 'Delete Set from Style'
    bl_description = 'This cannot be undone, are you sure?'
    bl_options = {'REGISTER', 'UNDO'}
    icon = 'SORT_DESC'

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        DNA_Generator.Outfit_Generator.ColorGen.DeleteSetFromStyle(bpy.context.scene.my_tool.colorStyleName, bpy.context.scene.my_tool.currentColorStyleKey)
        return {'FINISHED'}


class clearGeneratorStyle(bpy.types.Operator):
    bl_idname = 'genstyle.clear'
    bl_label = 'Clear Style'
    bl_description = 'Clear Style'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.scene.my_tool.currentGeneratorStyle != 'Elemental':
            context.scene.my_tool.currentGeneratorStyle = ''
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
        # resolutions = [2048, 1024, 512, 256, 128, 64]
        # resolutions = [2048, 1024, 512, 64]
        resolutions = [1024, 64]
        # resolutions = [512]
        should_overwrite = bpy.context.scene.my_tool.shouldForceDownres
        TextureEditor.create_downres_textures(input_path, resolutions, should_overwrite)
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


class downresElementTextures(bpy.types.Operator):
    bl_idname = 'downres.elementtextures'
    bl_label = 'Down-res Element Textures'
    bl_description = "This can't be undoooooooooone"
    bl_options = {'REGISTER', 'UNDO'}


    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        elements_folder_path = os.path.join(bpy.context.scene.my_tool.root_dir, 'INPUT', 'ELEMENTS')
        TextureEditor.downres_element_textures(elements_folder_path, [1024], False)
        return {'FINISHED'}

# -------------------------------------------------------------------------------


class reimportCharacters(bpy.types.Operator):
    bl_idname = 'reimport.chars'
    bl_label = 'Re-import Character objects'
    bl_description = 'Re-import Character mesh, armature and etc'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        input_path = os.path.join(bpy.context.scene.my_tool.root_dir, 'INPUT')
        charinfo_path = os.path.join(input_path, 'CHARACTERS')

        Scene_Setup.reimport_all_character_objects(charinfo_path)
        return {'FINISHED'}


class reimportLight(bpy.types.Operator):
    bl_idname = 'reimport.light'
    bl_label = 'Re-import Lights'
    bl_description = 'Re-import Character mesh, armature and etc'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        input_path = os.path.join(bpy.context.scene.my_tool.root_dir, 'INPUT')
        charinfo_path = os.path.join(input_path, 'CHARACTERS')
        for dir in os.listdir(charinfo_path):
            if dir.endswith('.blend') and 'light' in dir:
                light_path = os.path.join(charinfo_path, dir)
                Scene_Setup.reimport_lights(light_path)
                break

        return {'FINISHED'}


class forceLoadDNAFromUI(bpy.types.Operator):
    bl_idname = 'forceload.dna'
    bl_label = 'Force Load DNA'
    bl_description = 'Force Load DNA from UI'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        Exporter.Previewer.CreateDNADictFromUI()
        if not bpy.context.scene.my_tool.handmadeLock:
            bpy.context.scene.my_tool.handmadeBool = False
        return {'FINISHED'}


class countUpAllRarities(bpy.types.Operator):
    bl_idname = 'rarities.count'
    bl_label = 'Calculate Absolute Rarities'
    bl_description = 'Calculate Absolute Rarities'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        index = int(bpy.context.scene.my_tool.CurrentBatchIndex)
        batch_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{}".format(index))
        NFTRecord_save_path = os.path.join(batch_path, "_NFTRecord_{}.json".format(index))
        Rarity_save_path = os.path.join(batch_path, "_RarityCounter_{}.json".format(index))

        Rarity_Wrangler.count_all_rarities(batch_path, index)
        LoadNFT.update_collection_rarity_property(NFTRecord_save_path, Rarity_save_path)
        return {'FINISHED'}


class countUpAllItems(bpy.types.Operator):
    bl_idname = 'items.count'
    bl_label = 'Count All Used Items'
    bl_description = 'Count All Used Items in Batches'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path,'TotalItemCounter.json')
        Rarity_Wrangler.count_all_items_in_batch(bpy.context.scene.my_tool.batch_json_save_path, [1,10], save_path)
        return {'FINISHED'}


class findAllNFTsWithItems(bpy.types.Operator):
    bl_idname = 'find.items'
    bl_label = 'Find NFTs with items'
    bl_description = 'Find all NFTs with items'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        search_string = bpy.context.scene.my_tool.searcherString
        search_string = search_string.replace(" ", "")
        search_string = search_string.rstrip(',')
        if search_string:
            items = re.split(',', search_string)
            output_path = os.path.join(bpy.context.scene.my_tool.root_dir, "Blend_My_NFT", "OUTPUT")
            Rarity_Wrangler.find_nfts_with_items(items, output_path, output_path)
        return {'FINISHED'}


class renameSet(bpy.types.Operator):
    bl_idname = 'set.rename'
    bl_label = 'Rename Set'
    bl_description = 'This cannot be undone are u suuuuuuuuuuuure'
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        _from = bpy.context.scene.my_tool.renameSetFrom
        _to = bpy.context.scene.my_tool.renameSetTo
        if _from and _to:
            DNA_Generator.Outfit_Generator.ColorGen.rename_color_sets(_from, _to)
        else:
            print("Please fill in the boxes properly")
        return {'FINISHED'}


class testButton(bpy.types.Operator):
    bl_idname = 'test.button'
    bl_label = 'For tests'
    bl_description = '(╬ಠิ益ಠิ)'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("(╬ಠิ益ಠิ)")

        return {'FINISHED'}


# ------------------------------- Panels ----------------------------------------------

#Create Preview Panel

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
        row.prop(mytool, "maxNFTs")
        row.operator(createBatch.bl_idname, text=createBatch.bl_label)

        box = layout.box()
        row = box.row()
        row.operator(saveCurrentNFT.bl_idname, text=saveCurrentNFT.bl_label)
        row.operator(saveNewNFT.bl_idname, text=saveNewNFT.bl_label)


class WCUSTOM_PT_CreateCustomRange(bpy.types.Panel):
    bl_label = "Re-generate NFTs in Range"
    bl_idname = "WCUSTOM_PT_CreateCustomRange"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GENERATION'
    bl_parent_id = 'WCUSTOM_PT_PreviewNFTs'
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.prop(mytool, "customGenerateString", text='')
        row.scale_x = 0.5
        row.operator(createCustomBatch.bl_idname, text=createCustomBatch.bl_label)



class WCUSTOM_PT_ModelSettings(bpy.types.Panel):
    bl_label = "Model Settings"
    bl_idname = "WCUSTOM_PT_ModelSettings"
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
            row.scale_y = 1.5
            if inputDNA.startswith(char):
                row.operator(swapCharacter.bl_idname, text=char, emboss=False).character_name = char
            else:
                row.operator(swapCharacter.bl_idname, text=char).character_name = char

        row = layout.row()
        row.prop(mytool, "isCharacterLocked", toggle=1, expand=True)

        box = layout.box()
        row = box.row()
        row.prop(mytool, "textureSize", expand=True)







class WCUSTOM_PT_ParentSlots(bpy.types.Panel):
    bl_label = "Slots"
    bl_idname = "WCUSTOM_PT_ParentSlots"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GENERATION'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool


class WCUSTOM_PT_AllSlots(bpy.types.Panel):
    bl_label = "All Slots"
    bl_idname = "WCUSTOM_PT_AllSlots"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GENERATION'
    bl_parent_id = 'WCUSTOM_PT_ParentSlots'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        row = layout.row()
        row.prop(mytool, "inputDNA")
        row.operator(randomizePreview.bl_idname, text=randomizePreview.bl_label)

        box = layout.box()
        row = box.row()
        row.scale_x = 1.3
        row.label(text='Any Slot', icon='OUTLINER_COLLECTION')
        row.prop(mytool, "inputGeneral", text='')
        row.scale_x = 1

        row = layout.row()
        row.prop(mytool, "element", expand=False, text='')
        if bpy.context.scene.my_tool.element != 'None':
            row.prop(mytool, "elementStyle", expand=True)
        else:
            row.prop(mytool, "elementStyle", expand=True, emboss=False)

        row.scale_x = 0.75
        if bpy.context.scene.my_tool.isElementLocked:
            row.prop(mytool, "isElementLocked", toggle=1, expand=True, icon='LOCKED', text=' Element')
        else:
            row.prop(mytool, "isElementLocked", toggle=1, expand=True, icon='UNLOCKED', text=' Element')
        if bpy.context.scene.my_tool.isElementStyleLocked:
            row.prop(mytool, "isElementStyleLocked", toggle=1, expand=True, icon='LOCKED', text='Style')
        else:
            row.prop(mytool, "isElementStyleLocked", toggle=1, expand=True, icon='UNLOCKED', text='Style')

        row.scale_x = 0.5
        row = layout.row()
        row.label(text='')
        row.separator(factor=0)
        row.prop(mytool, "NonElementalProbability", text='', emboss=False)
        row.prop(mytool, "FullElementalProbability", text='', emboss=False)
        row.prop(mytool, "OutfitElementalProbability", text='', emboss=False)
        row.separator(factor=0)
        row.scale_x = 1.6
        row.label(text='')

        row = layout.row()
        row.operator(randomizeAllColor.bl_idname, text=randomizeAllColor.bl_label)
        row.operator(randomizeAllSets.bl_idname, text=randomizeAllSets.bl_label)

        row.scale_x = 0.5
        row.prop(mytool, "currentGeneratorStyle", text='')
        row.operator(clearGeneratorStyle.bl_idname, text=clearGeneratorStyle.bl_label)

        box = layout.box()
        row = box.row()
        row.label()
        row.prop(mytool, "handmadeBool")
        if bpy.context.scene.my_tool.handmadeLock:
            row.prop(mytool, "handmadeLock", text='', icon='LOCKED')
        else:
            row.prop(mytool, "handmadeLock", text='', icon='UNLOCKED')
        row.scale_x = 1
        row.label()



class WCUSTOM_PT_TorsoSlots(bpy.types.Panel):
    bl_label = "Torso Slots"
    bl_idname = "WCUSTOM_PT_TorsoSlots"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GENERATION'
    bl_parent_id = 'WCUSTOM_PT_ParentSlots'

    slots = {"inputUT": ("MOD_CLOTH"),
    "inputMT": ("MOD_CLOTH"),
    "inputBP": ("CON_ARMATURE")}
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        for name in self.slots:
            row = layout.row()
            row.label(text=config.Slots[name][1], icon=self.slots[name])
            label = ''
            row.scale_x = 1.5
            if bpy.context.scene.my_tool[name] is not None:
                inputDNA = bpy.context.scene.my_tool.inputDNA
                dna_index = int(config.Slots[name][0][:2])
                dna_splitstrand = inputDNA.split(',')[dna_index + 2].split('-')
                if(len(dna_splitstrand) > 3):
                    color_key = dna_splitstrand[3] or 'X'
                else:
                    color_key = ''
                texture_index = dna_splitstrand[2]
                variant = bpy.context.scene.my_tool[name]
                label = "{} {} {}".format(variant.name.split('_')[3],texture_index, color_key)
                row.label(text=label)
                row.scale_x = 1
                row.prop(mytool, name, text="")
                row.scale_x = 0.5
                row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label).collection_name = name
                if len(variant.objects) > 1:
                    row.operator(randomizeTexture.bl_idname, text=randomizeTexture.bl_label).collection_name = name
                else:
                    row.operator(randomizeTexture.bl_idname, text=randomizeTexture.bl_label,emboss=False).collection_name = name
                if color_key == 'Empty':
                    row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label,emboss=False).collection_name = name
                else:
                    row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label).collection_name = name
            else:
                row.label(text=label)
                row.scale_x = 1
                row.prop(mytool, name, text="")
                row.scale_x = 0.5
                if len(bpy.data.collections[config.Slots[name][0]].children) > 1:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label).collection_name = name
                else:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label,emboss=False).collection_name = name
                row.label(text='')
                row.label(text='')

class WCUSTOM_PT_ArmSlots(bpy.types.Panel):
    bl_label = "Arms Slots"
    bl_idname = "WCUSTOM_PT_ArmSlots"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GENERATION'
    bl_parent_id = 'WCUSTOM_PT_ParentSlots'

    slots = {
    "inputFA": ("LOOP_BACK"),
    "inputW": ("FORWARD"),
    "inputH": ("VIEW_PAN")}
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        for name in self.slots:
            row = layout.row()
            row.label(text=config.Slots[name][1], icon=self.slots[name])
            label = ''
            row.scale_x = 1.5
            if bpy.context.scene.my_tool[name] is not None:
                inputDNA = bpy.context.scene.my_tool.inputDNA
                dna_index = int(config.Slots[name][0][:2])
                dna_splitstrand = inputDNA.split(',')[dna_index + 2].split('-')
                if(len(dna_splitstrand) > 3):
                    color_key = dna_splitstrand[3] or 'X'
                else:
                    color_key = ''
                texture_index = dna_splitstrand[2]
                variant = bpy.context.scene.my_tool[name]
                label = "{} {} {}".format(variant.name.split('_')[3],texture_index, color_key)
                row.label(text=label)
                row.scale_x = 1
                row.prop(mytool, name, text="")
                row.scale_x = 0.5
                # print(len(bpy.data.collections[config.Slots[name][0]].children))
                if len(bpy.data.collections[config.Slots[name][0]].children) > 1:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label).collection_name = name
                else:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label,emboss=False).collection_name = name
                if len(variant.objects) > 1:
                    row.operator(randomizeTexture.bl_idname, text=randomizeTexture.bl_label).collection_name = name
                else:
                    row.operator(randomizeTexture.bl_idname, text=randomizeTexture.bl_label,emboss=False).collection_name = name
                if color_key == 'Empty':
                    row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label,emboss=False).collection_name = name
                else:
                    row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label).collection_name = name
            else:
                row.label(text=label)
                row.scale_x = 1
                row.prop(mytool, name, text="")
                row.scale_x = 0.5
                if len(bpy.data.collections[config.Slots[name][0]].children) > 1:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label).collection_name = name
                else:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label,emboss=False).collection_name = name
                row.label(text='')
                row.label(text='')

class WCUSTOM_PT_LegSlots(bpy.types.Panel):
    bl_label = "Leg Slots"
    bl_idname = "WCUSTOM_PT_LegSlots"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GENERATION'
    bl_parent_id = 'WCUSTOM_PT_ParentSlots'

    slots = {
    "inputPTK": ("OUTLINER_OB_ARMATURE"),
    "inputPTN": ("HANDLE_ALIGNED"),
    "inputC": ("LINCURVE"),
    "inputA": ("LINCURVE"),
    "inputF": ("MOD_DYNAMICPAINT"),}
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        for name in self.slots:
            row = layout.row()
            row.label(text=config.Slots[name][1], icon=self.slots[name])
            label = ''
            row.scale_x = 1.5
            if bpy.context.scene.my_tool[name] is not None:
                inputDNA = bpy.context.scene.my_tool.inputDNA
                dna_index = int(config.Slots[name][0][:2])
                dna_splitstrand = inputDNA.split(',')[dna_index + 2].split('-')
                if(len(dna_splitstrand) > 3):
                    color_key = dna_splitstrand[3] or 'X'
                else:
                    color_key = ''
                texture_index = dna_splitstrand[2]
                variant = bpy.context.scene.my_tool[name]
                label = "{} {} {}".format(variant.name.split('_')[3],texture_index, color_key)
                row.label(text=label)
                row.scale_x = 1
                row.prop(mytool, name, text="")
                row.scale_x = 0.5
                if len(bpy.data.collections[config.Slots[name][0]].children) > 1:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label).collection_name = name
                else:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label,emboss=False).collection_name = name
                if len(variant.objects) > 1:
                    row.operator(randomizeTexture.bl_idname, text=randomizeTexture.bl_label).collection_name = name
                else:
                    row.operator(randomizeTexture.bl_idname, text=randomizeTexture.bl_label,emboss=False).collection_name = name
                if color_key == 'Empty':
                    row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label,emboss=False).collection_name = name
                else:
                    row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label).collection_name = name
            else:
                row.label(text=label)
                row.scale_x = 1
                row.prop(mytool, name, text="")
                row.scale_x = 0.5
                if len(bpy.data.collections[config.Slots[name][0]].children) > 1:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label).collection_name = name
                else:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label,emboss=False).collection_name = name     
                row.label(text='')
                row.label(text='')

class WCUSTOM_PT_HeadSlots(bpy.types.Panel):
    bl_label = "Head Slots"
    bl_idname = "WCUSTOM_PT_HeadSlots"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GENERATION'
    bl_parent_id = 'WCUSTOM_PT_ParentSlots'

    slots = {
    "inputEX": ("GHOST_ENABLED"),
    "inputHA": ("SOLO_ON"),
    "inputHL": ("PARTICLEMODE"),
    "inputHS": ("PARTICLEMODE"),
    "inputMH": ("HIDE_OFF"),
    "inputLH": ("USER"),
    "inputEL": ("PMARKER_ACT"),
    "inputES": ("PMARKER_SEL"),
    "inputN": ("NODE_INSERT_OFF")}
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.label(text="")
        row.scale_x = 0.3
        row.label(text="RANDOMIZE")
        for name in self.slots:
            row = layout.row()
            row.label(text=config.Slots[name][1], icon=self.slots[name])
            label = ''
            row.scale_x = 1.5
            if bpy.context.scene.my_tool[name] is not None:
                inputDNA = bpy.context.scene.my_tool.inputDNA
                dna_index = int(config.Slots[name][0][:2])
                dna_splitstrand = inputDNA.split(',')[dna_index + 2].split('-')
                if(len(dna_splitstrand) > 3):
                    color_key = dna_splitstrand[3] or 'X'
                else:
                    color_key = ''
                texture_index = dna_splitstrand[2]
                variant = bpy.context.scene.my_tool[name]
                label = "{} {} {}".format(variant.name.split('_')[3],texture_index, color_key)
                row.label(text=label)
                row.scale_x = 1
                row.prop(mytool, name, text="")
                row.scale_x = 0.5
                if len(bpy.data.collections[config.Slots[name][0]].children) > 1:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label).collection_name = name
                else:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label,emboss=False).collection_name = name
                if len(variant.objects) > 1:
                    row.operator(randomizeTexture.bl_idname, text=randomizeTexture.bl_label).collection_name = name
                else:
                    row.operator(randomizeTexture.bl_idname, text=randomizeTexture.bl_label,emboss=False).collection_name = name
                if color_key == 'Empty':
                    row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label,emboss=False).collection_name = name
                else:
                    row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label).collection_name = name
            else:
                row.label(text=label)
                row.scale_x = 1
                row.prop(mytool, name, text="")
                row.scale_x = 0.5
                if len(bpy.data.collections[config.Slots[name][0]].children) > 1:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label).collection_name = name
                else:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label,emboss=False).collection_name = name  
                row.label(text='')
                row.label(text='')

class WCUSTOM_PT_OtherSlots(bpy.types.Panel):
    bl_label = "Other Slots"
    bl_idname = "WCUSTOM_PT_OtherSlots"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GENERATION'
    bl_parent_id = 'WCUSTOM_PT_ParentSlots'
    slots = {"inputBG": ("NODE_TEXTURE"),
            "inputENV": ("STICKY_UVS_DISABLE")}
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        for name in self.slots:
            row = layout.row()
            row.label(text=config.Slots[name][1], icon=self.slots[name])
            label = ''
            row.scale_x = 1.5
            if bpy.context.scene.my_tool[name] is not None:
                inputDNA = bpy.context.scene.my_tool.inputDNA
                dna_index = int(config.Slots[name][0][:2])
                dna_splitstrand = inputDNA.split(',')[dna_index + 2].split('-')
                color_key = dna_splitstrand[3] or 'X'
                texture_index = dna_splitstrand[2]
                variant = bpy.context.scene.my_tool[name]
                label = "{} {} {}".format(variant.name.split('_')[3],texture_index, color_key)
                row.label(text=label)
                row.scale_x = 1
                row.prop(mytool, name, text="")
                row.scale_x = 0.5
                if len(bpy.data.collections[config.Slots[name][0]].children) > 1:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label).collection_name = name
                else:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label,emboss=False).collection_name = name
                if len(variant.objects) > 1:
                    row.operator(randomizeTexture.bl_idname, text=randomizeTexture.bl_label).collection_name = name
                else:
                    row.operator(randomizeTexture.bl_idname, text=randomizeTexture.bl_label,emboss=False).collection_name = name
                if color_key == 'Empty':
                    row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label,emboss=False).collection_name = name
                else:
                    row.operator(randomizeColor.bl_idname, text=randomizeColor.bl_label).collection_name = name
            else:
                row.label(text=label)
                row.scale_x = 1
                row.prop(mytool, name, text="")
                row.scale_x = 0.5
                if len(bpy.data.collections[config.Slots[name][0]].children) > 1:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label).collection_name = name
                else:
                    row.operator(randomizeMesh.bl_idname, text=randomizeMesh.bl_label,emboss=False).collection_name = name
                row.label(text='')
                row.label(text='')


#-----------------------------------------------------------------------
class WCUSTOM_PT_DeleteRange(bpy.types.Panel):
    bl_label = "Delete NFTs"
    bl_idname = "WCUSTOM_PT_DeleteRange"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GENERATION'
    bl_parent_id = 'WCUSTOM_PT_ELoadFromFile'
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        box = layout.box()

        row = box.row()
        row.scale_y = 0.6
        box2 = row.box()
        box2.operator(deleteNFT.bl_idname, text=deleteNFT.bl_label, emboss=False)
        box2 = row.box()
        box2.operator(deleteAllNFTs.bl_idname, text=deleteAllNFTs.bl_label, emboss=False)

        row = box.row()
        row.scale_x = 0.5
        row.prop(mytool, "deleteStart")
        row.prop(mytool, "deleteEnd")
        row.scale_x = 1
        box2 = row.box()
        box2.scale_y = 0.5
        box2.operator(deleteRangeNFT.bl_idname, text=deleteRangeNFT.bl_label,emboss=False)


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

        box = layout.box()
        row = box.row()
        index = int(bpy.context.scene.my_tool.CurrentBatchIndex)
        nft_save_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path, "Batch_{}".format(index))
        
        record_path = os.path.join(mytool.batch_json_save_path, '_NFTRecord.json')
        record = json.load(open(record_path))

        single_path = os.path.join(nft_save_path, '_NFTRecord_{}.json'.format(index))
        single = json.load(open(single_path))

        if os.path.exists(nft_save_path):
            row.label(text="Total Generated: " + str(single['numNFTsGenerated']))

        if record.get('numCharacters'):
            char_dict = record['numCharacters']
            row = box.row()
            row.label(text="Total:")
            for char in config.Characters:
                row.label(text="{}: {}".format(char, char_dict[char]))

            single_dict = single['numCharacters']
            row = box.row()
            row.label(text="Batch:")
            for char in config.Characters:
                row.label(text="{}: {}".format(char, single_dict[char]))

        box = layout.box()
        row = box.row()
        row.prop(mytool, "loadNFTIndex")
        row.operator(loadNFT.bl_idname, text=loadNFT.bl_label)
        
        row = box.row()
        row.operator(loadPrevNFT.bl_idname, text=loadPrevNFT.bl_label)
        row.operator(loadNextNFT.bl_idname, text=loadNextNFT.bl_label)
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
        row = layout.box().row()
        if os.path.exists(bpy.context.scene.my_tool.batch_json_save_path):
            batch_path = bpy.context.scene.my_tool.batch_json_save_path
            row.label(text="Current Batch: {} / {}".format(bpy.context.scene.my_tool.CurrentBatchIndex, len(next(os.walk(batch_path))[1])))
        else:
            # row.label(text="Current Batch: {}".format(bpy.context.scene.my_tool.CurrentBatchIndex))
            row.label(text="Please create or load directory")

        box = layout.box()

        row = box.row()
        row.prop(mytool, "BatchSliderIndex")

        row.operator(loadBatch.bl_idname, text=loadBatch.bl_label)
        row = box.row()
        row.operator(saveBatch.bl_idname, text=saveBatch.bl_label)
        row.operator(saveNewBatch.bl_idname, text=saveNewBatch.bl_label)
        row = layout.row()
        box = row.box()
        box.scale_y = 0.6
        box.operator(updateBatch.bl_idname, text=updateBatch.bl_label, emboss=False)
        
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

        row = layout.box()
        row.operator(loadDirectory.bl_idname, text=loadDirectory.bl_label)



class WCUSTOM_PT_GenerationExtra(bpy.types.Panel):
    bl_label = "Extras"
    bl_idname = "WCUSTOM_PT_GenerationExtra"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GENERATION'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.operator(forceLoadDNAFromUI.bl_idname, text=forceLoadDNAFromUI.bl_label)

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
        export_path = os.path.join(mytool.separateExportPath, "Blend_My_NFT", "OUTPUT")



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
        
        export_path = os.path.join(mytool.separateExportPath, "Blend_My_NFT", "OUTPUT")
        if os.path.exists(export_path) and bpy.context.scene.my_tool.root_dir != bpy.context.scene.my_tool.separateExportPath:
            batches_path = os.path.join(bpy.context.scene.my_tool.separateExportPath, "Blend_My_NFT", "OUTPUT")
            batch_path = os.path.join(batches_path, "Batch_{}".format(mytool.BatchRenderIndex))
            box = layout.box()
            boxbox = box.box()
            row = boxbox.row()
            row.label(text="WARNING:")
            row = box.row()
            row.label(text="Only render once all NFTs have been generated and finalized.")
            layout.separator()

            batch_count = len(next(os.walk(batches_path))[1])
            box = layout.box()
            row = box.row()
            row.label(text="Total Batches: {}".format(batch_count))            
            row = box.row()
            row.prop(mytool, "BatchRenderIndex")
            if bpy.context.scene.my_tool.renderMultiBatch and bpy.context.scene.my_tool.renderFullBatch:
                row.prop(mytool, "BatchRenderEndIndex")

            row = box.row()
            if os.path.exists(batch_path):
                batch_count = len(next(os.walk(batch_path))[1])
                row.label(text="Number in batch: {}".format(batch_count))
            else:
                batch_count = 0
                row.label(text="This batch doesn't exist")
            row.prop(mytool, "renderFullBatch",toggle=-1)

            if bpy.context.scene.my_tool.renderFullBatch:
                row.prop(mytool, "renderMultiBatch")
            else:
                row.label(text='')
            layout.separator()

            box = layout.box()
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

                row = box.row()
                row.prop(mytool, "rangeBool")

                row.prop(mytool, "customRenderRangeBool", toggle=1)
                row.scale_x=2

                if mytool.customRenderRangeBool:
                    row.label(text="Render total: ¯\_(ツ)_/¯")
                elif range_start > batch_count or range_start > range_end:
                    row.label(text="Render range: Out of range")
                else:
                    if mytool.rangeBool:
                        row.label(text="Render range: {} ~ {}".format(range_start, range_end))
                    else:
                        row.label(text="Render total: {}".format(range_end - range_start + 1))

                row = box.row()
                if mytool.customRenderRangeBool:
                    row.prop(mytool, "customRenderRange")
                elif mytool.rangeBool:
                    row.prop(mytool, "renderSectionIndex")
                    row.prop(mytool, "renderSectionSize")
                else:
                    row.prop(mytool, "renderSectionIndex", text="Range Start")
                    row.prop(mytool, "renderSectionSize", text="Range End")

            layout.separator(factor=0)
            box = layout.box()

            row = box.row()
            row.prop(mytool, "imageBool", toggle=1)
            row.prop(mytool, "animationBool", toggle=1)
            row.prop(mytool, "modelBool", toggle=1)
            row.prop(mytool, "gifBool", toggle=1)

            row = box.row()
            row = box.row()
            row.prop(mytool, "exportDimension")
            row = box.row()
            row.prop(mytool, "imageFrame")
            row.prop(mytool, "frameLength")

            layout.separator()
            box = layout.box()
            box2 = box.box()
            box2.operator(createBlenderSave.bl_idname, text=createBlenderSave.bl_label.upper())



#-------------------------------------------

class WCUSTOM_PT_EvaluateLogs(bpy.types.Panel):
    bl_label = "Evaluate Logs"
    bl_idname = "WCUSTOM_PT_EvaluateLogs"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EXPORTING'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        row = layout.row()
        row.prop(mytool, "evalMinTime")
        row.prop(mytool, "evalMaxTime")
        row = layout.row()
        row.scale_x = 2
        row.prop(mytool, "evalFilePath", text='')
        row.scale_x = 1
        row.operator(chooseLogPath.bl_idname, text=chooseLogPath.bl_label)
        row = layout.box()
        row.operator(evaluateExportLog.bl_idname, text=evaluateExportLog.bl_label)


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

        export_path = os.path.join(mytool.separateExportPath, "Blend_My_NFT", "OUTPUT")
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
            export_path = os.path.join(mytool.separateExportPath, "Blend_My_NFT", "OUTPUT")
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
    bl_label = "Files Set Up"
    bl_idname = "WCUSTOM_PT_Initialize"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SET UP'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        box = layout.box()
        row = box.row()
        row.label(text="Collections:")
        row = box.row()
        row.operator(loadDirectory.bl_idname, text=loadDirectory.bl_label)
        row = box.row()
        row.operator(createSlotFolders.bl_idname, text=createSlotFolders.bl_label)
        row = box.row()
        row.operator(reimportCharacters.bl_idname, text=reimportCharacters.bl_label)
        row.operator(reimportLight.bl_idname, text=reimportLight.bl_label)

        layout.separator(factor=1.5)
        box = layout.box()
        row = box.row()
        row.label(text="Textures:")
        row = box.row()
        row.operator(renameAllOriginalTextures.bl_idname, text=renameAllOriginalTextures.bl_label)
        row = box.row()
        row.operator(downresTextures.bl_idname, text=downresTextures.bl_label)
        row.scale_x = 0.4
        row.prop(mytool, 'shouldForceDownres')

        box.separator(factor=1.5)
        row = box.row()
        row.operator(downresElementTextures.bl_idname, text=downresElementTextures.bl_label)



        row.scale_x = 1
        layout.separator(factor=1.5)
        box = layout.box()
        box.label(text="Calculator:")
        row = box.row()
        row.operator(countUpAllRarities.bl_idname, text=countUpAllRarities.bl_label)
        row = box.row()
        row.operator(countUpAllItems.bl_idname, text=countUpAllItems.bl_label)
        
        layout.separator(factor=1.5)
        box = layout.box()
        row = box.row()
        row.prop(mytool, "searcherString", text='')
        row.scale_x = 0.4
        row.operator(findAllNFTsWithItems.bl_idname, text=findAllNFTsWithItems.bl_label)

        layout.separator(factor=1.5)

        row = layout.row()
        row.operator(testButton.bl_idname, text=testButton.bl_label)


        # box = layout.box()
        # row = box.row()
        # row.label(text="Clean up:")
        # row = box.row()
        # row.operator(purgeData.bl_idname, text=purgeData.bl_label)




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
        box = layout.box()

        row = box.row()
        row.operator(prevColorStyle.bl_idname, text=prevColorStyle.bl_label)
        row.scale_x = 1.5
        row.prop(mytool, "colorStyleName", text="")
        row.scale_x = 0.5
        row.prop(mytool, "colorStyleRarity", text="")
        row.scale_x = 1
        row.operator(nextColorStyle.bl_idname, text=nextColorStyle.bl_label)

        row = box.row()
        row.operator(addNewColourStyle.bl_idname, text=addNewColourStyle.bl_label)
        row.operator(saveStyleRarity.bl_idname, text=saveStyleRarity.bl_label)

        row = box.row()
        row.operator(deleteColorStyle.bl_idname, text=deleteColorStyle.bl_label, emboss=False)

        layout.separator(factor=0)
        # if DNA_Generator.Outfit_Generator.ColorGen.DoesGlobalColorExist():
        #     row = layout.row()
        #     row.operator(deleteColourStyle.bl_idname, text=deleteColourStyle.bl_label, emboss=False)
        
        box = layout.box()
        row = box.row()
        row.operator(prevStyleColorSet.bl_idname, text=prevStyleColorSet.bl_label)
        #row.prop(mytool, "colorStyleColorListKey", text='')
        current_key = bpy.context.scene.my_tool.currentColorStyleKey
        tint_key = bpy.context.scene.my_tool.colorSetName
        row.label(text=current_key)
        row.operator(nextStyleColorSet.bl_idname, text=nextStyleColorSet.bl_label)
        row = box.row()
        # row.operator(updateColourStyle.bl_idname, text="Add Set ({}) to Style".format(tint_key), icon=updateColourStyle.icon)
        row.operator(updateColourStyle.bl_idname, text="Add Set ({}) to Style".format(tint_key))
        # row = box.row()
        # row.operator(deleteColorSet.bl_idname, text="Delete Set ({}) from Style".format(current_key),icon=deleteColorSet.icon, emboss=False)
        row.operator(deleteColorSet.bl_idname, text="Delete Set ({}) from Style".format(current_key), emboss=False)


        row = layout.row()
        row.label(text='')
        row.scale_x = 2
        row.operator(randomizeAllColor.bl_idname, text=randomizeAllColor.bl_label)
        row.scale_x = 1
        row.label(text='')
        


class WCUSTOM_PT_TintUI(bpy.types.Panel):
    bl_label ="Tint Panel"
    bl_idname = "WCUSTOM_PT_TintUI"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ARTIST'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        
        row = layout.row()
        row.prop(mytool, "colorSetName", text="")
        row = layout.row()
        row.prop(mytool, "RTint", text="Red Tint")
        row = layout.row()
        row.prop(mytool, "GTint", text="Green Tint")
        row = layout.row()
        row.prop(mytool, "BTint", text="Blue Tint")
        row = layout.row()
        row.prop(mytool, "AlphaTint", text="Alpha Tint")
        row = layout.row()
        row.prop(mytool, "WhiteTint", text="White Tint")

        layout.separator(factor=1.5)

        row = layout.row()
        row.operator(prevGlobalColorSet.bl_idname, text=prevGlobalColorSet.bl_label)
        row.scale_x = 0.75
        row.operator(loadGlobalColorSet.bl_idname, text=loadGlobalColorSet.bl_label)
        row.scale_x = 1
        row.operator(nextGlobalColorSet.bl_idname, text=nextGlobalColorSet.bl_label)
        row = layout.row()
        row.operator(addGlobalColorSet.bl_idname, text=addGlobalColorSet.bl_label)
        row = layout.row()
        row.operator(deleteGlobalColorSet.bl_idname, text=deleteGlobalColorSet.bl_label)

        layout.separator()

        box = layout.box()
        row = box.row()
        row.prop(mytool, "inputColorListSceneObject", text='')
        row.scale_x = 0.5
        row.operator(loadColorOnMesh.bl_idname, text=loadColorOnMesh.bl_label)



class WCUSTOM_PT_TintPreviewUI(bpy.types.Panel):
    bl_label ="Preview Panel"
    bl_idname = "WCUSTOM_PT_TintPreviewUI"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ARTIST'
    bl_parent_id = 'WCUSTOM_PT_ArtistUI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        current_key = bpy.context.scene.my_tool.currentColorStyleKey

        row = layout.row()
        row.prop(mytool, "RTintPreview", text="{} Red Tint".format(current_key))
        row = layout.row()
        row.prop(mytool, "GTintPreview", text="{} Green Tint".format(current_key))
        row = layout.row()
        row.prop(mytool, "BTintPreview", text="{} Blue Tint".format(current_key))
        row = layout.row()
        row.prop(mytool, "AlphaTintPreview", text="{} Alpha Tint".format(current_key))
        row = layout.row()
        row.prop(mytool, "WhiteTintPreview", text="{} White Tint".format(current_key))

        layout.separator(factor=0.75)

        box = layout.box()
        row = box.row()
        # row.operator(colourCopyUp.bl_idname, text=colourCopyUp.bl_label, icon=colourCopyUp.icon)
        row.operator(colourCopyDown.bl_idname, text=colourCopyDown.bl_label, icon=colourCopyDown.icon)


class WCUSTOM_PT_RenameColors(bpy.types.Panel):
    bl_label ="Rename Sets"
    bl_idname = "WCUSTOM_PT_RenameColors"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ARTIST'
    bl_parent_id = 'WCUSTOM_PT_ArtistUI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        box = layout.box()
        box.label(text="Changing colour names will make any old NFTs unuseable")


        row = layout.row()
        row.prop(mytool, "renameSetFrom", text='')
        row.scale_x = 0.1
        row.label(text="to")
        row.scale_x = 1
        row.prop(mytool, "renameSetTo", text='')

        row = layout.row()
        row.operator(renameSet.bl_idname, text=renameSet.bl_label)

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
    WCUSTOM_PT_ModelSettings,
    WCUSTOM_PT_PreviewNFTs,
    WCUSTOM_PT_ParentSlots,
    WCUSTOM_PT_AllSlots,
    WCUSTOM_PT_HeadSlots,
    WCUSTOM_PT_TorsoSlots,
    WCUSTOM_PT_ArmSlots,
    WCUSTOM_PT_LegSlots,
    WCUSTOM_PT_OtherSlots,
    WCUSTOM_PT_GenerationExtra,
    GU_PT_collection_custom_properties,
    WCUSTOM_PT_OutputSettings,
    WCUSTOM_PT_Render,
    WCUSTOM_PT_CreateMetadata,
    WCUSTOM_PT_RefactorExports,
    WCUSTOM_PT_ArtistUI,
    WCUSTOM_PT_RenameColors,
    WCUSTOM_PT_TintPreviewUI,
    WCUSTOM_PT_TintUI,
    WCUSTOM_PT_DeleteRange,
    WCUSTOM_PT_EvaluateLogs,
    WCUSTOM_PT_CreateCustomRange,
    # BMNFTS_PT_Documentation,


    # Operators:

    loadBatch,
    saveBatch,
    saveNewBatch,
    resetBatch,
    randomizeAllColor,
    randomizeColor,
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
    # organizeScene,
    createCharacterCollections,
    renderBatch,
    createBlenderSave,
    chooseExportFolder,
    moveDataToLocal,
    purgeData,
    exportMetadata,
    addNewColourStyle,
    updateColourStyle,
    nextColorStyle,
    prevColorStyle,
    nextGlobalColorSet,
    prevGlobalColorSet,
    addGlobalColorSet,
    loadGlobalColorSet,
    deleteGlobalColorSet,
    nextStyleColorSet,
    prevStyleColorSet,
    deleteColourStyle,
    confirmRefactor,
    refactorExports,
    reimportCharacters,
    reimportLight,
    colourCopyUp,
    colourCopyDown,
    loadColorOnMesh,
    deleteColorStyle,
    deleteColorSet,
    updateBatch,
    saveStyleRarity,
    clearGeneratorStyle,
    randomizeAllSets,
    downresTextures,
    renameAllOriginalTextures,
    countUpAllRarities,
    randomizeTexture,
    randomizeMesh,
    deleteRangeNFT,
    forceLoadDNAFromUI,
    renameSet,
    countUpAllItems,
    downresElementTextures,
    chooseLogPath,
    evaluateExportLog,
    findAllNFTsWithItems,
    createCustomBatch,
    testButton

)

addon_keymaps = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=BMNFTS_PGT_MyProperties)

    # wm = bpy.context.window_manager
    # kc = wm.keyconfigs.addon
    # if kc:
    #     km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    #     kmi = km.keymap_items.new(test.bl_idname, type='Z', value='PRESS', ctrl=True)
    #     addon_keymaps.append((km, kmi))  

    # UIList1:

    # bpy.types.Scene.custom = bpy.props.CollectionProperty(type=UIList.CUSTOM_PG_objectCollection)
    # bpy.types.Scene.custom_index = bpy.props.IntProperty()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.my_tool

    # for km, kmi in addon_keymaps:
    #     km.keymap_items.remove(kmi)
    # addon_keymaps.clear()

    # UIList 1:

    # del bpy.types.Scene.custom
    # del bpy.types.Scene.custom_index

if __name__ == '__main__':
    register()
