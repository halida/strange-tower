#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/11 10:50:37>
# last-update-time: <halida 11/11/2009 19:14:13>
# ---------------------------------
# 

def collideToMap(map,x,y):
    try:
        return (map['map'][y][x] == '#')
    except:
        return True

def collideToSprite(map,x,y):
    sprites = map['sprites']
    sprites = filter(lambda s:
                         (s.px==x and s.py==y),
                     sprites)
    return sprites
