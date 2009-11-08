#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:14:40>
# last-update-time: <halida 11/08/2009 12:58:09>
# ---------------------------------
# 

from qtlib import *
import sprite

PC_NOP,PC_MOVE,PC_SEARCH = range(3)

#events
PCMOVED = 'pcMoved()'
ONMESSAGE = 'onMessage(QString)'

class Game(QObject):
    def __init__(self):
        super(Game,self).__init__()
        self.map = None
        self.sprites = []
        self.items = []
        self.pc = sprite.PC()
        self.pcCmd = None

    def loadMap(self,map):
        self.map = map.map.split('\n')
        self.pc.setPos(*map.pc_pos)
        self.sprites.append(self.pc)

    def step(self):
        #split cmd
        cmd, args = self.pcCmd
        if cmd == PC_MOVE:
            newlocation = (args[0] + self.pc.px,
                           args[1] + self.pc.py)
            if not self.checkCollideToMap(*newlocation):
                self.pc.move(*args)
                emit(self,PCMOVED)
            else:
                self.msg('Opps,you hit a wall.')

        elif cmd == PC_SEARCH:
            self.msg('Searching...')            
        else:
            raise Exception("this cmd not defined:",self.pcCmd)

    def msg(self,m):
        emit(self,ONMESSAGE,m)
        
    def checkCollideToMap(self,x,y):
        return self.map[y][x] == '#'

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
        elif key == Qt.Key_S:
            self.pcCmd = PC_SEARCH,None
        if self.pcCmd:
            self.step()
