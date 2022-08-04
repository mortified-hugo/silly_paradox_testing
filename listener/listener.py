import os
import time


class Listener:
    def __init__(self, path):
        self.filename = path
        self._cached_stamp = os.path.getmtime(self.filename)

    def run(self, func, *args):
        stamp = os.path.getmtime(self.filename)
        condition = (stamp == self._cached_stamp)
        time.sleep(1)
        if not condition:
            time.sleep(9)
            self._cached_stamp = stamp
            return func(*args)
        else:
            time.sleep(1)
