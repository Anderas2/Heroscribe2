# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 16:02:50 2019

@author: Andreas
"""

from xml.dom.minidom import parse
import xml.dom.minidom
from pathlib import Path

from src.heroscribe.list.LObject import LObject
from src.heroscribe.list.List import  List
from src.heroscribe.list.LBoard import LBoard
from src.heroscribe.list.Kind import Kind
from src.heroscribe.list.Icon import Icon

from src.heroscribe import Constants

class Read():

    def __init__(self, file_loc):

        self.object_list = List()
        self.piece = LObject()

        # There will be a board of type LBoard later, but not right now.
        #self.board
        self.content = ''
        # gives the state during parsing if we are on a board or not.
        self.on_board = False


        DomTree = xml.dom.minidom.parse(str(file_loc))
        object_xml = DomTree.documentElement
        #for key in object_xml._attrs.keys():
        self.object_list.version = object_xml.getAttribute('version')
        self.object_list.vector_prefix = object_xml.getAttribute('vectorPrefix')
        self.object_list.vector_suffix = object_xml.getAttribute('vectorSuffix')
        self.object_list.raster_prefix = object_xml.getAttribute('rasterPrefix')
        self.object_list.raster_suffix = object_xml.getAttribute('rasterSuffix')
        self.object_list.sample_prefix = object_xml.getAttribute('samplePrefix')
        self.object_list.sample_suffix = object_xml.getAttribute('sampleSuffix')

        # heroscribe folders
        for kind in object_xml.getElementsByTagName("kind"):
            kind_id = kind.getAttribute('id')
            kind_name = kind.getAttribute('name')
            self.object_list.kinds.add(Kind(kind_id, kind_name))


        # game boards
        for xmlboard in object_xml.getElementsByTagName("board"):
            self.object_list.board = self.read_xml_board(xmlboard)

        # other game pieces
        for xmlpiece in object_xml.getElementsByTagName("object"):
            piece = self.get_game_piece(xmlpiece)
            self.object_list.object_list[piece.id] = piece





    def get_game_piece(self, xmlpiece):
        piece = LObject()
        piece.id = xmlpiece.getAttribute("id")
        piece.name = xmlpiece.getAttribute("name")
        piece.kind = xmlpiece.getAttribute("kind")

        piece.door = xmlpiece.getAttribute("door")
        piece.trap = xmlpiece.getAttribute("trap")
        piece.u_trap = xmlpiece.getAttribute("untraceabletrap")

        piece.width = xmlpiece.getAttribute("width")
        piece.height = xmlpiece.getAttribute("height")
        piece.zorder = xmlpiece.getAttribute("zorder")
        piece.mini_icon = xmlpiece.getAttribute("miniIcon")

        # TODO: put tag dictionary into the xml file and read them here,
        # for better filter functions
        piece.tags  = xmlpiece.getAttribute("tags")

        for xmlicon in xmlpiece.getElementsByTagName("icon"):
            icon, region = self.read_xml_icon(xmlicon)
            piece.put_icon(icon, region)

        piece.note = self.get_notes(xmlpiece)
        return piece

    def get_notes(self, xml_anything):
        ''' extracts all text from all notes nodes in xml_anything'''
        notes = ''
        if xml_anything.getElementsByTagName("note"):
            for xmlnote in xml_anything.getElementsByTagName("note"):
                notes = notes + xmlnote.childNodes[0]._data
        return notes



    def read_xml_icon(self, xmlicon):
        '''reads an icon into the icon data structure and returns it
        '''

        path = xmlicon.getAttribute('path')
        xoffset = xmlicon.getAttribute('xoffset')
        if bool(xoffset):
            xoffset = float(xoffset)
        else:
            xoffset = 0
        yoffset = xmlicon.getAttribute('yoffset')
        if bool(yoffset):
            yoffset = float(yoffset)
        else:
            yoffset = 0
        original = xmlicon.getAttribute('original')
        original = original.lower in ['true']
        region = xmlicon.getAttribute('region')
        return Icon(path, xoffset, yoffset, original), region


    def read_xml_board(self, xmlboard):
        board = LBoard(xmlboard.getAttribute('width'),
                              xmlboard.getAttribute('height'))
        board.border_doors_offset = float(xmlboard.getAttribute("borderDoorsOffset"))
        board.adjacent_boards_offset = float(xmlboard.getAttribute('adjacentBoardsOffset'))
        board.name = xmlboard.getAttribute('name')
        board.default = xmlboard.getAttribute('default')

        for xmlicon in xmlboard.getElementsByTagName("icon"):
            icon, region = self.read_xml_icon(xmlicon)
            board.put_icon(icon, region)

        # corridors are defined to make them a little darker in the US version.
        for xmlcorridor in xmlboard.getElementsByTagName("corridor"):
            left = int(xmlcorridor.getAttribute("left"))
            top = int(xmlcorridor.getAttribute("top"))
            width = int(xmlcorridor.getAttribute("width"))
            height = int(xmlcorridor.getAttribute("height"))
            if (left + width -1 > board.width
            or left < 1
            or top + height -1 > board.width
            or top < 1):
                # TODO: Make a better understandable error message
                raise ValueError("Corridors: out of board border")

            # mark squares on board as corridor
            # TODO: Check corridor markings
            for x in range(0, width):
                for y in range(0, height):
                    board.corridors[x + left -1 ][y + top -1] = True


        for xmlroom in xmlboard.getElementsByTagName("room"):
            # TODO: For questimator extension, read rooms here
            pass
        return board



file_loc = Path('C:/Users/Andreas/25 Heroquest/Heroscribe 2/Sample.xml')
readfile = Read(file_loc)







