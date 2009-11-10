#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/08 06:30:35>
# last-update-time: <halida 11/10/2009 11:18:32>
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
    game.levels = [
        random_map.createMap(map=map1,upP=(1,3)),
        random_map.randomMap(),
        random_map.randomMap(),
        random_map.randomMap(upStair=False),
        ]
    game.changeMap(level=0)
    game.pc.setPos(2,2)
