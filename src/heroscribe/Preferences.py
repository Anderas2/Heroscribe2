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

class Preferences():
    ''' sets and reads stuff that can be chosen by the user and shall
    stay the same from session to session'''

    def __init__ (self):
        language_dict = {"en":{"add_objects" : "Add Objects",
                       "edit_objects": "Edit Objects",
                       "darken": "Darken/Color",
                       "import":"Import",
                       "export":"Export",
                       "questimate":"Questimate",
                      },
                 "de":{"add_objects" : "Neues Teil",
                       "edit_objects": "Teil bearbeiten",
                       "darken": "abdunkeln / färben",
                       "import":"Import",
                       "export":"Export",
                       "questimate":"Questimate",
                      },
                 "fr":{"add_objects" : "Nouveau Piece",
                       "edit_objects": "Editer Piece",
                       "darken": "sombrer / coulourer",
                       "import":"importer",
                       "export":"exporter",
                       "questimate":"Questimate",
                      },
                 }
        self.gui_texts = language_dict['en']
