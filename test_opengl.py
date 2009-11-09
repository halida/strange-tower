#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/09 00:19:51>
# last-update-time: <halida 11/09/2009 10:25:07>
# ---------------------------------
# 

from qtopengllib import *

class TestGL2(QtOpenGL.QGLWidget,MouseOperationPlugin,ResizePlugin):
    def init(self):
        MouseOperationPlugin.init(self)        
        self.show()

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_TEXTURE_2D)

    def paintGL(self):
        glViewport(0,0,self.width(),self.height())
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        gluPerspective(90.0, self.width()/self.height(), 1.0, 100.0);

        glLoadIdentity()
        gluLookAt(0.0, 1.0, 6.0,
                  0.0, 0.0, 0.0,
                  0.0, 1.0 ,0.0)
        glTranslated(0.0, 0.0, -10.0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #self.mouseChangeView()

        glBegin(GL_TRIANGLES);
        glColor3f(1.0, 0.0, 0.0);
        glVertex3f(2.0, 2.5, -1.0);
        glColor3f(0.0, 1.0, 0.0);
        glVertex3f(-3.5, -2.5, -1.0);
        glColor3f(0.0, 0.0, 1.0);
        glVertex3f(2.0, -4.0, 0.0);
        glEnd();

class TestGL(QtOpenGL.QGLWidget,MouseOperationPlugin,ResizePlugin):
    coords = ( 
        ( +1, -1, -1 ),
        ( -1, -1, -1 ),
        ( -1, +1, -1 ),
        ( +1, +1, -1 ),
        )

    def init(self):
        MouseOperationPlugin.init(self)
        self.clearColor = QColor(Qt.black)
        self.object = 0
        self.show()

    def initializeGL(self):
        self.obj = self.makeObject()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_TEXTURE_2D)

    def paintGL(self):
        self.qglClearColor(self.clearColor)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        #glViewport(0,0,0,0)
        gluLookAt(0,0,-10,
                  0,1,0,
                  0,1,0)
        glTranslated(0.0, 0.0, -10.0)
        self.mouseChangeView()
        glCallList(self.obj)
        
    def makeObject(self):
        dlist = glGenLists(1)
        glNewList(dlist, GL_COMPILE)

        map = QPixmap('data/tileset/map.png')
        map = map.copy(0,0,256,256)
        self.bindTexture(map)

        glBegin(GL_QUADS)
        for j in range(4):
            tx = {False: 1, True: 0}[j == 0 or j == 3]
            ty = {False: 1, True: 0}[j == 0 or j == 1]
            glTexCoord2d(tx, ty)
            glVertex3d(0.2 * TestGL.coords[j][0],
                       0.2 * TestGL.coords[j][1],
                       0.2 * TestGL.coords[j][2])
        glEnd()

        glEndList()
        return dlist

    
class HelloGL(QtOpenGL.QGLWidget,MouseOperationPlugin,ResizePlugin):
    def init(self):
        MouseOperationPlugin.init(self)
        self.object = 0
        self.trolltechGreen = QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)
        self.show()

    def initializeGL(self):
        self.qglClearColor(QColor(Qt.black))
        self.object = self.makeObject()
        GL.glShadeModel(GL.GL_FLAT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        GL.glTranslated(0.1, 0.0, -10.0)
        self.mouseChangeView()
        GL.glCallList(self.object)

    def makeObject(self):
        genList = GL.glGenLists(1)
        GL.glNewList(genList, GL.GL_COMPILE)

        GL.glBegin(GL.GL_QUADS)

        x1 = +0.06
        y1 = -0.14
        x2 = +0.14
        y2 = -0.06
        x3 = +0.08
        y3 = +0.00
        x4 = +0.30
        y4 = +0.22

        self.quad(x1, y1, x2, y2, y2, x2, y1, x1)
        self.quad(x3, y3, x4, y4, y4, x4, y3, x3)

        self.extrude(x1, y1, x2, y2)
        self.extrude(x2, y2, y2, x2)
        self.extrude(y2, x2, y1, x1)
        self.extrude(y1, x1, x1, y1)
        self.extrude(x3, y3, x4, y4)
        self.extrude(x4, y4, y4, x4)
        self.extrude(y4, x4, y3, x3)

        Pi = 3.14159265358979323846
        NumSectors = 200

        for i in range(NumSectors):
            angle1 = (i * 2 * Pi) / NumSectors
            x5 = 0.30 * math.sin(angle1)
            y5 = 0.30 * math.cos(angle1)
            x6 = 0.20 * math.sin(angle1)
            y6 = 0.20 * math.cos(angle1)

            angle2 = ((i + 1) * 2 * Pi) / NumSectors
            x7 = 0.20 * math.sin(angle2)
            y7 = 0.20 * math.cos(angle2)
            x8 = 0.30 * math.sin(angle2)
            y8 = 0.30 * math.cos(angle2)

            self.quad(x5, y5, x6, y6, x7, y7, x8, y8)

            self.extrude(x6, y6, x7, y7)
            self.extrude(x8, y8, x5, y5)

        GL.glEnd()
        GL.glEndList()

        return genList

    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.qglColor(self.trolltechGreen)

        GL.glVertex3d(x1, y1, -0.05)
        GL.glVertex3d(x2, y2, -0.05)
        GL.glVertex3d(x3, y3, -0.05)
        GL.glVertex3d(x4, y4, -0.05)

        GL.glVertex3d(x4, y4, +0.05)
        GL.glVertex3d(x3, y3, +0.05)
        GL.glVertex3d(x2, y2, +0.05)
        GL.glVertex3d(x1, y1, +0.05)

    def extrude(self, x1, y1, x2, y2):
        self.qglColor(self.trolltechGreen.dark(250 + int(100 * x1)))

        GL.glVertex3d(x1, y1, +0.05)
        GL.glVertex3d(x2, y2, +0.05)
        GL.glVertex3d(x2, y2, -0.05)
        GL.glVertex3d(x1, y1, -0.05)

def main():
    run(TestGL2)
    pass

if __name__=="__main__":
    main()




