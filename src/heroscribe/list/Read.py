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

from src.heroscribe.list import LObject, LBoard, List, Kind, Icon
from src.heroscribe import Constants

import xml.sax

class Read():

    def __init__(self, file_loc):

        self.object_list = List()
        self.piece = LObject()

        self.board = LBoard()
        self.content = ''
        self.on_board = False # gives the state during parsing if we are on a
                                # board or not.

        parser = xml.sax.make_parser()
        # did not find a "setValidation" function
        parser.parse(file_loc)





    def get_objects(self):
        return self.object_list

    def resolve_entity(self, public_id, system_id):
        ''' checks if the input file is indeed our object.xml,
        if it has version 1.5;
        switches to old "InputSource" if it is version 1.5.
        '''
        if ( public_id == "-//org.lightless//HeroScribe Object List 1.5//EN"):
            return xml.sax.InputSource("DtdXsd/objectList-1.5.dtd")
        else:
            return None

    def start_document(self):
        self.content = ''
        self.on_board = False;

    def start_element(self, uri, local_name, q_name, attrs):
        ''' takes the output of the sax parser and treats the content depending
        on the "q_name".
        Normally "q_name" should be objectList, board, object or note.
        '''
        self.content = ''
        if q_name == "objectList":
            self.object_list.version = attrs.getValue("version")
            if not self.object_list.version == Constants.version:
                raise xml.sax.SAXException(
                "HeroScribe's and Objects.xml's version numbers don't match.")

            self.object_list.vectorPrefix = attrs.getValue("vectorPrefix")
            self.object_list.vectorPrefix = attrs.getValue("vectorSuffix")
            self.object_list.vectorPrefix = attrs.getValue("rasterPrefix")
            self.object_list.vectorPrefix = attrs.getValue("vectorSuffix")
            self.object_list.vectorPrefix = attrs.getValue("samplePrefix")
            self.object_list.vectorPrefix = attrs.getValue("vectorSuffix")

        elif q_name == "kind":
            self.object_list.kinds.add(Kind(attrs.getValue("id"),
                                            attrs.getValue("name")))

        elif q_name == "board":
            board = LBoard(int(attrs.getValue("width")),
                           int(attrs.getValue("height")))
            board.border_doors_offset = float(
                                        attrs.getValue("borderDoorsOffset"))
            board.adjacent_boards_offset = float(
                                    attrs.getValue("adjacentBoardsOffset"))
            self.on_board = True

        elif q_name == "object":
            piece = LObject()
            piece.id = attrs.getValue("id")
            piece.name = attrs.getValue("name")
            piece.kind = attrs.getValue("kind")
            piece.door = bool(attrs.getValue("door").lower() in ["true", "door"])
            piece.trap = bool(attrs.getValue("trap").lower() in ["true", "trap"])
            piece.width = int(attrs.getValue("width"))
            piece.height = int(attrs.getValue("height"))
            piece.zorder = int(attrs.getValue("zorder"))
            piece.note = None
            self.piece = piece

        elif q_name == "icon":
            icon = Icon()
            icon.path = attrs.getValue("path")
            icon.path = attrs.getValue("xoffset")
            icon.path = attrs.getValue("yoffset")
            icon.path = bool(attrs.getValue("original").lower() in ["true", "original"])
            if self.on_board:
                board.putIcon(icon, attrs.getValue("region"))
            else:
                self.piece.putIcon(icon, attrs.getValue("region"))

        elif q_name == "corridor":
            if self.on_board:
                width = int(attrs.getValue("width"))
                height = int(attrs.getValue("height"))
                left = int(attrs.getValue("left"))
                top = int(attrs.getValue("top"))

                if (left + width > board.width
                or left < 1
                or top + height > board.width
                or top < 1):
                    raise xml.sax.SAXException(
                                            "Corridors: out of board border")

                for x in range(0, width):
                    for y in range(0, height):
                        self.board.corridors[x + left][y + top] = True
        else:
            # if q_name is something unknown, don't treat it.
            # TODO: include "room"?
            # TODO: include monster fight values?
            pass



    def end_element(self, uri, local_name, q_name):
        ''' at the end of an element, check if it has both layouts.
        If yes, store in the appropriate data structure

        :uri: unused?

        :local_name: unused?

        :q_name: name of the overarching element in object.xml.
            can be "board", "object", or "note"
        '''
        if q_name == "board":
            # check if both layouts are there
            if ("Europe" not in self.board.region.keys()
            and "USA" not in self.board.region.keys() ):
                raise xml.sax.SAXException("There should be an icon for Europe and one for USA for each board.")

            self.object_list.board = self.board
            self.on_board = False

        elif q_name == "object":
            if ("Europe" not in self.piece.region.keys()
            and "USA" not in self.piece.region.keys() ):
                raise xml.sax.SAXException("There should be an icon for Europe and one for USA for each board.")

            self.object_list.object_list[self.piece.id] = self.piece

        elif q_name == "note":
            self.piece.note = self.content

    def end_document(self):
        self.content = None
        self.piece = None




    def error(self, e):
        raise xml.sax.SAXParseException(e);

    def characters(self, in_str, start=None, length=None):
        ''' appends in_str at position start, with a certain
        length of length'''
        # TODO: this function seems to be unused! Confirm and remove this function
        self.content = self.content + in_str # dummy to preserve base functionality
