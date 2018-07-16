import ctypes
import math
import random

def dummy():
    return

def PANIC(id,MoreInfomation,*more):
    print("PANIC at id "+repr(id))
    print(MoreInfomation)
    if "div_0" in more:
        number=1/0
    os._exit(id)
    while True:
        dummy()
    return

def str2bool(string):
    if string=="True":
        return True
    elif string=="None":
        return None
    else:
        return False

class TwoVec:
    def __init__(self,**xya):
        if "x" in xya:
            self.x=xya["x"]
        else:
            self.x=0
        if "y" in xya:
            self.y=xya["y"]
        else:
            self.y=0
        if "a" in xya:
            self.a=xya["a"]
        else:
            self.a=0
    def __add__(self,other):
        return TwoVec(x=self.x+other.x,y=self.y+other.y,a=self.a+other.a)

class X11:
    def __init__(self,lib,scr_width,scr_height):
        self.so=ctypes.CDLL(lib)
        self.so.init_x11(scr_width,scr_height)
        self.width=scr_width
        self.height=scr_height-1
    def draw_line(self,x1,y1,x2,y2):
        self.so.draw_line(int(x1),int(self.height-y1),int(x2),int(self.height-y2))
    def draw_Line(self,position1,position2):
        self.so.draw_line(int(position1.x),int(self.height-position1.y),int(position2.x),int(self.height-position2.y))
    def draw_dot(self,x,y):
        self.so.draw_dot(int(x),int(self.height-y))
    def draw_arc(self,x,y,w,h,ang1,ang2):
        self.so.draw_arc(int(x),int(self.height-y),int(w),int(h),int(ang1),int(ang2))
    def draw_Arc(self,p):
        self.draw_arc(p.x,p.y,p.a,p.a,0,64*360)
    def flush(self):
        self.so.x_flush()
    def draw_base(self):
        for x in range(0,int(self.width/100)+1):
            self.draw_line(100*x,0,100*x,self.height)
        for y in range(0,int(self.height/100)+1):
            self.draw_line(0,100*y,self.width,100*y)
    def draw_func(self,func,min_x,max_x,**more):
        x_rate=(max_x-min_x)
        if "y_rate" in more:
            _y_rate=more["y_rate"]
        else:
            _y_rate=1.0
        def _y(x):
            return _y_rate*func((max_x-min_x)*x/self.width)
        for x in range(0,self.width-1):
            #self.draw_dot(x,_y(x))
            self.draw_line(x,_y(x),x+1,_y(x+1))
    def __del__(self):
        self.so.close_display()

#must make sure that whatever you put in func,func can return a proper value
#and you had better wish that func(x_1) will never be equal to func(x_2) while x_1 is not equal to x_2
def NSolve_Cut(func,value,delta,**more):
    if "x_i" in more:
        x_i=more["x_i"]
    else:
        x_i=random.uniform(0,100)
    if "x_j" in more:
        x_j=more["x_j"]
    else:
        x_j=random.uniform(0,100)
    x_k=random.uniform(0,100)
    n=0
    def fund(x):
        return func(x)-value
    while func(x_i)==func(x_j):
        x_i=random.uniform(0,100)
        x_j=random.uniform(0,100)
    if abs(fund(x_k))<=abs(delta):
        return x_j
    while True:
        x_k=x_j-fund(x_j)/(fund(x_j)-fund(x_i))*(x_j-x_i)
        n=n+1
        if abs(fund(x_k))<=abs(delta):
            #print("NSolve:"+repr(n)+" times used")
            return x_k
        x_i=x_j
        x_j=x_k
        if func(x_i)==func(x_j):
            PANIC(x_j,"传进来的函数是弯的，没救了")
def NSolve_Revar(func,value,delta,**more):
    if "x" in more:
        x=more["x"]
    else:
        x=random.uniform(0,100)
    n=0
    def fund(x):
        return func(x)-value+x
    while True:
        x=fund(x)
        n=n+1
        if abs(fund(x)-x)<=abs(delta):
            print("NSolve:"+repr(n)+" times used")
            return x