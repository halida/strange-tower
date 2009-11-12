#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:14:40>
# last-update-time: <halida 11/13/2009 06:49:51>
# ---------------------------------
# 

from qtlib import *

from items import *
from keymap import *
from viewlib import *

import sprite,pc,maplib

#game events
ONMESSAGE = 'onMessage(QString)'
INVCHANGED = 'invChanged()'

MAPCHANGED = 'mapChanged()'
UPDATED = 'updated(QString,int)'#int is the sprite id
STEPED = 'steped()'

#game updates
SPRITE_MOVE_NONE = 'spritemovenone'
SPRITE_MOVE_LEFT = 'spritemoveleft'
SPRITE_MOVE_RIGHT = 'spritemoveright'
SPRITE_MOVE_UP = 'spritemoveup'
SPRITE_MOVE_DOWN = 'spritemovedown'

SPRITE_DIE = 'spritedie'
SPRITE_CREATE = 'spritecreate'

SPRITE_MOVES = (
    SPRITE_MOVE_NONE,
    SPRITE_MOVE_LEFT, 
    SPRITE_MOVE_RIGHT,
    SPRITE_MOVE_UP,  
    SPRITE_MOVE_DOWN, 
)

DIRECT_TO_EVENT = {
    (-1,-1):SPRITE_MOVE_LEFT,
    (-1, 0):SPRITE_MOVE_LEFT,
    (-1,+1):SPRITE_MOVE_LEFT,
    (+1,-1):SPRITE_MOVE_RIGHT,
    (+1, 0):SPRITE_MOVE_RIGHT,
    (+1,+1):SPRITE_MOVE_RIGHT,
    (0,-1):SPRITE_MOVE_UP,  
    (0, 0):SPRITE_MOVE_NONE,
    (0,+1):SPRITE_MOVE_DOWN, 
    }

class Game(QObject):
    ACTIVE_RANGE = 20
    def __init__(self):
        super(Game,self).__init__()
        self.uiwrapper = None
        self.userCmd = None
        self.map = None

        self.pc = pc.PC()
        self.sprites = []

    def loadModule(self,module):
        module.setGame(self)

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
        if direct:
            self.pc.setPos(*newloc)

        #set sprites
        if self.map.has_key('sprites'):
            self.sprites += self.map['sprites']
        self.sprites.insert(0,self.pc)

        #event
        self.msg("move to level:%d"%self.currentLevel)
        emit(self,MAPCHANGED)

    def msg(self,m):
        emit(self,ONMESSAGE,m)
        
    def step(self):
        #print "stepping.."
        
        #phase user command
        if self.userCmd: self.userCmd()

        #moving
        sprites = filter(lambda s:
                             isinstance(s,sprite.LivingSprite),
                         self.sprites)
        sprites = filter(self.nearPC,sprites)
        for s in sprites:
            if s.moving: s.moving(self)
        sprites = filter(lambda s:s.toLoc!=None,
                         sprites)

        #caution: if s die, s still can act.
        for s in sprites:
            self.checkSpriteMoving(s)

        emit(self,STEPED)
        #print "stepped"

    def checkSpriteMoving(self,s):
        #check map collide
        collide = maplib.collideToMap(self.map,*s.toLoc)
        #oops, cannot move
        if collide:
            if s == self.pc: 
                if type == maplib.COLLIDE_TO_WALL:
                    self.msg('Opps,you hit a wall.')
                elif type == maplib.COLLIDE_OUT_MAP:
                    self.msg('You don\'t want go out.')
            return

        #check sprite collide
        torgets = self.collideToSprite(s.toLoc)
        torgets = filter(
            lambda s:
                isinstance(s,sprite.LivingSprite),
            torgets)

        #when empty, sprite move
        if not torgets:
            direct = s.directTo(*s.toLoc)
            s.moveTo(*s.toLoc)
            movingEvent = DIRECT_TO_EVENT[direct]
            s.toLoc = None
            emit(self,UPDATED,
                 movingEvent,id(s))
            if s==self.pc: self.checkGroud()

        #when collide to sprite, attack
        else:
            for t in torgets:
                #attack
                if t.group != s.group:
                    self.atk(s,t); return#only attack once

    def checkGroud(self):
        sprites = self.collideToSprite(self.pc.getPos())
        for s in sprites:
            if s!=self.pc:
                emit(self,ONMESSAGE,s.getDesc())

    def nearPC(self,s):
        return ((abs(self.pc.px - s.px) < self.ACTIVE_RANGE) and
                (abs(self.pc.px - s.px) < self.ACTIVE_RANGE))

    def collideToSprite(self,pos):
        return filter(lambda st:
                          st.getPos()==pos,
                      self.sprites,)

    def atk(self,s,d):
        #check if hit
        if randint(1,20) > s.hit - d.ac:
            self.msg('%s not hit torget.'%s.name)
            return

        #hit
        hit = randint(*s.atk) - d.abs
        if hit <0: hit = 0
        d.hp -= hit
        self.msg("%s take %d damage from %s."%(d.name,hit,s.name))

        #die
        if d.hp <= 0:
            self.msg("%s die."%d.name)
            if d == self.pc:
                self.step = None#end game
            else:
                self.sprites.remove(d)
                emit(self,UPDATED,SPRITE_DIE,id(d))

    def spriteByID(self,ID):
        for s in self.sprites:
            if id(s) == ID: return s
