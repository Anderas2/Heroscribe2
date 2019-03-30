# -*- coding: utf-8 -*-
""""
  HeroScribe2 QObject

  An object placed on the board has an z-order (is it below or above other
  stuff?); a rotation facing N, E, S or W; and a position.

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

from src.heroscribe.list.List import List

class QObject():
    '''Represents one object on the board; while having a link to
    the general object list for general comparison.
    '''
    count = 0
    def __init__(self, piece_id, object_list,
                 order = None):

        self.id = piece_id
        self.objects = object_list # type "heroscribe.list.List"

        if order == None:
            if piece_id in object_list.object_list.keys():
                self.order = self.get_order()
        else:
            self.order = order

        self.rotation = 0
        self.top = -1
        self.left = -1
        self.zorder = 0

    def get_order(self):
        self.count = self.count + 1
        return self.count

    def compare_to(self, other_piece):
        if self.zorder < other_piece.zorder:
            return -1
        elif self.zorder > other_piece.zorder:
            return 1
        elif self.order < other_piece.order:
            return -1
        elif self.order > other_piece.order:
            return 1
        else:
            return 0

    def __str__(self):
        return self.objects.get_object(self.id) + " ( " + str(self.zorder) + " ) "