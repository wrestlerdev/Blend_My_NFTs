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
    #Clears scene and deletes all hierarchy except for ignore folder
    config.custom_print("Creating Slot Folders")
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
                #Set Up Null texture slot
                slot_col_type = bpy.data.collections.new("00-" + slot.partition('-')[2] + "Null" )
                slot_coll.children.link(slot_col_type)
                slot_col_var = bpy.data.collections.new(slot.partition('-')[2] + "_" + slot_col_type.name.partition('-')[2] + "_000_" + "Null" )
                slot_col_type.children.link(slot_col_var)
                tex_object = bpy.context.scene.objects["BLANK"].copy()
                tex_object.data = bpy.context.scene.objects["BLANK"].data.copy()
                tex_object.hide_viewport = True
                tex_object.hide_render = True
                slot_col_var.objects.link(tex_object)

                characterCollectionDict = {}
                for char in config.Characters: # set up null texture slot for character variants
                    varient_coll_char = bpy.data.collections.new(slot.partition('-')[2] + "_" + slot_col_type.name.partition('-')[2]+ "_000_" + "Null_"  + char)
                    characterCollectionDict[char] = varient_coll_char
                    new_object = bpy.context.scene.objects["BLANK"].copy()
                    new_object.data = bpy.context.scene.objects["BLANK"].data.copy()                                                
                    varient_coll_char.objects.link(new_object)
                    varient_coll_char.hide_viewport = True
                    varient_coll_char.hide_render = True
                    slot_col_var.children.link(varient_coll_char)

                #Move on to types and varients if they exist
                for type in os.listdir(type_path):                
                    varient_path = CheckAndFormatPath(type_path, type)
                    if varient_path != "":
                        #create varient collection and link to slot
                        type_coll = bpy.data.collections.new(type)
                        slot_coll.children.link(type_coll)
                        for varient in os.listdir(varient_path):             
                            item_path = CheckAndFormatPath(varient_path, varient)
                            new_var_name = "{}_{}_{}".format(slot[3:], type[3:], varient)
                            if item_path != "":
                                varient_coll = bpy.data.collections.new(new_var_name)
                                varient_coll.hide_viewport = True
                                varient_coll.hide_render = True
                                type_coll.children.link(varient_coll)

                                for file in os.listdir(item_path):
                                    if file.rpartition('.')[2] == "blend":
                                        directory = os.path.join(item_path, file, "Collection")
                                        directory = directory.replace('\\', '/')
                                        characterCollectionDict = {}
                                        for char in config.Characters:
                                            varient_coll_char = bpy.data.collections.new(new_var_name + "_" + char)
                                            varient_coll.children.link(varient_coll_char)
                                            characterCollectionDict[char] = varient_coll_char
                                            varient_coll_char.hide_viewport = True
                                            varient_coll_char.hide_render = True

                                        file_path = ""
                                        file_path = os.path.join(directory, "Item")
                                        file_path = file_path.replace('\\', '/') 
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
                                                    for obj in char.objects:
                                                        for c in config.Characters:
                                                            if char.name.partition(".")[0] == c:
                                                                characterCollectionDict[c].objects.link(obj)
                                                                obj.hide_viewport = True
                                                                obj.hide_render =  True
                                                                if obj.modifiers:
                                                                    for mod in obj.modifiers:
                                                                        if mod.type == 'SUBSURF':
                                                                            mod.show_viewport = False
                                                                            mod.show_render = True
                                                                            mod.levels = mod.render_levels
                                                                obj.name = new_var_name

                                        for c in config.Characters:
                                            bpy.ops.object.select_all(action='DESELECT')
                                            for obj in characterCollectionDict[c].objects:
                                                obj.hide_viewport = False
                                                obj.hide_render =  False
                                                cube = obj
                                                cube.select_set( state = True, view_layer = bpy.context.view_layer )
                                                bpy.context.view_layer.objects.active = cube

                                            for obj in characterCollectionDict[c].objects:
                                                obj.hide_viewport = True
                                                obj.hide_render =  True

                                        texture_path = CheckAndFormatPath(item_path, "Textures")
                                        if(texture_path != ""):
                                            index = 0
                                            for texture_set in os.listdir(texture_path):
                                                set_path = CheckAndFormatPath(texture_path, texture_set)
                                                fallback_texture_set_path = CheckAndFormatPath(texture_path, config.fallback_texture_set_name)
                                                if(set_path != ""):
                                                    tex_object = bpy.context.scene.objects["BLANK"].copy()
                                                    tex_object.data = bpy.context.scene.objects["BLANK"].data.copy()
                                                    tex_object.name = new_var_name + "_" + texture_set
                                                    varient_coll.objects.link(tex_object)
                                                    if fallback_texture_set_path != set_path:
                                                        config.custom_print("{} has alternate texture sets ({})".format(varient, texture_set), col=config.bcolors.OK)
                                                        SetUpObjectMaterialsAndTextures(type, texture_set, tex_object, set_path, characterCollectionDict, fallback_texture_set=fallback_texture_set_path) 
                                                    else:
                                                        SetUpObjectMaterialsAndTextures(type, texture_set, tex_object, set_path, characterCollectionDict) 

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
                                            for child_col in tempHolder.children:
                                                for child_obj in child_col.objects:
                                                    child_col.objects.unlink(child_obj)
                                                bpy.data.collections.remove(child_col)                                    
                                            bpy.data.collections.remove(tempHolder)
                                            bpy.ops.outliner.orphans_purge()
    bpy.ops.file.make_paths_absolute()
    return


def SetUpObjectMaterialsAndTextures(type, texture_set, obj, texture_path, characterCol, fallback_texture_set=''): 
    materialSets = next(os.walk(texture_path))[1] 
    if len(materialSets) > 0: # is there more than one material group
        mats = set()
        for char in config.Characters: #go through all materials on characters and put their name in front
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
                material = GetMaterialDomain(type, texture_set, texture_path, matfolderlink[m], fallback_texture_set=fallback_texture_set)
                tempcopy = material.copy()
                tempcopy.name = m
                obj.data.materials.append(None)
                obj.material_slots[i].material = tempcopy
                tempcopy.name = m
            else:
                material = GetMaterialDomain(type, texture_set, texture_path, matfolderlink[m], fallback_texture_set=fallback_texture_set)
                tempcopy = material.copy()
                tempcopy.name = m
                obj.material_slots[i].material = tempcopy
                tempcopy.name = m     

            #if texture object is a textile we shouldnt treat it like other material
            textile = texture_set.split("-")[1]
            if(textile in config.Textiles):
                LinkTextileNodes(tempcopy, textile, os.path.join(fallback_texture_set, matfolderlink[m]) )
            else:
                LinkImagesToNodes(tempcopy, os.path.join(texture_path, matfolderlink[m]))
                if fallback_texture_set and os.path.isdir(fallback_texture_set):
                    LinkImagesToNodes(tempcopy, os.path.join(fallback_texture_set, matfolderlink[m]))
            i += 1

            
    else: # only one texture set for variant
        material_slots = obj.material_slots
        for m in material_slots:
            material = GetMaterialDomain(type, texture_set, texture_path, "", fallback_texture_set=fallback_texture_set)
            material.use_nodes = True
            matcopy = material.copy()
            m.material = matcopy

            #if texture object is a textile we shouldnt treat it like other material
            textile = texture_set.split("-")[1]
            if(textile in config.Textiles):
                LinkTextileNodes(matcopy, textile, fallback_texture_set)
            else:
                LinkImagesToNodes(matcopy, texture_path)
                if fallback_texture_set and os.path.isdir(fallback_texture_set):
                    LinkImagesToNodes(matcopy, fallback_texture_set)



def GetMaterialDomain(type, texture_set, texture_path, matfolderlink = "", fallback_texture_set=''):
    textile = texture_set.split("-")[1]
    resultTextile = [s for s in config.Textiles if textile in s]
    if resultTextile != []:
        material = bpy.data.materials['MasterTextile']
        return material

    if matfolderlink:
        resultD = [s for s in os.listdir( (texture_path + "/" + matfolderlink) ) if "_D." in s]
        resultE = [s for s in os.listdir( (texture_path + "/" + matfolderlink) ) if "_E." in s]
        resultO = [s for s in os.listdir( (texture_path + "/" + matfolderlink) ) if "_O." in s]
    else:
        resultD = [s for s in os.listdir(texture_path) if "_D." in s]
        resultE = [s for s in os.listdir(texture_path) if "_E." in s]
        resultO = [s for s in os.listdir(texture_path) if "_O." in s]

    if fallback_texture_set and os.path.isdir(fallback_texture_set): # check first texture set
        if not resultD:
            resultD = [s for s in os.listdir( (fallback_texture_set + "/" + matfolderlink) ) if "_D." in s]
        if not resultE:
            resultE = [s for s in os.listdir( (fallback_texture_set + "/" + matfolderlink) ) if "_E." in s]
        if not resultO:
            resultO = [s for s in os.listdir( (fallback_texture_set + "/" + matfolderlink) ) if "_O." in s]

    
    if resultD == [] and resultE != []:
        material = bpy.data.materials['MasterUnlitV01']
    elif resultO != []:
        if "Tattoo" in type:
            material = bpy.data.materials['MasterTattooV01']
        else:
            material = bpy.data.materials['MasterTransparentV01']
    else:
        material = bpy.data.materials['MasterV01']
    return material   

def LinkTextileNodes(matcopy, textile_type, texture_path):
    matcopy.node_tree.nodes["TextileNode"].node_tree = bpy.data.node_groups[textile_type]
    for tex in os.listdir(texture_path):      
        mapType = tex.rpartition("_")[2]
        mapType = mapType.partition(".")[0]

        if "ID" == mapType:
            if not matcopy.node_tree.nodes["ColorIDNode"].image:
                file = os.path.join(texture_path, tex)
                file = file.replace('/', '\\')
                newImage = bpy.data.images.load(file, check_existing=False)
                matcopy.node_tree.nodes["ColorIDNode"].image = newImage
                matcopy.node_tree.nodes["ColorIDNode"].image.colorspace_settings.name = 'Raw'
                matcopy.node_tree.nodes["ColorID_RGBMix"].outputs["Value"].default_value = 1

        if "N" == mapType:
                    if not matcopy.node_tree.nodes["NormalNode"].image:
                        file = os.path.join(texture_path, tex)
                        file = file.replace('/', '\\')
                        newImage = bpy.data.images.load(file, check_existing=False)
                        matcopy.node_tree.nodes["NormalNode"].image = newImage
                        matcopy.node_tree.nodes["NormalNode"].image.colorspace_settings.name = 'Raw'
                        matcopy.node_tree.nodes["NormalMix"].outputs["Value"].default_value = 1

def LinkImagesToNodes(matcopy, texture_path):
        # get the nodes
        for tex in os.listdir(texture_path):      
            mapType = tex.rpartition("_")[2]
            mapType = mapType.partition(".")[0]
            if "D" == mapType:
                if not matcopy.node_tree.nodes["DiffuseNode"].image:
                    file = os.path.join(texture_path, tex)
                    file = file.replace('/', '\\')
                    newImage = bpy.data.images.load(file, check_existing=False)
                    matcopy.node_tree.nodes["DiffuseNode"].image = newImage
                    matcopy.node_tree.nodes["DiffuseMix"].outputs["Value"].default_value = 1

            if "N" == mapType:
                if not matcopy.node_tree.nodes["NormalNode"].image:
                    file = os.path.join(texture_path, tex)
                    file = file.replace('/', '\\')
                    newImage = bpy.data.images.load(file, check_existing=False)
                    matcopy.node_tree.nodes["NormalNode"].image = newImage
                    matcopy.node_tree.nodes["NormalNode"].image.colorspace_settings.name = 'Raw'
                    matcopy.node_tree.nodes["NormalMix"].outputs["Value"].default_value = 1

            if "ID" == mapType:
                if not matcopy.node_tree.nodes["ColorIDNode"].image:
                    file = os.path.join(texture_path, tex)
                    file = file.replace('/', '\\')
                    newImage = bpy.data.images.load(file, check_existing=False)
                    matcopy.node_tree.nodes["ColorIDNode"].image = newImage
                    matcopy.node_tree.nodes["ColorIDNode"].image.colorspace_settings.name = 'Raw'
                    matcopy.node_tree.nodes["ColorID_RGBMix"].outputs["Value"].default_value = 1

            if "M" == mapType:
                if not matcopy.node_tree.nodes["MetallicNode"].image:
                    file = os.path.join(texture_path, tex)
                    file = file.replace('/', '\\')
                    newImage = bpy.data.images.load(file, check_existing=False)
                    matcopy.node_tree.nodes["MetallicNode"].image = newImage
                    matcopy.node_tree.nodes["MetallicNode"].image.colorspace_settings.name = 'Linear'
                    matcopy.node_tree.nodes["MetallicMix"].outputs["Value"].default_value = 1

            if "R" == mapType:
                if not matcopy.node_tree.nodes["RoughnessNode"].image:
                    file = os.path.join(texture_path, tex)
                    file = file.replace('/', '\\')
                    newImage = bpy.data.images.load(file, check_existing=False)
                    matcopy.node_tree.nodes["RoughnessNode"].image = newImage
                    matcopy.node_tree.nodes["RoughnessNode"].image.colorspace_settings.name = 'Linear'
                    matcopy.node_tree.nodes["RoughnessMix"].outputs["Value"].default_value = 1

            if "E" == mapType:
                if not matcopy.node_tree.nodes["EmissiveNode"].image:
                    file = file = os.path.join(texture_path, tex)
                    file = file.replace('/', '\\')
                    newImage = bpy.data.images.load(file, check_existing=False)
                    matcopy.node_tree.nodes["EmissiveNode"].image = newImage 
                    matcopy.node_tree.nodes["EmissiveMix"].outputs["Value"].default_value = 1

            if "O" == mapType:
                if not matcopy.node_tree.nodes["OpacityNode"].image:
                    file = file = os.path.join(texture_path, tex)
                    file = file.replace('/', '\\')
                    newImage = bpy.data.images.load(file, check_existing=False)
                    matcopy.node_tree.nodes["OpacityNode"].image = newImage 
                    matcopy.node_tree.nodes["OpacityNode"].image.colorspace_settings.name = 'Linear'
                    matcopy.node_tree.nodes["OpacityMix"].outputs["Value"].default_value = 1

            if "I" == mapType:
                if not matcopy.node_tree.nodes["IntensityNode"].image: 
                    file = file = os.path.join(texture_path, tex)
                    file = file.replace('/', '\\')
                    newImage = bpy.data.images.load(file, check_existing=False)
                    matcopy.node_tree.nodes["IntensityNode"].image = newImage 
                    matcopy.node_tree.nodes["IntensityNode"].image.colorspace_settings.name = 'Linear'
                    matcopy.node_tree.nodes["IntensityMix"].outputs["Value"].default_value = 1


def CheckAndFormatPath(path, pathTojoin = ""):
    if pathTojoin != "" :
        path = os.path.join(path, pathTojoin)
    new_path = path.replace('\\', '/')

    if not os.path.exists(new_path):
        return ""
    return new_path


# -------------------------------------------------


def reimport_all_character_objects(folder_path):
    delete_all_actions()
    for dir in os.listdir(folder_path):
        if dir.endswith('.blend') and 'Rigs_master' in dir:
            rig_blendfile_path = os.path.join(folder_path, dir)
    for char in config.Characters:
        bpy.ops.outliner.orphans_purge()
        reimport_character_objects(char, rig_blendfile_path)
        set_up_character_skinTattoo_materials(folder_path, char)
    bpy.ops.file.make_paths_absolute()
    return


def reimport_character_objects(character, rig_blendfile_path): # reimports objects/actions for a single character
    clear_old_character_objects(character)
    bpy.data.collections[character].hide_viewport = False
    bpy.data.collections[character].hide_render = False
    bpy.ops.outliner.orphans_purge()

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
            obj.hide_viewport = False
            obj.hide_render =  False
            rigMesh = obj
            rigMesh.select_set( state = True, view_layer = bpy.context.view_layer )
            bpy.context.view_layer.objects.active = rigMesh
            set_up_character_elemental_materials(obj)

    if len(bpy.context.selected_objects) > 1:
        bpy.context.view_layer.objects.active = bpy.data.objects[character + "_Body"]            
    return


#-------------------------------------------------------------------


def set_up_character_skinTattoo_materials(folderpath, character):
    matcopy =  bpy.data.materials['CharacterSkin_Master'].copy()
    matcopy.name = "CharacterSkin_Master" + "_" + character
    texture_path = os.path.join(folderpath, character + "_master", character + "Texture")
    for type in ["Color", "Roughness", "Normal", "Tattoos"]:
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
    return


def set_up_character_elemental_materials(obj): # sets up element material in eye/eyelashes/eyebrows etc
    if obj.type == "MESH":
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


#-------------------------------------------------------------------

def import_character_actions(character, rig_blendfile_pathr):
    actions = []
    with bpy.data.libraries.load(rig_blendfile_pathr) as (data_from, data_to):
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


#-------------------------------------------------------------------


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



#-------------------------------------------------------------------


if __name__ == '__main__':
    pass
