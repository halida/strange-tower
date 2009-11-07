#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 04:25:20>
# last-update-time: <halida 11/07/2009 14:23:30>
# ---------------------------------
# 

from qtlib import *

class M(QGraphicsView):
    def init(self):
        self.scene = QGraphicsScene()
        #self.scene.setSceneRect(0,0,100,100)

        rect = QGraphicsRectItem(0,0,800,600)
        rect.setPos(0,0)
        #text2 = QGraphicsTextItem("haha2")
        #text2.setPos(100,100)

        self.scene.addItem(rect)
#        self.scene.addItem(text2)
        self.setScene(self.scene)

        self.resize(800,600)
        #self.setSceneRect(0,0,0,0)
        print self.sceneRect()
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.show()

def main():
    run(M)
    pass

if __name__=="__main__":
    main()
