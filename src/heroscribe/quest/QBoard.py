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

#from src.heroscribe.quest.Quest import Quest
from src.heroscribe.quest.QObject import QObject


class QBoard ():
    ''' stores information about what is on the board.
    Ensures there are no two pieces of the same kind on the same square.'''
    def __init__(self, width, height, quest):

        # notes which square was marked dark
        self.dark = [[False for y in range(0, self.height)]
                                  for x in range(0, self.width)]
        self.objects = [] # List of QObjects
        self.quest = quest # type Quest
        self.width = width
        self.height = height


    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def is_dark(self, left, top):
        if (left == 0
        or left == self.width + 1
        or top == 0
        or top == self.height + 1 ):
            return False;
        else:
            return self.dark[left - 1][top - 1]


    def toggle_dark(self, left, top):
        if ( left == 0
        or left == self.width + 1
        or top == 0
        or top == self.height + 1 ):
            return

        self.dark[left - 1][top - 1] =  not self.dark[left - 1][top - 1]
        self.quest.setModified(True);


    def add_object(self, new_piece):
        ''' checks if the new game piece is already on the board. If not,
        places it there.'''
        for game_piece in self.objects:
            if (game_piece.left == new_piece.left
            and game_piece.top == new_piece.top
            and game_piece.rotation == new_piece.rotation
            and game_piece.id == new_piece.id):
                return False

        self.objects.append(new_piece)
        self.quest.set_modified(True)
        return True


    def remove_object(self, piece) :
        found_index = None
        for index, game_piece in enumerate(self.objects):
            if (game_piece.left == piece.left
            and game_piece.top == piece.top
            and game_piece.rotation == piece.rotation
            and game_piece.id == piece.id):
                found_index = index
                break
        if found_index != None:
            del self.objects[found_index]
            self.quest.set_modified(True);
            return True
        else:
            return False






