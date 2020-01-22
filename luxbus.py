#!/usr/bin/env python3
from subprocess import Popen, PIPE
from contextlib import contextmanager

from threading import Thread
import time, os

DBUS_KEY_LOGIN = "org.freedesktop.login1"
DBUS_MONITOR_COMMAND = "gdbus monitor -y -d".split(" ")

@contextmanager
def gdbus_monitor(key):
    cmd = DBUS_MONITOR_COMMAND + [key]
    with Popen(cmd, stdout=PIPE) as proc:
        print("starting dbus monitor", cmd)
        yield proc.stdout
        print("stopping dbus monitor", cmd)

class Login:
    UNKNOWN    = 'UNKNOWN'
    LOGGED_IN  = 'LOGGED_IN'
    LOGGED_OFF = 'LOGGED_OFF'

    state = LOGGED_IN
    state_change_delay = 0.05  # 50ms

    watcher:Thread = None
    subscribers:list = None

    def __init__(l):
        l.subscribers = []

    def debug(l, *args):
        if os.environ.get("DEBUG"):
            print("DEBUG:", *args)

    def read_dbus_line(l, line):
        if "user" not in line:
            # only listen to "user" events
            return
        elif "'IdleHint': <true>"    in line: l.state = Login.LOGGED_OFF
        elif "'IdleHint': <false>"   in line: l.state = Login.LOGGED_IN
        elif "'LockedHint': <true>"  in line: l.state = Login.LOGGED_OFF
        elif "'LockedHint': <false>" in line: l.state = Login.LOGGED_IN
        else:
            # no callback or delay required if state is not changed
            return

        l.debug("dbus line:", line, "derived state:", l.state)

        for cb in l.subscribers: cb(l.state)
        time.sleep(l.state_change_delay)

    def read_dbus(l):
        print("Login.watcher started")
        with gdbus_monitor(DBUS_KEY_LOGIN) as stream:
            for line in stream: l.read_dbus_line(str(line))
        print("Login.watcher stopped")

    def watch(l):
        # send default state to subscribers
        for cb in l.subscribers: cb(l.state)
        # start watching state changes
        l.watcher = t = Thread(target=l.read_dbus)
        t.daemon = True
        t.start()
        # join the watcher Thread shortly to allow startup
        t.join(0.1)
        l.debug("watcher Thread is up!")
        return l

    def join(l, timeout=None):
        l.watcher.join(timeout=timeout)
        return l

def main(): Login().watch().join()

if __name__ == '__main__': main()
