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

from sortedcontainers import SortedDict


# FIXME: Make helper_os! name it differently than "os" to avoid clashes with the
# python class "os"!

# TODO: reduce the six-fold-symbol madness if possible

# TODO: find out where this is used.

# TODO: Reduce the java style madness if possible
from src.heroscribe.helper.OS import os as helper_os

class List():
    ''' stores objects and returns them or their path on request.
    '''
    def __init__(self):
        self.board = None
        self.object_list = SortedDict()
        self.kinds = set() # Java Treeset is sorted, i do that in the getter
        self.version = None
        self.vector_prefix = ""
        self.vector_suffix = ""
        self.raster_prefix = ""
        self.raster_suffix = ""
        self.sample_prefix = ""
        self.sample_suffix = ""


    def objects_iterator(self):
        ''' returns all values in this list, unique, sorted by value.
        '''
        # TODO: Not sure this works, testing necessary!
        # apparently there are objects of type LObject stored in the object
        # list.
        return sorted(set(self.object_list.values()))

    # This method is used here and in GUI.
    def kinds_iterator(self):
        ''' returns an iterable sorted list of the kinds.
        Not sure I need this function in python to be honest
        '''
        return list(sorted(self.kinds))


    def get_object(self, obj_id):
        ''' using get instead of addressing via []
        makes it secure. Returns None if the object is not found.
        '''
        return self.object_list.get(obj_id, None)


    def get_board(self):
        ''' java-type getter for the board variable. Absolutely not
        needed in python, but...
        '''
        return self.board


    def get_kind(self, kind_id):
        ''' function to search a "kind" by ID.
        Necessary only because it is a java style class not a python built-in
        datatype.
        '''
        iterator = self.kindsIterator()
        found = None
        for item in iterator:
            if kind_id == item.id:
                found = item
                break
        return found


    def get_vector_path(self, obj_id = None, region_key = None):
        ''' gets the path of the vector graphic either from the object list
        or from the board; while the region key gives the EU or US version.
        '''
        if obj_id == None:
            return helper_os.get_absolute_path(self.vector_prefix +
                         self.get_board().get_icon(region_key).path +
                         self.vector_suffix)
        else:
            return helper_os.get_absolute_path(self.vector_prefix +
                         self.get_object(obj_id).get_icon(region_key).path +
                         self.vector_suffix)


    def get_raster_path(self, obj_id = None, region_key = None):
        ''' gets the path of the raster graphic either from the object list
        or from the board; while the region key gives the EU or US version.
        '''
        if obj_id == None:
            return helper_os.get_absolute_path(self.raster_prefix +
                         self.get_board().get_icon(region_key).path +
                         self.raster_suffix)
        else:
            return helper_os.get_absolute_path(self.raster_prefix +
                         self.get_object(obj_id).get_icon(region_key).path +
                         self.raster_suffix)


    def get_sample_path(self, obj_id = None, region_key = None):
        ''' gets the path of the sample graphic either from the object list
        or from the board; while the region key gives the EU or US version.
        '''
        if obj_id == None:
            return helper_os.get_absolute_path(self.sample_prefix +
                         self.get_board().get_icon(region_key).path +
                         self.sample_suffix)
        else:
            return helper_os.get_absolute_path(self.sample_prefix +
                         self.get_object(obj_id).get_icon(region_key).path +
                         self.sample_suffix)

