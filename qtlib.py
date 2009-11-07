#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/10/24 07:54:49>
# last-update-time: <halida 11/07/2009 11:32:18>
# ---------------------------------
# 

import os,sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

app = QApplication(sys.argv)

def run(formClass):
    form = formClass()
    if hasattr(form,"init"):
        form.init()
    app.exec_()

def connect(fromObj, signal, to, optional=None):
    if not optional:
        QObject.connect(fromObj,SIGNAL(signal),to)
    else:
        QObject.connect(fromObj,SIGNAL(signal),to,SLOT(optional))

def emit(obj,signal,*args):
    obj.emit(SIGNAL(signal),*args)

def addDockWidget(parent,name,widget,place,objname=None,allowed=None):
    if not isinstance(parent, QMainWindow):
        raise Exception("Only mainwindow can add dock widget: %s"%unicode(parent))
    if not objname:
        objname = name
    dockWidget = QDockWidget(name, parent)
    dockWidget.setObjectName(objname)
    if allowed:
        dockWidget.setAllowedAreas(allowed)
    dockWidget.setWidget(widget)
    parent.addDockWidget(place, dockWidget)
    
def setApp(name,domain,appname,icon):
    app.setOrganizationName(name)
    app.setOrganizationDomain(domain)
    app.setApplicationName(appname)
    app.setWindowIcon(icon)

def createAction(parent,
                 text,
                 slot=None,
                 shortcut=None,
                 icon=None,
                 tip=None,
                 checkable=False,
                 signal="triggered()"):
    action = QAction(text, parent)
    if icon:
        action.setIcon(QIcon(":/%s.png" % icon))
    if shortcut:
        action.setShortcut(shortcut)
    if tip:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if slot:
        connect(action, signal, slot)
    if checkable:
        action.setCheckable(True)
    return action

def addActions(target, actions):
    for action in actions:
        if not action:
            target.addSeparator()
        else:
            target.addAction(action)

def loadUi(uifile):
    if uifile.find(".") == -1:
        uifile = uifile + ".ui"
    form,base = uic.loadUiType(uifile)
    return form
    
def layoutAdds(layout,widgets):
    #if widgets is only one
    t = type(widgets)
    if t <> type([]) and t <> type(()):
        widgets = (widgets,)
    #create by type
    for w in widgets:
        if not w:
            layout.addStretch()
        elif isinstance(w,QLayout):
            layout.addLayout(w)
        elif isinstance(w,QWidget):
            layout.addWidget(w)
        else:
            raise Exception("Unknown object add to layout:%s"%unicode(w))

def createButtonLayout(bts):
    bl = QHBoxLayout()
    
    for name,e in bts:
        if not name:
            bl.addStretch()
        button = QPushButton(name)
        connect(button,"clicked()",e)
        bl.addWidget(button)
    return bl
