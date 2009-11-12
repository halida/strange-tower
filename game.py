#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:14:40>
# last-update-time: <halida 11/12/2009 21:00:29>
# ---------------------------------
# 

from qtlib import *

from items import *
from keymap import *
from viewlib import *

import sprite,pc,maplib

#game events
PCMOVED = 'pcMoved()'
MAPCHANGED = 'mapChanged()'
ONMESSAGE = 'onMessage(QString)'
INVCHANGED = 'invChanged()'
SPRITECHANGED = 'spriteChanged(QString,int)'
STEPED = 'steped()'

#step updates
SPRITE_MOVE = 'spritemove'
SPRITE_DIE = 'spritedie'
SPRITE_CREATE = 'spritecreate'

class Game(QObject):
    ACTIVE_RANGE = 20
    def __init__(self):
        super(Game,self).__init__()
        self.uiwrapper = None
        self.userCmd = None
        self.map = None
        self.sprites = []
        self.pc = pc.PC()
        self.pcInv = []

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
        
    def checkPCCollideToMap(self):
        x,y = self.pc.px,self.pc.py
        try:
            if x<0 or y<0: raise
            result = maplib.collideToMap(self.map,x,y)
        except:
            self.msg('You don\'t want go out.')
            return True
        
        if result:
            self.msg('Opps,you hit a wall.')
        return result

    def step(self):
        #print "stepping.."
        
        #phase user command
        if self.userCmd: self.userCmd()

        #moving
        sprites = filter(lambda s:isinstance(s,sprite.LivingSprite),
                         self.sprites)
        sprites = filter(self.nearPC,sprites)
        for s in sprites:
            if s.moving: s.moving(self)
        sprites = filter(lambda s:s.toLoc!=None,
                         sprites)

        #check collide
        for s in sprites:
            if s == self.pc: self.checkPCCollideToMap()
            if not maplib.collideToMap(self.map,*s.toLoc):
                torgets = self.collide(s.toLoc)
                torgets = filter(lambda s:isinstance(s,sprite.LivingSprite),
                                 torgets)
                if not torgets:#no collide
                    s.moveTo(*s.toLoc)
                    s.toLoc = None
                    emit(self,SPRITECHANGED,SPRITE_MOVE,self.sprites.index(s))
                else:#collide to sprite
                    for t in torgets:
                        #attack
                        if t.group != s.group:
                            self.atk(s,t)

            #if pc moving
            if s == self.pc:
                #check whats on the ground
                sprites = self.collide(self.pc.getPos())
                for s in sprites:
                    if s!=self.pc:
                        emit(self,ONMESSAGE,s.getDesc())
                emit(self,PCMOVED)
        emit(self,STEPED)
        #print "stepped"

    def nearPC(self,s):
        return ((abs(self.pc.px - s.px) < self.ACTIVE_RANGE) and
                (abs(self.pc.px - s.px) < self.ACTIVE_RANGE))

    def collide(self,pos):
        return filter(lambda st:
                          st.getPos()==pos,
                      self.sprites,)

    def atk(self,s,d):
        #check if hit
        if randint(1,20) > s.hit - d.ac:
            self.msg('%s not hit.'%s.name)
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
                i = self.sprites.index(d)
                self.sprites.remove(d)
                emit(self,SPRITECHANGED,SPRITE_DIE,i)

