""" customized deque """
from collections import deque


class DeQueue(deque):
    def __init__(self, iterable=(), maxlen=20):
        super().__init__(iterable, maxlen)

        self.__index: int = -1

    @property
    def idx(self):
        return self.__index % len(self)

    def here(self):
        if (length := len(self)) != 0:
            return self[self.__index % length]

    def prev(self):
        self.__index -= 1
        return self.here()

    def next(self):
        self.__index += 1
        return self.here()
