#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/08 07:17:28>
# last-update-time: <halida 11/11/2009 13:04:26>
# ---------------------------------
# draw a map

from qtlib import *

from viewlib import *

import game

class MapGraphCreater():
    EDGE = 10
    SW,SH = SIZE = 40,40
    bgcolor = QColor(240,240,240)
    mapTileset = QPixmap('Graphics/Tilesets/map.png')

    rect = QRectF(0,0,
                  P_SIZE*SIZE[0],
                  P_SIZE*SIZE[1],)
    path = QPainterPath()
    path.addRect(rect)
    
    mapImage = QPixmap(P_SIZE*SIZE[0],
                       P_SIZE*SIZE[1],)
    
    def __init__(self,g):
        self.game = g
        self.scrPos = -100,-100
        self.graph = None
        self.updateMap()
        connect(self.game,game.PCMOVED,self.checkUpdateMap)

    def checkUpdateMap(self):
        #check if PC move to the edge
        EDGE = self.EDGE
        sx,sy = self.scrPos
        sw,sh = self.SIZE
        px,py = pcpos = self.game.pc.getPos()
        #print "check pc out:",pcpos,self.scrPos,self.SIZE
        if ((sx+EDGE <= px < sx+sw-EDGE) and 
            (sy+EDGE <= py < sy+sh-EDGE)):
            return
        self.updateMap()

    def updateMap(self):            
        #if on edge, update map
        px,py = pcpos = self.game.pc.getPos()
        sx,sy = self.scrPos = px - self.SW/2 , py - self.SH/2
        map = self.game.map['map']
        mapSize = self.game.map['size']

        #draw background
        self.mapImage.fill(self.bgcolor)

        #draw map
        painter = QPainter(self.mapImage)
        y = 0
        while y<self.SH and sy+y<mapSize[1]:
            if sy+y<0: y+=1;continue
            #print "mapsize:",mapSize
            x = 0
            while x<self.SW and sx+x<mapSize[0]:
                if sx+x<0: x+=1;continue
                target = QRectF(x*P_SIZE,y*P_SIZE,
                                P_SIZE,P_SIZE)
                #print "haha:",sy+y,sx+x,x,y
                floor = map[sy+y][sx+x]
                dx,dy = self.floorToImage(floor)
                source = QRectF(dx*P_SIZE,dy*P_SIZE,P_SIZE,P_SIZE)
                painter.drawPixmap(target,self.mapTileset,source)
                #print 'printing:',x,y
                x += 1
            y += 1

        #create mapgraph
        if not self.graph:
            self.graph = MapGraph()
        self.graph.setPixmap(self.mapImage)                
        self.graph.setPos(sx*P_SIZE,sy*P_SIZE)

    def floorToImage(self,floor):
        if floor == '.':
            pos = 0,0
        elif floor == '#':
            pos = 2,0
        elif floor == ' ':
            pos = 3,0
        else:
            raise Exception("floor error:",floor)
        return pos

class MapGraph(QGraphicsPixmapItem):
    def __init__(self):
        super(MapGraph,self).__init__()
    def boundingRect(self):
        return MapGraphCreater.rect
    def shape(self):
        return MapGraphCreater.path
