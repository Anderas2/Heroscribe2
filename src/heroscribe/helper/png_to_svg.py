# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 13:06:06 2018

@author: Anderas

This file can be called with a minimum set of icon properties (see icon_infos
right at the end of the file) and with an input path.

In the input path, any png file will be treated. The pngs are best presented
in 200 pixel or more size; with light and dark interior and transparent ex-
terior.

"""

from matplotlib.colors import rgb2hex
import os  # links to the file system for opening and closing of files
import sys
import subprocess as cmd # allows to use the cmd and external exe files
import re
import tempfile
from scipy.ndimage.filters import median_filter
import gzip # to make or unpack gz archives
from src.heroscribe.helper.hs_eps_2_pic import EPS2PNG

from shutil import copyfileobj
#from math import ceil
from PIL import Image
from PIL import ImageFilter
#from datetime import datetime
#from copy import deepcopy # to make real copies of dicts

from matplotlib.colors import LinearSegmentedColormap as LSC
import numpy as np

def checkpath(outpath, alternative_path=None):
    '''checks if an output path exists and if not, makes it.'''
    if alternative_path == None:
        alternative_path = outpath
    if outpath == None:
        outpath = alternative_path
    if outpath == None:
        raise NameError('Checkpath was called without a single valid path')

    if outpath[-1:] != '\\':
        outpath += '\\'
    if not os.path.exists(os.path.dirname(outpath)):
            os.makedirs(os.path.dirname(outpath))
            print('made new folder: ', outpath)
    return outpath

def talk(in_str, verbose=0):
    if verbose > 0:
        print(in_str)

def find(key, dictionary):
    ''' recursive function to seach a nested dictionary for a certain key;
        then return the values for the keys.
    '''
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result


"""
Created on Sat Sep  1 10:36:19 2018

6.853
1x1 circle	5.921 x 5.918
2x1 ellipse	11.788 x 5.918
3x1 ellipse	17.871 x 5.918
1-square width	6.853
2-square width	13.999
3-square width	20.778
4-square width	27.566
5-square width	34.341
6-square width	41.099
7-square width	47.843
8-square width	54.644
9-square width	61.497
10-square width	68.192
11-square width	74.965
12-square width	81.739
13-square width	88.512
14-square width	95.285
15-square width	102.059
16-square width	108.832
17-square width	115.605
18-square width	122.379
19-square width	129.152
20-square width	135.925
@author: Andreas
"""
# Globals and imports

class SymbolSizes():
    ''' provides the heroscribe-typical sizes in mm, pt, for raster images and
        for sample images. An additional "hires" was defined if ever I want
        to make printable raster images from the maps.

        It also has a set of methods to calculate scale factors among several
        kinds of files.

    '''
    def __init__(self, verbose = 0):
        self.VERBOSE = verbose

        # list of "correct" circular sizes.
        # circles represent monsters and other figures and need to be smaller
        # than the squares that contain them.
        circles = {}
        circles['mm'] = [0, 5.921, 11.788, 17.871]
        circles['raster'] = [int((x *  30 / circles['mm'][1])+0.5) for x in circles['mm']]
        circles['sample'] = [int((x *  50 / circles['mm'][1])+0.5) for x in circles['mm']]
        circles['hires'] = [int((x *  174 / circles['mm'][1])+0.5) for x in circles['mm']]

        # list of "correct" square sizes.
        # a 1x3 three square sized symbol should have square[1] x square[3] size
        # in the bounding box.
        # squares are used for everything from funrniture over traps and rooms
        # as long as it is not a figure
        squares = {}
        squares['mm'] = [0, 6.853, 13.999, 20.778, 27.566, 34.341, 41.099,
           47.843, 54.644, 61.497, 68.192, 74.965, 81.739, 88.512, 95.285,
           102.059, 108.83, 115.605, 122.379, 129.152, 135.925,]
        squares['raster'] = [int((x *  34 / squares['mm'][1])+0.5) for x in squares['mm']]
        squares['sample'] = [int((x *  54 / squares['mm'][1])+0.5) for x in squares['mm']]
        squares['hires'] = [int((x *  200 / squares['mm'][1])+0.5) for x in squares['mm']]

        self.circles = circles
        self.squares = squares


    def calculate_scale_svg(self, svg_file, circle = True,
                            square_width = 1, square_height = 1,
                            size="sample"):
        ''' takes an eps file and calculates a scaling factor to be compatible
        with heroscribe

        eps_file: Full path to a file. The eps file to be scaled.
        header: A dict that must contain circle, width and height attributes
        circle: boolean. There are circular and rectangular symbols in Heroquest;
            monsters are circular and all the rest is rectangular. Set to true
            for circular and ellipsoid symbols; set to false for rectangular
            symbols like traps or room symbols.
        width, height: The target width and height expressed in heroquest map
            squares. A long pit trap for example is width 2 and height 1; most
            symbols are height and width 1.

        '''
        box = self.get_bounding_box(svg_file)

        if circle:
            size = self.circles[size][min(square_width, square_height)]
        else:
            size = self.squares[size][min(square_width, square_height)]

        length = []
        for i in range(0,2):
            length.append(box[i+2] - box[i])

        scale_factor = min(length) / size

        return scale_factor


    def add_viewBox(self, scale_factor,
                    infile,
                    outfile):
        ''' the "viewBox" is a helper that redefines the scale of the
        svg. All coordinates inside stay the same, but the viewbox
        defines a new coordinate system. So with a double size viewbox,
        the svg is shown in half size.'''

        box = self.get_bounding_box(infile)
        size_x = (box[2] - box[0]) * scale_factor
        size_y = (box[3] - box[1]) * scale_factor

        new_box_text = ' viewBox="{} {} {} {}"> '.format(
                box[0], box[1], box[0] + size_x, box[1] + size_y)


        with open(infile, 'r') as f:
            talk('opened {}'.format(infile), self.VERBOSE)

            with open(outfile, 'w') as f2:
                talk('opened {}'.format(outfile), self.VERBOSE)

                f2.write(f.readline()) # read and write the first line
                re_style = re.compile(r'(<svg.*?")(>)')

                for line in f:
                    if re_style.findall(line):
                        if new_box_text not in line:
                            line = re_style.sub(r'\1' + new_box_text, line)

                    f2.write(line)



    def calculate_scale_pt(self, file_height, file_width,
                        header):
        ''' takes an eps file and calculates a scaling factor to be compatible
        with heroscribe

        file_height, file_width: Height and width coming from a file
        header: A dict that must contain circle, width and height attributes
        circle: boolean. There are circular and rectangular symbols in Heroquest;
            monsters are circular and all the rest is rectangular. Set to true
            for circular and ellipsoid symbols; set to false for rectangular
            symbols like traps or room symbols.
        width, height: The target width and height expressed in heroquest map
            squares. A long pit trap for example is width 2 and height 1; most
            symbols are height and width 1.

        '''
        if header['circle']:
            sizes_pt = self.circles['pt']
            sizes_mm = self.circles['mm']
        else:
            sizes_pt = self.squares['pt']
            sizes_mm = self.squares['mm']

        size_min = sizes_pt[min(header['width'], header['height'])]
        #size_max = circles[max(width, height)]
        size_w = sizes_mm[header['width']]
        size_h = sizes_mm[header['height']]

        scale_factor = size_min / min(file_height, file_width)
        max_factor = max(file_height, file_width) / min(file_height, file_width)

        if file_height < file_width:
            header['width_mm'] = max_factor * size_w
            header['height_mm'] = size_h
        else:
            header['width_mm'] = size_w
            header['height_mm'] = max_factor *  size_h

        return scale_factor, header



    def scale_pixel(self, inpath, outpath,
                                header,
                                size_type="sample"):
        ''' takes an png image file and calculates a scaling factor to be
        compatible with heroscribe, also scales the picture.

        inpath: complete path to the file
        outpath: complete path to the target

        header: A dict that must contain icon_type, width and height attributes

        icon_type: "circle" or "square".

        width, height: The target width and height expressed in heroquest map
            squares. A long pit trap for example is width 2 and height 1; most
            symbols are height and width 1.

        '''

        # sanity checks
        if not all(k in header for k in ['width', 'height']):
            message = "Failure in call to function scale_pixel\n"
            message += "I need a valid header dict including \n"
            message += "'width', 'height'"
            raise NameError(message)

        if not "icon_type" in header:
            if "circle" in header:
                header['icon_type'] = 'circle' if header['circle'] else 'square'
            else:
                message = "Failure in call to function scale_pixel\n"
                message += "I need a valid header dict including \n"
                message += "'icon_type' or 'circle'"
                raise NameError(message)

        if not ("circle" in header['icon_type']
        or "square" in header['icon_type']):
            message = "Failure in call to function scale_pixel\n"
            message += "The icon_type needs to be one of the following: \n"
            message += "circle, square \n"
            raise NameError(message)

        if not ("sample" in size_type
                or "raster" in size_type
                or "high_res"  in size_type):
            message = "Failure in call to function scale_pixel\n"
            message += "the size type needs to be one of the following: \n"
            message += "raster, sample or hires"
            raise NameError(message)

        if not isinstance(header['height'], int) \
        or not isinstance(header['width'], int):
            message = "Failure in call to function scale_pixel\n"
            message += "height and width must be of type int \n"
            message += "because they give the size in game board squares\n "
            message += "given was height={} and width={}".format(
                    header['height'],header['width'])
            raise NameError(message)

        # sanity checks over, to work.
        if header['icon_type'] == "circle":
            size_w = self.circles[size_type][header['width']]
            size_h = self.circles[size_type][header['height']]

        elif header['icon_type'] == "square":
            size_w = self.squares[size_type][header['width']]
            size_h = self.squares[size_type][header['height']]

        px_size = min(size_w, size_h)

        img = Image.open(inpath)
        size = min(img.width, img.height)
        percent_rast = (px_size / float(size))
        hsize = int((float(img.height) * float(percent_rast)))
        wsize = int((float(img.width)  * float(percent_rast)))
        img_rast = img.resize((wsize, hsize), Image.LANCZOS)
        img_rast.save(outpath, fmt='png')
        return header



    def get_bounding_box(self, svg_file):
        ''' searches with a regex for the svg header line,
        and inside that for any size found.'''
        sizestr = ''
        with open(svg_file, 'r') as file:
            for line in file:
                if "<svg" in line:
                    sizestr = line
                    break
        min_x = 0
        min_y = 0
        width = 0
        height = 0
        re_width = re.compile(r'(width=")(\d+)(")')
        if re_width.findall(sizestr):
            match = re_width.findall(sizestr)
            width = int(match[0][1])

        re_height = re.compile(r'(height=")(\d+)(")')
        if re_height.findall(sizestr):
            match = re_height.findall(sizestr)
            height = int(match[0][1])

        re_viewBox = re.compile(r'(viewBox=")(\d+\W)(\d+\W)(\d+\W)(\d+\W)"')
        if (re_viewBox.findall(sizestr)):
            match = re_height.findall(sizestr)
            min_x = int(match[0][1])
            min_y = int(match[0][2])
            width = int(match[0][3])
            height = int(match[0][4])

        return (min_x, min_y, width, height)




###############################################################################

class BlackGradients():

    def __init__(self, verbosity=0, inpath=None, outpath=None):
        basepath = os.path.abspath(os.curdir)
        mc_path = basepath

        # make the path pointing to the multicolor folder by force
        if "\\Code" not in mc_path:
            mc_path = mc_path + "\\Code"
        if "\\Multicolor_Symbols" not in mc_path:
            mc_path = mc_path + "\\Multicolor_Symbols"
        sys.path.append(mc_path)

        # and point the basepath to the base folder by force
        if "\\Multicolor_Symbols" in basepath:
            basepath = basepath.replace("\\Multicolor_Symbols","")
        if "\\Code" in basepath:
            basepath = basepath[:basepath.find("\\Code")] # remove everything after "\\Code"


        self.__basepath = basepath
        self.__codepath = basepath + "\\Code"
        self.VERBOSE = verbosity
        self.AUTOTRACE =  self.__basepath + "\\autotrace\\autotrace.exe"

        if outpath == None:
            self.OUT_FOLDERS = basepath + '\\output\\'
        else:
            self.OUT_FOLDERS = outpath
        self.OUT_BMP = self.OUT_FOLDERS + 'bmp_for_svg\\'
        self.OUT_SVG = self.OUT_FOLDERS + 'svg\\'

        if inpath == None:
            self.INPATH = basepath + '\\input\\'
        else:
            self.INPATH = inpath

        #self.make_gradients() # generate color gradients
        #self.alternate_gradients()
        self.black_gradient_only()


###############################################################################
# A function that uses autotrace to make symbols. As it does not work perfectly
# it trepeats the try until it works. Unelegant, slow, but better than manual.

#autotrace help https://www.systutorials.com/docs/linux/man/1-autotrace/

    def make_vector(self, pic_path, svg_path,
                    savetime = False, outformat = 'svg',
                    despeckle = 10,
                    errorthresh = 2,
                    cornerdetect = 4):
        ''' Uses autotrace to generate eps files.
        it repeats the proces some times until it worked well at least once.

        pic_name: get the full path of the bmp file to be treated
        height, width: pixel size of picture
        circle: True - calculates dpi according to a heroquest circle size.
                False - calculates dpi like a heroquest square.
        '''
        # check if file exist and delete if yes
        if os.path.isfile(svg_path):
            if savetime == False:
                os.remove(svg_path)
            else:
                if os.stat(svg_path).st_size > 0:
                    print('skipped ' + os.path.basename(pic_path))
                    return svg_path
                else:
                    os.remove(svg_path)
        # Autotrace has two important properties:
        # 1. It uses cymk as color
        #    and the color translation is not perfect.
        # 2. it costs lots of time to trace the files.
        #
        # So we trace here only the EU files (Black and White)
        # and the coloring will be done later.
        # for autotrace: bmp white is interpreted "transparent"

        image = Image.open(pic_path)

        #print(image)
        im = np.array(image.convert('LA'))
        im_alpha = im[:,:,1] # save alpha channel
        im_zero = im_alpha==0 # get mask (invert alpha channel)
        im_zero = im_zero*255 # multiply mask with white

        im = im[:,:,0] # keep grey channel, discard alpha channel

        # define a Look Up Table that sets the brightest color to off-white
        LUT=np.zeros(256,dtype=np.uint8)
        LUT[10:235+1]=np.linspace(start=0,stop=255,
                            num=(235-10)+1,
                            endpoint=True,dtype=np.uint8)
        LUT[-20:]=253
        im = LUT[im]

         # Set image content in transparent areas to white
        im = np.maximum(im, im_zero) # apply the max of white mask and image
        image_out = Image.fromarray(im)
        if image_out != 'RGB':
            image_out = image_out.convert('RGB')

        bmp_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".bmp")
        bmp_temp.close()

        try:
            with open(bmp_temp.name, 'wb') as file:
                image_out.save(file, fmt="bmp")

            talk('making vector file with the name {}.'.format(svg_path),
                 self.VERBOSE)
            despeckle = 10
            # compose command line argument for autotrace
            command = '"' + self.AUTOTRACE + '"' \
                    + ' -output-file "' + svg_path +  '"' \
                    + ' -output-format ' + outformat + ' ' \
                    + ' -despeckle-level ' + str(despeckle) \
                    + ' -color-count 0' \
                    + ' -background-color FFFFFF' \
                    + ' -input-format bmp ' \
                    + ' -error-threshold ' + str(errorthresh) \
                    + ' -corner-surround ' + str(cornerdetect) \
                    + ' "' + bmp_temp.name + '"'
            # open cmd and execute autotrace
            p=cmd.Popen(command, stdout=cmd.PIPE, stderr=cmd.PIPE)
            if len(p.communicate()[1]) > 1:
                message = ''
                message += ('Function "Make Vectors" here.\n')
                message += ('A problem occured while generating vectors\n')
                message += ('file concerned: \n', pic_path)
                message += ('\n\nError message:\n')
                message += (p.communicate()[1].decode('utf-8'))
                raise NameError(message)
            p.kill()

        except Exception as err:
            print("failure in autotrace function")
            print(err)
            print(bmp_temp.name)
            raise
        else:
            bmp_temp.close()
            os.remove(bmp_temp.name)

        # check file size, if it is bigger than 0, return the file
        try:
            filesize = os.stat(svg_path).st_size
        except:
            filesize = 0
        if filesize > 0:
            return svg_path
        return None


###############################################################################
    def tuple_mult(self, in_tuple, scalar, integer = False):
        '''multiplies in_tuple with a scalar'''
        if integer:
            return tuple([int(round(float(a) * float(scalar), 0)) for a in in_tuple])
        else:
            return tuple([float(a) * float(scalar) for a in in_tuple])

    def black_gradient_only(self, mid=0.55):
        ''' a function to define lots of colors. Currently it defines just one.
        '''
        colors = { 'white':(1., 1., 1.),
                   'black':(0., 0., 0.),
                  }
        self.colors = colors
        gradients = {}
        rgbs = {}
        icons = {}

        gradient_name = 'black'
        gradients[gradient_name] = LSC.from_list(gradient_name,
                                                [(0, colors['black']),
                                                 (mid, colors['black']),
                                                 (1, colors['white'])],
                                                 N=256)

        rgbs[gradient_name] = {'dark':colors['black'],
                             'bright':colors['white']}


        self.gradients = gradients
        self.gradient_names = gradients.keys()
        self.rgbs = rgbs
        self.icons = icons

    def set_midpoint(self, mid):
        new_gradients = {}
        for gradient in self.gradients:
            new_gradients[gradient] = LSC.from_list(gradient,
                                                [(0, self.rgbs['black']['dark']),
                                                 (mid, self.rgbs['black']['dark']),
                                                 (1, self.rgbs['black']['bright'])],
                                                 N=256)
        self.gradients = new_gradients


###############################################################################
# finally. Work on all the png's in the input folder
# find all png in this folder


    def hex2rgb(self, hex_str):
        h = hex_str.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))

    def recolor_svg_file(self, gradient_name, infile_path, outfilepath,
                         gradient_mid = 0.55):

        ''' Applies one color gradient to one EU svg file as it comes
        out of Autotrace and then changes the name from _EU to _gradientname
        gradient_name: A valid gradient name from this class (see gradient_names)
        infile: complete path to an svg file in black and white without changes
                after Autotrace generated it
        outpath: A folder where the colored svg shall be stored
        header: header information dict for this file.
        '''
        #sanity checks

        infile = infile_path

        talk('start svg recoloring of file \n{} \nwith gradient {}'.format(
                infile, gradient_name), self.VERBOSE)
        self.set_midpoint(gradient_mid)

        if gradient_name in self.rgbs:

            # make the exact text lines that need to be included in the eps
            color = rgb2hex(self.rgbs[gradient_name]['dark'])
            dark_fill = 'style="fill:{};'.format(color)
            color = rgb2hex(self.rgbs[gradient_name]['bright'])
            bright_fill = 'style="fill:{};'.format(color)

        else:
            message = "Problem in the recolor_svg function.\n"
            message += 'I didnt find your color {} among my gradients.\n'.format(gradient_name)
            message += 'You can find the list of available colors in "gradient_names".\n'
            message += 'Available are: {}'.format(self.rgbs.keys())
            raise NameError(message)

         # group 1: useless numbers and group 2: the number we search for.
        re_colorfind = re.compile(r'(style="fill:)(#\w{6})(;)')

        ##########################################################
        # first, generate the new filename
        new_name = os.path.basename(infile)
        talk('extracted this filename from the path: {}'.format(new_name),
             self.VERBOSE)
        if os.path.isfile(outfilepath): # check if the file is there already
            os.remove(outfilepath) # if yes remove it

        ###########################################################
        # now work on the file, line by line, and change the colors
        with open(infile, 'r') as f:
            talk('opened {}'.format(infile), self.VERBOSE)

            with open(outfilepath, 'w') as f2:
                talk('opened {}'.format(outfilepath), self.VERBOSE)

                talk('making {} from {}'.format(
                            os.path.basename(outfilepath),
                            os.path.basename(infile)), self.VERBOSE-1)

                f2.write(f.readline()) # read and write the first line
                add_on = """ version = '2.0' xmlns="http://www.w3.org/2000/svg"> """
                re_style = re.compile(r'(<svg.*?")(>)')

                for line in f:
                    if re_style.findall(line):
                        if add_on not in line:
                            line = re_style.sub(r'\1' + add_on, line)

                    if re_colorfind.findall(line):
                        # if it finds a color definition, replace
                        # it by a new color definition.
                        match = re_colorfind.findall(line)
                        color = self.hex2rgb(match[0][1])
                        color = (color[0] + color[1] + color[2])/3

                        if color >= gradient_mid:
                            # apply bright color
                            line = re_colorfind.sub(bright_fill, line)
                        else:
                            # apply dark color
                            line = re_colorfind.sub(dark_fill, line)

                    # after all necessary changes have been done,
                    # write the line to the new file
                    f2.write(line)
        talk('finished recoloring {}'.format(new_name),self.VERBOSE)

###############################################################################



###############################################################################
    def enhance_contrast(self, im, contrast):
        ''' takes an np array of an image and applies a contrast enhancing
        Look Up Table. Returns an np array of an image.
        '''
                # Make a look up table to
        # enhance contrast a little bit. LUT means Look up table
        LUT = np.zeros(256,dtype = np.uint8)
        LUT[contrast:256 - contrast] = np.linspace(start = 0,
                                                 stop = 255,
                                                 num = (256-(2*contrast)),
                                                 endpoint = True,
                                                 dtype = np.uint8)
        LUT[-contrast:] = 255
        LUT[0:contrast] = 0
        return LUT[im]

###############################################################################


    def recolor_one_png(self, gradient_name = None,
                          infile = None,
                          outfile = None,
                          upsampling = 0,
                          scale_px = False,
                          temp_file = None,
                          medianfilter = 5,
                          contrast = 10):
        ''' Applies one color gradient to one png and changes
        the name to file_gradientname.png
        '''
        #sanity checks
        if (not infile
        or not infile.endswith(".png")):
            message = "Problem in the recolor png function.\n"
            message += "I did not receive a filename, or the file was no png.\n"
            message += "I received {}".format(infile)
            raise NameError(message)

        if outfile:
            if os.path.isfile(outfile):
                os.remove(outfile)
            checkpath(os.path.dirname(outfile))

        if gradient_name:
            if gradient_name in self.gradients:
                gradient_LSC = self.gradients[gradient_name]
            else:
                message = 'I didnt find your color {} among my gradients.\n'.format(gradient_name)
                message += 'You can find the list of available colors in "gradient_names".'
                raise NameError(message)

        if scale_px:
            scale_px = int(scale_px)
        # now work on the image
        image = Image.open(infile)
        image = image.convert('RGBA')
        if upsampling:
            # make a new picture to have a bit of frame around the old one
            im_new = Image.new('RGBA',
                               size = (image.size[0] + 4, image.size[1] + 4),
                               color = (255, 255, 255, 0)
                               )
            pos = (2, 2)
            im_new.paste(image, box = pos)
            image = im_new.resize( (image.size[0] * upsampling + 1, image.size[1] * upsampling + 1),
                                 resample = Image.BILINEAR)

        if medianfilter > 0:
            image = image.filter(ImageFilter.MedianFilter( medianfilter))


        im = np.array(image.convert('LA'))
        im_alpha = im[:,:,1] # save alpha channel
        im = im[:,:,0] # keep grey channel, discard alpha channel
#        if medianfilter > 0:
#            im = ImageFilter.MedianFilter(im, medianfilter)
#            im = median_filter(im, size= (medianfilter, medianfilter),
#                               mode = 'wrap')

        if contrast > 0:
            # apply contrast enhancing Look Up Table
            im = self.enhance_contrast(im, contrast)


        # Set image content in transparent areas to white
        im_zero = im_alpha==0 # get mask
        im_zero = im_zero*255 # multiply mask with white
        im = np.maximum(im, im_zero) # apply the max of white mask and image

        if gradient_name:
            im_grad = gradient_LSC(im) # apply color gradient to grey image
            im_grad = np.uint8(im_grad*255) # with colorspace 255

            # for direct use: png in scale_px size with alpha mask
            im_grad[:,:,3]=im_alpha # get mask back into image
            image_out = Image.fromarray(im_grad)

        else:
            image_out = Image.fromarray(im)

        if temp_file:
            if image_out.mode !='RGBA':
                save_image = image_out.convert('RGBA')
            else:
                save_image = image_out
            save_image.save(temp_file, fmt="png")

        if scale_px:
            scale = scale_px / min(*image_out.size)
            hsize = int((float(image_out.height) * float(scale)))
            wsize = int((float(image_out.width)  * float(scale)))
            image_out = image_out.resize((wsize, hsize), Image.LANCZOS)

        if outfile:
            image_out.save(outfile, fmt="png")
            return outfile
        elif temp_file:
            return temp_file
        else:
            return None

###############################################################################

    def from_gz(self, fpath, out_path):
        with gzip.open(fpath, 'rb') as f_in:
            with open(out_path, 'wb') as f_out:
                copyfileobj(f_in, f_out)



    def cronjob(self, inpath,
             outpath,
        icon_infos = None,
        verbosity = 0,
        picturesize = 400,
        medianfilter = 4):
        '''translates EPS to SVG, via PNG :-(

        inpath: Input path containing symbols
        outpath: where to upt the symbols
        verbosity: the higher, the more it talks
        picturesize: dots per symbol to render the eps.
        a symbol normally has 30 pixel on the screen, if you put 400 here like
        advertised, it will give a more than tenfold oversampling and allows
        some despeckling.
        medianfilter: for many symbols, this is good. For fine graphics like
        game board lines, this is deadly and should be set to 0
        '''

        if icon_infos == None:
            icon_infos = {}

        if 'circle' not in icon_infos:
            icon_infos['circle'] = True
            talk('No infos were given, I suppose these are circular symbols', verbosity)
        if 'height' not in icon_infos:
            icon_infos['height'] = 1
            talk('No height infos were given, I suppose these are height 1 symbols', verbosity)
        if 'width' not in icon_infos:
            icon_infos['width'] = 1
            talk('No width infos were given, I suppose these are width 1 symbols', verbosity)
        elif not 'projectfolder' in icon_infos:
            icon_infos['projectfolder'] = 'YeOldeInn'

        # to change colors and make vectors
        mc = BlackGradients(inpath=inpath, outpath=outpath, verbosity=verbosity )
        mc.OUT_FOLDERS = outpath

        # to resize vectors
        symsize = SymbolSizes()

        # to read f*** heroscribe eps files into png's
        EP = EPS2PNG(pixel=picturesize)

        # this could take lots of colors. It takes only black today.
        gradient_name = list(mc.gradient_names)[0]

        list_of_files = []
        for (dirpath, dirnames, filenames) in os.walk(inpath):
            for filename in filenames:
                if filename.endswith('.eps.gz'):
                    list_of_files.append(os.sep.join([dirpath, filename]))


        for file in list_of_files:
            try:

                icon_name = file[:-7] #remove .eps.gz
                icon_name = icon_name.replace("_EU", "") #remove _EU tag
                icon_name = icon_name.replace(inpath, outpath)
                png_name = icon_name + '.png'
                svg_name = icon_name + '.svg'


                eps_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".eps")
                eps_temp.close()
                png_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                png_temp.close()
                png_name_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                png_name_temp.close()
                svg_name_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".svg")
                svg_name_temp.close()
                svg_name_temp2 = tempfile.NamedTemporaryFile(delete=False, suffix=".svg")
                svg_name_temp2.close()




                if os.path.exists(svg_name):
                    continue

                print('unzipping')
                mc.from_gz(file, eps_temp.name)

                print('png calculation')
                EP.eps_2_png(eps_temp.name, png_temp.name, epscrop=True)

                print('recoloring')
                png_name = mc.recolor_one_png(gradient_name = gradient_name,
                                                infile = png_temp.name,
                                                outfile = png_name,
                                                temp_file = png_name_temp.name,
                                                scale_px = picturesize,
                                                medianfilter = medianfilter)
                print('Tracing Vector file')
                mc.make_vector(png_name_temp.name, svg_name_temp.name,
                                             despeckle = 10)
                print('controlling colors of vector file')
                mc.recolor_svg_file(gradient_name, svg_name_temp.name, svg_name_temp2.name)

                scale_factor = symsize.calculate_scale_svg(svg_name_temp2.name)

    #            symsize.add_viewBox(scale_factor,
    #                                infile = svg_name_temp2.name,
    #                                outfile = svg_name)
                symsize.add_viewBox(1,
                                    infile = svg_name_temp2.name,
                                    outfile = svg_name)
            except:
                os.remove(svg_name_temp.name)
                os.remove(svg_name_temp2.name)
                os.remove(png_name_temp.name)
                os.remove(eps_temp.name)
                os.remove(png_temp.name)
                raise
            else:
                os.remove(svg_name_temp.name)
                os.remove(svg_name_temp2.name)
                os.remove(png_name_temp.name)
                os.remove(eps_temp.name)
                os.remove(png_temp.name)

icon_infos = {'circle':True, #True or False
              'height':1, # for circles 1-3, for squares 1-20
              'width':1,
              'projectfolder':'YeOldeInn', # what you want
              'despeckle' : 10,
              'multicolor': True, # True if many colors are wanted...
              'type' : 'monster', # room, monster, trap
              }

inpath = 'C:\\Users\\Andreas\\Questimator\\input\\'
outpath = 'C:\\Users\\Andreas\\Questimator\\output\\'

bg = BlackGradients()
bg.cronjob(inpath = inpath, outpath = outpath,
     icon_infos = icon_infos,
     picturesize = 200,
     medianfilter = 0)
