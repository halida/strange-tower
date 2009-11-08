#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:25:07>
# last-update-time: <halida 11/08/2009 14:25:01>
# ---------------------------------
# 

class Sprite(object):
    def __init__(self):
        self.setPos(0,0)
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
