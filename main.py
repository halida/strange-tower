#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:08:29>
# last-update-time: <halida 11/11/2009 20:21:44>
# ---------------------------------
# 

from qtlib import *
from items import *

import game,test_module1,sprite

import game_viewer,inv_viewer,smallmap

class UiWrapper():
    def __init__(self,gv):
        #super(UiWrapper,self).__init__()
        self.gv = gv
        self.game = gv.game

    def selectItem(self):        
        itemlist = [i[NAME] for i in self.game.pcInv]
        if le(itemlist) <= 0: return 
        n,ok = QInputDialog.getItem(None,'','sect item:',itemlist,0,False)
        if ok: return itemlist.index(n)

    def selectTorget(self):
        #select torget
        items = self.gv.scene.selectedItems()
        if not items:
            self.game.msg('you should select torget first.')
            return
        item = items[0]

        #get torget foe
        for s,g in self.gv.sprites:
            if g == item:
                if s == self.game.pc:
                    self.game.msg('you cannot shoot yourself!')
                return s

        # #get foe in range
        # sprites = filter(lambda s:isinstance(s,sprite.Foe),
        #                  self.game.sprites)
        # sprites = filter(self.game.nearPC,sprites)
        # if not sprites:
        #     self.game.msg('no foe in range.')
        #     return

        # #create select dialog
        # posList = map(lambda s:str(s.getPos()),sprites)
        # n,ok = QInputDialog.getItem(None,'','select item:',posList,0,False)
        # if ok: return sprites[posList.index(n)]

class PairEdit(QHBoxLayout):
    def __init__(self):
        super(PairEdit,self).__init__()
        #l = QHBoxLayout(self)
        self.carw = QSpinBox()
        self.cdrw = QSpinBox()
        layoutAdds(self,(self.carw,self.cdrw))

    def setValue(self,p):
        self.carw.setValue(p[0])
        self.cdrw.setValue(p[1])
        
    def value(self):
        return self.carw.value(),self.cdrw.value()

    def setReadOnly(self,r):
        self.carw.setReadOnly(r)
        self.cdrw.setReadOnly(r)

class SpinBox(QSpinBox):
    def __init__(self):
        super(SpinBox,self).__init__()
        self.setRange(-1000000,1000000)

class PCViewer(QWidget):
    name = 'PC Viewer'
    INT,STR,TXT,PAIR = range(4)
    UPDATE_METHODS = {
        INT:(SpinBox,'setValue','value'),
        STR:(QLineEdit,'setText','text'),
        TXT:(QTextEdit,'setText','text'),
        PAIR:(PairEdit,'setValue','value')
        }
    ITEMS = (
        #name&class
        #attr
        ('hp','HP',INT),
        ('atk','Attack',PAIR),
        ('hit','To hit',INT),
        ('abs','Absorb',INT),
        ('ac','Amor Class',INT),
        )

    def __init__(self,g):
        super(PCViewer,self).__init__()
        self.game = g
        self.widgets = []
        l = QFormLayout(self)
        for name,showName,type in self.ITEMS:
            wClass,wSet,wGet = self.UPDATE_METHODS[type]
            w = wClass()
            w.setReadOnly(True)
            self.widgets.append(w)
            l.addRow(showName,w)
        #event
        self.onChange()
        connect(self.game,game.STEPED,self.onChange)

    def onChange(self):
        for i,w in enumerate(self.widgets):
            name,showName,type = self.ITEMS[i]
            wClass,wSet,wGet = self.UPDATE_METHODS[type]            
            data = getattr(self.game.pc,name)
            getattr(w,wSet)(data)
            
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
        self.game = game.Game()
        self.game.loadModule(test_module1)
        #views
        self.gv = game_viewer.GameViewer(self.game)
        self.game.uiwrapper = UiWrapper(self.gv)

        self.mv = MessageViewer(self.game)
        self.iv = inv_viewer.InvViewer(self.game)
        self.smv = smallmap.SmallMapViewer(self.game)
        self.pcv = PCViewer(self.game)

        #layout
        self.setViews(self.smv,self.iv,self.mv,self.pcv)
        self.setCentralWidget(self.gv)
        self.createStatusBar()
        #event
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
