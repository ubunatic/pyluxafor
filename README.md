# pyluxafor

Control your Luxafor light from the command line!
Requires `python-usb` in and `gdbus` in Linux. Requires Linux.
For Mac and Windows, just use the official app or submit a patch here!

```
sudo ./lux.py  
changed state: LOGGED_IN
setting pat: None rgb (0, 255, 0)
Login.watcher started
LUXAFOR Control started, press Q to quit
starting dbus monitor ['gdbus', 'monitor', '-y', '-d', 'org.freedesktop.login1']
```

Press `h` for help.

```
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
```

Press any button to set colors and patterns. Have fun!