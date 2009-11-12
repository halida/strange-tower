#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/11 10:50:37>
# last-update-time: <halida 11/12/2009 21:38:34>
# ---------------------------------
# 

COLLIDE_NO = 0
COLLIDE_OUT_MAP = 1
COLLIDE_TO_WALL = 2

def collideToMap(map,x,y):
    if x<0 or y<0: return COLLIDE_OUT_MAP
    try:
        result = (map['map'][y][x] == '#')
        return (COLLIDE_TO_WALL if result else COLLIDE_NO)
    except:
        return COLLIDE_OUT_MAP

def collideToSprite(map,x,y):
    sprites = map['sprites']
    sprites = filter(lambda s:
                         (s.px==x and s.py==y),
                     sprites)
    return sprites
