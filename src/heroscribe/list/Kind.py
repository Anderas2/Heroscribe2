# -*- coding: utf-8 -*-
""""
  HeroScribe2
  Copyright (C) 2019 Andreas Wagener and Shane Adams

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

class Kind():
    # class variable shared by all instances
    count = 0

    def __init__(self, kind_id, name):
        ''' stores id, name and the order.
        Like that the folders can be rearranged. '''
        self.id = kind_id
        self.name  = name
        self.order = self.__get_order()

    # two underlines in the beginning make it moderately private
    def __get_order(self):
        ''' counts the class variable 'count' one higher and
        returns it.'''
        Kind.count += 1
        return Kind.count

    def compareTo(self, other_kind):
        ''' checks the order of two kinds and returns a comparison value'''
        if not isinstance(other_kind, Kind):
            raise NameError('comparing a Kind is possible only with another Kind')
        if self.order < other_kind.order:
            return -1
        elif self.order > other_kind.order:
            return 1
        else:
            return 0

    # now what happens if someone external casts to string?
    def __str__(self):
        return self.name