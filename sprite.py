#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:25:07>
# last-update-time: <halida 11/10/2009 11:29:41>
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
    def __init__(self,pos,itemdata):
        super(Item,self).__init__()
        self.itemdata = itemdata
        self.setPos(*pos)
    def getName(self):
        return self.itemdata['name']

class Stair(Sprite):
    def __init__(self,pos,upstair=False,downstair=False):
        super(Stair,self).__init__()
        self.upstair = upstair
        self.downstair = downstair
        self.setPos(*pos)
