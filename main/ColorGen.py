from ctypes import sizeof
import bpy
import os
import re
import copy
import time
import json
import random
import importlib
from functools import partial
from mathutils import Color

#Color dict which uses a letter to definae style. 0 element is main color, all other elements are complemntary colors
# cols = {
#     "a" : [(0.00000, 0.04706, 0.03529), (0.64706, 0.41569, 0.21176), (0.84706, 0.81176, 0.78039), (0.84706, 0.65490, 0.58431), (0.54902,0.00784,0.00784)],
#     "b" : [(0.62745,0.76471,0.84706), (0.13333,0.35686,0.44706), (0.19608,0.24706,0.00392), (0.84706,0.46667,0.38039), (0.74902,0.26667,0.26667)],
#     "c" : [(0.31373,0.70588,0.74902), (0.84706,0.63922,0.01569), (0.74902,0.49020,0.01176), (0.74902,0.35686,0.01176), (0.64706,0.48235,0.33725)]
# }
letterstyles = 'abcdefghijklmnopqrstuvw'
cols = {
    "a" : [(0.0194444444444444,0.22,0.96),(0.569444444444444,0.16,0.96),(0.633333333333333,0.7,34),(0,0,0.68),(0,0,1),(0.611111111111111,0.38,0.03),(0.991666666666667,0.85,0.85),(0.111111111111111,0.13,0.99)],
    "b" : [(0.997222222222222,0.68,82),(0.569444444444444,0.16,96),(0.633333333333333,0.7,34),(0,0,68),(0,0,100),(0.611111111111111,0.43,3),(0.0194444444444444,0.27,98),(0.111111111111111,0.13,98)],
    "c" : [(0.0388888888888889,0.83,95),(0.402777777777778,0.81,35),(0.569444444444444,0.16,96),(0.633333333333333,0.7,34),(0,0,100),(0.611111111111111,0.43,3),(0.111111111111111,0.13,99),(0.0277777777777778,0.44,31)],
    "d" : [(0.119444444444444,0.1,0.96),(0.633333333333333,0.7,34),(0.933333333333333,0.56,38),(0.0222222222222222,0.45,31),(0,0,100),(0.611111111111111,0.38,3),(0.136111111111111,0.81,99),(0.0388888888888889,0.83,95)],
    "e" : [(0.130555555555556,0.69,98),(0.402777777777778,0.81,35),(0.633333333333333,0.7,34),(0,0,100),(0.611111111111111,0.38,3),(0.111111111111111,0.13,99)],
    "f" : [(0.433333333333333,0.99,47),(0.0388888888888889,0.83,95),(0.933333333333333,0.56,38),(0,0,100),(0.611111111111111,0.38,3),(0.136111111111111,0.81,99),(0.569444444444444,0.16,96)],
    "g" : [(0.563888888888889,0.15,93),(0.0194444444444444,0.27,0.98),(0.991666666666667,0.85,0.85),(0.0388888888888889,0.83,0.95),(0,0,100),(0.611111111111111,0.38,0.03),(0.633333333333333,0.7,34),(0.933333333333333,0.56,38)],
    "h" : [(0.580555555555556,0.76,45),(0.0194444444444444,0.27,98),(0.991666666666667,0.85,0.85),(0.136111111111111,0.81,99),(0,0,68),(0,0,100),(0.611111111111111,0.38,3),(0.569444444444444,0.16,96),(0.933333333333333,0.56,38)],
    "i" : [(0.0138888888888889,81,65),(0.980555555555556,62,32),(0.0833333333333333,20,65),(0.966666666666667,41,88),(0.0361111111111111,50,25),(0.111111111111111,14,8)],
    "j" : [(0.925,0.39,45),(0.0388888888888889,0.83,95),(0,0,68),(0.433333333333333,0.99,47),(0,0,100),(0.611111111111111,0.38,3),(0.569444444444444,0.16,96),(0.633333333333333,0.7,34)],
    "k" : [(0.025,0.28,39),(0.111111111111111,0.13,99),(0,0,100),(0.611111111111111,0.38,3),(0.0388888888888889,0.83,95)],
    "l" : [(0.588888888888889,0.08,74),(0.0194444444444444,0.27,98),(0.991666666666667,0.85,85),(0.633333333333333,0.7,34),(0.933333333333333,0.56,38),(0,0,100),(0.611111111111111,0.38,3)],    
    "m" : [(0.536111111111111,0.1,0.9),(0.0972222222222222,0.25,0.7),(0.0916666666666667,0.29,0.5),(0.233333333333333,0.28,0.41),(0.233333333333333,0.32,0.78),(0.666666666666667,0.49,0.61),(0.758333333333333,0.56,0.58),(0.633333333333333,0.25,0.83),(0.0972222222222222,0.78,0.77)],
    "n" : [(0.116666666666667,0.26,0.91),(0.0305555555555556,0.81,0.83),(0.422222222222222,0.36,0.42),(0.319444444444444,0.21,0.72),(0.605555555555556,0.6,0.7),(0.666666666666667,0.2,0.83),(0.0583333333333333,0.65,0.59),(0.125,0.46,0.67),(0.138888888888889,0.87,0.92)],
    "o" : [(0.605555555555556,0.72,0.31),(0.586111111111111,0.89,0.61),(0.433333333333333,0.38,0.45),(0.219444444444444,0.34,0.62),(0.105555555555556,0.68,0.74),(0.025,0.8,0.5),(0.0305555555555556,0.59,0.76),(0.136111111111111,0.1,0.44),(0.0888888888888889,0.71,0.33)],
    "p" : [(0.497222222222222,0.16,0.02),(0.308333333333333,0.41,0.77),(0.527777777777778,0.15,0.94),(0.497222222222222,0.01,0.98),(0.622222222222222,0.14,0.91),(0.766666666666667,0.65,0.48),(0.669444444444444,0.61,0.43),(0.533333333333333,0.85,0.93),(0.605555555555556,0.3,0.37)],
    "q" : [(0.497222222222222,0.16,0.02),(0.108333333333333,0.09,0.47),(0.747222222222222,0.03,0.75),(0.630555555555556,0.01,0.95),(0.211111111111111,0.03,0.87),(0.111111111111111,0.08,0.76),(0.119444444444444,0.8,0.89),(0.111111111111111,0.75,0.73),(0.0722222222222222,0.76,0.49)],
    "r" : [(0.497222222222222,0.16,0.02),(0.755555555555556,0.6,0.38),(0.669444444444444,0.44,0.66),(0.908333333333333,0.09,0.97),(0.0333333333333333,0.76,0.52),(0.586111111111111,0.09,0.96),(0.630555555555556,0.32,0.44),(0.727777777777778,0.62,0.18),(0.105555555555556,0.12,0.99)],
    "s" : [(0.0638888888888889,33,87),(0,0,91),(0,0,11),(0.630555555555556,41,75),(0.272222222222222,35,100),(0.397222222222222,50,50)],
    "t" : [(0.0138888888888889,81,65),(0.980555555555556,62,32),(0.0833333333333333,20,65),(0.966666666666667,41,88),(0.0361111111111111,50,25),(0.111111111111111,14,8)],
    "u" : [(0.738888888888889,10,88),(0.558333333333333,23,54),(0.291666666666667,12,27),(0.238888888888889,23,39),(0.111111111111111,1,82),(0.35,32,12)],
    "v" : [(0.133333333333333,55,86),(0.075,39,64),(0.155555555555556,36,52),(0.108333333333333,66,70),(0.0722222222222222,8,84),(0.141666666666667,40,45)],
    "w" : [(0.0333333333333333,36,33),(0.0416666666666667,68,69),(0.0861111111111111,64,27),(0.0388888888888889,6,89),(0.594444444444445,87,80),(0.0611111111111111,34,60)],
    "x" : [(0.158333333333333,52,93),(0.0222222222222222,78,83),(0.516666666666667,20,75),(0.897222222222222,11,29),(0.0888888888888889,58,19),(0.119444444444444,3,87)]
}

haircols = [(0.66667,0.53333,0.40000), (0.87059,0.74510,0.60000), (0.14118,0.10980,0.06667), (0.30980,0.10196,0.00000), (0.60392,0.20000,0.00000) ]
#skincols = [(0.310, 0.102, 0.000), (0.21403, 0.129142,0.019756), (0.227,0.062,0.0000), (0.841,0.431,0.195) ]
skincols = [(0.310, 0.102, 0.000)]

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



def SetUpCharacterStyle():
    global availableColorStyleKeys, styleKey


    save_path = bpy.context.scene.my_tool.root_dir
    color_style_path = CheckAndFormatPath(save_path, "INPUT/GlobalStyles.json")
    globalStyleInfo = json.load(open(color_style_path))

    styleIndex = random.randrange(0, len( list(globalStyleInfo.keys()) ) )
    styleKey = list(globalStyleInfo.keys())[styleIndex]
    availableColorStyleKeys =  globalStyleInfo[styleKey]
    print(styleKey)
    print(availableColorStyleKeys)
    return styleKey

def CheckAndFormatPath(path, pathTojoin = ""):
    if pathTojoin != "" :
        path = os.path.join(path, pathTojoin)

    new_path = path.replace('\\', '/')

    if not os.path.exists(new_path):
        return ""
    return new_path

def PickOutfitColors(attribute, chidlrenObjs):
    global styleKey, availableColorStyleKeys
    global colorkey

    save_path = save_path = bpy.context.scene.my_tool.root_dir
    if(attribute == "17-UpperHead"):
        colIndex = random.randrange(0, len(haircols) ) 
        col = haircols[colIndex]

    colors = [(random.uniform(0,1.0), random.uniform(0,1.0), random.uniform(0,1.0), 1.0)] * 3
    color_list_path = CheckAndFormatPath(save_path, "INPUT/GlobalColorList.json")
    globalColorInfo = json.load(open(color_list_path))

    colorkeyindex = random.randrange(0, len(availableColorStyleKeys))
    colorkey = availableColorStyleKeys[colorkeyindex]
    colorChoice = globalColorInfo[colorkey]
    print(colorChoice)

    for child in chidlrenObjs:
        obj = bpy.data.objects[child.name]
        print("-------------------")
        print(child.name)
        print(obj.name)
        material_slots = obj.material_slots
        for m in material_slots:
            material = m.material
            for node in material.node_tree.nodes:
                if (node.label == "RTint"):
                    node.outputs["Color"].default_value = colorChoice["R"]
                if (node.label == "GTint"):
                    node.outputs["Color"].default_value = colorChoice["G"]
                if (node.label == "BTint"):
                    node.outputs["Color"].default_value = colorChoice["B"]
    return colorkey

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

def textureindex_has_been_updated(tool, last_tool):
    color_dict = {"001": "red", "002": "purple", "004": "green", "003": "grey", "007": "white"}
    # get index to point to color hierarchy keys
    # then get the name corresponding to it to fill
    texture_string = bpy.context.scene.my_tool[tool]
    texture_string = texture_string.upper()
    texture_string = ''.join([i for i in texture_string if not i.isdigit()])
    if not texture_string:
        bpy.context.scene.my_tool[tool] = bpy.context.scene.my_tool[last_tool]
        return
    texture_string = texture_string[:1]

    index = ord(texture_string) - 65 # 65 is A in ascii
    color_keys = list(color_dict.keys())
    if index >= len(color_keys):
        index = len(color_keys) - 1
        texture_string = bpy.context.scene.my_tool[last_tool]

    color_keys = sorted(color_keys)
    color_key = color_keys[index]

    bpy.context.scene.my_tool[tool] = texture_string
    bpy.context.scene.my_tool[last_tool] = texture_string
    return


def add_to_textureindex(amount):
    color_dict = {"001": "red", "002": "purple", "004": "green", "003": "grey", "007": "white"}
    max_sets = len(color_dict.keys())

    index = ord(bpy.context.scene.my_tool.textureSetIndex) - 65
    index += amount
    if index >= max_sets:
        index = 0
    elif index < 0:
        index = max_sets - 1

    texture = chr(index + 65)
    bpy.context.scene.my_tool.textureSetIndex = texture
    bpy.context.scene.my_tool.lastSetIndex = texture
    return index



def colourindex_has_been_updated(tool, last_tool):
    color_dict = {"001": "red", "002": "purple", "005": "green", "003": "grey"}
    color_keys = list(color_dict.keys())
    color_keys = sorted(color_keys)

    max_color = len(color_keys)
    string = bpy.context.scene.my_tool.get(tool)
    if string in color_keys:
    # index = ''.join([i for i in string if i.isdigit()])
        index = str(color_keys.index(string))
        if index:
            if int(index) >= max_color:
                index = str(max_color - 1)
            color_key = color_keys[int(index)]
            new_string_index = color_key
            # new_string_index = "{:03d}".format(int(index))
            if len(new_string_index) > 3:
                new_string_index = new_string_index[:3]
        else:
            new_string_index = color_key
            # new_string_index = "{:03d}".format(int(bpy.context.scene.my_tool[last_tool]))
        bpy.context.scene.my_tool[last_tool] = int(index)
        bpy.context.scene.my_tool[tool] = new_string_index
    bpy.context.scene.my_tool[tool] = color_keys[bpy.context.scene.my_tool[last_tool]]


def add_to_colourindex(amount):
    color_dict = {"001": "red", "002": "purple", "005": "green", "003": "grey"}
    color_keys = list(color_dict.keys())
    color_keys = sorted(color_keys)
    max_color = len(color_keys)

    index = bpy.context.scene.my_tool.colourStyleIndex
    index = color_keys.index(index)

    index += amount
    if index >= max_color:
        index = 0
    elif index < 0:
        index = max_color - 1
        
    color_key = color_keys[index]
    bpy.context.scene.my_tool.colourStyleIndex = color_key
    bpy.context.scene.my_tool.lastStyleIndex = index
    return index

def SaveNewColorStyle(ColorListName, R, G, B, root_dir):
    print(ColorListName)
    print(R)
    NewColorStyle = {}
    NewColorStyle["ComonName"] = ColorListName
    NewColorStyle["R"] = [R[0],R[1],R[2],R[3]]
    NewColorStyle["G"] = [G[0],G[1],G[2],G[3]]
    NewColorStyle["B"] = [B[0],B[1],B[2],B[3]]
    print(NewColorStyle)
    GlobalColorList = OpenColorList(root_dir)
    GlobalColorList[ColorListName] = NewColorStyle
    WriteToColorList(GlobalColorList, root_dir)


def DeleteColorList(ColorListName, root_dir):
    GlobalColorList = OpenColorList(root_dir)
    GlobalColorList.pop(ColorListName, None)
    WriteToColorList(GlobalColorList, root_dir)


def DoesColorListExist(ColorListName, root_dir):
    path = os.path.join(root_dir, "INPUT\GlobalColorList.json")
    GlobalColorList = json.load(open(path))
    if GlobalColorList.get(ColorListName) is not None:
        print("Exists")
        doesListExist = True
    else:
        print("Does not exist")
        doesListExist = False
    return doesListExist

def OpenColorList(root_dir):
    path = os.path.join(root_dir, "INPUT\GlobalColorList.json")
    GlobalColorList = json.load(open(path))
    return GlobalColorList

def WriteToColorList(GlobalColorList, root_dir):
    path = os.path.join(root_dir, "INPUT\GlobalColorList.json")
    try:
      ledger = json.dumps(GlobalColorList, indent=1, ensure_ascii=True)
      print(ledger)
      with open(path, 'w') as outfile:
         outfile.write(ledger + '\n')
    except:
      print("ColorStyle was not sent")

def ColorHasbeenUpdated(ColorTint):
    print(inputColorListSceneObject)
    inputColorListSceneObject = bpy.context.scene.my_tool.inputColorListSceneObject
    Rtint = bpy.context.scene.my_tool.RTint
    if inputColorListSceneObject is not None:
        for mat in inputColorListSceneObject.material_slots:
            print("Material")
    return None