#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:14:40>
# last-update-time: <halida 11/10/2009 11:30:03>
# ---------------------------------
# 

from qtlib import *
from items import *

import sprite,pc

(PC_NOP,PC_MOVE,PC_SEARCH,
 PC_DOWNSTAIR,PC_UPSTAIR,
 PC_DROP,PC_PICKUP,
 ) = range(7)

#events
PCMOVED = 'pcMoved()'
MAPCHANGED = 'mapChanged()'
ONMESSAGE = 'onMessage(QString)'
INVCHANGED = 'invChanged()'
SPRITECHANGED = 'spriteChanged(int)'

class Game(QObject):
    def __init__(self,uiwrapper):
        super(Game,self).__init__()
        self.uiwrapper = uiwrapper
        uiwrapper.game = self
        self.map = None
        self.sprites = []
        self.pc = pc.PC()
        self.sprites.append(self.pc)
        self.pcCmd = None
        self.pcInv = []

    def loadModule(self,module):
        module.setGame(self)
        self.map = self.levels[self.currentLevel]

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
            
        elif cmd == PC_DOWNSTAIR:
            if self.map['downstair'] <> self.pc.getPos():
                self.msg('there is no downstair here.')
            else:
                self.changeMap(-1)
        elif cmd == PC_UPSTAIR:
            if self.map['upstair'] <> self.pc.getPos():
                self.msg('there is no upstair here.')
            else:
                self.changeMap(1)

        elif cmd == PC_DROP:
            item = self.pcInv.pop(args)
            s = sprite.Item(self.pc.getPos(),item)
            self.sprites.append(s)
            self.msg('drop item: '+s.getName())
            emit(self,INVCHANGED)
            emit(self,SPRITECHANGED,len(self.sprites)-1)

        elif cmd == PC_PICKUP:
            s = self.getSpriteByPos(*self.pc.getPos())
            if not s or not isinstance(s,sprite.Item):
                self.msg('Nothing on the groud.')
            else:
                self.msg('pick upped: %s'%s.getName())
                index = self.sprites.index(s)
                self.sprites.remove(s)
                self.pcInv.append(s.itemdata)
                emit(self,SPRITECHANGED,index)
                emit(self,INVCHANGED)

        else:
            raise Exception("this cmd not defined:",self.pcCmd)

    def getSpriteByPos(self,x,y):
        for s in self.sprites:
            if s == self.pc: continue
            if s.getPos() == (x,y):
                return s
        return None

    def changeMap(self,direct=None,level=None):
        #save old map
        if self.map:
            self.sprites.pop(0)#pop pc
            self.map['sprites'] = self.sprites
            self.sprites = []

        #load new map
        if direct:
            self.currentLevel += direct
        elif level<>None:
            self.currentLevel = level
        else:
            raise Exception('changeMap have no params!')
        self.map = self.levels[self.currentLevel]

        #set pc location
        if direct > 0:
            newloc = self.map['downstair']
        else:
            newloc = self.map['upstair']
        self.pc.setPos(*newloc)

        #set sprites
        if self.map.has_key('sprites'):
            self.sprites += self.map['sprites']
        self.sprites.insert(0,self.pc)

        #event
        self.msg("move to level:%d"%self.currentLevel)
        emit(self,MAPCHANGED)
        emit(self,PCMOVED)

    def msg(self,m):
        emit(self,ONMESSAGE,m)
        
    def checkCollideToMap(self,x,y):
        return self.map['map'][y][x] == '#'

    def evalKeymap(self,key,sft,ctl,alt):
        self.pcCmd = None
        #move
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

        #level up and down
        if key == Qt.Key_Less:
            self.pcCmd = PC_DOWNSTAIR,None
        if key == Qt.Key_Greater:
            self.pcCmd = PC_UPSTAIR,None

        #item pick up and drop
        if key == Qt.Key_D:
            itemNum = self.uiwrapper.selectItem()
            if itemNum<>None:
                self.pcCmd = PC_DROP,itemNum
        if key == Qt.Key_Comma:
            self.pcCmd = PC_PICKUP,None

        #quit
        if key == Qt.Key_Q and sft:
            sys.exit()

        if self.pcCmd:
            self.step()
