# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 12:48:13 2019

@author: Andreas
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