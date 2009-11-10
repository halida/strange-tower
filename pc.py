#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/08 06:21:16>
# last-update-time: <halida 11/10/2009 17:05:27>
# ---------------------------------
# 

from sprite import *

class PC(Sprite):
    view = V_PC
    size = (1,2)
    def __init__(self):
        super(PC,self).__init__()
    def getDesc(self):
        return "it's you."
