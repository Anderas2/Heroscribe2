# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 06:08:20 2018

@author: Andreas
"""

from os import path as ospath, remove
#from sys import path as syspath
import subprocess as cmd # allows to use the cmd and external exe files
import gzip
from shutil import copyfileobj

GHOSTSCRIPT = 'gswin32c'

class EPS2PNG():
    def __init__(self, verbosity=0, pixel=300):
        self.pixel = pixel
        self.__VERBOSITY_LEVEL = verbosity


    # print only if verbosity is wanted
    def verbose(self, in_string, verbosity=1):
        if self.__VERBOSITY_LEVEL >= verbosity:
            print(in_string)

    def eps_2_png(self, in_file, out_file, epscrop=True):
        if ospath.isfile(out_file):
            remove(out_file)

        dpi = str(int(self.pixel/(18/72)))

        command = GHOSTSCRIPT + ' ' \
        + '-sDEVICE=pngalpha '
        if epscrop:
            command = command + '-dEPSCrop '
        command = command \
        + '-r' + dpi + ' ' \
        + '-o "' + out_file + '" '  \
        + '"' + in_file + '"'

        self.verbose('')
        self.verbose(command)

        p = cmd.Popen(command, stdout=cmd.PIPE, stderr=cmd.PIPE)
        if len(p.communicate()[1]) > 1:
            print('Function "Make PNG from EPS" here.\n')
            print('A problem occured while generating the pictures\n')
            print('\n\nError message:\n')
            print(p.communicate()[1].decode('utf-8'))
        p.kill()



    # to unzip gz files
    def from_gz(self, fpath):
        with gzip.open(fpath, 'rb') as f_in:
            with open(fpath[:-3], 'wb') as f_out:
                copyfileobj(f_in, f_out)





