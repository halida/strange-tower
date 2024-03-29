#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/08 06:42:37>
# last-update-time: <halida 11/12/2009 21:04:53>
# ---------------------------------
# 

from qtlib import *

from items import *

import game

class InvViewer(QListWidget):
    name = "Inventory Viewer"
    def __init__(self,g):
        super(InvViewer,self).__init__()
        self.game = g
        connect(self.game,game.INVCHANGED,self.updateInv)
        self.updateInv()

    def updateInv(self):
        self.clear()
        for item in self.game.pc.inv:
            self.addItem(item[NAME])


