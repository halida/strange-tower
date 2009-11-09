#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/09 01:02:47>
# last-update-time: <halida 11/09/2009 10:16:44>
# ---------------------------------
# 

from qtlib import *
import math
from PyQt4 import QtOpenGL

X,Y,Z = 'x','y','z'

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except ImportError:
    raise Exception('cannot import opengl!')

class MouseOperationPlugin():
    def init(self):
        self.factor = 1.0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.lastPos = QPoint()    

    def getRotation(self,c):
        if c == 'x':
            return self.xRot
        elif c == 'y':
            return self.yRot
        else:
            return self.zRot

    def setRotation(self,c,angle):
        angle = self.normalizeAngle(angle)
        rot = self.getRotation(c)
        if angle != rot:
            if c == 'x':
                self.xRot = angle
            elif c == 'y':
                self.yRot = angle
            else:
                self.zRot = angle
            emit(self,c+"RotationChanged(int)", angle)
            self.updateGL()

    def mousePressEvent(self, event):
        self.lastPos = QPoint(event.pos())

    def wheelEvent(self,event):
        self.factor = 1.41 ** (-event.delta()/240.0) * self.factor

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setRotation(X,self.xRot + 8 * dy)
            self.setRotation(Y,self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setRotation(X,self.xRot + 8 * dy)
            self.setRotation(Z,self.zRot + 8 * dx)

        self.lastPos = QPoint(event.pos())

    def mouseChangeView(self):
        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        #todo scale

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

class ResizePlugin():
    def resizeGL(self, width, height):
        side = min(width, height)
        glViewport((width - side) / 2, (height - side) / 2, side, side)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        glMatrixMode(GL_MODELVIEW)
