#!/usr/bin/python3
# coding : UTF-8
# -*- coding: utf8 -*-
import os
import sys
import time
import ctypes
import operator
from math import pi as pi
from math import sin as sin
from math import cos as cos
from math import tan as tan
from math import asin as asin
from math import acos as acos
from math import atan as atan
from math import sqrt as sqrt
import math
from bs4 import BeautifulSoup
from classes import X11 as X11
from classes import dummy as dummy
from classes import PANIC as PANIC
from classes import NSolve_Cut as NSolve
from classes import TwoVec as TwoVec
from classes import Ncurses as Ncurses
from classes import str2bool as str2bool

NAM=locals()
def factory_var(x):
    def _factory_var():
        def __factory_var(z):
            global NAM
            return NAM[z]
        return __factory_var(x)
    return _factory_var

def factory_value(s):
    def _factory_value():
        def __factory_value(w):
            return w
        return __factory_value(s)
    return _factory_value

def factory_eval(e):
    def _factory_eval():
        def __factory_eval(g):
            return eval(g)
        return __factory_eval(e)
    return _factory_eval

class varType:
    def __init__(self,str):
        self.type   =   None
        self.var    =   None
        if str  ==  None:
            return
        try:
            if str[0]   ==  r"#":
                self.type   =   0
                self.var    =   factory_value(str[1:])
                return
            if str[0]   ==  r"@":
                self.type   =   1
                self.var    =   factory_var(str[1:])
                return
            if str[0]   ==  r"$":
                self.type   =   2
                self.var    =   factory_value(str2bool(str[1:]))
                return
            if str[0]   ==  r"&":
                self.type   =   3
                self.var    =   factory_value(float(str[1:]))
                return
            if str[0]   ==  r"%":
                self.type   =   4
                self.var    =   factory_value(int(str[1:]))
                return
        except Exception as e:
            print(e)
            PANIC(-1,"varType:the given var is not a string")

def Read(str):
    try:
        if str[0]   ==  r"#":
            return str[1:]
        if str[0]   ==  r"@":
            return eval(str[1:])
        if str[0]   ==  r"$":
            return str2bool(str[1:])
        if str[0]   ==  r"&":
            return float(str[1:])
        if str[0]   ==  r"%":
            return int(str[1:])
    except Exception as e:
        print(e)
        PANIC(-2,"Read:the given var is not a string")
    return None

class Point:
    def __init__(self,**args):
        self._position=TwoVec()
        self._id=None
        self._next=None
        self._enable=None
        self._r=None
        self.touching=False
        self.position=TwoVec()
        self.id=None
        self.next=None
        self.enable=None
        self.r=None
#_ local 
#r relative a absolute (to main)
#d delta a all
#_ //ra//da
def local_to_global(r,A):
    return TwoVec(x=r.x*cos(A)-r.y*sin(A),y=r.x*sin(A)+r.y*cos(A),a=A)
def global_to_local(r,A):
    return TwoVec(x=r.x*cos(-A)-r.y*sin(-A),y=r.x*sin(-A)+r.y*cos(-A),a=-A)

def l_get_r_position(_r):
    return _r
def g_get_r_position(_r,p):
    return local_to_global(_r,p.a)
def g_get_a_position(_r,p):
    return p+local_to_global(_r,p.a)

def l_get_r_velocity(_r,v):
    return TwoVec(x=-_r.y*v.a,y=_r.x*v.a,a=v.a)
def g_get_r_velocity(_r,p,v):
    return local_to_global(l_get_r_velocity(_r,v),p.a)
def g_get_a_velocity(_r,p,v):
    return g_get_r_velocity(_r,p,v)+v

def fake_hit_and_no_one_knows_why(mass,interia,mode,i_,_r,p,v):
    impuse=None
    delta=None
    def _hit(mass,interia,_i,r):
        return TwoVec(x=_i.x/mass,y=_i.y/mass,a=(_i.y*r.x-_i.x*r.y+_i.a)/interia)
    if mode[2]=="g":
        impuse=global_to_local(i_,p.a)
    else:
        impuse=i_
    delta=_hit(mass,interia,impuse,_r)
    if mode[0]=="d":
        if mode[1]=="l":
            return delta
        else:
            return local_to_global(delta,p.a)
    else:
        return local_to_global(delta,p.a)+v

def hit(mass,interia,mode,i,r,p,v):
    return v+TwoVec(x=i.x/mass,y=i.y/mass,a=(i.y*r.x-i.x*r.y+i.a)/interia)
#initial vars are functions so that they can be changed in different turns
#moving vars are float so they need to be calculated before start, and calc_ functions should be called in __main__
#values are functions so that they can be changed in different turns
class Object:
    def init_position(self,bs):
        i_position      =   bs.position.init_position
        self._position  =   TwoVec()
        self._position.x=   varType(i_position.x["var"])
        self._position.y=   varType(i_position.y["var"])
        self._position.a=   varType(i_position.a["var"])
    def calc_position(self):
        self.position   =   TwoVec()
        self.position.x =   self._position.x.var()
        self.position.y =   self._position.y.var()
        self.position.a =   self._position.a.var()

    def init_velocity(self,bs):
        i_velocity      =   bs.velocity.init_velocity
        self._velocity  =   TwoVec()
        self._velocity.x=   varType(i_velocity.x["var"])
        self._velocity.y=   varType(i_velocity.y["var"])
        self._velocity.a=   varType(i_velocity.a["var"])
    def calc_velocity(self):
        self.velocity   =   TwoVec()
        self.velocity.x =   self._velocity.x.var()
        self.velocity.y =   self._velocity.y.var()
        self.velocity.a =   self._velocity.a.var()

    def init_parameter(self,bs):
        self._id        =   varType(bs["id"])
        self._type      =   varType(bs["type"])
        self._enable    =   varType(bs["enable"])
        self._gravity   =   varType(bs["gravity"])
        self._mass      =   varType(bs["mass"])
        self._interia   =   varType(bs["interia"])
    def calc_parameter(self):
        self.id         =   self._id.var()
        self.type       =   self._type.var()
        self.enable     =   self._enable.var()
        self.gravity    =   self._gravity.var()
        self.mass       =   self._mass.var()
        self.interia    =   self._interia.var()

    def init_collision(self,bs):
        self.near_point =   {}
        self.away_point =   {}
        for p in bs.collision.find_all("point",{'type':'#near'}):
            self.near_point[Read(p["id"])]=Point()
            self.near_point[Read(p["id"])]._position.x=  varType(p.x["var"])
            self.near_point[Read(p["id"])]._position.y=  varType(p.y["var"])
            self.near_point[Read(p["id"])]._position.a=  varType(p.a["var"])
            self.near_point[Read(p["id"])]._r         =  varType("$None")
            self.near_point[Read(p["id"])]._id        =  varType(p["id"])
            self.near_point[Read(p["id"])]._next      =  varType(p["next"])
            self.near_point[Read(p["id"])]._enable    =  varType(p["enable"])
        for p in bs.collision.find_all("point",{"type":"#away"}):
            self.away_point[Read(p["id"])]=Point()
            self.away_point[Read(p["id"])]._position.x=  varType(p.x["var"])
            self.away_point[Read(p["id"])]._position.y=  varType(p.y["var"])
            self.away_point[Read(p["id"])]._position.a=  varType(p.a["var"])
            self.away_point[Read(p["id"])]._r         =  varType(p.r["var"])
            self.away_point[Read(p["id"])]._id        =  varType(p["id"])
            self.away_point[Read(p["id"])]._next      =  varType(p["next"])
            self.away_point[Read(p["id"])]._enable    =  varType(p["enable"])
    def calc_collision(self):
        for p in self.near_point:
            self.near_point[p].position.x   =self.near_point[p]._position.x.var()
            self.near_point[p].position.y   =self.near_point[p]._position.y.var()
            self.near_point[p].position.a   =self.near_point[p]._position.a.var()
            self.near_point[p].r            =self.near_point[p]._r.var()
            self.near_point[p].id           =self.near_point[p]._id.var()
            self.near_point[p].next         =self.near_point[p]._next.var()
            self.near_point[p].enable       =self.near_point[p]._enable.var()
        for p in self.away_point:
            self.away_point[p].position.x   =self.away_point[p]._position.x.var()
            self.away_point[p].position.y   =self.away_point[p]._position.y.var()
            self.away_point[p].position.a   =self.away_point[p]._position.a.var()
            self.away_point[p].r            =self.away_point[p]._r.var()
            self.away_point[p].id           =self.away_point[p]._id.var()
            self.away_point[p].next         =self.away_point[p]._next.var()
            self.away_point[p].enable       =self.away_point[p]._enable.var()

    def __init__(self,bs):
        self.init_position(bs)
        self.init_velocity(bs)
        self.init_parameter(bs)
        self.init_collision(bs)
        self.env={}

    def set_env(key,value):
        self.env[key]=value
    def has_env(key):
        if key in env:
            return True
        else:
            return False
    def unset_env(key):
        if key in env:
            _temp=env[key]
            del env[key]
            return _temp
        else:
            return None

    def get_near_position(self,p):
        return g_get_a_position(self.near_point[p].position,self.position)

    def get_near_velocity(self,p):
        return g_get_a_velocity(self.near_point[p].position,self.position,self.velocity)

    def get_away_position(self,p):
        return g_get_a_position(self.away_point[p].position,self.position)

    def get_away_velocity(self,p):
        return g_get_a_velocity(self.away_point[p].position,self.position,self.velocity)

    def move(self,delta_t,force):
        self.position.x=   self.velocity.x*delta_t    +self.position.x
        self.position.y=   self.velocity.y*delta_t    +self.position.y
        self.position.a=   self.velocity.a*delta_t    +self.position.a
        self.velocity.x=   force(self).x*delta_t   /self.mass+self.velocity.x
        self.velocity.y=   force(self).y*delta_t   /self.mass+self.velocity.y
        self.velocity.a=   force(self).a*delta_t/self.interia+self.velocity.a

    def DRAW(self,x11):
        this=TwoVec()
        x11.draw_dot(self.position.x,self.position.y)
        for p in self.near_point:
            next    =   self.near_point[p].next
            x11.draw_Line(self.get_near_position(p),self.get_near_position(next))
        for p in self.away_point:
            this    =   self.get_away_position(p)
            this.a  =   self.away_point[p].r
            x11.draw_Arc(this)
        x11.flush()

def force(self):
    global g
    return TwoVec(x=0,y=-g*self.mass,a=0)

#init arg
args = sys.argv[:]
argc = len(args)
#init xml and x11
f=open(args[3],'r',encoding="utf-8")
xml=f.read()
f.close()
xml_main=BeautifulSoup(xml,"html5lib")
screen=xml_main.screen
x11=X11(args[1],varType(screen["width"]).var(),varType(screen["height"]).var())
# ncurses=Ncurses(args[2])
xml_objects=xml_main.find_all("object",{"type":"#object"})
#init objects and points
objs={}

for xml_object in xml_objects:
    objs[Read(xml_object["id"])]=Object(xml_object)
exec(xml_main.init_value.string)
for i in objs:
    objs[i].calc_position()
    objs[i].calc_velocity()
    objs[i].calc_parameter()
    objs[i].calc_collision()
#
# ncurses.put_string(0,0,"test")
circle      =   0
draw_rate   =   1000
draw_count  =   0
delta_t     =   0.0001
Time        =   0
while True:
    circle      +=  1
    draw_count  +=  1
    Time        +=  delta_t
    x11.draw_base()
    # time.sleep(0.01)
    #x11.draw_func(lambda I:hit(objs[1].mass,objs[1].interia,"agg",TwoVec(x=0,y=I,a=0),TwoVec(x=0,y=0,a=0),objs[i].position,objs[i].velocity).y,0,100)
    for i in objs:
        objs[i].move(delta_t,force)
        for p in objs[i].near_point:
            if (objs[i].get_near_position(p).y<=0)&(objs[i].get_near_velocity(p).y<=0):
                if objs[i].near_point[p].touching==False:
                    objs[i].near_point[p].touching=True
                    objs[i].DRAW(x11)
                    print(str(objs[i].velocity.y))
                    objs[i].velocity=hit(objs[i].mass,objs[i].interia,"agg",TwoVec(x=0,y=NSolve(lambda iy:hit(objs[i].mass,objs[i].interia,"agg",TwoVec(x=0,y=iy,a=0),objs[i].near_point[p].position,objs[i].position,objs[i].velocity).y,-e*objs[i].get_near_velocity(p).y,0.000001),a=0),objs[i].near_point[p].position,objs[i].position,objs[i].velocity)
                    draw_rate=500
            else:
                objs[i].near_point[p].touching=False
    if draw_count>=draw_rate:
        draw_count=0
        for i in objs:
            objs[i].DRAW(x11)
    # if Time>=30:
        # for i in objs:
            # print("!")
            # print(objs[1].near_point[0].position.x)
            # print(objs[1].near_point[0].position.y)
            # objs[1].velocity=hit(objs[1].mass,objs[1].interia,"agg",TwoVec(x=0,y=1,a=0),objs[1].near_point[2].position,objs[1].position,objs[1].velocity)
            # print(objs[i].velocity.y)
            # print(objs[i].position.a)
            # debugging
        # Time=0
        # time.sleep(3)
        # del ncurses
        # os._exit(0)















































































