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

from pandas import read_excel

class Preferences():
    ''' sets and reads stuff that can be chosen by the user and shall
    stay the same from session to session'''

    def __init__ (self):

        # TODO: Find and read system language for mac and win.
        # default shall be english;
        # if the user overrides it, it can be a different language
        sys_language = 'en'

        # read language file
        language_file = "https://docs.google.com/spreadsheets/d/1jYDOBCMFmcqQ2fmbhGuSnknJfX520HQRyitI4vNtDwc/export?format=xlsx"
        in_lan = read_excel(language_file)
        in_lan.set_index(['text'], inplace=True)
        self.gui_texts = in_lan[sys_language].to_dict()
