#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/08 07:18:42>
# last-update-time: <halida 11/10/2009 12:45:08>
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
                if hasattr(s,'view'):
                    spriteGraph = QGraphicsPixmapItem()
                    pixmap = QPixmap(s.view)
                    if hasattr(s,'size'):
                        pos = (
                            0,
                            -(s.size[1]-1)*P_SIZE)
                        spriteGraph.setOffset(*pos)
                        pixmap = pixmap.copy(0,0,
                                             s.size[0]*P_SIZE,
                                             s.size[1]*P_SIZE)
                    spriteGraph.setPixmap(pixmap)
                else:
                    spriteGraph = QGraphicsEllipseItem(0,0,P_SIZE,P_SIZE)
                    spriteGraph.setBrush(QColor(Qt.red))
                #spriteGraph.setFlags(QGraphicsItem.ItemIsMovable)
                z = 10 if s==self.game.pc else 1
                spriteGraph.setZValue(z)
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

class SmallMapViewer(QGraphicsView):
    def __init__(self,scene):
        super(SmallMapViewer,self).__init__()
        self.scene = scene
        self.setScene(self.scene)
        self.scale(0.1,0.1)
