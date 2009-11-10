#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/08 07:18:42>
# last-update-time: <halida 11/10/2009 11:15:12>
# ---------------------------------
# 

from qtlib import *

from viewlib import *

import game,map_graph

class GameViewer(QGraphicsView):
    def __init__(self,g):
        super(GameViewer,self).__init__()
        self.sprites = {}
        self.setRenderHint(QPainter.Antialiasing)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setGame(g)
        self.scale(0.8,0.8)

    def wheelEvent(self,event):
        """
        use mouse wheel to scale the screen.
        """
        factor = 1.41 ** (-event.delta()/240.0)
        self.scale(factor,factor)

    def setGame(self,g):
        self.game = g

        self.updateMap()

        #events
        connect(self.game,game.MAPCHANGED,self.updateMap)
        connect(self.game,game.PCMOVED,self.updateSprites)
        connect(self.game,game.SPRITECHANGED,self.updateSprites)

    def updateMap(self):
        self.sprites = []
        self.scene.clear()
        self.mapGraph = map_graph.MapGraph(self.game)
        self.scene.addItem(self.mapGraph)
        self.updateSprites()

    def updateSprites(self,index=0):
        #remove changed sprite
        if 0 < index < len(self.sprites):#0 is pc
            s,g = self.sprites.pop(index)
            self.scene.removeItem(g)

        #update one by one
        for i,s in enumerate(self.game.sprites):
            #check sprites exists
            spriteGraph = None
            if i<len(self.sprites):
                sprite , spriteGraph = self.sprites[i]
                if sprite != s:
                    spriteGraph = None

            #create sprite graph
            if not spriteGraph:
                spriteGraph = QGraphicsEllipseItem(0,0,P_SIZE,P_SIZE)
                spriteGraph.setFlags(QGraphicsItem.ItemIsMovable)
                spriteGraph.setZValue(1)
                spriteGraph.setBrush(QColor(Qt.red))
                self.scene.addItem(spriteGraph)
                self.sprites.insert(i, (s,spriteGraph) )
                #print "adding:",sprite

            #check pos
            spos = s.getPos()
            gpos = spriteGraph.pos()
            gposx,gposy = gpos.x(),gpos.y()
            if (gposx/P_SIZE <> spos[0]) or (gposy/P_SIZE <> spos[1]):
                spriteGraph.setPos(spos[0]*P_SIZE,
                                   spos[1]*P_SIZE)

