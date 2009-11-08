#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:14:40>
# last-update-time: <halida 11/08/2009 12:22:15>
# ---------------------------------
# 

from qtlib import *
import sprite

PC_NOP,PC_MOVE = range(2)

#events
PCMOVED = 'pcMoved()'

class Game(QObject):
    def __init__(self):
        super(Game,self).__init__()
        self.map = None
        self.sprites = []
        self.items = []
        self.pc = sprite.PC()
        self.pcCmd = None

    def loadMap(self,map):
        self.map = map.map
        self.pc.setPos(*map.pc_pos)
        self.sprites.append(self.pc)

    def step(self):
        #pc cmd
        cmd, args = self.pcCmd
        if cmd == PC_MOVE:
            self.pc.move(*args)
        emit(self,PCMOVED)

    def evalKeymap(self,key):
        self.pcCmd = None
        if key == Qt.Key_J:
            self.pcCmd = PC_MOVE,(0,1)
        elif key == Qt.Key_K:
            self.pcCmd = PC_MOVE,(0,-1)
        elif key == Qt.Key_H:
            self.pcCmd = PC_MOVE,(-1,0)
        elif key == Qt.Key_L:
            self.pcCmd = PC_MOVE,(1,0)
        if self.pcCmd:
            self.step()
