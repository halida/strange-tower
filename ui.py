#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
user interface
"""

from qtlib import *

import game,game_viewer

class UserInterface(object):
    def __init__(self,gv):
        self.gv = gv
        self.game = gv.game

    def selectItem(self):
        """
        tell the game what item is selected.
        """
        itemlist = [i[NAME] for i in self.game.pcInv]
        if le(itemlist) <= 0: return 
        n,ok = QInputDialog.getItem(None,'','sect item:',itemlist,0,False)
        if ok: return itemlist.index(n)

    def selectTorget(self):
        """
        tell the game what torget is selected.
        """
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

