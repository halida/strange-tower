#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:25:07>
# last-update-time: <halida 11/07/2009 15:00:40>
# ---------------------------------
# 

class Sprite(object):
    def __init__(self):
        self.setPos(0,0)

    def setPos(self,x,y):
        self.px = x
        self.py = y

    def getPos(self):
        return self.px,self.py

    def move(self,x,y):
        self.px += x
        self.py += y

class PC(Sprite):
    def __init__(self):
        super(PC,self).__init__()
