#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/12 12:40:11>
# last-update-time: <halida 11/12/2009 20:40:42>
# ---------------------------------
# 

from qtlib import *

import game,game_viewer

class UiWrapper():
    def __init__(self,gv):
        #super(UiWrapper,self).__init__()
        self.gv = gv
        self.game = gv.game

    def selectItem(self):        
        itemlist = [i[NAME] for i in self.game.pcInv]
        if le(itemlist) <= 0: return 
        n,ok = QInputDialog.getItem(None,'','sect item:',itemlist,0,False)
        if ok: return itemlist.index(n)

    def selectTorget(self):
        #select torget
        items = self.gv.scene.selectedItems()
        if not items:
            self.game.msg('you should select torget first.')
            return
        item = items[0]

        #get torget foe
        for s,g in self.gv.sprites:
            if g == item:
                if s == self.game.pc:
                    self.game.msg('you cannot shoot yourself!')
                return s

        # #get foe in range
        # sprites = filter(lambda s:isinstance(s,sprite.Foe),
        #                  self.game.sprites)
        # sprites = filter(self.game.nearPC,sprites)
        # if not sprites:
        #     self.game.msg('no foe in range.')
        #     return

        # #create select dialog
        # posList = map(lambda s:str(s.getPos()),sprites)
        # n,ok = QInputDialog.getItem(None,'','select item:',posList,0,False)
        # if ok: return sprites[posList.index(n)]            

