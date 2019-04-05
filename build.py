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

infile = sys.argv[1]

im = Image.open(infile)

width, height = im.size

if (len(sys.argv) == 3):
    sz = int(sys.argv[2])
    sc = sz / max(width, height)
    t_width = int(width * sc)
    t_height = int(height * sc)
    im.thumbnail([t_width, t_height])
    width = t_width
    height = t_height

if (len(sys.argv) == 4):
    t_width = int(sys.argv[2])
    t_height = int(sys.argv[3])
    im.thumbnail([t_width, t_height], Image.ANTIALIAS)
    width = t_width
    height = t_height

out = ""

for y in range(1, height, 2):
    for x in range(0, width):
        skip = 0

        r, g, b, a = im.getpixel((x, y - 1))
        if a <= OPACITY_TOLERANCE:
            skip += 1
            background = "\033[49m"
        else:
            background = "\033[48;2;" + str(r) + ";" + str(g) + ";" + str(b) + "m"

        r, g, b, a = im.getpixel((x, y))
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

f = open(infile + '.txt', 'w', encoding="utf-8")
f.write(out)
f.close()
