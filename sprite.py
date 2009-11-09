#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:25:07>
# last-update-time: <halida 11/08/2009 21:52:02>
# ---------------------------------
# 

class Sprite(object):
    def __init__(self,pos=(0,0)):
        self.data = None
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

    #pack and load
    def pack(self):
        return dict(pos=self.getPos(),data=self.data)
    @staticmethod
    def load(data):
        s = Sprite()
        s.setPos(*data['pos'])
        s.data=data['data']
        return s

