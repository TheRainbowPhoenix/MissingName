# USAGE
#
# Convert :
# python build.py t.png
#
# Rescale :
# python build.py c.png 128 78
#
# View :
# cat t.png.txt
# cat c.png.txt

import os, sys, subprocess
from PIL import Image

# t_width = int(subprocess.check_output(['tput', 'cols']))
# t_height = int(subprocess.check_output(['tput', 'lines']))

# DEFINES

OPACITY_TOLERANCE = 128

# CODE

def _make(im, width, height):
    out = ""

    mx, my = im.size
    if height >= my:
        heigt = my-1
    if width >= mx:
        width = mx-1
    for y in range(1, my, 2):
        for x in range(0, mx):
            skip = 0

            layers = im.getpixel((x, y-1))
            #print(layers)
            if len(layers)==4:
                r,g,b,a = layers
            else:
                r,g,b = layers
                a = 255

            #r, g, b, a = im.getpixel((x, y - 1))
            if a <= OPACITY_TOLERANCE:
                skip += 1
                background = "\033[49m"
            else:
                background = "\033[48;2;" + str(r) + ";" + str(g) + ";" + str(b) + "m"

            layers = im.getpixel((x, y))
            if len(layers)==4:
                r, g, b, a = layers
            else:
                r,g,b = layers
                a = 255

            if a <= OPACITY_TOLERANCE:
                skip += 1
                foreground = "\033[39m"
            else:
                foreground = "\033[38;2;" + str(r) + ";" + str(g) + ";" + str(b) + "m"

            if skip < 2:
                out += "{}{}▄".format(background, foreground)
            else:
                out += "{}{} ".format(background, foreground)

        out += '\n'
    out += "\033[m"
    return out

def _open(infile):
    im = Image.open(infile)
    if infile.lower().endswith(".gif"):
        im = im.convert('RGBA')
    
    return im


def makeS(infile, sz):
    im =_open(infile)
    width, height = im.size
    
    sc = sz / max(width, height)
    t_width = int(width * sc)
    t_height = int(height * sc)
    im.thumbnail([t_width, t_height])
    width = t_width
    height = t_height

    return _make(im, width, height)
   

def makeXY(infile, x, y):
    im=_open(infile)
    width, height = im.size
    
    t_width = min(width, int(x))
    t_height = min(height, int(y))
    im.thumbnail([t_width, t_height], Image.ANTIALIAS)
    width = t_width
    height = t_height

    return _make(im, width, height)

def make(infile):
    im=_open(infile)
    width, height = im.size

    return _make(im, width, height)

if len(sys.argv)<2:
    print("build.py c.png 200 200")
    exit(0)

infile = sys.argv[1]


#width, height = im.size

out = ""

if (len(sys.argv) == 3):
    out = makeS(infile, int(sys.argv[2]))

if (len(sys.argv) == 4):
    out = makeXY(infile, sys.argv[2], sys.argv[3])

if out == "":
    out = make(infile)

f = open(infile + '.txt', 'w', encoding="utf-8")
f.write(out)
f.close()



