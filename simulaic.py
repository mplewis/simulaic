#!/usr/bin/python

'''Converts an image to a fixed color palette and optionally a fixed size.'''

# credit goes to http://stackoverflow.com/a/237193/254187
#            and http://stackoverflow.com/a/237747/254187

import Image
import argparse
import os
import sys

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
PARSER.add_argument('image', nargs='?', help='The image to be converted. Cannot be used with --demo.')
PARSER.add_argument('--demo', action='store_true', help='Processes a demonstration image. Cannot be used with an image file.')
PARSER.add_argument('-t', '--theme',
                    help='The set of colors to use in the rendered image. ' + 
                         'Themes available: ' + AVAILABLE_THEMES_STR + '; ' +
                         'default theme: ' + DEFAULT_THEME)
PARSER.add_argument('-w', '--width', type=int,
                    help='Width of the output image, in pixels.')
PARSER.add_argument('-e', '--height', type=int,
                    help='Height of the output image, in pixels.')

# store parsed args in ARGS
ARGS = PARSER.parse_args()

IMGPATH = ARGS.image
DEMO_MODE = ARGS.demo

if IMGPATH == None and DEMO_MODE == False:
    print 'ERROR: You must either specify an image to process or use --demo to process a demonstration image.'
    sys.exit()
elif IMGPATH != None and DEMO_MODE == True:
    print 'ERROR: Cannot process an image and run in demonstration mode. Please specify either --demo or provide a demonstration image, but not both.'
    sys.exit()

# use default theme if none selected
if ARGS.theme != None:
    SELECTED_THEME = ARGS.theme
else:
    SELECTED_THEME = DEFAULT_THEME

# resize if both height and width are specified
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

# split the input name apart into its useful elements
if DEMO_MODE == True:
    dirname = os.getcwd()
    name = 'demo'
    ext = 'jpg'
else:
    dirname, filename = os.path.split(IMGPATH)
    name, ext = os.path.splitext(filename)
# output naming convention:
#     input file:  "mypic.jpg", filter: BW
#     output file: "conv-mypic-BW.jpg"
newpathname = os.path.join(dirname, 'conv-' + name + '-' + SELECTED_THEME +
                           '.png')

# use the palette we defined earlier
pimage = Image.new("P", (1, 1), 0)
pimage.putpalette(PALETTE)

# open the source image, either from demo data or from the file path
if DEMO_MODE == True:
    import base64
    import StringIO
    with open('demo.b64', 'r') as f:
        b64_demo_data = f.read()
    binary_demo_data = base64.b64decode(b64_demo_data)
    imagef = Image.open(StringIO.StringIO(binary_demo_data))
else:
    imagef = Image.open(IMGPATH)

imagec = imagef.convert("RGB")

# resize it to our target size, if requested
if DO_RESIZE:
    print 'Resizing image to ' + str(WIDTH) + 'x' + str(HEIGHT)
    imagec = imagec.resize(NEW_SIZE, Image.ANTIALIAS)

print('Processing ' + name + '.' + ext + ' to ' + SELECTED_THEME + ' as ' +
      newpathname)

# quantize it using our palette image
imagep = imagec.quantize(palette=pimage)

# save
imagep.save(newpathname)