#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/08 06:30:35>
# last-update-time: <halida 11/12/2009 23:05:54>
# ---------------------------------
# 

from items import *

import random_map,sprite

map1 = """
###################################.....
###################################.....
###################################.....
################################## .....
###################################.....
     ...................................
     ...................................
     ...................................
"""

map2 = """
........................................
..........###...........................
..........#.............................
..........###...........................
........................................
"""


INC = """
You saw a big tower stabing into the sky,
you want to seek out what's on its top.
and now, after several weeks prepaire,
you start journey to explore the unknown.
"""

END = """
this is the top of the tower,
you look into the sky,
only found darkness there.
eventhough you comes to this end,
the tower is still a mistery to you.
                    ----the end.
"""

def setGame(game):
    game.pc.inv = [
        I_ration,
        I_t_shirt,
        ]
    game.levels = []

    #button
    buttonMap = random_map.createMap(map=map1,upP=(34,3))
    buttonMap['sprites'].append(sprite.Sign(INC,(35,3)))
    buttonMap['sprites'].append(sprite.Foe((5,6),))
    buttonMap['sprites'].append(sprite.Foe((35,6),))
    game.levels.append(buttonMap)

    #levels
    #game.levels.append(random_map.randomBigMap())
    for i in range(2):
        map = random_map.randomMap()
        random_map.randomFoe(map)
        game.levels.append(map)

    #top
    topMap = random_map.createMap(map=map2,downP=(34,2))
    topMap['sprites'].append(sprite.Sign(END,(11,2)))
    game.levels.append(topMap)
    
    #init
    game.pc.setPos(2,6)
    game.changeMap(level=0)


