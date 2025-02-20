# Importing Image from PIL package
from PIL import Image
 
# creating a image object
im = Image.open(r"/workspace/Experiments/Pictures/leave.jpg")
px = im.load()

xBound = 300
yBound = 224

img = Image.new('RGB', (xBound, yBound))

color = [255, 255, 255]
colorname = "white"

threashold = 200
findColor = True

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

for x in range(xBound):
    for y in range(yBound):
        c = 0
        findColor = True
        while findColor:
            if px[x, y] == (findDif(color[0], c), findDif(color[1], c), findDif(color[2], c)):
                r = findDif(color[0], c)
                g = findDif(color[1], c)
                b = findDif(color[2], c)
                findColor = False
                print("Found", colorname, "color at coords:", x, ",", y)
                img.putpixel((x, y), (r, g, b))
            elif px[x, y] == (findDif(color[0], c), findDif(color[1], c), findSum(color[2], c)):
                r = findDif(color[0], c)
                g = findDif(color[1], c)
                b = findSum(color[2], c)
                findColor = False
                print("Found", colorname, "color at coords:", x, ",", y)
                img.putpixel((x, y), (r, g, b))
            elif px[x, y] == (findDif(color[0], c), findSum(color[1], c), findDif(color[2], c)):
                r = findDif(color[0], c)
                g = findSum(color[1], c)
                b = findDif(color[2], c)
                findColor = False
                print("Found", colorname, "color at coords:", x, ",", y)
                img.putpixel((x, y), (r, g, b))
            elif px[x, y] == (findDif(color[0], c), findSum(color[1], c), findSum(color[2], c)):
                r = findDif(color[0], c)
                g = findSum(color[1], c)
                b = findSum(color[2], c)
                findColor = False
                print("Found", colorname, "color at coords:", x, ",", y)
                img.putpixel((x, y), (r, g, b))
            elif px[x, y] == (findSum(color[0], c), findDif(color[1], c), findDif(color[2], c)):
                r = findSum(color[0], c)
                g = findDif(color[1], c)
                b = findDif(color[2], c)
                findColor = False
                print("Found", colorname, "color at coords:", x, ",", y)
                img.putpixel((x, y), (r, g, b))
            elif px[x, y] == (findSum(color[0], c), findDif(color[1], c), findSum(color[2], c)):
                r = findSum(color[0], c)
                g = findDif(color[1], c)
                b = findSum(color[2], c)
                findColor = False
                print("Found", colorname, "color at coords:", x, ",", y)
                img.putpixel((x, y), (r, g, b))
            elif px[x, y] == (findSum(color[0], c), findSum(color[1], c), findDif(color[2], c)):
                r = findSum(color[0], c)
                g = findSum(color[1], c)
                b = findDif(color[2], c)
                findColor = False
                print("Found", colorname, "color at coords:", x, ",", y)
                img.putpixel((x, y), (r, g, b))
            elif px[x, y] == (findSum(color[0], c), findSum(color[1], c), findSum(color[2], c)):
                r = findSum(color[0], c)
                g = findSum(color[1], c)
                b = findSum(color[2], c)
                findColor = False
                print("Found", colorname, "color at coords:", x, ",", y)
                img.putpixel((x, y), (r, g, b))
            else:
                r = px[x, y][0]
                g = px[x, y][1]
                b = px[x, y][2]
                contrast = 50
                f = (returnGreat(r, g, b)-contrast)
                img.putpixel((x, y), (f, f, f))
            if c == threashold:
                break
            c += 1
img.save("newImg.jpg")
print("Image Saved!")