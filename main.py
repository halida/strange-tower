#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:08:29>
# last-update-time: <halida 11/11/2009 17:35:44>
# ---------------------------------
# 

from qtlib import *
from items import *

import game,test_module1

import game_viewer,inv_viewer,smallmap

class UiWrapper():
    def selectItem(self):
        itemlist = [i[NAME] for i in self.game.pcInv]
        if len(itemlist) <= 0:
            return 
        n,ok = QInputDialog.getItem(None,'','select item:',itemlist,0,False)
        if ok:
            return itemlist.index(n)
            
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

class M(QMainWindow):
    def init(self):
        self.uiwrapper = UiWrapper()
        self.game = game.Game(self.uiwrapper)
        self.game.loadModule(test_module1)

        #views
        self.gv = game_viewer.GameViewer(self.game)
        self.mv = MessageViewer(self.game)
        self.iv = inv_viewer.InvViewer(self.game)
        self.smv = smallmap.SmallMapViewer(self.game)

        #layout
        self.setViews(self.smv,self.iv,self.mv)
        self.setCentralWidget(self.gv)

        #event
        #self.setWindowState(Qt.WindowMaximized)
        self.resize(0,0)
        self.show()

    def setViews(self,*views):
        #docks menu
        menubar = self.menuBar()
        self.docksMenu = QMenu('&Views',self)
        menubar.addMenu(self.docksMenu)
        connect(self.docksMenu,'aboutToShow()',self.updateDocksMenu)

        self.dockDatas = []
        for view in views:
            #create dock widget
            dockWidget = QDockWidget(view.name,self)
            dockWidget.setObjectName(view.name)
            dockWidget.setWidget(view)
            self.addDockWidget(Qt.LeftDockWidgetArea,dockWidget)

            #create action
            action = createAction(
                self,'&'+view.name,
                lambda enable,dock=dockWidget: dock.setVisible(enable),
                checkable=True,)
            action.setChecked(True)
            self.docksMenu.addAction(action)

    def updateDocksMenu(self):
        for data in self.dockDatas:
            action = data['action']
            dockWidget = data['dock']
            view = data['view']
            aciton.setChecked(dockWidget.isVisible)

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
