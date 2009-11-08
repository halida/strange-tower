#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/08 07:18:42>
# last-update-time: <halida 11/08/2009 16:35:54>
# ---------------------------------
# 

from qtlib import *

from viewlib import *

import game,map_graph

class GameViewer(QGraphicsView):
    def __init__(self,g):
        super(GameViewer,self).__init__()
        self.setRenderHint(QPainter.Antialiasing)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.sprites = {}
        self.setGame(g)
        #self.scale(0.3,0.3)

    def wheelEvent(self,event):
        """
        use mouse wheel to scale the screen.
        """
        factor = 1.41 ** (-event.delta()/240.0)
        self.scale(factor,factor)

    def setGame(self,g):
        self.game = g

        self.scene.clear()
        self.updateMap()
        self.updateSprites()

        #events
        connect(self.game,game.PCMOVED,self.updateSprites)

    def updateMap(self):
        self.mapGraph = map_graph.MapGraph(self.game)
        connect(self.game,game.MAPCHANGED,self.mapGraph.updateMap)
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

