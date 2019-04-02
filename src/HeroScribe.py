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
#import src.heroscribe.
from src.heroscribe.helper.OS_Helper import OS_Helper

from src.heroscribe.Preferences import Preferences

from src.heroscribe.list.List import List
from src.heroscribe.list.Read import Read as listread
from src.heroscribe.gui.test_gui import hs2_window as gui

from src.heroscribe.quest.Quest import Quest
import sys

class HeroScribe():
    def __init__(self):
        self.osh = OS_Helper()
        if self.osh.isMac :
            # set mac specific things here
            pass

        self.osh.errorprint("starting up.")
        self.preferences = Preferences()
        self.osh.errorprint("reading objects...")

        self.objects = listread("Objects.xml").object_list
        self.osh.errorprint("objects read.")
        self.quest = Quest(width = 1,
                             height = 1,
                             board = self.objects.get_board())
        self.osh.errorprint("Quest loaded. Starting GUI.")
        app = QApplication(sys.argv)
        self.gui = gui()
        #self.osh.errorprint("Gui done.")


