import webcolors

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

def returnAvg(a, b, c=False, d=False, e=False, f=False):
    if a != False and b != False and c != False and d != False and e != False and f != False:
        return (a + b + c + d + e + f)/6
    elif a != False and b != False and c != False and d != False and e != False:
        return (a + b + c + d + e)/5
    elif a != False and b != False and c != False and d != False:
        return (a + b + c + d)/4
    elif a != False and b != False and c != False:
        return (a + b + c)/3
    elif a != False and b != False:
        return (a + b)/2

def returnGreat(a, b, c):
    if a == b == c:
        return a
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

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def rgb2name(rgb):
    try:
        named_color = webcolors.rgb_to_name(rgb, spec='css3')
    except ValueError:
        named_color = closest_colour(rgb)
    return named_color

def inColBounds(pxCol, colName):
    # Finds shades of blue for water
    if colName == "plastic":
        if pxCol == "blue":
            return False
        elif pxCol == "mediumblue":
            return False
        elif pxCol == "navy":
            return False
        elif pxCol == "midnightblue":
            return False
        elif pxCol == "dodgerblue":
            return False
        elif pxCol == "steelblue":
            return False
        elif pxCol == "darkslategray":
            return False
        elif pxCol == "darkslateblue":
            return False
        elif pxCol == "teal":
            return False
        elif pxCol == "aqua":
            return False
        elif pxCol == "aquamarine":
            return False
        elif pxCol == "paleturquosie":
            return False
        elif pxCol == "powderblue":
            return False
        elif pxCol == "yellow":
            return False
        elif pxCol == "turquoise":
            return False
        elif pxCol == "skyblue":
            return False
        elif pxCol == "mediumtorquoise":
            return False
        elif pxCol == "mediumaquamarine":
            return False
        elif pxCol == "lightgoldenrodyellow":
            return False
        elif pxCol == "lemonchiffon":
            return False
        elif pxCol == "khaki":
            return False
        elif pxCol == "gold":
            return False
        elif pxCol == "deepskyblue":
            return False
        elif pxCol == "darkturquosie":
            return False
        elif pxCol == "paleturquosie":
            return False
        else:
            return True
    # Finds red pixels in an image
    elif colName == "red":
        if pxCol == "brown":
            return True
        elif pxCol == "indianred":
            return True
        elif pxCol == "indiancoral":
            return True
        elif pxCol == "crimson":
            return True
        elif pxCol == "lightcoral":
            return True
        elif pxCol == "darkred":
            return True
        elif pxCol == "orangered":
            return True
        elif pxCol == "darkpink":
            return True
        elif pxCol == "firebrick":
            return True
        elif pxCol == "deeppink":
            return True
        elif pxCol == "red":
            return True
        elif pxCol == "maroon":
            return True
        elif pxCol == "tomatoe":
            return True
        else:
            return False
    # Finds yellow pixels in an image
    elif colName == "yellow":
        if pxCol == "yellow":
            return True
        elif pxCol == "olive":
            return True
        elif pxCol == "gold":
            return True
        elif pxCol == "goldenrod":
            return True
        elif pxCol == "khaki":
            return True
        elif pxCol == "lemonchiffon":
            return True
        elif pxCol == "lightgoldenrodyellow":
            return True
        elif pxCol == "lightyellow":
            return True
        elif pxCol == "palegoldenrod":
            return True
        elif pxCol == "darkkhaki":
            return True
        else:
            return False
    # Finds green pixels in an image
    elif colName == "green":
        if pxCol == "green":
            return True
        elif pxCol == "lime":
            return True
        elif pxCol == "chartreuse":
            return True
        elif pxCol == "darkgreen":
            return True
        elif pxCol == "darkolivegreen":
            return True
        elif pxCol == "darkseagreen":
            return True
        elif pxCol == "forestgreen":
            return True
        elif pxCol == "greenyellow":
            return True
        elif pxCol == "lawngreen":
            return True
        elif pxCol == "lightgreen":
            return True
        elif pxCol == "limegreen":
            return True
        elif pxCol == "mediumseagreen":
            return True
        elif pxCol == "mediumspringgreen":
            return True
        elif pxCol == "olivedrab":
            return True
        elif pxCol == "palegreen":
            return True
        elif pxCol == "seagreen":
            return True
        elif pxCol == "springgreen":
            return True
        elif pxCol == "yellowgreen":
            return True
        else:
            return False
    # Finds blue pixels in an image
    elif colName == "blue":
        if pxCol == "blue":
            return True
        elif pxCol == "navy":
            return True
        elif pxCol == "teal":
            return True
        elif pxCol == "aqua":
            return True
        elif pxCol == "aliceblue":
            return True
        elif pxCol == "aquamarine":
            return True
        elif pxCol == "aquamarine":
            return True
        elif pxCol == "azure":
            return True
        elif pxCol == "cadetblue":
            return True
        elif pxCol == "cornflowerblue":
            return True
        elif pxCol == "cyan":
            return True
        elif pxCol == "darkblue":
            return True
        elif pxCol == "darkcyan":
            return True
        elif pxCol == "darktorquoise":
            return True
        elif pxCol == "deepskyblue":
            return True
        elif pxCol == "dodgerblue":
            return True
        elif pxCol == "lightblue":
            return True
        elif pxCol == "lightcyan":
            return True
        elif pxCol == "lightskyblue":
            return True
        elif pxCol == "mediumblue":
            return True
        elif pxCol == "mediumtorquoise":
            return True
        elif pxCol == "midnightblue":
            return True
        elif pxCol == "paletorquoise":
            return True
        elif pxCol == "powderblue":
            return True
        elif pxCol == "skyblue":
            return True
        elif pxCol == "slateblue":
            return True
        elif pxCol == "steelblue":
            return True
        elif pxCol == "turquoise":
            return True
        else:
            return False
    elif colName == "bluegreen":
        if pxCol == "green":
            return True
        elif pxCol == "lime":
            return True
        elif pxCol == "chartreuse":
            return True
        elif pxCol == "darkgreen":
            return True
        elif pxCol == "darkolivegreen":
            return True
        elif pxCol == "darkseagreen":
            return True
        elif pxCol == "forestgreen":
            return True
        elif pxCol == "greenyellow":
            return True
        elif pxCol == "lawngreen":
            return True
        elif pxCol == "lightgreen":
            return True
        elif pxCol == "limegreen":
            return True
        elif pxCol == "mediumseagreen":
            return True
        elif pxCol == "mediumspringgreen":
            return True
        elif pxCol == "olivedrab":
            return True
        elif pxCol == "palegreen":
            return True
        elif pxCol == "seagreen":
            return True
        elif pxCol == "springgreen":
            return True
        elif pxCol == "yellowgreen":
            return True
        if pxCol == "blue":
            return True
        elif pxCol == "navy":
            return True
        elif pxCol == "teal":
            return True
        elif pxCol == "aqua":
            return True
        elif pxCol == "aliceblue":
            return True
        elif pxCol == "aquamarine":
            return True
        elif pxCol == "aquamarine":
            return True
        elif pxCol == "azure":
            return True
        elif pxCol == "cadetblue":
            return True
        elif pxCol == "cornflowerblue":
            return True
        elif pxCol == "cyan":
            return True
        elif pxCol == "darkblue":
            return True
        elif pxCol == "darkcyan":
            return True
        elif pxCol == "darktorquoise":
            return True
        elif pxCol == "deepskyblue":
            return True
        elif pxCol == "dodgerblue":
            return True
        elif pxCol == "lightblue":
            return True
        elif pxCol == "lightcyan":
            return True
        elif pxCol == "lightskyblue":
            return True
        elif pxCol == "mediumblue":
            return True
        elif pxCol == "mediumtorquoise":
            return True
        elif pxCol == "midnightblue":
            return True
        elif pxCol == "paletorquoise":
            return True
        elif pxCol == "powderblue":
            return True
        elif pxCol == "skyblue":
            return True
        elif pxCol == "slateblue":
            return True
        elif pxCol == "steelblue":
            return True
        elif pxCol == "turquoise":
            return True
    else:
        return True