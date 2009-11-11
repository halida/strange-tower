#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/08 07:18:42>
# last-update-time: <halida 11/11/2009 12:33:28>
# ---------------------------------
# 

from qtlib import *

from viewlib import *

import game,map_graph

class GameViewer(QGraphicsView):
    FRAMERATE = 8
    def __init__(self,g):
        super(GameViewer,self).__init__()
        self.sprites = {}
        self.updates = []
        self.animations = []

        self.setRenderHint(QPainter.Antialiasing)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        #timer
        self.timer = QTimeLine(500)
        self.timer.setFrameRange(1,self.FRAMERATE)
        connect(self.timer,"finished()",self.finishStep)
        #connect(self.timer,"frameChanged(int)",
        #        lambda i:self.game.msg(str(self.sprites[3][1].pos())))

        self.setBackgroundBrush(QBrush(QColor(250,250,250)))
        self.setMinimumSize(640,480)
        self.mapGraphCreater = map_graph.MapGraphCreater(g)

        self.setGame(g)
        
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
        connect(self.game,game.STEPED,self.step)
        connect(self.game,game.SPRITECHANGED,self.updateSprite)

    def updateMap(self):
        print "map updating.."
        self.sprites = []
        self.scene.clear()
        self.mapGraphCreater.graph=None
        self.mapGraphCreater.updateMap()
        self.scene.addItem(self.mapGraphCreater.graph)

        #create sprites
        for i,s in enumerate(self.game.sprites):
            self.createSprite(i,s)

        self.centerPC()

    def createSprite(self,i,s):
        if hasattr(s,'view'):#sprite has view
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
        else:#sprite have no view
            spriteGraph = QGraphicsEllipseItem(0,0,P_SIZE,P_SIZE)
            spriteGraph.setBrush(QColor(Qt.red))
        #spriteGraph.setFlags(QGraphicsItem.ItemIsMovable)
        #sprite pos
        z = 10 if s==self.game.pc else 1
        spriteGraph.setZValue(z)
        spriteGraph.setPos(s.px*P_SIZE,s.py*P_SIZE)
        #finish
        self.scene.addItem(spriteGraph)
        self.sprites.insert(i, (s,spriteGraph) )
        #print "adding:",s

    def step(self):
        #init
        
        #set animations
        for type,index in self.updates:
            if type == game.SPRITE_CREATE:
                self.createSprite(index,self.game.sprites[index])
            elif type == game.SPRITE_DIE:
                print index
                s,g = self.sprites.pop(index)
                self.scene.removeItem(g)
                #todo
            elif type == game.SPRITE_MOVE:
                s,g = self.sprites[index]
                oldp = ox,oy = g.x(),g.y()
                newp = nx,ny = s.px*P_SIZE,s.py*P_SIZE
                sx = (nx - ox) / self.FRAMERATE
                sy = (ny - oy) / self.FRAMERATE
                #g.setPos(s.px*P_SIZE,s.py*P_SIZE)

                a = QGraphicsItemAnimation()
                a.setItem(g)
                a.setTimeLine(self.timer)
                #set move
                step = self.FRAMERATE
                #print "set moving:",index,ox,oy,nx,ny
                for i in range(step):
                    pos = (ox + sx * i,
                           oy + sy * i,)
                    a.setPosAt(i/float(step),QPointF(*pos))
                    #print s.name,pos
                self.animations.append(a)
            else:
                raise Exception("type error:",type)
            
        if self.timer.state() != QTimeLine.Running:
            self.timer.start()

    def finishStep(self):
        self.timer.stop()
        self.timer.setCurrentTime(0)
        self.animations = []

        #print 'finishing step..',self.updates
        for type,index in self.updates:
            if type == game.SPRITE_MOVE:
                s,g = self.sprites[index]
                #print "seting new pos:",index,s.px*P_SIZE,s.py*P_SIZE
                g.setPos(s.px*P_SIZE,s.py*P_SIZE)

        self.updates = []
        self.centerPC()

    def updateSprite(self,type,index):
        #buffer updates
        #print "buffering:",type,index
        self.updates.append( (type,index) )

    def centerPC(self):
        pc,pcGraph = self.sprites[0]
        #center pc
        self.centerOn(pcGraph)

