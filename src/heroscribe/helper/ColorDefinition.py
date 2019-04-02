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

from matplotlib.colors import LinearSegmentedColormap as LSC

class ColorSchemes():

    def __init__(self, style = "Europe"):

        c_furniture_grey
        c_furniture_brown
        c_monster
        c_hero
        c_trap
        c_trap_untraceable
        c_room
        c_corridor
        c_dark
        c_mini

    def make_a_gradient(self, dark, bright, name, gradient_dict, rgbs):

        gradient_dict[name] = LSC.from_list(gradient_name,
                                        [(0, colors[dark]),
                                         (0.55, colors[dark]),
                                         (1, colors[bright])],
                                         N=256
                                        )
        rgbs[name] = {'dark':colors[dark],
                    'bright':colors[bright]}


    def us_colors(self):

        # colors taken from http://www.heroscribe.org/help.html#New%20icons
        colors = {
        'white':(1.,1.,1.),
        'black':(0.,0.,0.),

        'maroon': self.tuple_mult((153, 67, 100,), 1./255),
        'light maroon': self.tuple_mult((194, 145, 156,), 1./255),

        'beige': self.tuple_mult((244, 231, 223,), 1./255),

        'trapped_orange': self.tuple_mult((250, 124, 50,), 1./255),
        'untraceable_green': self.tuple_mult((193, 232, 211,), 1./255),

        'red_hero': self.tuple_mult((201, 22, 58,), 1./255),

        'us_green': self.tuple_mult((100, 160, 110,), 1./255),

        'us_corridor': self.tuple_mult((225, 211, 210,), 1./255),
        'us_corridor_square_border': self.tuple_mult((186, 158, 154,), 1./255),
        'us_room_square_border': self.tuple_mult((212, 196, 193,), 1./255),
        'us_room_border': self.tuple_mult((95, 35, 24,), 1./255),
        }
        self.colors = colors

        gradients = {}
        rgbs = {}
###############################################################################
        make_a_gradient(colors['maroon'], colors['beige'],
                        name='furniture_grey', gradients, rgbs)
        make_a_gradient(colors['maroon'], colors['beige'],
                        name='furniture_brown', gradients, rgbs)

        make_a_gradient(colors['us_green'], colors['white'],
                        name='monster', gradients, rgbs)

        make_a_gradient(colors['maroon'], colors['trapped_orange'],
                        name='trap', gradients, rgbs)
        make_a_gradient(colors['maroon'], colors['untraceable_green'],
                        name='trap_untraceaple', gradients, rgbs)

        make_a_gradient(colors['red_hero'], colors['white'],
                        name='hero', gradients, rgbs)

        make_a_gradient(colors['black'], colors['white'],
                        name='mini', gradients, rgbs)

        make_a_gradient(colors['black'], colors['white'],
                        name='room', gradients, rgbs)

        make_a_gradient(colors['black'], colors['white'],
                        name='corridor', gradients, rgbs)

        make_a_gradient(colors['black'], colors['white'],
                        name='darksquare', gradients, rgbs)


###############################################################################
        self.gradients = gradients
        self.gradient_names = gradients.keys()
        self.rgbs = rgbs

        # Make a look up table that I can use later to
        # enhance contrast a little bit. LUT means Look up table
        LUT=np.zeros(256,dtype=np.uint8)
        LUT[10:235+1]=np.linspace(start=0,stop=255,
                                num=(235-10)+1,
                                endpoint=True,dtype=np.uint8)
        LUT[-20:]=255
        self.__LUT = LUT


    def alternate_gradients(self):
        colors = {
        'white':(1., 1., 1.),
        'black':(0.,0.,0.),
        'red_dark':(0.6, 0.122, 0.122),
        'red_light':(1.0, 0.325, 0.325),
        'red_medium':(0.8, 0.0, 0.0),
        'orange_dark':(0.631, 0.459, 0.0),
        'orange_light':(1.0, 0.835, 0.396),
        'orange_medium':(0.878, 0.639, 0.0),
        'yellow_dark':(0.773, 0.769, 0.298),
        'yellow_light':(0.996, 0.992, 0.647),
        'yellow_medium':(1.0, 0.965, 0.0),
        'green_dark':(0.149, 0.549, 0.055),
        'green_light':(0.533, 1.0, 0.427),
        'green_medium':(0.149, 0.8, 0.0),
        'turqoise_dark':(0.0, 0.541, 0.471),
        'turqoise_light':(0.522, 1.0, 0.937),
        'turqoise_medium':(0.251, 0.906, 0.929),
        'blue_dark':(0.137, 0.467, 0.871),
        'blue_light':(0.631, 0.812, 1.0),
        'blue_medium':(0.392, 0.651, 1.0),
        'violet_dark':(0.329, 0.243, 0.867),
        'violet_light':(0.773, 0.733, 1.0),
        'violet_medium':(0.596, 0.529, 1.0),
        'pink_dark':(0.686, 0.0, 0.749),
        'pink_light':(0.973, 0.675, 1.0),
        'pink_medium':(0.941, 0.443, 0.984),
                }
        self.colors = colors


        gradients = {}
        rgbs = {}
        for color in colors:
            for color2 in colors:
                if color2 == 'white' or color == 'black':
                    make_a_gradient(color, color2,
                                    cymks, gradients, rgbs, icons, variant)
        self.gradients = gradients
        self.gradient_names = gradients.keys()
        self.cymks = cymks
        self.rgbs = rgbs
        self.icons = icons
        self.variant = variant


        # Make a look up table to
        # enhance contrast a little bit. LUT means Look up table
        LUT=np.zeros(256,dtype=np.uint8)
        LUT[10:235+1]=np.linspace(start=0,stop=255,
                                num=(235-10)+1,
                                endpoint=True,dtype=np.uint8)
        LUT[-20:]=255
        self.__LUT = LUT
