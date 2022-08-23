import bpy
import os
import json
import shutil
import bmesh
from . import config


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
    print("Hello")
    delete_hierarchy(bpy.context.scene.collection)
    bpy.ops.outliner.orphans_purge()

    slots_path = CheckAndFormatPath(save_path, "INPUT/SLOTS")
    # print(slots_path)
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
                                # print(varient)
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
                                                    # print(char.name)
                                                    for obj in char.objects:
                                                        # print(obj.name)
                                                        for c in config.Characters:
                                                            if char.name.partition(".")[0] == c:
                                                                # print(c)
                                                                characterCollectionDict[c].objects.link(obj)
                                                                obj.hide_viewport = True
                                                                obj.hide_render =  True
                                                                if obj.modifiers:
                                                                    for mod in obj.modifiers:
                                                                        if mod.type == 'SUBSURF':
                                                                            # print(obj.name)
                                                                            mod.show_viewport = False
                                                                            mod.show_render = True
                                                                            mod.levels = mod.render_levels

                                        for c in config.Characters:
                                            bpy.ops.object.select_all(action='DESELECT')
                                            for obj in characterCollectionDict[c].objects:
                                                obj.hide_viewport = False
                                                obj.hide_render =  False
                                                cube = obj
                                                cube.select_set( state = True, view_layer = bpy.context.view_layer )
                                                bpy.context.view_layer.objects.active = cube

                                            # if len(bpy.context.selected_objects) > 1:                    
                                            #     bpy.ops.object.join() # OBJECTJOIN
                                            if len(characterCollectionDict[c].objects) > 0:
                                                objectToCalc = characterCollectionDict[c].objects[0]
                                                #area = find_mesh_area(objectToCalc)
                                                area = 0.0

                                                characterCollectionDict[c]["Volume"] = (area * 2) / 1000

                                            else:
                                                characterCollectionDict[c]["Volume"] = 0.0

                                            for obj in characterCollectionDict[c].objects:
                                                obj.hide_viewport = True
                                                obj.hide_render =  True

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
                                                    SetUpObjectMaterialsAndTextures(tex_object, set_path, characterCollectionDict, type) 
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
                                            # print("No Textures" + varient)
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
    bpy.ops.file.make_paths_absolute()
    return

def SetUpObjectMaterialsAndTextures(obj, texture_path, characterCol, type): 
    materialSets = next(os.walk(texture_path))[1] 
    #is there more than one material group
    if len(materialSets) > 0:
        mats = set()
        #go through all materials on characters and put their name in front
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
                material = GetMatrialDomain(texture_path, matfolderlink[m])
                tempcopy = material.copy()
                tempcopy.name = m
                obj.data.materials.append(None)
                obj.material_slots[i].material = tempcopy
                tempcopy.name = m
            else:
                material = GetMatrialDomain(texture_path, matfolderlink[m])
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

            if "Hair" in type:
                for n in tempcopy.node_tree.nodes:
                    if n.type == "GROUP" and n.node_tree == bpy.data.node_groups["OutfitElementMixer"]:
                        n.node_tree = bpy.data.node_groups["SkinElementMixer"]
            
    else:
        material_slots = obj.material_slots
        for m in material_slots:
            material = GetMatrialDomain(texture_path)
            material.use_nodes = True
            matcopy = material.copy()
            m.material = matcopy
            LinkImagesToNodes(matcopy, texture_path)

            if "Hair" in type:
                print(type)
                #for n in matcopy.node_tree.nodes:
                    # if n.type == "GROUP" and n.node_tree == bpy.data.node_groups["OutfitElementMixer"]:
                    #     n.node_tree = bpy.data.node_groups["SkinElementMixer"]
    
    # for i in reversed(range(0, len(obj.material_slots))):
    #     if obj.material_slots[i].link != 'OBJECT':
    #         print("Deleting: " + str(i))
    #         obj.material_slots[i].link = 'OBJECT'
    #         #obj.data.materials.pop(index = i)
def GetMatrialDomain(texture_path, matfolderlink = ""):
    if matfolderlink:
        resultD = [s for s in os.listdir( (texture_path + "/" + matfolderlink) ) if "_D." in s]
        resultE = [s for s in os.listdir( (texture_path + "/" + matfolderlink) ) if "_E." in s]
        resultO = [s for s in os.listdir( (texture_path + "/" + matfolderlink) ) if "_O." in s]
    else:
        resultD = [s for s in os.listdir(texture_path) if "_D." in s]
        resultE = [s for s in os.listdir(texture_path) if "_E." in s]
        resultO = [s for s in os.listdir(texture_path) if "_O." in s]

    if resultD == [] and resultE != []:
        material = bpy.data.materials['MasterUnlitV01']
    elif resultO != []:
        material = bpy.data.materials['MasterTransparentV01']
    else:
        material = bpy.data.materials['MasterV01']

    return material   

def LinkImagesToNodes(matcopy, texture_path):
        # get the nodes
        
        for tex in os.listdir(texture_path):      
            mapType = tex.rpartition("_")[2]
            # print(mapType)
            mapType = mapType.partition(".")[0]
            # print('TEXTURE IS: ' + mapType)
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

            if "I" == mapType:
                # print("I is choosen")
                file = file = os.path.join(texture_path, tex)
                file = file.replace('/', '\\')
                newImage = bpy.data.images.load(file, check_existing=False)
                matcopy.node_tree.nodes["IntensityNode"].image = newImage 
                matcopy.node_tree.nodes["IntensityNode"].image.colorspace_settings.name = 'Linear'
                matcopy.node_tree.nodes["IntensityMix"].outputs["Value"].default_value = 1
            # if node.label == "RTint":
            #     node.outputs["Color"].default_value = parent["color_primary"]


def CheckAndFormatPath(path, pathTojoin = ""):
    if pathTojoin != "" :
        path = os.path.join(path, pathTojoin)

    new_path = path.replace('\\', '/')

    if not os.path.exists(new_path):
        return ""

    return new_path



def bmesh_copy_from_object(obj, transform=True, triangulate=True, apply_modifiers=False):
    """Returns a transformed, triangulated copy of the mesh"""

    assert obj.type == 'MESH'

    if apply_modifiers and obj.modifiers:
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        me = obj_eval.to_mesh()
        bm = bmesh.new()
        bm.from_mesh(me)
        obj_eval.to_mesh_clear()
    else:
        me = obj.data
        if obj.mode == 'EDIT':
            bm_orig = bmesh.from_edit_mesh(me)
            bm = bm_orig.copy()
        else:
            bm = bmesh.new()
            bm.from_mesh(me)

    # TODO. remove all customdata layers.
    # would save ram

    if transform:
        bm.transform(obj.matrix_world)

    if triangulate:
        bmesh.ops.triangulate(bm, faces=bm.faces)

    return bm

def bmesh_calc_area(bm):
    """Calculate the surface area."""
    return sum(f.calc_area() for f in bm.faces)

def bmesh_calc_vol(bm):
    return bm.calc_volume()

def find_mesh_area(obj):
    scene = bpy.context.scene
    unit = scene.unit_settings
    scale = 1.0 if unit.system == 'NONE' else unit.scale_length
    #obj = bpy.context.active_object

    # depsgraph = bpy.context.evaluated_depsgraph_get()
    # obj_eval = obj.evaluated_get(depsgraph)
    # x = obj_eval.dimensions.x
    # y = obj_eval.dimensions.y
    # z = obj_eval.dimensions.z
    # area = x * y * z
    #print("x: ", x, " y: ", y, " z: ", z, " Volume: ",  area)

    #bm = bmesh_copy_from_object(obj, apply_modifiers=True)
    #area = bmesh_calc_area(bm)
    #area = bmesh_calc_vol(bm)
    #bm.free()

    #return area
    # if unit.system == 'NONE':
    #     area_fmt = clean_float(area, 8)
    # else:
    #     length, symbol = get_unit(unit.system, unit.length_unit)

    #     area_unit = area * (scale ** 2.0) / (length ** 2.0)
    #     area_str = clean_float(area_unit, 4)
    #     area_fmt = f"{area_str} {symbol}"



# -------------------------------------------------


def reimport_all_character_objects(folder_path):
    delete_all_actions()
    for dir in os.listdir(folder_path):
        if dir.endswith('.blend') and 'Rigs_master_tattoo' in dir:
            rig_blendfile_path = os.path.join(folder_path, dir)
    for char in config.Characters:
        bpy.ops.outliner.orphans_purge()
        bpy.ops.outliner.orphans_purge()
        bpy.ops.outliner.orphans_purge()
        bpy.ops.outliner.orphans_purge()
        bpy.ops.outliner.orphans_purge()
        reimport_character_objects(char, rig_blendfile_path)
        set_up_character_skinTattoo_materials(folder_path, char)
        
        
    if bpy.data.node_groups.get("TattooNef.001") != None:
        # bpy.data.node_groups["TattooNef.001"] = "TattooNef"
        pass
    bpy.ops.file.make_paths_absolute()
    return


def reimport_character_objects(character, rig_blendfile_path):
    clear_old_character_objects(character)
    bpy.data.collections[character].hide_viewport = False
    bpy.data.collections[character].hide_render = False
    bpy.ops.outliner.orphans_purge()
    bpy.ops.outliner.orphans_purge()
    bpy.ops.outliner.orphans_purge() # i think doing this 3 times gets rid of the orphan node groups too

    layer_collection = bpy.context.view_layer.layer_collection.children["Script_Ignore"].children[character]
    bpy.context.view_layer.active_layer_collection = layer_collection
    

    filename = character + '_Rig'
    file_path   = os.path.join(rig_blendfile_path, "Collection", filename)
    directory = os.path.join(rig_blendfile_path, "Collection")
    bpy.ops.wm.append(filepath=file_path, directory=directory, filename=filename)
    import_character_actions(character, rig_blendfile_path)

    rig = bpy.data.objects['armature_' + character.lower()]

    for obj in bpy.data.objects:
        if obj.parent == rig:
            # Do stuff
            obj.hide_viewport = False
            obj.hide_render =  False
            rigMesh = obj
            rigMesh.select_set( state = True, view_layer = bpy.context.view_layer )
            bpy.context.view_layer.objects.active = rigMesh
            set_up_character_elemental_materials(obj)
                
    if len(bpy.context.selected_objects) > 1:
        bpy.context.view_layer.objects.active = bpy.data.objects[character + "_Body"]            



        # bpy.ops.object.join() # OBJECTJOIN
        # print("JOINING")
    
    # for col in bpy.data.collections[character].children:
    #     for obj in col.objects:
    #         if obj.type == 'ARMATURE':
    #             for bodyMesh in obj.objects:
    #                 if bodyMesh.type == 'MESH':
    #                     bodyMesh.hide_viewport = False
    #                     bodyMesh.hide_render =  False
    #                     cube = bodyMesh
    #                     cube.select_set( state = True, view_layer = bpy.context.view_layer )
    #                     bpy.context.view_layer.objects.active = cube
    # if len(bpy.context.selected_objects) > 1:                    
    #     bpy.ops.object.join()
    return


def set_up_character_skinTattoo_materials(folderpath, character):
    matcopy =  bpy.data.materials['CharacterSkin_Master'].copy()
    matcopy.name = "CharacterSkin_Master" + "_" + character
    texture_path = os.path.join(folderpath, character + "_master", character + "Texture")
    for type in ["Color", "Roughness", "Normal"]:
        for tex in os.listdir(texture_path):
            if "_Body_" + type in tex:
                file = os.path.join(texture_path, tex)
                file = file.replace('/', '\\')
                newImage = bpy.data.images.load(file, check_existing=False)
                matcopy.node_tree.nodes[type].image = newImage
                if type == "Normal":
                    matcopy.node_tree.nodes[type].image.colorspace_settings.name = 'Linear'
    #Find the body mesh and set index 01 to be skin master
    bpy.data.objects[character + "_Body"].material_slots[0].material = matcopy
    print(character)


    # elementtexture_node = bpy.data.node_groups["ElementTextures" + character]

    # node_group = elementtexture_node.nodes.new("ShaderNodeGroup")
    # node_group.node_tree = bpy.data.node_groups["TattooElementPicker"]
    # node_group.location = (100,100)

    # output_node = elementtexture_node.nodes["Group Output"]
    # for type in ["Diffuse", "Roughness", "Metallic", "Normal", "Emission"]:
    #     elementtexture_node.links.new(output_node.inputs[type], node_group.outputs[type])

    return


def set_up_character_elemental_materials(obj):
    if obj.type == "MESH":
        # print(obj.name)
        for mat in obj.material_slots:
            nodes = mat.material.node_tree.nodes

            normal_node = None
            for n in nodes:
                if n.type == "TEX_IMAGE":
                    if 'normal' in n.image.name.lower() or 'nomal' in n.image.name.lower():
                        normal_node = n

            og_BDSF = mat.material.node_tree.nodes["Principled BSDF"]
            og_bdsf_loc = og_BDSF.location
            
            node_type = "SkinElementMixer"
            if "ball" in obj.name.lower() or "highlight" in obj.name.lower():
                node_type = "FullBodyElementMixer"

            if not "glass" in obj.name:
                node_group = nodes.new("ShaderNodeGroup")
                node_group.node_tree = bpy.data.node_groups[node_type]
                node_group.location = (og_bdsf_loc[0] + 400, og_bdsf_loc[1])
                node_group.name = node_type
                if normal_node:
                    mat.material.node_tree.links.new(node_group.inputs[1], normal_node.outputs[0])
                else:
                    node_group.inputs[1].default_value = (0.5, 0.5, 1, 1)

                mat.material.node_tree.links.new(node_group.inputs[0], og_BDSF.outputs[0])

                output_node = mat.material.node_tree.nodes["Material Output"]
                output_node.location = (og_bdsf_loc[0] + 800, og_bdsf_loc[1])

                mat.material.node_tree.links.new(output_node.inputs[0], node_group.outputs[0])



def import_character_actions(character, rig_blendfile_pathr):
    actions = []
    with bpy.data.libraries.load(rig_blendfile_pathr) as (data_from, data_to):
        #names = [name for name in data_from.collections]
        actions = [action for action in data_from.actions]
        for action in actions:
            if action.endswith(character.lower() + '_action'):
                dir = os.path.join(rig_blendfile_pathr, "Action")
                file_name = action
                file_path = os.path.join(dir, file_name)      
                bpy.ops.wm.append(filepath=file_path, directory=dir, filename=file_name, set_fake=True )
            
    return actions

def delete_all_actions():
    for action in bpy.data.actions:
        bpy.data.actions.remove(action)

def clear_old_character_objects(char_name):
    coll = bpy.data.collections[char_name]
    recurse_delete_collection(coll)
    bpy.ops.outliner.orphans_purge()
    return

def recurse_delete_collection(collection):
    for obj in collection.objects:
        collection.objects.unlink(obj)
        bpy.data.objects.remove(obj)
    for child in collection.children:
        recurse_delete_collection(child)
        collection.children.unlink(child)
    return


def reimport_lights(blend_path):
    parent_name = "Rendering"
    folder_name = "Lighting"

    if bpy.data.collections.get(parent_name) is None: # creates render folder
        render_folder = bpy.data.collections.new(parent_name)
        bpy.data.collections["Script_Ignore"].children.link(render_folder)
    else:
        render_folder = bpy.data.collections[parent_name]

    for obj in bpy.data.collections["Script_Ignore"].objects: # imports camera into render folder that exist in script ignore
        if obj.type == 'CAMERA':
            bpy.data.collections["Script_Ignore"].objects.unlink(obj)
            bpy.data.collections[folder_name].objects.link(obj)

    if bpy.data.collections.get(folder_name) is None: # delete all within lighting folder, purge, then reimport from lighting file
        folder = bpy.data.collections.new(folder_name)
        bpy.data.collections[parent_name].children.link(folder)
    else:
        folder = bpy.data.collections[folder_name]
        for coll in folder.children:
            for obj in coll.objects:
                coll.objects.unlink(obj)
            bpy.data.collections.remove(coll)
        bpy.ops.outliner.orphans_purge()
    layer_collection = bpy.context.view_layer.layer_collection.children["Script_Ignore"].children[render_folder.name].children[folder.name]
    bpy.context.view_layer.active_layer_collection = layer_collection

    file_path   = os.path.join(blend_path, "Collection", "light_setup")
    directory = os.path.join(blend_path, "Collection")
    filename = 'light_setup'
    bpy.ops.wm.append(filepath=file_path, directory=directory, filename=filename)
    return




if __name__ == '__main__':
    pass



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
