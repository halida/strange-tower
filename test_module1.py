#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/08 06:30:35>
# last-update-time: <halida 11/10/2009 12:42:31>
# ---------------------------------
# 

from items import *

import random_map

map1 = """
########################################
#                                      #
#                                      #
#                                      #
#                                      #
#                                      #
########################################
"""

def setGame(game):
    game.pcInv = [
        I_ration,
        I_t_shirt,
        ]
    game.levels = []
    game.levels.append(random_map.createMap(map=map1,upP=(1,3)))
    for i in range(12):
        game.levels.append(random_map.randomMap())
    game.levels.append(random_map.randomMap(upStair=False))

    game.changeMap(level=0)
    game.pc.setPos(2,2)
