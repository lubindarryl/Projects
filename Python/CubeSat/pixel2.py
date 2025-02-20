# Importing Image from PIL package
from PIL import Image
 
# creating a image object
im = Image.open(r"/workspace/Experiments/Pictures/leave.jpg")
px = im.load()

# Max = 300
xBound = 300

#Max = 224
yBound = 224

img = Image.new('RGB', (xBound, yBound))

color = [255, 0, 0]
colorname = "Red"

threashold = 125
needColor = True

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



def inBounds(rVal, gVal, bVal, threashold, color, colorMax):
    rLBound = color[0]-threashold
    rUBound = color[0]+threashold
    gLBound = color[1]-threashold
    gUBound = color[1]+threashold
    bLBound = color[2]-threashold
    bUBound = color[2]+threashold
    pxGreatString = returnGreatString(rVal, gVal, bVal)
    pxGreat = returnGreat(rVal, gVal, bVal)
    pxLow = returnLow(rVal, gVal, bVal)
    if (rLBound <= rVal <= rUBound) and (gLBound <= gVal <= gUBound) and (bLBound <= bVal <= bUBound): 
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
            if inBounds(r, g, b, threashold, color, colorMax):
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