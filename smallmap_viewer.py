#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/10 13:19:39>
# last-update-time: <halida 11/12/2009 22:02:14>
# ---------------------------------
# 

from qtlib import *

from viewlib import *

import game

class SmallMapViewer(QLabel):
    name = "Small Map Viewer"
    FLOOR_TO_COLOR = {
        '.':(255,255,255),
        '#':(  0,  0,  0),
        ' ':(240,240,240),
        }
    PC_SIZE = 2
    def __init__(self,g):
        super(SmallMapViewer,self).__init__()
        self.game = g
        self.map = None
        self.pcPos = None
        connect(self.game,game.MAPCHANGED,self.updateMap)
        connect(self.game,game.STEPED,self.update)

    def checkUpdate(self):
        px,py = self.game.pc.getPos()
        if not self.pcPos:
            self.pcPos = px,py
            self.update()
            return

        x,y = self.pcPos
        if abs(x-px) < 10 or abs(y-py) < 10:
            self.pcPos = px,py
            self.update()

    def updateMap(self):
        mapSize = self.game.map['size']
        self.setMinimumSize(*mapSize)

        self.map = QPixmap(*mapSize)
        #print "start painting"
        painter = QPainter(self.map)
        for y,row in enumerate(self.game.map['map']):
            for x,floor in enumerate(row):
                color = self.FLOOR_TO_COLOR[floor]
                #print x,y,color
                painter.setPen(QColor(*color))
                #painter.setBrush(QColor(*color))
                painter.drawPoint(x,y)
        #print "end printing"

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setPen(Qt.red)
        painter.setBrush(Qt.red)

        #draw map
        if self.map:
            painter.drawPixmap(0,0,self.map)

        #draw pc
        px,py = self.game.pc.getPos()
        painter.drawEllipse(
            px - self.PC_SIZE,
            py - self.PC_SIZE,
            self.PC_SIZE*2,self.PC_SIZE*2)
