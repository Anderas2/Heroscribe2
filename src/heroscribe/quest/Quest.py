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


from src.heroscribe.list.LBoard import LBoard
from src.heroscribe.quest.QBoard import QBoard
#from src.heroscribe.quest.Write import Write

from itertools import chain


class Quest():
    def __init__(self,
                 width,
                 height,
                 board,
                 file = None,
                 name = '',
                 region = 'Europe',
                 speech = '',
                 notes = []):

        self.width = width
        self.height = height
        #self.boards = [[]]

        self.boards = [[QBoard(board.width, board.height, self) for y in range(0, self.height)]
                                                            for x in range(0, self.width)]

        self.horizontal_bridges = [[[False for x in range(0, self.width-1)]
                                    for y in range(0, self.height)]
                                    for z in range(0, board.height)]

        self.vertical_bridges = [[[False for x in range(0, self.width)]
                                    for y in range(0, self.height-1)]
                                    for z in range(0, board.width)]
        self.notes = notes
        self.region = region
        self.name = name
        self.speech = speech
        self.file = file
        self.modified = False

        def set_horizontal_bridge(self, value, col, row, top):
            if (0 <= col
            and col < self.width - 1 ):
                self.horizontal_bridges[col][row][top-1] = value

        def set_vertical_bridge(self, value, col, row, left):
            if (0 <= row
            and row < self.height - 1 ):
                self.vertical_bridges[col][row][left-1] = value

        def get_horizontal_bridge(self, col, row, top):
            return self.horizontal_bridges[col][row][top-1]

        def get_vertical_bridge(self, col, row, left):
            return self.vertical_bridges[col][row][left-1]

        def get_board(col, row):
            return self.boards[col][row]

        def set_board(board, col, row):
            self.boards[col][row] = board

        def is_modified():
            return self.modified

        def set_modified(mod):
            self.modified = mod

        def get_name():
            return self.name

        def set_name(new_name):
            self.name = new_name
            self.modified = True

        def objects_iterator():
            out = chain.from_iterable(zip(*self.boards))
            return list(out)

        def notes_iterator():
            return self.notes

        def add_Note(new_note):
            self.notes.add(new_note)
            self.modified = True

        def get_speech():
            return self.speech

        def set_speech(new_speech):
            self.speech = new_speech
            self.modified = True

        def get_file():
            return self.file

        def get_width():
            return self.width

        def get_height():
            return self.height

        def get_region():
            return self.region

        def set_region(new_region):
            if not new_region in self.region:
                self.region = new_region
                self.modified = True

        def save():
            try:
                Write.write(self)
                self.modified = False
            except:
                raise

