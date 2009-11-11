#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/08 06:21:16>
# last-update-time: <halida 11/11/2009 10:12:06>
# ---------------------------------
# 

from sprite import *

class PC(LivingSprite):
    view = V_PC
    size = (1,2)
    name = "you"
    def __init__(self):
        super(PC,self).__init__()
        self.hp = 100
        self.atk = (1,10); self.hit = 20
        self.abs = 1    ; self.ac  = 5

    def getDesc(self):
        return "it's you."

