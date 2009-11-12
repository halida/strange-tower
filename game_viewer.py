#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/08 07:18:42>
# last-update-time: <halida 11/13/2009 06:48:37>
# ---------------------------------
# 

from qtlib import *

from viewlib import *

import game,map_graph,view_to_pic,sprite

class GameViewer(QGraphicsView):
    FRAMERATE = 4
    STEP_TIME = 200
    def __init__(self,g):
        super(GameViewer,self).__init__()
        self.sprites = {}
        self.updates = []
        self.moves = []
        self.animates = {}

        #hide scrollbar, not let user know the detail
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHint(QPainter.Antialiasing)
        #scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        #moving timer
        self.timer = QTimeLine(self.STEP_TIME)
        self.timer.setFrameRange(1,self.FRAMERATE)
        connect(self.timer,"finished()",self.finishStep)
        connect(self.timer,"frameChanged(int)",
                self.animate)

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
        #events
        connect(self.game,game.MAPCHANGED,self.updateMap)
        connect(self.game,game.STEPED,self.step)
        connect(self.game,game.UPDATED,self.updateSprite)

    def updateMap(self):
        print "map updating.."
        self.sprites = {}
        self.scene.clear()
        self.mapGraphCreater.updateMap(createGraph=True)
        self.scene.addItem(self.mapGraphCreater.graph)

        #create sprites
        for s in self.game.sprites:
            self.createSprite(s)

        self.centerPC()#locate the right pos first
        if REAL_TIME:self.step()#first step

    def createSprite(self,s):
        if not hasattr(s,'view'):#no view
            spriteGraph = QGraphicsEllipseItem(0,0,P_SIZE,P_SIZE)
            spriteGraph.setBrush(QColor(Qt.red))
        else:#have view
            spriteGraph = QGraphicsPixmapItem()
            self.updateSprite(game.SPRITE_MOVE_NONE,id(s))
            if hasattr(s,'size'):
                spriteGraph.setOffset((1-s.size[0])*P_SIZE,
                                      (1-s.size[1])*P_SIZE)
        spriteGraph.setFlags(QGraphicsItem.ItemIsSelectable)
        if hasattr(s,'ground'):
            z = 1#not living, on the ground
        else:
            z = s.py+1

        spriteGraph.setZValue(z)
        spriteGraph.setPos(s.px*P_SIZE,s.py*P_SIZE)

        #finish
        self.scene.addItem(spriteGraph)
        self.sprites[id(s)]=spriteGraph
        return spriteGraph
        #print "adding:",s

    def animate(self,frame):
        for type,id in self.updates:
            if type in game.SPRITE_MOVES:
                #move animation
                s = self.game.spriteByID(id)
                g = self.sprites[id]
                if hasattr(s,'animate'):
                    self.createAnimate(type,s,g,frame)
                    
    def createAnimate(self,type,s,g,frame):
        c = s.__class__
        try:
            pixmap = self.animates[c]
        except:
            pixmap = QPixmap('graphics/view/'+s.view+'.png')
            self.animates[c] = pixmap

        s.slide = (s.slide+1)%4
        seq = view_to_pic.ANIMATE_SEQ[type]
        pixmap = pixmap.copy(s.size[0]*s.slide*P_SIZE,
                             s.size[1]*seq    *P_SIZE,
                             s.size[0]*P_SIZE,
                             s.size[1]*P_SIZE)
        g.setPixmap(pixmap)

    def step(self):
        for type,id in self.updates:

            if type in game.SPRITE_MOVES:
                s = self.game.spriteByID(id)
                g = self.sprites[id]

                oldp = ox,oy = g.x(),g.y()
                newp = nx,ny = s.px*P_SIZE,s.py*P_SIZE
                sx = (nx - ox) / self.FRAMERATE
                sy = (ny - oy) / self.FRAMERATE

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
                self.moves = []

            elif type == game.SPRITE_CREATE:
                s = self.game.spriteByID(id)
                g = self.createSprite(s)
                self.updates.remove((type,id))

            elif type == game.SPRITE_DIE:
                g = self.sprites.pop(id)
                self.scene.removeItem(g)
                self.updates.remove((type,id))

            else:
                raise Exception("type error:",type)

        #ok, start step
        if self.timer.state() != QTimeLine.Running:
            self.timer.start()

    def finishStep(self):
        self.timer.stop()
        self.timer.setCurrentTime(0)
        self.animations = []

        #print 'finishing step..',self.updates
        for type,id in self.updates:
            if type in game.SPRITE_MOVES:
                s = self.game.spriteByID(id)
                g = self.sprites[id]
                #print "seting new pos:",index,s.px*P_SIZE,s.py*P_SIZE
                g.setPos(s.px*P_SIZE,s.py*P_SIZE)
                g.setZValue(s.py+1)

        self.updates = []
        self.centerPC()
        #if real time, end step means new game step
        if REAL_TIME: self.game.step()

    def updateSprite(self,type,index):
        #buffer updates
        #print "buffering:",type,index
        self.updates.append( (str(type),index) )

    def centerPC(self):
        pcGraph = self.sprites[id(self.game.pc)]
        #center pc
        self.centerOn(pcGraph)

