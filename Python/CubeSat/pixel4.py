# Importing Image from PIL package
from PIL import Image
from functions import returnAvg, returnGreat, returnGreatString, returnLow, findSum, findDif, difGreat, determineMax
# creating a image object
im = Image.open(r"/workspace/Experiments/Pictures/oceanPlastic.jpg")
px = im.load()

# Max = 300
xBound = 1920

#Max = 224
yBound = 1324

img = Image.new('RGB', (xBound, yBound))

color = [0, 0, 150]
colorname = "Blue"
rC = color[0]
gC = color[1]
bC = color[2]
colorAvg = (rC + gC + bC)/3
threasholdNum = returnGreat(rC, gC, bC)*colorAvg/(rC + gC + bC)
threasholdDif = returnGreat(rC, gC, bC)/2 + (rC + gC + bC)/3
needColor = True

"""
def findSum(num, bound):
    if num == 255:
        return 255
    else:
        return num + bound

def findDif(num, bound):
    if num == 0:
        return 0
    else:
        return num - bound

def returnGreat(a, b, c):
    if a >= b:
        if a >= c:
            return a
    if b >= c:
        if b >= a:
            return b
    if c >= a: 
        if c >= b:
            return c

def returnLow(a, b, c):
    if a <= b:
        if a <= c:
            return a
    if b <= c:
        if b <= a:
            return b
    if c <= a: 
        if c <= b:
            return c

def returnGreatString(a, b, c):
    if a == b == c:
        return "all"
    if a >= b:
        if a >= c:
            return 'r'
    if b >= c:
        if b >= a:
            return 'g'
    if c >= a: 
        if c >= b:
            return 'b'

def difGreat(great, low, threashDif):
    if (great - low) <= threashDif:
        return True
    else:
        return False

def determineMax(inputVal, inputCol):
    r = "r"
    g = "g"
    b = "b"
    both = "all"
    if inputVal == inputCol:
        return True
    elif inputCol == "all":
        return True
    else:
        return False
"""


def inBounds(rVal, gVal, bVal, threasholdDif, threasholdNum, color):
    # Difference Variables
    rgDif = (rVal - gVal)/2
    gbDif = (gVal - bVal)/2
    rbDif = (rVal - bVal)/2
    rgDifColor = (color[0] - color[1])
    gbDifColor = (color[1] - color[2])
    rbDifColor = (color[0] - color[2])
    rgLBound = rgDifColor - threasholdDif
    rgUBound = rgDifColor + threasholdDif
    gbLBound = gbDifColor - threasholdDif
    gbUBound = gbDifColor + threasholdDif
    rbLBound = rbDifColor - threasholdDif
    rbUBound = rbDifColor + threasholdDif

    # Number Range Variables
    rLBound = color[0]-threasholdNum
    rUBound = color[0]+threasholdNum
    gLBound = color[1]-threasholdNum
    gUBound = color[1]+threasholdNum
    bLBound = color[2]-threasholdNum
    bUBound = color[2]+threasholdNum
    
    if (rLBound <= rVal <= rUBound) and (gLBound <= gVal <= gUBound) and (bLBound <= bVal <= bUBound) and (rgLBound <= rgDif <= rgUBound) and (gbLBound <= gbDif <= gbUBound) and (rbLBound <= rbDif <= rbUBound): 
        return True
    else:
        return False

colorMax = returnGreatString(color[0], color[1], color[2])
colorMaxVal = returnGreat(color[0], color[1], color[2])
colorMinVal = returnLow(color[0], color[1], color[2])
colorMaxMinDif = difGreat(colorMaxVal, colorMinVal, colorMaxVal - colorMinVal)

for x in range(xBound):
    for y in range(yBound):
        needColor = True
        while needColor:
            r = px[x,y][0]
            g = px[x,y][1]
            b = px[x,y][2]
            if not inBounds(r, g, b, threasholdDif, threasholdNum, color):
                needColor = False
                print("Found", colorname, "color at coords:", x, ",", y)
                img.putpixel((x, y), (r, g, b))
            else:
                contrast = 50
                f = (returnGreat(r, g, b)-contrast)
                img.putpixel((x, y), (f, f, f))
                needColor = False
img.save("newImg.jpg")
print("Image Saved!")