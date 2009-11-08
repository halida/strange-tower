#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/07 04:25:20>
# last-update-time: <halida 11/08/2009 12:26:12>
# ---------------------------------
# 

from qtlib import *

class M(QGraphicsView):
    def init(self):
        self.scene = QGraphicsScene()

        rect = QGraphicsRectItem(0,0,800,600)
        rect.setPos(0,0)

        self.scene.addItem(rect)
        self.setScene(self.scene)

        self.resize(800,600)
        print self.sceneRect()
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.show()

def main():
    run(M)
    pass

if __name__=="__main__":
    main()
