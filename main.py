#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 03:08:29>
# last-update-time: <halida 11/08/2009 12:41:00>
# ---------------------------------
# 

from qtlib import *

import game,test_map1

MAX_MAP_SIZE = MAX_MAPX,MAX_MAPY =60,40

P_SIZE = 10
class MapGraph(QGraphicsItem):

    def __init__(self,map):
        super(MapGraph,self).__init__()
        self.rect = QRectF(0,0,
                           P_SIZE*MAX_MAPX,
                           P_SIZE*MAX_MAPY)
        self.path = QPainterPath()
        self.path.addRect(self.rect)

        self.image = QImage(self.rect)
        self.bgcolor = QColor(Qt.black)
        self.map = map

    def boundingRect(self):
        return self.rect
    
    def shape(self):
        return self.path

    def paint(self,painter,option,widget=None):
        #draw background
        painter.fillRect(self.rect,self.bgcolor)
        #draw map
        for y,row in enumerate(self.map):
            for x,floor in enumerate(row):
                #print x,y,floor
                color = self.floorToPicture(floor)
                painter.fillRect(x*P_SIZE,y*P_SIZE,
                                 P_SIZE,P_SIZE,color)

    def floorToPicture(self,floor):
        if floor == '.':
            color = Qt.black
        elif floor == '#':
            color = Qt.gray
        else:
            raise Exception("floor error:%s"%floor)
        return QColor(color)

class GameView(QGraphicsView):
    def __init__(self):
        super(GameView,self).__init__()
        self.setRenderHint(QPainter.Antialiasing)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.sprites = {}

    def wheelEvent(self,event):
        """
        use mouse wheel to scale the screen.
        """
        factor = 1.41 ** (-event.delta()/240.0)
        #print factor
        self.scale(factor,factor)

    def setGame(self,g):
        self.game = g

        self.scene.clear()
        self.updateMap()
        self.updateSprites()

        #events
        connect(self.game,game.PCMOVED,self.updateSprites)

    def updateMap(self):
        self.mapGraph = MapGraph(self.game.map)
        self.scene.addItem(self.mapGraph)

    def updateSprites(self):
        for sprite in self.game.sprites:
            #check sprites exists
            if self.sprites.has_key(sprite):
                spriteGraph = self.sprites[sprite]
            else:
                spriteGraph = QGraphicsEllipseItem(0,0,P_SIZE,P_SIZE)
                spriteGraph.setFlags(QGraphicsItem.ItemIsMovable)
                spriteGraph.setBrush(QColor(Qt.red))
                self.scene.addItem(spriteGraph)
                self.sprites[sprite] = spriteGraph
            #check pos
            spos = sprite.getPos()
            gpos = spriteGraph.pos()
            gposx,gposy = gpos.x(),gpos.y()
            if (gposx/P_SIZE <> spos[0]) or (gposy/P_SIZE <> spos[1]):
                spriteGraph.setPos(spos[0]*P_SIZE,
                                   spos[1]*P_SIZE)


class M(QMainWindow):
    def init(self):
        self.game = game.Game()
        self.game.loadMap(test_map1)
        self.v = GameView()
        self.v.setGame(self.game)
        #layout
        self.setCentralWidget(self.v)
        #event
        self.resize(800,600)
        self.show()

    def keyPressEvent(self,event):
        #change event to keymap
        key = event.key()
        #change keymap to command
        self.game.evalKeymap(key)
        #print event

def main():
    run(M)
    pass

if __name__=="__main__":
    main()
