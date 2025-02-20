# Importing Image from PIL package
from PIL import Image
from functions import returnAvg, returnGreat, returnGreatString, returnLow, findSum, findDif, difGreat, determineMax
# creating a image object
im = Image.open(r"/workspace/Experiments/Pictures/redSample2.png")
px = im.load()

# Max and Min for Pixels in Image
xBound, yBound = im.size

img = Image.new('RGB', (xBound, yBound))

color = [250, 0, 0]
colorname = "Red"
rC = color[0]
gC = color[1]
bC = color[2]
colorAvg = (rC + gC + bC)/3
threasholdNum = 255
threasholdDif = returnGreat(rC, gC, bC)/2 + (rC + gC + bC)/3
needColor = True

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