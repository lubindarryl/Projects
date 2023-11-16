from PIL import Image, ImageFilter
im = Image.open(r"/workspace/Experiments/Pictures/ocean5.png")

img = im.convert("L")
img.save("greyScale.png")

imEdges = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
imEdges = img.filter(ImageFilter.FIND_EDGES)

imEdges.save("edgeGrayScale.png")