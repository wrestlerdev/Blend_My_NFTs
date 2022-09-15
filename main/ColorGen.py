from hashlib import new
import bpy
import os
import time
import json
import random
from mathutils import Color
from . import config

def MonocromaticColor(col, offset):

    numColors = 3 #how many colors we want our scheme to have
    colors = [None] * numColors #the final color palette array

    #get our hue first, outside of the loop,
    #so all the colors we make will have the same hue
    #h = random.random()
    h = col[0]

    for i in range(numColors - 1, -1, -1):
        #all these colors are going to have the same saturation,
        #though you could experiment with changing this as well
        s = 1
        #the value is going to go from 0 to 1 in steps
        #so that the last color will have 1 value, and the first color will be black.
        #you could instead multiply this by i + 1,
        #so that the darkest color will be a dark shade of your hue rather than black.
        v = (1/numColors) * (i + offset)
        c = Color()
        c.hsv = (h, col[1] + random.uniform(-0.25, 0.25), v)
        colors[(numColors - 1) - i] = (c.r, c.g, c.b)
        
    return colors

def AnalagousColor(col, span):
    colors = [None] * 3
    #span = 0.125 # how wide a section of the color wheel we want to span

    #h1 = random.random() # pick a random hue
    h1 = col[0]
    h2 = (h1 + (span/2)) % 1 #go along the color wheel for half of the span
    h3 = (h1 - (span/2)) #go the opposite direction for half of the span

    #we can't use the modulo operator for negative numbers
    #because its behavior is poorly defined, so we have to check manually
    if (h3 < 0):
        #"abs" means "absolute value", the total distance of a number
        #from zero (so abs(-3) == abs(3) == 3, for instance)
        h3 =  1 - (abs(h3) % 1)
    
    c0 = Color()
    c0.hsv = (col[0], col[1], col[2])
    colors[0] = (c0.r, c0.g, c0.b, 1.0)
    
    c1 = Color()
    c1.hsv = (h2, random.uniform(0.5, 1), col[2] + random.uniform(-0.1, 0.1))
    colors[1] = (c1.r, c1.g, c1.b, 1.0)
    
    c2 = Color()
    c2.hsv = (h3, random.uniform(0.9, 1), col[2]  + random.uniform(-0.1, 0.1))
    colors[2] = (c2.r, c2.g, c2.b, 1.0)
    
    return colors


def TriadicColor(col):
    #triadic color scheme, four would be a tetradic square color scheme,
    #five would be a pentadic, etc
    numColors = 3

    colors = [None] * numColors
    size = 1/numColors

    #get an offset so we don't get the same color scheme every time.
    #starting from a random h like we did before gives weird issues
    #where you get multiple of the same color
    #offset = random.random()
    offset = col[0]

    for i in range(0, numColors):
        h = i * size
        #add the offset to the hue value then make sure it wraps around
        c = Color()
        c.hsv = ( (h + offset) % 1, 1, 1.0)
        colors[i] = (c.r, c.g, c.b)
    return colors

def SplitComplmentaryColor(col, split):
    colors = [None] * 3
    #split = 0.125

    #h1 = random.random()
    h1 = col[0]
    h2 = (((h1 + 0.5) % 1) + split) % 1
    h3 = ((h1 + 0.5) % 1) - split

    if (h3 < 0):
        h3 = 1 - (abs(h3) % 1)

    c0 = Color()
    c0.hsv = (h1, col[1], 1)
    colors[0] = (c0.r, c0.g, c0.b, 1.0)
    
    c1 = Color()
    c1.hsv = (h2, col[1], 1)
    colors[1] = (c1.r, c1.g, c1.b, 1.0)
    
    c2 = Color()
    c2.hsv = (h3, col[1], 1)
    colors[2] = (c2.r, c2.g, c2.b, 1.0)
    return colors

availableColorStyleKeys = []
styleKey = ""
colorkey = ""

def RGBtoHex(vals, rgbtype=1):
    """Converts RGB values in a variety of formats to Hex values.

     @param  vals     An RGB/RGBA tuple
     @param  rgbtype  Valid valus are:
                          1 - Inputs are in the range 0 to 1
                        256 - Inputs are in the range 0 to 255

     @return A hex string in the form '#RRGGBB' or '#RRGGBBAA'
    """

    if len(vals)!=3 and len(vals)!=4:
        raise Exception("RGB or RGBA inputs to RGBtoHex must have three or four elements!")
    if rgbtype!=1 and rgbtype!=256:
        raise Exception("rgbtype must be 1 or 256!")

    #Convert from 0-1 RGB/RGBA to 0-255 RGB/RGBA
    if rgbtype==1:
        vals = [255*x for x in vals]

    #Ensure values are rounded integers, convert to hex, and concatenate
    return '#' + ''.join(['{:02X}'.format(int(round(x))) for x in vals])


#----------------------------------------------------------------------------------------------


def SetUpCharacterStyle():
    global availableColorStyleKeys, styleKey

    number_List_Of_i = []
    rarity_List_Of_i = []
    globalStyleInfo = OpenGlobalStyleList()

    batch_index = int(bpy.context.scene.my_tool.CurrentBatchIndex)
    style_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path,  "Batch_{:03d}".format(batch_index), "_Styles_{:03d}.json".format(batch_index))
    
    #find rarity of styles for this batch
    try:
        batch_style = json.load(open(style_path))
        for style in batch_style.keys():
            rarity = batch_style[style]
            if rarity > 0:
                number_List_Of_i.append(style)
                rarity_List_Of_i.append(float(rarity))
    except:
        config.custom_print(f"Batch Style JSON could not be opened at {style_path}", "", config.bcolors.RESET)

        for style in globalStyleInfo.keys():
            rarity = globalStyleInfo[style]["StyleRarity"]
            if rarity > 0:
                number_List_Of_i.append(style)
                rarity_List_Of_i.append(float(rarity))

    #choose style
    if len(number_List_Of_i) > 0:
        colorChosen = random.choices(number_List_Of_i, weights=rarity_List_Of_i, k=1)

    styleKey = colorChosen[0]
    availableColorStyleKeys =  globalStyleInfo[styleKey]["ColorSets"]
    return styleKey


def CheckAndFormatPath(path, pathTojoin = ""):
    if pathTojoin != "" :
        path = os.path.join(path, pathTojoin)

    new_path = path.replace('\\', '/')

    if not os.path.exists(new_path):
        return ""
    return new_path


def PickOutfitColors(attribute, style_key=''):
    global styleKey, availableColorStyleKeys
    global colorkey

    if style_key:
        globalStyleInfo = OpenGlobalStyleList()
        availableColorStyleKeys = globalStyleInfo[style_key]["ColorSets"]

    globalColorInfo = OpenGlobalColorList()

    #This needs to be thought about, will leave for now but hair styles might become wack
    colorkeyindex = random.randrange(0, len(availableColorStyleKeys))
        
    colorkey = availableColorStyleKeys[colorkeyindex]
    colorChoice = globalColorInfo[colorkey]
                
    return colorkey, colorChoice

#Loop through styles - called from UI
def NextStyle(direction):
    GlobalStyleList = OpenGlobalStyleList()
    keys_list = list(GlobalStyleList)  
    if bpy.context.scene.my_tool.colorStyleName in GlobalStyleList:
        currentIndex = list(GlobalStyleList.keys()).index(bpy.context.scene.my_tool.colorStyleName)      
        nextIndex = currentIndex + direction
        if(nextIndex >= 0 and nextIndex < len(keys_list)):
            key = keys_list[nextIndex]
        elif nextIndex < 0:
            key = keys_list[ len(keys_list) - 1]
        else:
            key = keys_list[ 0 ]
    else:
        key = keys_list[ 0 ]
    bpy.context.scene.my_tool.colorStyleName = key
    StyleColorList = GlobalStyleList[key]["ColorSets"]
    # bpy.context.scene.my_tool.colorStyleRarity = GlobalStyleList[key]["StyleRarity"]
    bpy.context.scene.my_tool.colorStyleRarity = get_style_rarity(key)
    bpy.context.scene.my_tool.currentColorStyleKey = StyleColorList[0]
    

#Loop through color sets - called from UI
def NextStyleColor(direction):
    GlobalStyleList = OpenGlobalStyleList()
    if bpy.context.scene.my_tool.colorStyleName in GlobalStyleList:
        StyleColorList = GlobalStyleList[bpy.context.scene.my_tool.colorStyleName]["ColorSets"]
        currentIndex = StyleColorList.index(bpy.context.scene.my_tool.currentColorStyleKey)      
        nextIndex = currentIndex + direction
        if nextIndex < 0:
            nextIndex = len(StyleColorList) - 1
        elif nextIndex >= len(StyleColorList):
            nextIndex = 0
        bpy.context.scene.my_tool.currentColorStyleKey = StyleColorList[nextIndex]

#add a new color set to color style
def AddColorSetToStyle():
    GlobalStyleList = OpenGlobalStyleList()
    GlobalColorSetList = OpenGlobalColorList()
    if not bpy.context.scene.my_tool.colorStyleName in GlobalStyleList:
        config.custom_print("This is not a valid Style", '', config.bcolors.ERROR )
        return
    elif not bpy.context.scene.my_tool.colorSetName in GlobalColorSetList:
        config.custom_print("This is not an existing Set", '', config.bcolors.ERROR )
        return
    StyleColorSetList = GlobalStyleList[bpy.context.scene.my_tool.colorStyleName]["ColorSets"]
    StyleColorSetList.append(bpy.context.scene.my_tool.colorSetName)
    GlobalStyleList[bpy.context.scene.my_tool.colorStyleName]["ColorSets"] = StyleColorSetList
    WriteToGlobalStyleList(GlobalStyleList)


def SaveNewColorStyle():
    GlobalStyleList = OpenGlobalStyleList()
    if bpy.context.scene.my_tool.colorStyleName not in GlobalStyleList:
        new_style = {}
        new_style["StyleRarity"] = bpy.context.scene.my_tool.colorStyleRarity
        new_style["ColorSets"] = []
        GlobalStyleList[bpy.context.scene.my_tool.colorStyleName] = new_style
    WriteToGlobalStyleList(GlobalStyleList)
    AddColorSetToStyle()


def NextGlobalColorSet(direction):
    GlobalColorList = OpenGlobalColorList()
    keys_list = list(GlobalColorList.keys())
    if bpy.context.scene.my_tool.colorSetName in GlobalColorList:
        currentIndex = keys_list.index(bpy.context.scene.my_tool.colorSetName)      
        nextIndex = currentIndex + direction
        if(nextIndex >= 0 and nextIndex < len(keys_list)):
            key = keys_list[nextIndex]
        elif nextIndex < 0:
            key = keys_list[ len(keys_list) - 1]
        else:
            key = keys_list[ 0 ]
    else:
        key = keys_list[ 0 ]
    bpy.context.scene.my_tool.colorSetName = key
    UpdateColorWheels()
    return key


def LoadColorSet():
    GlobalColorList = OpenGlobalColorList()
    if bpy.context.scene.my_tool.colorSetName in GlobalColorList:
        UpdateColorWheels()
        return True
    else:
        return False


def UpdateColorWheels():
    GlobalColorList = OpenGlobalColorList()
    ColorSet = GlobalColorList[bpy.context.scene.my_tool.colorSetName]
    bpy.context.scene.my_tool.RTint = ColorSet["R"]
    bpy.context.scene.my_tool.GTint = ColorSet["G"]
    bpy.context.scene.my_tool.BTint = ColorSet["B"]
    bpy.context.scene.my_tool.AlphaTint = ColorSet["A"]
    bpy.context.scene.my_tool.WhiteTint = ColorSet["W"]


def AddNewGlobalColorSet():
    R = bpy.context.scene.my_tool.RTint
    G = bpy.context.scene.my_tool.GTint
    B = bpy.context.scene.my_tool.BTint
    A = bpy.context.scene.my_tool.AlphaTint
    W = bpy.context.scene.my_tool.WhiteTint
    ColorListName = bpy.context.scene.my_tool.colorSetName

    NewColorStyle = {}
    NewColorStyle["CommonName"] = ColorListName
    NewColorStyle["R"] = [R[0],R[1],R[2],R[3]]
    NewColorStyle["G"] = [G[0],G[1],G[2],G[3]]
    NewColorStyle["B"] = [B[0],B[1],B[2],B[3]]
    NewColorStyle["A"] = [A[0],A[1],A[2],A[3]]
    NewColorStyle["W"] = [W[0],W[1],W[2],W[3]]
    GlobalColorList = OpenGlobalColorList()
    GlobalColorList[ColorListName] = NewColorStyle
    WriteToGlobalColorList(GlobalColorList)


def DeleteGlobalColorSet():
    if not DoesGlobalColorSetExist():
        config.custom_print("This is not a valid colour set to delete", '', config.bcolors.ERROR )
        return

    Set = bpy.context.scene.my_tool.colorSetName
    GlobalStyle = OpenGlobalStyleList()

    if bpy.context.scene.my_tool.currentColorStyleKey == Set:
        NextStyleColor(1)

    styles = GlobalStyle.keys()
    for style in styles:
        sets = GlobalStyle[style]["ColorSets"]
        if Set in sets:
            sets.remove(Set)
            GlobalStyle[style]["ColorSets"] = sets

    NextGlobalColorSet(1)
    WriteToGlobalStyleList(GlobalStyle)

    GlobalColorList = OpenGlobalColorList()
    GlobalColorList.pop(Set)
    
    WriteToGlobalColorList(GlobalColorList)
    return


def DeleteGlobalColorStyle():
    LastColorStyleName = bpy.context.scene.my_tool.colorStyleName
    if DoesStyleExist():
        NextStyle(1)
        GlobalStyleList = OpenGlobalStyleList()
        GlobalStyleList.pop(LastColorStyleName)
        WriteToGlobalStyleList(GlobalStyleList)
        config.custom_print("Color style ({}) has been deleted °˖✧◝(⁰▿⁰)◜✧˖°".format(LastColorStyleName), '', config.bcolors.ERROR )
    else:
        config.custom_print(f"This {bpy.context.scene.my_tool.colorStyleName} isn't a valid colour style key", '', config.bcolors.ERROR )


def DeleteSetFromStyle(Style, Set):
    if not DoesStyleExist(Style):
        config.custom_print(f"This style {Style} doesn't exist", '', config.bcolors.ERROR )
        return

    if not DoesGlobalColorSetExist(Set):
        config.custom_print(f"This set {Set} doesn't exist", '', config.bcolors.ERROR )
        return

    GlobalStyle = OpenGlobalStyleList()
    sets = GlobalStyle[Style]["ColorSets"]
    sets.remove(Set)
    GlobalStyle[Style] = sets
    NextStyleColor(1)
    WriteToGlobalStyleList(GlobalStyle)
    return


def DoesGlobalColorSetExist(Set=''):
    GlobalColorList = OpenGlobalColorList()
    if not Set:
        Set = bpy.context.scene.my_tool.colorSetName
    if GlobalColorList.get(Set) is not None:
        doesListExist = True
    else:
        doesListExist = False
    return doesListExist


def DoesStyleExist(Style=''):
    GlobalStyles = OpenGlobalStyleList()
    if not Style:
        Style = bpy.context.scene.my_tool.colorStyleName
    if GlobalStyles.get(Style) is not None:
        doesStyleExist = True
    else:
        doesStyleExist = False
    return doesStyleExist


def OpenGlobalColorList():
    root_dir = bpy.context.scene.my_tool.root_dir
    path = os.path.join(root_dir, "INPUT\GlobalColorList.json")
    GlobalColorList = json.load(open(path))
    return GlobalColorList


def WriteToGlobalColorList(GlobalColorList):
    root_dir = bpy.context.scene.my_tool.root_dir
    path = os.path.join(root_dir, "INPUT\GlobalColorList.json")
    try:
        ledger = json.dumps(GlobalColorList, indent=1, ensure_ascii=True)
        with open(path, 'w') as outfile:
            outfile.write(ledger + '\n')
    except:
        config.custom_print("ColorStyle was not sent", '', config.bcolors.ERROR )


def OpenGlobalStyleList():
    root_dir = bpy.context.scene.my_tool.root_dir
    path = os.path.join(root_dir, "INPUT\GlobalStyles.json")
    GlobalStyleList = json.load(open(path))
    return GlobalStyleList


def WriteToGlobalStyleList(GlobalStyleList):
    root_dir = bpy.context.scene.my_tool.root_dir
    path = os.path.join(root_dir, "INPUT\GlobalStyles.json")
    try:
      ledger = json.dumps(GlobalStyleList, indent=1, ensure_ascii=True)
      with open(path, 'w') as outfile:
         outfile.write(ledger + '\n')
    except:
        config.custom_print("ColorStyle was not sent", '', config.bcolors.ERROR )


def OpenBatchColorRarity(batch_index):
    path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path,  "Batch_{:03d}".format(batch_index), "_Styles_{:03d}.json".format(batch_index))
    GlobalColorList = json.load(open(path))
    return GlobalColorList



def ColorHasbeenUpdated(ColorTint):
    inputColorListSceneObject = bpy.context.scene.my_tool.inputColorListSceneObject
    Rtint = bpy.context.scene.my_tool.RTint
    Gtint = bpy.context.scene.my_tool.GTint
    Btint = bpy.context.scene.my_tool.BTint
    Atint = bpy.context.scene.my_tool.AlphaTint
    Wtint = bpy.context.scene.my_tool.WhiteTint
    if inputColorListSceneObject:
        collection_name = inputColorListSceneObject.users_collection[0].name
        collection_name = collection_name.rpartition('_')[0]
        if inputColorListSceneObject is not None:
            for m in inputColorListSceneObject.material_slots:
                material = m.material
                for node in material.node_tree.nodes:
                    if (node.label == "RTint"):
                        node.outputs["Color"].default_value = Rtint
                    if (node.label == "GTint"):
                        node.outputs["Color"].default_value = Gtint
                    if (node.label == "BTint"):
                        node.outputs["Color"].default_value = Btint
                    if (node.label == "AlphaTint"):
                        node.outputs["Color"].default_value = Atint
                    if (node.label == "WhiteTint"):
                        node.outputs["Color"].default_value = Wtint
    return None


# -------------------------------------------------------


def UpdateStyleRarity(Style=''):
    if not Style:
        Style = bpy.context.scene.my_tool.colorStyleName
    batch_index = int(bpy.context.scene.my_tool.CurrentBatchIndex)
    style_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path,  "Batch_{:03d}".format(batch_index), "_Styles_{:03d}.json".format(batch_index))
    rarity = bpy.context.scene.my_tool.colorStyleRarity
    try:
        batch_style = json.load(open(style_path))
    except:
        config.custom_print(f"Batch Style JSON could not be opened at {style_path} ", '', config.bcolors.ERROR )

        config.custom_print(f"Batch Style JSON could not be opened at {style_path}", "", config.bcolors.ERROR)
        return

    batch_style[Style] = rarity

    try:
        ledger = json.dumps(batch_style, indent=1, ensure_ascii=True)
        with open(style_path, 'w') as outfile:
            outfile.write(ledger + '\n')
    except:
        config.custom_print(f"Batch Style JSON could not be saved at {style_path}", "", config.bcolors.ERROR)
    return


def get_style_rarity(style=''):
    batch_index = int(bpy.context.scene.my_tool.CurrentBatchIndex)
    style_path = os.path.join(bpy.context.scene.my_tool.batch_json_save_path,  "Batch_{:03d}".format(batch_index), "_Styles_{:03d}.json".format(batch_index))
    try:
        batch_style = json.load(open(style_path))
        if style in batch_style:
            return batch_style[style]
    except:
        config.custom_print(f"Batch Style JSON could not be opened at {style_path}", "", config.bcolors.ERROR)
    return 0



# -------------------------------------------------------


def UIColorKey_has_updated():
    GlobalColorList = OpenGlobalColorList()
    ColorSet = GlobalColorList[bpy.context.scene.my_tool.currentColorStyleKey]
    bpy.context.scene.my_tool.RTintPreview = ColorSet["R"]
    bpy.context.scene.my_tool.GTintPreview = ColorSet["G"]
    bpy.context.scene.my_tool.BTintPreview = ColorSet["B"]
    bpy.context.scene.my_tool.AlphaTintPreview = ColorSet["A"]
    bpy.context.scene.my_tool.WhiteTintPreview = ColorSet["W"]
    return


def copy_colour_down():
    bpy.context.scene.my_tool.RTint = bpy.context.scene.my_tool.RTintPreview
    bpy.context.scene.my_tool.GTint = bpy.context.scene.my_tool.GTintPreview
    bpy.context.scene.my_tool.BTint = bpy.context.scene.my_tool.BTintPreview
    bpy.context.scene.my_tool.AlphaTint = bpy.context.scene.my_tool.AlphaTintPreview
    bpy.context.scene.my_tool.WhiteTint = bpy.context.scene.my_tool.WhiteTintPreview
    return


#-----------------------------------------------------------


def create_batch_color(batch_path, batch_num, contains_all):
    default_style = "Random"
    default_weight = 50
    json_path = os.path.join(batch_path, "_Styles_{:03d}.json".format(batch_num))

    style_dict = {}
    if contains_all:
        GlobalStyles = OpenGlobalStyleList()
        for style in GlobalStyles.keys():
            rarity = GlobalStyles[style]["StyleRarity"]
            style_dict[style] = rarity
    else:
        style_dict[default_style] = default_weight

    ledger = json.dumps(style_dict, indent=1, ensure_ascii=True)
    with open(json_path, 'w') as outfile:
        outfile.write(ledger + '\n')
    return


#-----------------------------------------------------------


def rename_color_sets(old_name, new_name):
    GlobalColorSetList = OpenGlobalColorList()
    GlobalStyles = OpenGlobalStyleList()

    old_value = GlobalColorSetList.pop(old_name, None)
    if old_value:
        old_value["CommonName"] = new_name
        GlobalColorSetList[new_name] = old_value
    else:
        config.custom_print(f"NO SUCH COLOR SET EXSISTS", "", config.bcolors.ERROR)
        return

    for style in GlobalStyles.keys():
        colorset = GlobalStyles[style]["ColorSets"]
        new_colorset = [i if i != old_name else new_name for i in colorset]
        GlobalStyles[style]["ColorSets"] = new_colorset

    WriteToGlobalColorList(GlobalColorSetList)
    WriteToGlobalStyleList(GlobalStyles)
    return