#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
简便实用pyqt的library
"""
#判断操作系统
import platform, sys, os
WINDOWS = (platform.system() == 'Windows')

#是否当前project是debug状态

#分析命令行参数
import getopt
try:
    opts, args = getopt.getopt(sys.argv[1:], "d")
except getopt.GetoptError, err:
    print str(err)
    sys.exit(2)

DEBUG = False
#解析
for opt, arg in opts:
    if opt == '-d':
        #debug使用
        DEBUG = True
        print "debugging..."
    else:
        assert False, "unhandled option:%s,%s"% (opt, arg)
    
#去掉py2exe出错时显示的报错信息，
#把报错信息全部重定义到文件
if not DEBUG:
    sys.stderr = open("error.log","w+")
    sys.stdout = open("out.log","w+")

import logging
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.ERROR)

#是否当前project是debug状态----------------


#因为pyqt有一个hex函数，所以备份系统原有的函数
ohex = hex

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import random
randint = random.randint

#chinese
text = QTextCodec.codecForName("utf-8")
QTextCodec.setCodecForCStrings(text)

app = QApplication(sys.argv)

#translate
tr = app.tr

def run(formClass=None, show=True, maxmized=False):
    "运行一个QWidget的类"
    if not formClass:
        app.exec_()
        return
    if not isinstance(formClass, QWidget):
        form = formClass()
        if hasattr(form, 'NAME'):
            form.setWindowTitle(form.NAME)
    else:
        form = formClass
    if hasattr(form,"init"):
        form.init()
    #maxmized
    if maxmized:
        form.setWindowState(Qt.WindowMaximized)
    if show:
        form.show()
    app.exec_()

def connect(fromObj, signal, toObj, optional=None):
    "链接事件"
    if not optional:
        QObject.connect(fromObj, SIGNAL(signal), toObj)
    else:
        QObject.connect(fromObj, SIGNAL(signal), toObj, SLOT(optional))

def emit(obj, signal, *args):
    "发送消息"
    obj.emit(SIGNAL(signal), *args)

def addDockWidget(parent, name, widget,
                  place=Qt.LeftDockWidgetArea,
                  objname=None, allowed=None):
    "给mainwindow加子窗体"
    if not isinstance(parent, QMainWindow):
        raise Exception(
            "Only mainwindow can add dock widget: %s"%unicode(parent))
    if not objname:
        objname = name
    dockWidget = QDockWidget(name, parent)
    dockWidget.setObjectName(objname)
    if allowed:
        dockWidget.setAllowedAreas(allowed)
    dockWidget.setWidget(widget)
    parent.addDockWidget(place, dockWidget)
    return dockWidget
    
def setApp(name, domain, appname, icon):
    "设置app的一些属性"
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
                 signal="triggered()",
                 whatis=None):
    "创建action"
    action = QAction(text, parent)
    if icon:
        if isinstance(icon, QIcon):
            action.setIcon(icon)
        else:
            action.setIcon(QIcon(":/%s.png" % icon))
    if shortcut:
        action.setShortcut(shortcut)
    if tip:
        setTip(action, tip)
    if checkable:
        action.setCheckable(True)
        signal = 'toggled(bool)'
    if slot:
        connect(action, signal, slot)
    return action

def addActions(target, actions):
    "添加action"
    for action in actions:
        if not action:
            target.addSeparator()
        else:
            target.addAction(action)
    
def layoutAdds(layout, widgets):
    "快速添加widget到layout中"
    #if widgets is only one
    t = type(widgets)
    if t != type([]) and t != type(()):
        widgets = (widgets,)
    #create by type
    for w in widgets:
        if not w:
            layout.addStretch(1)
        elif isinstance(w, QLayout):
            layout.addLayout(w)
        elif isinstance(w, QWidget):
            layout.addWidget(w)
        else:
            raise Exception("Unknown object add to layout:%s"%unicode(w))

def createButtonLayout(bts):
    "建立按钮layout"
    bl = QHBoxLayout()
    
    for name, e in bts:
        if not name:
            bl.addStretch()
        button = QPushButton(name)
        connect(button, "clicked()", e)
        bl.addWidget(button)
    return bl

def showMsg(message, msgType="warning"):
    "显示消息"
    if not isinstance(message, basestring):
        message = unicode(message)
    func = getattr(QMessageBox, msgType)
    func(None, "", message)

def saveFileDlg(parent, fileType='(*.txt)'):
    "选择保存的文件名"
    return unicode(QFileDialog.getSaveFileName(
        parent,"请输入文件名",".",fileType))

def openFileDlg(parent, fileType='(*.*)'):
    "选择文件"
    return unicode(QFileDialog.getOpenFileName(
        parent,"请输入文件名",".",fileType))

def openFilesDlg(parent, fileType='(*.*)'):
    "选择多个文件"
    files = QFileDialog.getOpenFileNames(
        parent,"请输入文件名",".",fileType)
    return [unicode(f) for f in files]
    
def inputBox(parent, inf="请输入资料"):
    "用户输入信息"
    name, result = QInputDialog.getText(parent, "", inf)
    if not result: 
        return None
    return name

def connectButton(form):
    """
    快速把按钮和事件连接起来。
    把form中所有按钮，连接到和按钮名称一致的方法上面(去掉最前面的pb，以及首字母会变小写)
    比如bpSend会被连接到send方法上面。
    """
    for name in dir(form):
        button = getattr(form, name)
        if not isinstance(button, QAbstractButton): 
            #print "not button:",button
            continue
        funcname = name[2:3].lower() + name[3:]
        if not hasattr(form, funcname): 
            #print "not have func:",funcname
            continue
        func = getattr(form, funcname)
        connect(button, "clicked()", func)
        #print "connected:",button,func

def setTip(widget, tip):
    "设置提示"
    widget.setToolTip(tip)
    widget.setStatusTip(tip)
    widget.setWhatsThis(tip)

def changeStyle(widget, styleName, useStylePalette=True):
    """更改界面风格
    """
    QApplication.setStyle(QStyleFactory.create(styleName))
    if useStylePalette:#是否选择风格对应的色彩
        QApplication.setPalette(QApplication.style().standardPalette())
    else:
        QApplication.setPalette(widget.originalPalette)

def styles():
    "当前系统支持的界面风格"
    return QStyleFactory.keys()

def createMenu(window, menu, ):
    """快速创建menu"""
    menuBar = window.menuBar()
    for menuName, menuDatas in menu:
        menu = QMenu(menuName, window)
        for menuData in menuDatas:
            if menuData == "":#分隔符
                menu.addSeparator()
            elif isinstance(menuData, tuple):
                #menudata为显示，事件
                name, event = menuData
                #如果传入的是界面类，新建界面函数
                if hasattr(event, "NAME"):
                    #if issubclass(event, QWidget):
                    event = createFormFunc(event, window)
                #如果是字符串，连接到对应的函数
                elif isinstance(event, basestring):
                    event = getattr(window, event)
                action = createAction(window, name, event)
                menu.addAction(action)
            else:
                raise Exception("menu data format error!")
        menuBar.addMenu(menu)

def createFormFunc(menuData, window):
    "生成一个建立窗体的函数"
    def func(menuData = menuData, window = window):
        form = menuData()
        #成为子界面，防止被垃圾收集掉
        form.setParent(window, Qt.Window)
        #用户点击关闭后自动清除
        form.setAttribute(Qt.WA_DeleteOnClose)
        if hasattr(form,"NAME"):
            form.setWindowTitle(form.NAME)
        form.show()
        app.setActiveWindow(form)
    return func

def onDev():
    "开发中的占位函数"
    showMsg("开发中..")

def showTable(tableWidget, table, 
              changeFuncs=None,#转换每个栏位的函数列表
              stepper=None
              ):
    "把table 数据显示到tableWidget上面"
    if not table: return
    tableWidget.setRowCount(len(table))
    tableWidget.setColumnCount(len(table[0]))

    for i, row in enumerate(table):
        if stepper:
            stepper.step(1)
            if stepper.wasCanceled():
                return
            
        for j, item in enumerate(row):
            #转换为字符串
            if not changeFuncs:
                text = str(item)
            else:
                text = changeFuncs[j](item)

            item = QTableWidgetItem(text)
            tableWidget.setItem(i, j, item)

    #table界面整理一下
    tableWidget.resizeColumnsToContents()

    
