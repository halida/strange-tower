#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:25:07>
# last-update-time: <halida 11/13/2009 07:11:30>
# ---------------------------------
# 

class Sprite(object):
    def __init__(self,pos=(0,0)):
        self.setPos(*pos)
    # movable
    def setPos(self,x,y):
        self.px = x
        self.py = y
    def getPos(self):
        return self.px,self.py
    def move(self,x,y):
        self.px += x
        self.py += y
    def moveTo(self,x,y):
        self.px = x
        self.py = y

class Item(Sprite):
    view = 'item'
    ground = True
    def __init__(self,pos,itemdata):
        super(Item,self).__init__()
        self.itemdata = itemdata
        self.setPos(*pos)
    def getName(self):
        return self.itemdata['name']
    def getDesc(self):
        return "%s lays here." % self.getName()

class Stair(Sprite):
    ground = True
    def __init__(self,pos,upstair=False,downstair=False):
        super(Stair,self).__init__()
        self.upstair = upstair
        self.downstair = downstair
        self.setPos(*pos)
        if self.upstair:
            self.view = 'upstair'
        elif self.downstair:
            self.view = 'downstair'
    def getDesc(self):
        return "a staircase %s."% ('up' if self.upstair else 'down')

class Sign(Sprite):
    view = 'sign'
    def __init__(self,text,pos):
        super(Sign,self).__init__()
        self.text = text
        self.setPos(*pos)
    def getDesc(self):
        return "a sign: %s" % self.text

class LivingSprite(Sprite):
    group = 'base'
    moving = None
    def __init__(self):
        super(LivingSprite,self).__init__()
        self.hp = 10
        self.atk = (0,0); self.hit = 0
        self.abs = 0    ; self.ac  = 0
        self.toLoc = None
    def moveToUser(self,g):
        px,py = pp = g.pc.getPos()
        sx,sy = sp = self.getPos()
        tx,ty = self.directTo(px,py)
        self.toLoc = tx+sx,ty+sy
    def directTo(self,px,py):
        return cmp(px,self.px),cmp(py,self.py)

class Foe(LivingSprite):
    animate = True
    slide = 0
    group = 'foe'
    view = 'pc'
    size = (1,2)
    moving = LivingSprite.moveToUser
    name = "foe"
    def __init__(self,pos,hp=10,
                 atk=(1,2),hit=10,
                 abs=1,ac=5):
        super(Foe,self).__init__()
        self.setPos(*pos)
        self.hp = hp
        self.atk = atk
        self.hit = hit
        self.abs = abs
        self.ac = ac
    def getDesc(self):
        return "foe."

