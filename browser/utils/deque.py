""" customized deque """
from collections import deque


class DeQueue(deque):
    def __init__(self, iterable=(), maxlen=20):
        super().__init__(iterable, maxlen)

        self.__index: int = -1

    @property
    def idx(self):
        length = len(self)
        if length != 0:
            return self.__index % length

    def here(self):
        length = len(self)
        if length != 0:
            return self[self.__index % length]

    def prev(self):
        self.__index -= 1
        return self.here()

    def next(self):
        self.__index += 1
        return self.here()
