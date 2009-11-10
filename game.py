#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:14:40>
# last-update-time: <halida 11/10/2009 16:19:15>
# ---------------------------------
# 

from qtlib import *
from items import *

import sprite,pc

from keymap import *

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
        self.pcCmdPhaser = PCCmdPhaser(self)
        self.map = None
        self.sprites = []
        self.pc = pc.PC()
        self.sprites.append(self.pc)
        self.pcInv = []
        self.evalKeymap = self.pcCmdPhaser.evalKeymap

    def loadModule(self,module):
        module.setGame(self)
        self.map = self.levels[self.currentLevel]

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

class PCCmdPhaser():
    def __init__(self,g):
        self.g = g
        self.mapper = {
            PC_SEARCH                 : self.pcSearch,
            
            PC_MOVE_UP                : lambda :self.pcMove( 0,-1),
            PC_MOVE_DOWN              : lambda :self.pcMove( 0, 1),
            PC_MOVE_LEFT              : lambda :self.pcMove(-1, 0),
            PC_MOVE_RIGHT             : lambda :self.pcMove( 1, 0),

            PC_MOVE_UP_LEFT           : lambda :self.pcMove(-1,-1),
            PC_MOVE_UP_RIGHT          : lambda :self.pcMove( 1,-1),
            PC_MOVE_DOWN_LEFT         : lambda :self.pcMove(-1, 1),
            PC_MOVE_DOWN_RIGHT        : lambda :self.pcMove( 1, 1),

            PC_DOWNSTAIR              : lambda: self.pcStair(-1),
            PC_UPSTAIR                : lambda: self.pcStair( 1),

            PC_DROP                   : self.pcDrop,
            PC_PICKUP                 : self.pcPickup,
            PC_QUIT                   : self.pcQuit,
            
            }

    def evalKeymap(self,key,sft,ctl,alt):
        try:
            cmd = key2func[key]
        except:
            return
        self.phase(cmd)

    def phase(self,cmd):
        try:
            fun = self.mapper[cmd]
        except:
            raise Exception("this cmd not defined:",cmd)
        fun()

    def pcMove(self,dx,dy):
        newloc = (dx + self.g.pc.px,
                  dy + self.g.pc.py)
        if not self.g.checkCollideToMap(*newloc):
            self.g.pc.move(dx,dy)
            emit(self.g,PCMOVED)
        else:
            self.g.msg('Opps,you hit a wall.')
            
    def pcSearch(self):
        self.g.msg('Searching...')            
            
    def pcStair(self,stair):
        if stair == -1:
            if self.g.map['downstair'] <> self.g.pc.getPos():
                self.g.msg('there is no downstair here.')
            else:
                self.g.changeMap(-1)
        elif stair == 1:
            if self.g.map['upstair'] <> self.g.pc.getPos():
                self.g.msg('there is no upstair here.')
            else:
                self.g.changeMap(1)
        else:
            raise Exception("stair error:",stair)

    def pcDrop(self):
        i = self.g.uiwrapper.selectItem()
        if i==None: return
        item = self.g.pcInv.pop(i)
        s = sprite.Item(self.g.pc.getPos(),item)
        self.g.sprites.append(s)
        self.g.msg('drop item: '+s.getName())
        emit(self.g,INVCHANGED)
        emit(self.g,SPRITECHANGED,len(self.g.sprites)-1)

    def pcPickup(self):
        s = self.g.getSpriteByPos(*self.g.pc.getPos())
        if not s or not isinstance(s,sprite.Item):
            self.g.msg('Nothing on the groud.')
        else:
            self.g.msg('pick upped: %s'%s.getName())
            index = self.g.sprites.index(s)
            self.g.sprites.remove(s)
            self.g.pcInv.append(s.itemdata)
            emit(self.g,SPRITECHANGED,index)
            emit(self.g,INVCHANGED)
            
    def pcQuit(self):
        sys.exit(0)
