#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/12 12:38:55>
# last-update-time: <halida 11/12/2009 20:39:19>
# ---------------------------------
# 

from qtlib import *

import game

class MessageViewer(QListWidget):
    name = 'Message Viewer'
    MAX_COUNT = 20
    def __init__(self,g):
        super(MessageViewer,self).__init__()
        self.game = g
        connect(self.game,game.ONMESSAGE,self.showMsg)
        self.setMinimumSize(300,10)
        
    def showMsg(self,msg):
        self.insertItem(0,msg)
        self.setCurrentRow(0)
        if self.count() > self.MAX_COUNT:
            self.takeItem(self.MAX_COUNT)

