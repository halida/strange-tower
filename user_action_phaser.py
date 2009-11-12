#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/12 12:44:22>
# last-update-time: <halida 11/12/2009 20:59:22>
# ---------------------------------
# 

from keymap import *
from viewlib import *

import game

class UserActionPhaser():
    def __init__(self,gv,g):
        #redirect gv key input
        gv.keyPressEvent = self.keyPressEvent

        self.g = g
        self.g.userCmd = self.phase

        self.cmd = None
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

            PC_SHOOT                  : self.pcShoot,

            PC_DROP                   : self.pcDrop,
            PC_PICKUP                 : self.pcPickup,
            PC_QUIT                   : self.pcQuit,
            
            }

    def evalKeymap(self,key,sft,ctl,alt):
        try:
            cmd = key2func[key]
        except:
            return
        self.cmd = cmd
        return True

    def phase(self):
        if not self.cmd: return
        cmd = self.cmd
        self.cmd = None
        try:
            fun = self.mapper[cmd]
        except:
            raise Exception("this cmd not defined:",cmd)
        fun()

    def pcMove(self,dx,dy):
        newloc = (dx + self.g.pc.px,
                  dy + self.g.pc.py)
        self.g.pc.toLoc = newloc
            
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
        emit(self.g,SPRITECHANGED,SPRITE_CREATE,len(self.g.sprites)-1)

    def pcPickup(self):
        s = self.g.getSpriteByPos(*self.g.pc.getPos())
        if not s or not isinstance(s,sprite.Item):
            self.g.msg('Nothing on the groud.')
        else:
            self.g.msg('pick upped: %s'%s.getName())
            index = self.g.sprites.index(s)
            self.g.sprites.remove(s)
            self.g.pcInv.append(s.itemdata)
            emit(self.g,SPRITECHANGED,SPRITE_DIE,index)
            emit(self.g,INVCHANGED)

    def pcShoot(self):
        t = self.g.uiwrapper.selectTorget()
        if t==None: return
        self.g.atk(self.g.pc,t)
            
    def pcQuit(self):
        sys.exit(1)

    def keyPressEvent(self,event):
        #change event to keymap
        key = event.key()
        mod = event.modifiers()
        sft = ctl = alt = False
        if mod & Qt.ShiftModifier  : sft = True
        if mod & Qt.ControlModifier: ctl = True	
        if mod & Qt.AltModifier	   : alt = True

        #change keymap to command
        r = self.evalKeymap(key,sft,ctl,alt)

        #if not real time, game step when user key event
        if not REAL_TIME: 
            if r: self.game.step()
