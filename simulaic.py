#!/usr/bin/python

'''Converts an image to a fixed color palette and optionally a fixed size.'''

# credit goes to http://stackoverflow.com/a/237193/254187
#            and http://stackoverflow.com/a/237747/254187

import Image
import argparse
import os

# THEMES is the list of color palettes that can be selected for the output image
# it's stored in themes.py
from themes import THEMES

# DEFAULT_THEME is picked whenever no other theme is selected at the
# command line
DEFAULT_THEME = 'BW'

AVAILABLE_THEMES = []
for THEME_NAME in THEMES:
    AVAILABLE_THEMES.append(THEME_NAME)

AVAILABLE_THEMES_STR = ', '.join(AVAILABLE_THEMES)


# set up the parser
PARSER = argparse.ArgumentParser(description='Convert an image to a new ' + 
                                             'size and color fidelity.')
PARSER.add_argument('image', help='The image to be converted.')
PARSER.add_argument('-t', '--theme',
                    help='The set of colors to use in the rendered image. ' + 
                         'Themes available: ' + AVAILABLE_THEMES_STR + '; ' +
                         'default theme: ' + DEFAULT_THEME)
PARSER.add_argument('-w', '--width', type=int,
                    help='Width of the output image, in pixels.')
PARSER.add_argument('-e', '--height', type=int,
                    help='Height of the output image, in pixels.')

ARGS = PARSER.parse_args()

IMGPATH = ARGS.image

if ARGS.theme != None:
    SELECTED_THEME = ARGS.theme
else:
    SELECTED_THEME = DEFAULT_THEME

DO_RESIZE = False
if ARGS.height != None and ARGS.width != None:
    DO_RESIZE = True
    HEIGHT = ARGS.height
    WIDTH = ARGS.width
    NEW_SIZE = (WIDTH, HEIGHT)

# PALETTE contains the target rasterized color values for the image,
# taken from the selected theme.
PALETTE = []
for TRIPLE in THEMES[SELECTED_THEME]:
    PALETTE += TRIPLE

# pad PALETTE to 768 values (256 * RGB (3) = 768) because PIL needs it
if len(PALETTE) < 768:
    PALETTE += [0] * (768 - len(PALETTE))

dirname, filename = os.path.split(IMGPATH)
name, ext = os.path.splitext(filename)
newpathname = os.path.join(dirname, 'conv-' + name + '-' + SELECTED_THEME +
                           '.png')

# a palette image to use for quant
pimage = Image.new("P", (1, 1), 0)
pimage.putpalette(PALETTE)

# open the source image
imagef = Image.open(IMGPATH)
imagec = imagef.convert("RGB")

# resize it to our target size
if DO_RESIZE:
    print 'Resizing image to ' + str(WIDTH) + 'x' + str(HEIGHT)
    imagec = imagec.resize(NEW_SIZE, Image.ANTIALIAS)

print('Processing ' + IMGPATH + ' to ' + SELECTED_THEME + ' as ' +
      newpathname)

# quantize it using our palette image
imagep = imagec.quantize(palette=pimage)

# save
imagep.save(newpathname)