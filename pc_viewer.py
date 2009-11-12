#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/12 12:36:19>
# last-update-time: <halida 11/12/2009 20:37:30>
# ---------------------------------
# 

from qtlib import *

import game,sprite

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

