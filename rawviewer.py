#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
a raw viewer
"""
from qtlib import *
from viewlib import *
import game
import map_graph

class GameViewer(QWidget):
    def __init__(self, g):
        super(GameViewer, self).__init__()
        self.setMinimumSize(640, 480)
        self.game = g
        self.grapher = map_graph.MapGraphCreater(self.game)
        self.pixmap = QPixmap("data/tileset/map.png")
        self.grapher.updateMap()
        #self.grapher.mapImage.save("test.png")

        #events
        connect(self.game,game.MAPCHANGED,self.update)
        connect(self.game,game.STEPED,self.update)
        connect(self.game,game.UPDATED,self.update)
        self.update()

    def updateMap(self):
        self.grapher.updateMap()

    def paintEvent(self, event=None):
        print "on draw.."
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.black)
        
        #draw map
        ox, oy = self.grapher.getOffset()
        print ox, oy
        painter.drawPixmap(0-ox*P_SIZE,
                           0-oy*P_SIZE+320,
                           self.grapher.mapImage)
        #draw sprites
        
