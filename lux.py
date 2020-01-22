#!/usr/bin/env python3

from luxafor import LuxaforFlag as LF
from luxbus import Login
import sys, tty, termios, fcntl, os
from contextlib import contextmanager

def usage():
    print("""

    Commands
    ========
    q|Q|Ctrl-C exit
    h|H|u|U    show help/usage
    x|X        turn LEDs off

    Colors and Patterns
    ===================
    P    Police pattern
    R    Rainbow pattern
    w    white
    r    red
    g    green
    b    blue
    y    yellow
    p    pink
    c    cyan

    """)

# source of IO code: http://ballingt.com/nonblocking-stdin-in-python-3
@contextmanager
def raw(stream):
    original_stty = termios.tcgetattr(stream)
    try:
        tty.setcbreak(stream)
        yield
    finally:
        termios.tcsetattr(stream, termios.TCSANOW, original_stty)

@contextmanager
def nonblocking(stream):
    fd = stream.fileno()
    orig_fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    try:
        fcntl.fcntl(fd, fcntl.F_SETFL, orig_fl | os.O_NONBLOCK)
        yield
    finally:
        fcntl.fcntl(fd, fcntl.F_SETFL, orig_fl)

def main():
    lf = LF()
    login = Login()
    login.subscribers.append(lambda state: on_change_login_state(lf, state))
    login.watch()
    with raw(sys.stdin):
        with nonblocking(sys.stdin):
            main_loop(lf, login)

def getch(): return str(sys.stdin.read(1))

def on_change_login_state(lf, state):
    print("changed state:", state)
    if   state == Login.LOGGED_IN:  rgb = (0,   255,   0)
    elif state == Login.LOGGED_OFF: rgb = (128,   0, 128)
    else: return
    lf.set_colors(rgb, None)

def main_loop(lf, login):
    usage()
    print("LUXAFOR Control started, press Q to quit or H to show help.")
    rgb, pat, rep = (255, 0, 0), None, 1
    while True:
        login.join(0.1)  # join the login watcher Thread instead of sleeping here
        cmd = getch()
        if   cmd in ("q", "Q"): break
        elif cmd in ("h", "H"): usage()
        elif cmd == "":   continue
        elif cmd == "x":  lf.off(); continue
        elif cmd == "P":  rgb, pat, rep = None, LF.PATTERN_POLICE,      3
        elif cmd == "R":  rgb, pat, rep = None, LF.PATTERN_RAINBOWWAVE, 5
        elif cmd == "w":  rgb, pat = (255, 255, 255), None
        elif cmd == "r":  rgb, pat = (255,   0,   0), None
        elif cmd == "g":  rgb, pat = (0,   255,   0), None
        elif cmd == "b":  rgb, pat = (0,     0, 255), None
        elif cmd == "y":  rgb, pat = (128, 128,   0), None
        elif cmd == "p":  rgb, pat = (128,   0, 128), None
        elif cmd == "c":  rgb, pat = (  0, 128, 128), None

        # elif cmd == "rl": f.do_static_colour(LF.LED_ALL, 192,  32,  32); pat = None
        # elif cmd == "gl": f.do_static_colour(LF.LED_ALL,  32, 192,  32); pat = None
        # elif cmd == "bl": f.do_static_colour(LF.LED_ALL,  32,  32, 192); pat = None
        lf.set_colors(rgb, pat, rep=rep)


if __name__ == '__main__': main()
