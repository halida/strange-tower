#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/08 06:21:16>
# last-update-time: <halida 11/13/2009 06:23:33>
# ---------------------------------
# 

from sprite import *

class PC(LivingSprite):
    animate = True
    slide = 0
    group = 'pc'
    view = 'pc'
    size = (1,2)
    name = "you"

    def __init__(self):
        super(PC,self).__init__()
        self.hp = 1000
        self.atk = (1,10); self.hit = 20
        self.abs = 1    ; self.ac  = 5
        self.inv = []

    def getDesc(self):
        return "it's you."

