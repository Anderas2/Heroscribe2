# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 07:46:18 2019

@author: Andreas
"""

#import src.heroscribe.
from src.heroscribe.helper.OS_Helper import OS_Helper

from src.heroscribe.Preferences import Preferences

from src.heroscribe.gui.test_gui import hs2_window
from src.heroscribe.list.List import List
from src.heroscribe.quest.Quest import Quest
import sys

class HeroScribe():
    def __init__(self):
        self.osh = OS_Helper.OS_Helper()
        if self.osh.isMac :
            # set mac specific things here

            pass

