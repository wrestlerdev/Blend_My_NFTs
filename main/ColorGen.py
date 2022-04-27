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
letterstyles = 'abcdefghijkl'
cols = {
    "a" : [(0.0194444444444444,0.22,0.96),(0.569444444444444,0.16,0.96),(0.633333333333333,0.7,0.34),(0,0,0.68),(0.611111111111111,0.38,0.03),(0.991666666666667,0.85,0.85),(0.111111111111111,0.13,0.99)],
    "b" : [(0.997222222222222,0.68,0.82),(0.569444444444444,0.16,0.96),(0.633333333333333,0.7,0.34),(0,0,0.68),(0.611111111111111,0.43,0.03),(0.0194444444444444,0.27,0.98),(0.111111111111111,0.13,0.98)],
    "c" : [(0.0388888888888889,0.83,0.95),(0.402777777777778,0.81,0.35),(0.569444444444444,0.16,0.96),(0.633333333333333,0.7,0.34),(0.611111111111111,0.43,0.03),(0.111111111111111,0.13,0.99),(0.0277777777777778,0.44,0.31)],
    "d" : [(0.119444444444444,0.1,0.96),(0.633333333333333,0.7,0.34),(0.933333333333333,0.56,0.38),(0.0222222222222222,0.45,0.31),(0.611111111111111,0.38,0.03),(0.136111111111111,0.81,0.99),(0.0388888888888889,0.83,0.95)],
    "e" : [(0.130555555555556,0.69,0.98),(0.402777777777778,0.81,0.35),(0.633333333333333,0.7,0.34),(0,0,1),(0.611111111111111,0.38,0.03),(0.111111111111111,0.13,0.99)],
    "f" : [(0.433333333333333,0.99,0.47),(0.0388888888888889,0.83,0.95),(0.933333333333333,0.56,0.38),(0,0,1),(0.611111111111111,0.38,0.03),(0.136111111111111,0.81,0.99),(0.569444444444444,0.16,0.96)],
    "g" : [(0.563888888888889,0.15,0.93),(0.0194444444444444,0.27,0.98),(0.991666666666667,0.85,0.85),(0.0388888888888889,0.83,0.95),(0.611111111111111,0.38,0.03),(0.633333333333333,0.7,0.34),(0.933333333333333,0.56,0.38)],
    "h" : [(0.580555555555556,0.76,0.45),(0.0194444444444444,0.27,0.98),(0.991666666666667,0.85,0.85),(0.136111111111111,0.81,0.99),(0,0,0.68),(0,0,1),(0.611111111111111,0.38,0.03),(0.569444444444444,0.16,0.96),(0.933333333333333,0.56,0.38)],
    "i" : [(0.925,0.39,0.45),(0.0388888888888889,0.83,0.95),(0,0,0.68),(0.433333333333333,0.99,0.47),(0,0,1),(0.611111111111111,0.38,0.03),(0.569444444444444,0.16,0.96),(0.633333333333333,0.7,0.34)],
    "j" : [(0.025,0.28,0.39),(0.111111111111111,0.13,0.99),(0,0,1),(0.611111111111111,0.38,0.03),(0.0388888888888889,0.83,0.95)],
    "k" : [(0.588888888888889,0.08,0.74),(0.0194444444444444,0.27,0.98),(0.991666666666667,0.85,0.85),(0.633333333333333,0.7,0.34),(0.933333333333333,0.56,0.38),(0.611111111111111,0.38,0.03)],
    "l" : [(0,0,1), (0,0,1), (0.611111111111111,0.38,0.03), (0.611111111111111,0.38,0.03)],
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
        
        print(i)
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
    colors[0] = (c0.r, c0.g, c0.b)
    
    c1 = Color()
    c1.hsv = (h2, random.uniform(0.5, 1), col[2] + random.uniform(-0.1, 0.1))
    colors[1] = (c1.r, c1.g, c1.b)
    
    c2 = Color()
    c2.hsv = (h3, random.uniform(0.9, 1), col[2]  + random.uniform(-0.1, 0.1))
    colors[2] = (c2.r, c2.g, c2.b)
    
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
        c.hsv = ( (h + offset) % 1, 1, 1)
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
    colors[0] = (c0.r, c0.g, c0.b)
    
    c1 = Color()
    c1.hsv = (h2, col[1], 1)
    colors[1] = (c1.r, c1.g, c1.b)
    
    c2 = Color()
    c2.hsv = (h3, col[1], 1)
    colors[2] = (c2.r, c2.g, c2.b)
    return colors

style = []
styleChoice = ""

maincolor = (0.0, 0.0, 0.0)
secondarycolor = (0.0, 0.0, 0.0)

mainColorIndex = -1
SecondaryColorIndex = -1


def SetUpCharacterStyle(Character):
    global style, styleChoice
    global maincolor, secondarycolor
    global mainColorIndex, SecondaryColorIndex

    styleChoice = random.choice(letterstyles)    
    style = copy.deepcopy( cols[random.choice(styleChoice)] )



    if( random.random() > .05 ):
        mainColorIndex = 0
        #maincolor = style.pop(mainColorIndex)
        maincolor = style[mainColorIndex]
        SecondaryColorIndex = random.randrange(0, len(style))
        #secondarycolor = style.pop(SecondaryColorIndex)
        secondarycolor = style[SecondaryColorIndex]
    else:
        SecondaryColorIndex = 0
        #secondarycolor = style.pop(SecondaryColorIndex)
        secondarycolor = style[SecondaryColorIndex]
        mainColorIndex = random.randrange(0, len(style))
        #maincolor = style.pop(mainColorIndex)
        maincolor = style[mainColorIndex]

    for child in bpy.data.collections.get(Character).objects:
        obj = bpy.data.objects[child.name]
        obj["TestColor"] = skincols[random.randrange(len(skincols))]
        obj["metallic"] = random.random()
        obj.hide_viewport = False
        obj.hide_render = False

def PickOutfitColors(attribute, chidlrenObjs):
    global style, styleChoice
    global maincolor, secondarycolor
    global mainColorIndex, SecondaryColorIndex
    
    col = (0.0, 0.0, 0.0)
    colIndex = -1
    if(attribute == "01-UpperTorso"):
        col =  maincolor
        colIndex = mainColorIndex
    elif(attribute == "08-PelvisThick" or attribute == "08-PelvisThick"):
        col = secondarycolor
        colIndex = SecondaryColorIndex
    elif(attribute == "17-UpperHead"):
        colIndex = random.randrange(0, len(haircols) ) 
        col = haircols[colIndex]
    else:
        colIndex = random.randrange(0, len(style) ) 
        col = style[colIndex]
        #col = (random.random(), random.random(), random.random())
    
    for child in chidlrenObjs:
        obj = bpy.data.objects[child.name]

        c = Color()
        c.hsv = col[0], col[1], col[2]
        obj["TestColor"] = (c.r, c.g, c.b)
        #colors = MonocromaticColor(col, random.uniform(0,1))
        colors = AnalagousColor(col, random.uniform(0.075,0.35))
        #colors = SplitComplmentaryColor(col, random.uniform(0.1,0.3) )
        obj["R"] = colors[0]
        obj["G"] = colors[1]
        obj["B"] = colors[2]
        obj.hide_viewport = False
        obj.hide_render = False

        material_slots = obj.material_slots
        for m in material_slots:
            #material = m.material
            material = bpy.data.materials['Master']
            material.use_nodes = True
            matcopy = material.copy()
            m.material = matcopy
            #m.material = bpy.data.materials['Test_02']
            # get the nodes
            
            for node in material.node_tree.nodes:
                if (node.label == "RTint"):
                    node.color = colors[0]



        hexCodes = [None] * 3
        hexCodes[0] = RGBtoHex((colors[0]))
        hexCodes[1] = RGBtoHex((colors[1]))
        hexCodes[2] = RGBtoHex((colors[2]))


    # c = Color()
    # c.hsv = col[0], col[1], col[2]
    # #colors = MonocromaticColor(col, random.uniform(0,1))
    # colors = AnalagousColor(col, random.uniform(0.075,0.35))
    # #colors = SplitComplmentaryColor(col, random.uniform(0.1,0.3) )
    # print("------------------")
    # newImage = bpy.data.images.load(file, check_existing=True)
    # for child in chidlrenObjs:
    #     print(child)
    #     obj = bpy.data.objects[child.name]

    #     obj["TestColor"] = (c.r, c.g, c.b)

    #     obj["R"] = colors[0]
    #     obj["G"] = colors[1]
    #     obj["B"] = colors[2]
    #     obj.hide_viewport = False
    #     obj.hide_render = False
        

    #     material_slots = obj.material_slots
    #     for m in material_slots:
    #         #material = m.material
    #         material = bpy.data.materials['Master']
    #         material.use_nodes = True
    #         matcopy = material.copy()
    #         m.material = matcopy
    #         #m.material = bpy.data.materials['Test_02']
    #         # get the nodes
    #         print(m)
    #         # print(c)
    #         for node in material.node_tree.nodes:
    #             print(c)
    #             if (node.label == "Diffuse"):
    #                 node.image = newImage
    #             elif node.label == "RTint":
    #                 node.outputs["Value"].default_value = c.r
    #             elif node.label == "GTint":
    #                 node.outputs["Value"].default_value = c.g
    #             elif node.label == "BTint":
    #                 node.outputs["Value"].default_value = c.b


    # hexCodes = [None] * 3
    # hexCodes[0] = RGBtoHex((colors[0]))
    # hexCodes[1] = RGBtoHex((colors[1]))
    # hexCodes[2] = RGBtoHex((colors[2]))






    
    # for block in bpy.data.materials:
    #     if block.users == 0:
    #         bpy.data.materials.remove(block)

    # for block in bpy.data.textures:
    #     if block.users == 0:
    #         bpy.data.textures.remove(block)

    # for block in bpy.data.images:
    #     if block.users == 0:
    #         bpy.data.images.remove(block)
    return hexCodes

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
