#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/10 04:48:24>
# last-update-time: <halida 11/10/2009 15:02:19>
# ---------------------------------
# defines keymap

from qtlib import *

PC_FUNCS = (PC_NOP,PC_SEARCH,
            PC_MOVE_UP,PC_MOVE_DOWN,PC_MOVE_LEFT,PC_MOVE_RIGHT,
            PC_MOVE_UP_LEFT,PC_MOVE_UP_RIGHT,PC_MOVE_DOWN_LEFT,PC_MOVE_DOWN_RIGHT,
            PC_DOWNSTAIR,PC_UPSTAIR,
            PC_DROP,PC_PICKUP,
            PC_QUIT,
            ) = range(15)

func2key = {
    PC_SEARCH                 : Qt.Key_S,

    PC_MOVE_UP                : Qt.Key_K,
    PC_MOVE_DOWN              : Qt.Key_J, 
    PC_MOVE_LEFT              : Qt.Key_H,
    PC_MOVE_RIGHT             : Qt.Key_L,

    PC_MOVE_UP_LEFT           : Qt.Key_Y,
    PC_MOVE_UP_RIGHT          : Qt.Key_U,
    PC_MOVE_DOWN_LEFT         : Qt.Key_B,
    PC_MOVE_DOWN_RIGHT        : Qt.Key_N,

    PC_DOWNSTAIR              : Qt.Key_Less,
    PC_UPSTAIR                : Qt.Key_Greater,

    PC_DROP                   : Qt.Key_D,
    PC_PICKUP                 : Qt.Key_Comma,
    PC_QUIT                   : Qt.Key_Q,
}

def reverseDict(d):
    rd = {}
    for key,v in d.iteritems():
        if rd.has_key(key):
            raise Exception('Opps, reduplicate key to func: ',v)
        rd[v]=key
    return rd

key2func = reverseDict(func2key)

