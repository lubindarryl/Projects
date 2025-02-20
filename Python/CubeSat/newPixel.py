from PIL import Image, ImageFilter
im = Image.open(r"C:\Users\trued\Documents\Python\Experiments\Pictures\capture0.JPG")

def coordBound(img):
    xBound, yBound = img.size
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    percents = []
    px = img.load()
    total = 0
    white = 0

    # Finding x-coord
    for x in range(xBound):
        total = 0
        white = 0
        for y in range(yBound):
            if px[x, y] > 0:
                white += 1
            total += 1
        # Calculates percent of white pixels from edge detected image per x line
        if (white/total) != 1.0:
            percents.append(white/total)
    goodPercents = []
    for i, x in enumerate(percents):
        if x >= 0.006:
            goodPercents.append(i)
    x1 = goodPercents[0]
    x2 = goodPercents[goodPercents.__len__()-1]
    
    # Finding y-coord
    percents = []
    goodPercents = []
    for y in range(yBound):
        total = 0
        white = 0
        for x in range(xBound):
            if px[x, y] > 0:
                white += 1
            total += 1
        # Calculates percent of white pixels from edge detected image per y line
        if (white/total) != 1.0:
            percents.append(white/total)
    goodPercents = []
    for i, x in enumerate(percents):
        if x >= 0.006:
            goodPercents.append(i)
    y1 = goodPercents[0]
    y2 = goodPercents[goodPercents.__len__()-1]
    return ((x1, y1), (x2, y2))

def zoom(im):
    imGrey = im.convert("L")
    imGrey.save("greyScale.png")
    imEdges = imGrey.filter(ImageFilter.FIND_EDGES)
    px = imEdges.load()
    xBound, yBound = imGrey.size

    coords = []

    img = Image.new("L", (xBound, yBound))
    for x in range(xBound):
        for y in range(yBound):
            if px[x, y] >= 25:
                coords.append((x, y))
                img.putpixel((x, y), px[x, y])

    x1, y1 = coordBound(img)[0]
    x2, y2 = coordBound(img)[1]
    newXBound = x2 - x1
    newYBound = y2 - y1
    newImg = Image.new("RGB", (x2 - x1, y2 - y1))
    px = im.load()
    for ix, x in enumerate(range(x1, x2)):
        for iy, y in enumerate(range(y1, y2)):
            newImg.putpixel((ix, iy), px[x, y])
    return newImg

newImg = zoom(im)
newImg.save("result.png")