gcc ./draw.c -fPIC -shared -o ./libdraw.so -lX11
gcc ./curses.c -fPIC -shared -o ./libcurses.so -lncurses