#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:14:40>
# last-update-time: <halida 11/08/2009 17:45:09>
# ---------------------------------
# 

from qtlib import *
import sprite,pc

(PC_NOP,PC_MOVE,PC_SEARCH,PC_DOWNSTAIR,PC_UPSTAIR) = range(5)

#events
PCMOVED = 'pcMoved()'
MAPCHANGED = 'mapChanged()'
ONMESSAGE = 'onMessage(QString)'
ONINVCHANGE = 'onInvChange()'

class Game(QObject):
    def __init__(self):
        super(Game,self).__init__()
        self.map = None
        self.sprites = []
        self.items = []
        self.pc = pc.PC()
        self.sprites.append(self.pc)
        self.pcCmd = None
        self.pcinv = []

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
            if self.map[self.pc.py][self.pc.px] != '<':
                print self.map[self.pc.px][self.pc.px],self.pc.getPos()
                self.msg('there is no downstair here.')
            else:
                self.updateMap(-1)
        elif cmd == PC_UPSTAIR:
            if self.map[self.pc.py][self.pc.px] != '>':
                self.msg('there is no upstair here.')
            else:
                self.updateMap(1)

        else:
            raise Exception("this cmd not defined:",self.pcCmd)

    def updateMap(self,maplevel):
        self.currentLevel += maplevel
        self.map = self.levels[self.currentLevel]
        newloc = None
        for y,row in enumerate(self.map):
            for x,floor in enumerate(row):
                if maplevel > 0 and floor == '<':
                    newloc = x,y
                if maplevel < 0 and floor == '>':
                    newloc = x,y
        if not newloc:
            raise Exception('map do not have stairs, check the map!')
        self.pc.setPos(*newloc)
        emit(self,MAPCHANGED)
        emit(self,PCMOVED)
        print "map changed to level:",self.currentLevel

    def msg(self,m):
        emit(self,ONMESSAGE,m)
        
    def checkCollideToMap(self,x,y):
        return self.map[y][x] == '#'

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
        if key == Qt.Key_Comma:
            self.pcCmd = PC_DOWNSTAIR,None
        if key == Qt.Key_Period:
            self.pcCmd = PC_UPSTAIR,None

        #quit
        if key == Qt.Key_Q and sft:
            sys.exit()

        if self.pcCmd:
            self.step()
