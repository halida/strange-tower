#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:14:40>
# last-update-time: <halida 11/12/2009 20:17:27>
# ---------------------------------
# 

from qtlib import *

from items import *
from keymap import *
from viewlib import *

import sprite,pc,maplib

#events
PCMOVED = 'pcMoved()'
MAPCHANGED = 'mapChanged()'
ONMESSAGE = 'onMessage(QString)'
INVCHANGED = 'invChanged()'
SPRITECHANGED = 'spriteChanged(QString,int)'
STEPED = 'steped()'

SPRITE_MOVE = 'spritemove'
SPRITE_DIE = 'spritedie'
SPRITE_CREATE = 'spritecreate'

class Game(QObject):
    RANGE = 20
    REAL_TIME = True
    def __init__(self):
        super(Game,self).__init__()
        self.uiwrapper = None
        self.pcCmdPhaser = PCCmdPhaser(self)
        self.evalKeymap = self.pcCmdPhaser.evalKeymap
        self.map = None
        self.sprites = []
        self.pc = pc.PC()
        self.pcInv = []
        self.inputEnable = True

    def loadModule(self,module):
        module.setGame(self)
        if self.REAL_TIME:self.running()

    def running(self):
        self.timer = QTimer()
        connect(self.timer,"timeout()",self.step)
        self.timer.start(800)

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
        if self.REAL_TIME:
            self.pcCmdPhaser.phase()

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
        return ((abs(self.pc.px - s.px) < self.RANGE) and
                (abs(self.pc.px - s.px) < self.RANGE))

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

class PCCmdPhaser():
    def __init__(self,g):
        self.g = g
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
        if not self.g.REAL_TIME:
            if not self.g.inputEnable: return
            self.phase()
            self.g.step()

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
        sys.exit(0)
