# -*- coding: utf-8 -*-
""""
  HeroScribe2
  Copyright (C) 2019 Andreas Wagener and Shane Adams
  Heroscribe 1 was by Flavio Chierichetti and Valerio Chierichetti

  This module can parse a heroscribe 1 or heroscribe 2 quest xml file.

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

from xml.dom.minidom import parse
import xml.dom.minidom
from pathlib import Path
import sys.stderr as err

from src.heroscribe.helper.OS_Helper import OS_Helper
from src.heroscribe.list.LObject import LObject
from src.heroscribe.list.List import  List
from src.heroscribe.list.LBoard import LBoard
from src.heroscribe.list.Kind import Kind
from src.heroscribe.list.Icon import Icon
from src.heroscribe.quest.Quest import Quest
from src.heroscribe.quest.QBoard import QBoard
from src.heroscribe.quest.QObject import QObject

class ReadQuest():
    def __init__(self, file_loc, objects):
        self.quest
        self.objects = objects # of type Heroscribe.list.List
        self.content = ''
        self.file_loc = file_loc
        self.board #of type QBoard
        self.width = 0
        self.height = 0
        self.board_count = 0

        DomTree = xml.dom.minidom.parse(str(file_loc))
        xml_questfile = DomTree.documentElement

        version = float(xml_questfile.getAttribute('version'))
        if version <= 1:
            self.read_version_one_file(xml_questfile)
            self.version = version
        else:
            self.read_version_two_file(xml_questfile)
        self.quest.set_modified(False)




    def read_version_one_file(self, xml_questfile):
        name = xml_questfile.getAttribute('name')
        region = xml_questfile.getAttribute('region')

        width = int(xml_questfile.getAttribute('width'))
        height = int(xml_questfile.getAttribute('height'))
        width = 1 if width < 1 else width
        height = 1 if height < 1 else height
        boardname = xml_questfile.getAttribute('boardname')
        if boardname == '':
            boardname = "HeroQuest"
        if len(region) == 0:
            region = "Europe"
        if name == "":
            name = "Quest"
        self.board_count = 0

        self.quest = Quest(file = self.file_loc,
                         width = width,
                         height = height,
                         board = self.objects.get_board(),
                         name = name,
                         region = region)
        xml_board = xml_questfile.getElementsByTagName("board")[0]
        self.read_board(xml_board)

    def read_board(self, xml_board):
        if self.board_count > (self.width * self.height):
            raise NameError("Too many boards in this quest")
        self.board = QBoard(self.objects.get_board.width,
                            self.objects.get_board.height,
                            self.quest)

        self.quest.set_board(self.board,
                             self.board_count % self.width,
                             int(self.board_count / self.width)
                             )
        self.board_count += 1

        for xml_bridge in xml_board.getElementsByTagName("bridge"):
            pass

        if xml_board.getElementsByTagName("dark"):
            for xml_dark in  xml_board.getElementsByTagName("dark"):
                self.read_dark(xml_dark)

        if xml_board.getElementsByTagName("object"):
            for xml_piece in xml_board.getElementsByTagName("object"):
                self.read_piece(xml_piece)


    # Heroscribe 2 stuff
    def read_subtitle(self, xml_subtitle):
        # mini headline, centered ("Quest 03 - Group Quest") in Caxton BK BT
        pass

    def read_title(self, xml_title):
        #real headline, centered ("The Candlestick Laboratory") in Zapf Chancery Medium Italic
        pass

    def read_questtext(self, xml_questtext):
        # quest text: two paragraphs ("Look out heroes, all the candlesticks in Castle of Candle.") in Caxton BK BT
        pass

    def read_notes(self, xml_notes):
        # Single letters at the beginning of a phrase (A:) are formatted like Mark A in US format, or as normal but fat letter in EU format, in ITCClearface or even better, in HQModern.
        # shall understand the us divider line
        pass

    def read_specialmonsters(self, xml_monsters):
        # This little stat line that you can find in quest notes.
        # line above, then headline row, then stats, then line below. ITCCLearface or HQModern. Pink for US, Dark brown for EU.
        pass
    def read_wanderingmonster(self, xml_wanderingmonster):
        # To format the wandering monster of the quest.
        pass



    def read_piece(self, xml_piece):
        att = xml_piece._attrs
        piece = QObject(att['id']._value, self.objects)
        if self.objects.get_object(piece.id) == None:
            raise NameError("Can't find ", piece.id)
            # TODO: Offer something more friendly here! New icon,
            # icon reuse, whatever is not a softwarebreaking failure message!

        if "zorder" in att.keys():
            piece.zorder = float(att['zorder']._value)
        else:
            piece.zorder = self.objects.get_object(piece.id).zorder

        piece.left = int(float(att['left']._value))
        piece.top = int(float(att['top']._value))

        rotation = att['rotation']._value
        if "downward" in rotation:
            piece.rotation = 0
        elif "rightward" in rotation:
            piece.rotation = 1
        elif "upward" in rotation:
            piece.rotation = 2
        elif "leftward" in rotation:
            piece.rotation = 3
        else:
            piece.rotation = 0
            err.write("set rotation to downward for ", piece.id)

        if self.board.add_object(piece) == False:
            err.write("ignoring ", piece.id, "because an exact copy is already in the same place")



    def read_dark(self, xml_dark):
        width = int(xml_dark.getAttribute('width'))
        height = int(xml_dark.getAttribute('height'))
        left = int(xml_dark.getAttribute('left'))
        top = int(xml_dark.getAttribute('top'))

        if (left + width -1 > self.objects.get_board().width
        or left < 1
        or top + height - 1 > self.objects.get_board().height
        or top < 1):
            raise NameError("Darkened squares seem to be out of the Board area")
        for x in range(0, width):
            for y in range(0, height):
                if not self.board.isDark(left + x, top + y):
                    self.board.toggleDark(left + x, top + y)


    def get_quest(self):
        return self.quest

