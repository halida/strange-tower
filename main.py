#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:08:29>
# last-update-time: <halida 11/12/2009 20:56:51>
# ---------------------------------
# 

from qtlib import *
from items import *

import game,test_module1,sprite

import uiwrapper
import user_action_phaser
import game_viewer
import inv_viewer
import pc_viewer
import smallmap_viewer
import message_viewer

class M(QMainWindow):
    def init(self):
        self.game = game.Game()
        self.game.loadModule(test_module1)

        #views
        self.gv = game_viewer.GameViewer(self.game)
        self.game.uiwrapper = uiwrapper.UiWrapper(self.gv)
        self.uap = user_action_phaser.UserActionPhaser(self.gv,self.game)

        self.mv = message_viewer.MessageViewer(self.game)
        self.iv = inv_viewer.InvViewer(self.game)
        self.smv = smallmap_viewer.SmallMapViewer(self.game)
        self.pcv = pc_viewer.PCViewer(self.game)

        #layout
        self.setViews(self.smv,self.iv,self.mv,self.pcv)
        self.setCentralWidget(self.gv)
        self.createStatusBar()

        #event
        self.gv.setFocus()#set gv focus to trig key event
        #self.setWindowState(Qt.WindowMaximized)
        self.resize(0,0)
        self.show()
        self.msg('game created!')

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

    def createStatusBar(self):
        self.statusBar = QStatusBar(self)

        self.msger = QLabel()
        self.gvViewer = QLabel()

        self.statusBar.insertWidget(0,self.msger)
        self.statusBar.insertWidget(1,self.gvViewer)
        self.setStatusBar(self.statusBar)

        connect(self.gv.scene,'selectionChanged()',
                self.updateStatus)

    def msg(self,msg):
        self.msger.setText(msg)
        QTimer.singleShot(5000,lambda:self.msger.setText(""))

    def updateStatus(self):
        try:
            item = self.gv.scene.selectedItems()[0]
        except: return
        
        for s,g in self.gv.sprites:
            if g == item:
                self.gvViewer.setText(s.getDesc())
                QTimer.singleShot(5000,lambda:self.msger.setText(""))        

def main():
    run(M)
    pass

if __name__=="__main__":
    main()
