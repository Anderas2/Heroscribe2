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


'''The corridors are a list of lists currently:

corridors = [[]].
The outer list would be X, the inner list would be Y.
I don't know if that's intelligent.

I have seen that in the object.xml, for each board the corridors are defined.
I guess that's for the us-like coloring of corridors. Each square has a bool
value saying if it is a corridor or not.


The region currently is a _sorted dict_. It is the closest that I could find to
match the java treemap.
If it is set, I assign the input directly to a region key, resulting in
something like that:

region["square 1"] = "Goblin" (imagine an icon here)
resulting in
region = {"square 1": "Goblin"}

It might be more interesting to assign to a list of content so that you can
have several icons in one square.

region = {"square 1" : ["Goblin", "Carpet Room"]}

To keep in mind for later!
'''

from sortedcontainers import SortedDict # best fit for java TreeMap

class LBoard():
    def __init__(self, width, height):
        ''' defines a new board.

        :width: Board width in squares

        :height: Board height in squares
        '''
        self.region = SortedDict()

        if isinstance(width, int):
            self.width = width
        else:
            self.width = int(width)
        if isinstance(height, int):
            self.height = height
        else:
            self.height = int(height)

        self.borderDoorsOffset = 0
        self.adjacentBoardsOffset = 0

        # initializes the corridor matrix with "False";
        # width squares wide and height squares high.
        # attention, it's zero-based;
        # so the first square in the top left corner is [0][0]
        # and the last square in the lower right corner is [18][20]
        self.corridors = [[False for y in range(0, self.height)]
                                  for x in range(0, self.width)]





    def put_icon(self, icon, region_key):
        ''' takes an icon and puts it into the board dict at the specified
        region.

        :icon: An instance of Icon containing a game board

        :region_key: a string defining where to put the icon
        '''
        self.region[region_key] = icon

    def get_icon(self, region_key):
        ''' returns the icon if there is one in the region key.
        Else returns None.
        '''
        return self.region.get(region_key, None)
