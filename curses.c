#include <string.h>
#include <ncurses.h>
//gcc testncurses.c -o testcurses -lncurses
void init(void){
    initscr();
    cbreak();
    noecho();
    if(has_colors()){
        start_color();
    }
    curs_set(0);
}
void put_float(int x,int y,float number){
    char c[1024];
    sprintf(c,"%f",number);
    mvprintw(x,y,c);
    refresh();
}
void put_char(int x,int y,char c){
    mvprintw(x,y,&c);
    refresh();
}
void fresh(void){
    refresh();
}
void end(void){
    endwin();
}
// int main(int argc,char* argv[]){
    // initscr();
    // raw();
    // noecho();
    // curs_set(0);

    // char* c = "Hello, World!";

    // mvprintw(LINES/2,(COLS-strlen(c))/2,c);
    // mvprintw(0,0,c);
    // refresh();

    // getch();
    // endwin();

    // return 0;
// }