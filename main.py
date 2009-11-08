#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:08:29>
# last-update-time: <halida 11/08/2009 15:20:41>
# ---------------------------------
# 

from qtlib import *

import game,test_map1,test_module1

import game_viewer

import inv_viewer

class MessageViewer(QListWidget):
    MAX_COUNT = 20
    def __init__(self,g):
        super(MessageViewer,self).__init__()
        self.game = g
        connect(self.game,game.ONMESSAGE,self.showMsg)
        
    def showMsg(self,msg):
        self.insertItem(0,msg)
        if self.count() > self.MAX_COUNT:
            self.takeItem(self.MAX_COUNT)

class M(QMainWindow):
    def init(self):
        self.game = game.Game()
        self.game.loadMap(test_map1)
        self.game.loadModule(test_module1)
        self.gv = game_viewer.GameViewer(self.game)
        self.mv = MessageViewer(self.game)
        self.iv = inv_viewer.InvViewer(self.game)
        #layout
        self.setCentralWidget(self.gv)
        addDockWidget(self,'inventory viewer',self.iv)
        addDockWidget(self,'message viewer',self.mv)
        #event
        self.resize(800,600)
        self.show()

    def keyPressEvent(self,event):
        #change event to keymap
        key = event.key()
        mod = event.modifiers()
        sft = ctl = alt = False
        if mod & Qt.ShiftModifier  : sft = True
        if mod & Qt.ControlModifier: ctl = True	
        if mod & Qt.AltModifier	   : alt = True
        #change keymap to command
        self.game.evalKeymap(key,sft,ctl,alt)

def main():
    run(M)
    pass

if __name__=="__main__":
    main()
