#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/08 07:17:28>
# last-update-time: <halida 11/08/2009 16:37:12>
# ---------------------------------
# draw a map

from qtlib import *

from viewlib import *

class MapGraph(QGraphicsPixmapItem):

    def __init__(self,g):
        super(MapGraph,self).__init__()
        self.rect = QRectF(0,0,
                           P_SIZE*MAX_MAPX,
                           P_SIZE*MAX_MAPY)
        self.path = QPainterPath()
        self.path.addRect(self.rect)

        self.bgcolor = QColor(Qt.black)
        self.game = g
        self.mapTileset = QPixmap('data/tileset/map.png')
        #self.mapTileset = self.mapTileset.scaled(128,480)
        self.mapImage = QPixmap(P_SIZE*MAX_MAPX,P_SIZE*MAX_MAPY)
        self.updateMap()

    def boundingRect(self):
        return self.rect
    
    def shape(self):
        return self.path

    def updateMap(self):
        #draw background
        self.mapImage.fill(self.bgcolor)

        painter = QPainter(self.mapImage)
        #draw map
        for y,row in enumerate(self.game.map):
            for x,floor in enumerate(row):
                #print x,y,floor
                target = QRectF(x*P_SIZE,y*P_SIZE,P_SIZE,P_SIZE)
                dx,dy = self.floorToImage(floor)
                source = QRectF(dx*P_SIZE,dy*P_SIZE,P_SIZE,P_SIZE)
                painter.drawPixmap(target,self.mapTileset,source)
        self.setPixmap(self.mapImage)                

    def floorToImage(self,floor):
        if floor == '.':
            pos = 0,0
        elif floor == '#':
            pos = 3,5
        elif floor == ' ':
            pos = 1,0
        elif floor == '-':
            pos = 4,9
        elif floor in ('>','<'):
            pos = 4,9
        else:
            raise Exception("floor error:",floor)
        return pos

