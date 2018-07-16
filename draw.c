#include<X11/Xlib.h>
#include<X11/X.h>
#include<X11/Xutil.h>
#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include <string.h>
#include <locale.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <dirent.h>
#include <sys/mman.h>
#include <sys/ipc.h>
#include <sys/shm.h>
Display *display;
Window win;
GC gc;
void init_x11(int win_width,int win_height){
    display = XOpenDisplay(getenv("DISPLAY")); 
    if (display == NULL){
        fprintf(stderr,"Cannot connect to X server\n"); 
        exit(EXIT_FAILURE);
    }
    
    int screen_num     = DefaultScreen(display);
    int screen_width   = DisplayWidth (display,screen_num);
    int screen_height  = DisplayHeight(display,screen_num);
    Window root_window = RootWindow(display,screen_num);
    unsigned long white_pixel=WhitePixel(display,screen_num);
    unsigned long black_pixel=BlackPixel(display,screen_num);
    XEvent event;

    int win_x=0;
    int win_y=0;
    win=XCreateSimpleWindow(display,root_window,win_x,win_y,win_width,win_height,0,black_pixel,white_pixel);

    XMapWindow(display,win);

    XGCValues values;
    values.cap_style = CapButt;
    values.join_style= JoinBevel;
    unsigned long valuemask = GCCapStyle | GCJoinStyle;
    if((gc = XCreateGC(display,win,valuemask,&values))<0){fprintf(stderr,"XCreateGC:\n");exit(EXIT_FAILURE);}
}
void x_flush(){
    XFlush(display);
}
void draw_line(int x1,int y1,int x2,int y2){
    XDrawLine(display, win, gc, x1, y1, x2,y2);
}
void draw_dot(int x,int y){
    XDrawPoint(display,win,gc,x,y);
}
void draw_arc(int x,int y,int w,int h,short angle1,short angle2){
    XArc arc;
    arc.x=x;
    arc.y=y;
    arc.width=w;
    arc.height=h;
    arc.angle1=angle1;
    arc.angle2=angle2;
    //XDrawArcs(display, win, gc,&arc,1);
    //XDrawArc(display, win, gc, 50-(15/2), 100-(15/2), 15, 15, 0, 360*64);
    XDrawArc(display, win, gc, x-(w/2), y-(h/2), w, h, angle1, angle2);
}
void close_display(){
    XCloseDisplay(display);
}