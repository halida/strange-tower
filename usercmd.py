#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
phase user action
"""

from keymap import *
from viewlib import *

import game

class UserCmd:
    def __init__(self,gv,game):
        #redirect gv key input
        gv.keyPressEvent = self.keyPressEvent

        self.game = game
        self.game.setUserCmd(self.phase)

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
        """
        eval cmd, and return if this cmd evaled
        """
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
        newloc = (dx + self.game.pc.px,
                  dy + self.game.pc.py)
        self.game.pc.toLoc = newloc
            
    def pcSearch(self):
        self.game.msg('Searching...')            
            
    def pcStair(self,stair):
        if stair == -1:
            if self.game.map['downstair'] <> self.game.pc.getPos():
                self.game.msg('there is no downstair here.')
            else:
                self.game.changeMap(-1)
        elif stair == 1:
            if self.game.map['upstair'] <> self.game.pc.getPos():
                self.game.msg('there is no upstair here.')
            else:
                self.game.changeMap(1)
        else:
            raise Exception("stair error:",stair)

    def pcDrop(self):
        i = self.game.uiwrapper.selectItem()
        if i==None: return
        item = self.game.pc.inv.pop(i)
        s = sprite.Item(self.game.pc.getPos(),item)
        self.game.sprites.append(s)
        self.game.msg('drop item: '+s.getName())
        emit(self.game,INVCHANGED)
        emit(self.game,UPDATED,SPRITE_CREATE,id(s))

    def pcPickup(self):
        s = self.game.getSpriteByPos(*self.game.pc.getPos())
        if not s or not isinstance(s,sprite.Item):
            self.game.msg('Nothing on the groud.')
        else:
            self.game.msg('pick upped: %s'%s.getName())
            index = self.game.sprites.index(s)
            self.game.sprites.remove(s)
            self.game.pc.inv.append(s.itemdata)
            emit(self.game,SPRITECHANGED,SPRITE_DIE,index)
            emit(self.game,INVCHANGED)

    def pcShoot(self):
        t = self.game.uiwrapper.selectTorget()
        if t==None: return
        self.game.atk(self.game.pc,t)
            
    def pcQuit(self):
        print "game ends, bye!"
        sys.exit(0)

    def keyPressEvent(self,event):
        #change event to keymap
        key = event.key()
        mod = event.modifiers()
        sft = ctl = alt = False
        if mod & Qt.ShiftModifier  : sft = True
        if mod & Qt.ControlModifier: ctl = True	
        if mod & Qt.AltModifier	   : alt = True

        #change keymap to command
        evaled = self.evalKeymap(key,sft,ctl,alt)

        #if not real time, game steps when user key event
        if not REAL_TIME and evaled:
            self.game.step()
            


