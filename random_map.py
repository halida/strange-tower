#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# create-time:      <2009/11/08 08:55:52>
# last-update-time: <halida 11/08/2009 19:53:13>
# ---------------------------------
# 

from viewlib import *

import random

randint = random.randint

ROOM_NUMBER = 12
ROOM_SIZE = 3,10

def isOverlapping(ap,al,bp,bl):
    """
    check whether (ap,ap+al) is overlapping with (bp,bp+bl).
    """
    if ap < bp:
        return ap + al >= bp - 1 #-1 for not let 2 rooms join together
    if bp < ap:
        return bp + bl >= ap - 1

def roomConfict(r1,r2):
    r1p,r1s = r1
    r1x,r1y = r1p
    r1w,r1h = r1s

    r2p,r2s = r2
    r2x,r2y = r2p
    r2w,r2h = r2s
    
    if isOverlapping(r1x,r1w,r2x,r2w):
        if isOverlapping(r1y,r1h,r2y,r2h):
            return True
    return False

def randomMap(upStair=True,downStair=True):
    #create room
    rooms = []
    for i in range(ROOM_NUMBER):
        roomSize = rw,rh = randint(*ROOM_SIZE),randint(*ROOM_SIZE)
        roomPos = randint(0,MAX_MAPX - rw), randint(0,MAX_MAPY - rh)
        room = roomPos,roomSize
        #check room confict
        confict = False
        for r in rooms:
            if roomConfict(r,room):
                confict = True
        if not confict:
            rooms.append(room)

    #set up/down stairs
    if upStair:
        room_num = randint(0,len(rooms)-1)
        room = rooms[room_num]
        upP = (
            room[0][0] + randint(0,room[1][0]-1),
            room[0][1] + randint(0,room[1][1]-1),
            )
    if downStair:
        room_num = randint(0,len(rooms)-1)
        room = rooms[room_num]
        downP = (
            room[0][0] + randint(0,room[1][0]-1),
            room[0][1] + randint(0,room[1][1]-1),
            )
        while upStair and downP == upP:
            room_num = randint(0,len(rooms)-1)
            room = rooms[room_num]
            downP = (
                room[0][0] + randint(0,room[1][0]-1),
                room[0][1] + randint(0,room[1][1]-1),
                )

    #create door
    #todo
    #connect room

    #draw map
    map = []

    #fill with walls
    for i in range(MAX_MAPY):
        row = []
        for j in range(MAX_MAPX):
            row.append('#')
        map.append(row)

    #create road
    for i in range(len(rooms)-1):
        r1 = rooms[i]
        r2 = rooms[i+1]
        p1 = (
            r1[0][0] + randint(0,r1[1][0]-1),
            r1[0][1] + randint(0,r1[1][1]-1),
            )
        p2 = (
            r2[0][0] + randint(0,r2[1][0]-1),
            r2[0][1] + randint(0,r2[1][1]-1),
            )
        p3 = p1[0],p2[1]
        print p1,p2,p3
        for i in range(abs(p1[1]-p3[1])):
            map [ i + min(p1[1], p3[1]) ] [ p1[0] ] = ' '
        for i in range(abs(p2[0]-p3[0])):
            map [ p2[1] ] [ i + min(p2[0], p3[0]) ] = ' '

    #create room
    for room in rooms:
        rp,rs = room
        rx,ry = rp
        rw,rh = rs
        for i in range(rh):
            y = i + ry
            for j in range(rw):
                x = j + rx
                map[y][x] = '.'

    #create up/downstair
    if upStair:
        upx,upy = upP
        map[upy][upx] = '>'
    if downStair:
        downx,downy = downP
        map[downy][downx] = '<'

    #show map
    for r in rooms:
        print r
    if upStair:
        print upP
    if downStair:
        print downP
    for row in map:
        print ''.join(row)
    return map

    
