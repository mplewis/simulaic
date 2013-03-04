#!/usr/bin/python

# credit goes to http://stackoverflow.com/a/237193/254187
#            and http://stackoverflow.com/a/237747/254187

import Image
import argparse
import sys
import os

parser = argparse.ArgumentParser(description='Convert an image to a new ' + 
                                             'size and color fidelity.')

parser.parse_args()

# contains the target rasterized color values for the image
PALETTE = []

# contains the colors to push onto the palette
COLORS = [
    [0,   0,   0  ], # black
    [255, 255, 255], # white
    [255, 0,   0  ], # red
    [0,   255, 0  ], # green
    [0,   0,   255], # blue
    [0,   255, 255], # cyan
    [255, 0,   255], # magenta
    [255, 255, 0  ]  # yellow
]

# add the first NUMCOLORS colors from COLORS to PALETTE
NUMCOLORS = 99

for colornum in range(NUMCOLORS):
    try:
        PALETTE += COLORS.pop(0)
    except IndexError:
        print('WARNING: ' + str(NUMCOLORS) + ' colors requested but only ' + 
              str(colornum) + ' colors available, using the first ' + 
              str(colornum) + ' colors')
        break

# pad PALETTE to 768 values (256 * RGB (3) = 768)
if len(PALETTE) < 768:
    PALETTE += [0] * (768 - len(PALETTE))


for imgfn in sys.argv[1:]:
    dirname, filename = os.path.split(imgfn)
    name, ext = os.path.splitext(filename)
    # a palette image to use for quant
    pimage = Image.new("P", (1, 1), 0)
    pimage.putpalette(PALETTE)

    # open the source image
    image = Image.open(sys.argv[1])
    image = image.convert("RGB")

    # quantize it using our palette image
    imagep = image.quantize(palette=pimage)

    # save
    newpathname = os.path.join(dirname, "cga-%s.png" % name)
    imagep.save(newpathname)