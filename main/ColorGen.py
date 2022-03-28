import bpy
import random
from mathutils import Color

def MonocromaticColor(col, numberCols):

    numColors = 3 #how many colors we want our scheme to have
    colors = [None] * numColors #the final color palette array

    #get our hue first, outside of the loop,
    #so all the colors we make will have the same hue
    h = random.random()
    print(h)

    for i in range(0, numColors):
        #all these colors are going to have the same saturation,
        #though you could experiment with changing this as well
        s = 1
        #the value is going to go from 0 to 1 in steps
        #so that the last color will have 1 value, and the first color will be black.
        #you could instead multiply this by i + 1,
        #so that the darkest color will be a dark shade of your hue rather than black.
        v = (1/numColors) * (i + 0.5)
        c = Color()
        c.hsv = (h, s, v)
        colors[i] = c.r, c.g, c.b
        
        print(colors[i])
    return colors

def AnalagousColor():
    colors = [None] * 3
    span = 0.125 # how wide a section of the color wheel we want to span

    h1 = random.random() # pick a random hue
    h2 = (h1 + (span/2)) % 1 #go along the color wheel for half of the span
    h3 = (h1 - (span/2)) #go the opposite direction for half of the span

    #we can't use the modulo operator for negative numbers
    #because its behavior is poorly defined, so we have to check manually
    if (h3 < 0):
        #"abs" means "absolute value", the total distance of a number
        #from zero (so abs(-3) == abs(3) == 3, for instance)
        h3 =  1 - (abs(h3) % 1)
    
    c0 = Color()
    c0.hsv = (h1, 1, 1)
    colors[0] = (c0.r, c0.g, c0.b)
    
    c1 = Color()
    c1.hsv = (h2, 1, 1)
    colors[1] = (c1.r, c1.g, c1.b)
    
    c2 = Color()
    c2.hsv = (h3, 1, 1)
    colors[2] = (c2.r, c2.g, c2.b)
    
    return colors


def TriadicColor():
    #triadic color scheme, four would be a tetradic square color scheme,
    #five would be a pentadic, etc
    numColors = 3

    colors = [None] * numColors
    size = 1/numColors

    #get an offset so we don't get the same color scheme every time.
    #starting from a random h like we did before gives weird issues
    #where you get multiple of the same color
    offset = random.random()

    for i in range(0, numColors):
        h = i * size
        #add the offset to the hue value then make sure it wraps around
        c = Color()
        c.hsv = ( (h + offset) % 1, 1, 1)
        colors[i] = (c.r, c.g, c.b)
    return colors

def SplitComplmentaryColor():
    colors = [None] * 3
    split = 0.125

    h1 = random.random()
    h2 = (((h1 + 0.5) % 1) + split) % 1
    h3 = ((h1 + 0.5) % 1) - split

    if (h3 < 0):
        h3 = 1 - (abs(h3) % 1)

    c0 = Color()
    c0.hsv = (h1, 1, 1)
    colors[0] = (c0.r, c0.g, c0.b)
    
    c1 = Color()
    c1.hsv = (h2, 1, 1)
    colors[1] = (c1.r, c1.g, c1.b)
    
    c2 = Color()
    c2.hsv = (h3, 1, 1)
    colors[2] = (c2.r, c2.g, c2.b)
    return colors