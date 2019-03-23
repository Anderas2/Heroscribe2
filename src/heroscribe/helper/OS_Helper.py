# -*- coding: utf-8 -*-
""""
  HeroScribe2
  Copyright (C) 2019 Andreas Wagener and Shane Adams
  Heroscribe 1 was by Flavio Chierichetti and Valerio Chierichetti

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published
  by the Free Software Foundation.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from pathlib import Path # provides portable filenames across windows and Mac

import sys
import platform
import os
import pathlib

def errorprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class OS_Helper():
    ''' provides an absolute path to the heroscribe directory, hopefully
    system independent. Also a method for opening a webbrowser to display
    the object.html.'''
    def __init__(self):
        # try find the software location

        if '__file__' in globals():
            self.h_scribe_dir = pathlib.Path(__file__).parent

        else:
            self.h_scribe_dir = Path(os.getcwd())

        if self.h_scribe_dir.match("helper"):
            self.h_scribe_dir = self.h_scribe_dir.parent
        if self.h_scribe_dir.match("heroscribe"):
            self.h_scribe_dir = self.h_scribe_dir.parent
        if self.h_scribe_dir.match("src"):
            self.h_scribe_dir = self.h_scribe_dir.parent

        os.chdir(self.h_scribe_dir)



    def open_url(self, url, str_ref=None):
        file = Path(url)
        try:
            if str_ref != None:
                self.openbrowser(file + "#" + ref)
            else:
                self.openbrowser(file)
        except:
            errorprint("An error occured: \n", sys.exec_info()[0])
            raise # and stop the program anyway

    def openfile(self, file):
        if platform.system() == "Windows":
            webbrowser.open_new_tab(file)

        elif platform.system() == "Darwin":
            file_location = "file:///" + file
            webbrowser.open_new_tab(file_location)

    def get_absolute_path (relative):
        return self.h_scribe_dir / Path(relative)
'''
#notes
# This opens the path with any file handler that is associated to it
from pathlib import Path
filepath = Path("C:/Users/Andreas/25 Heroquest/Heroscribe 2/Objects.xml")
cmd = "rundll32 url.dll,FileProtocolHandler \"" + str(filepath) + "\""
import os
os.system(cmd)

# this may work, too
import webbrowser as wb
wb.open_new_tab('http://www.google.com')
'''
