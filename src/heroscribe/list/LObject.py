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

from sortedcontainers import SortedDict # best fit for java TreeMap

class LObject():
    def __init__(self):
        self.region = SortedDict()
        self.id = ''
        self.name = ''
        self.kind = None
        self.note = None
        self.height = 0
        self.width = 0
        self.zorder = 0
        self.door = False
        self.trap = False

    def put_icon(self, icon, region_key):
        ''' takes an icon and puts it into the board dict at the specified
        region.

        :icon: An instance of Icon

        :region_key: a string defining where to put the icon
        '''
        # TODO: I set a square = an icon. That means there can be one value per
        # region key only.
        # We need to see later if there should rather be a list of icons in
        # each square?
        self.region[region_key] = icon


    def get_icon(self, region_key):
        ''' returns the icon if there is one in the region key.
        Else returns None.
        '''
        return self.region.get(region_key, None)

    def compareTo(self, other_l_object):
        ''' compares the names of two LObjects in order to enable alphabetical
        sorting.
        '''
        # TODO: Enable custom sorting ?
        if not isinstance(other_l_object, LObject):
            raise NameError('comparing a LObject is possible only with another LObject')
        if self.name.lower() < other_l_object.name.lower():
            return -1
        elif self.name.lower() > other_l_object.name.lower():
            return 1
        else:
            return 0


    def __str__(self):
        return self.name
