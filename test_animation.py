#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/11 00:58:43>
# last-update-time: <halida 11/11/2009 10:35:36>
# ---------------------------------
# 

from qtlib import *

def main():
    ball1 = QGraphicsEllipseItem(0, 0, 20, 20);
    ball2 = QGraphicsEllipseItem(100, 100, 20, 20);

    timer = QTimeLine(5000);
    timer.setFrameRange(0, 100);

    animation1 = QGraphicsItemAnimation();
    animation1.setItem(ball1);
    animation1.setTimeLine(timer);
    animation2 = QGraphicsItemAnimation();
    animation2.setItem(ball2);
    animation2.setTimeLine(timer);

    for i in range(0,200):
        animation1.setPosAt(i / 200.0, QPointF(i, i));
        animation2.setPosAt(i / 200.0, QPointF(i, i));

    scene = QGraphicsScene();
    scene.setSceneRect(0, 0, 250, 250);
    scene.addItem(ball1);
    scene.addItem(ball2);

    view = QGraphicsView(scene);
    view.show();

    timer.start();
    app.exec_()

if __name__=="__main__":
    main()
