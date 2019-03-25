# -*- coding: utf-8 -*-
""""
  HeroScribe2
  Copyright (C) 2019 Shane Adams and Andreas Wagener
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



from pathlib import Path

class Icon():
    def __init__(self, filepath,
                 xoffset,
                 yoffset,
                 original,
                 image=None):
        self.path = Path(filepath)
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.original = original
        self.image = image
