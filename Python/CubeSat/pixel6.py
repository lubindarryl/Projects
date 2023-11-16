# Importing Image from PIL package
from PIL import Image
from functions import returnAvg, returnGreat, returnGreatString, returnLow, findSum, findDif, difGreat, determineMax
import time
import math
# creating a image object
im = Image.open(r"/workspace/Experiments/Pictures/oceanPlastic.jpg")
px = im.load()

# Max and Min for Pixels in Image
xBound, yBound = im.size

img = Image.new('RGB', (xBound, yBound))

color = [0, 0, 255]
colorname = "Blue"
rC = color[0]
gC = color[1]
bC = color[2]
threshold = 200
needColor = True

def inBounds(rVal, gVal, bVal, threshold, color):
    rMean = (rVal + color[0])/2
    inRoot = (2 + rMean/256) * pow(rVal - color[0], 2) + 4 * pow(gVal - color[1], 2) + (2 + (255 - rMean)/256) * (bVal - color[2])
    try:
        dif = math.sqrt(inRoot)
    except ValueError:
        return False
    if dif <= threshold:
        return False
    else:
        return True

for x in range(xBound):
    for y in range(yBound):
        needColor = True
        r = px[x,y][0]
        g = px[x,y][1]
        b = px[x,y][2]
        if inBounds(r, g, b, threshold, color):
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