#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/08 07:17:28>
# last-update-time: <halida 11/10/2009 11:42:40>
# ---------------------------------
# draw a map

from qtlib import *

from viewlib import *

import game

class MapGraph(QGraphicsPixmapItem):
    rect = QRectF(0,0,
                  P_SIZE*MAX_MAPX,
                  P_SIZE*MAX_MAPY)
    path = QPainterPath()
    path.addRect(rect)

    bgcolor = QColor(Qt.black)

    mapTileset = QPixmap('Graphics/Tilesets/040-Tower02.png')
    mapImage = QPixmap(P_SIZE*MAX_MAPX,P_SIZE*MAX_MAPY)
    
    def __init__(self,g):
        super(MapGraph,self).__init__()
        self.game = g
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
        for y,row in enumerate(self.game.map['map']):
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

