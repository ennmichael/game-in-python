from typing import NewType
import time
import enum


Seconds = NewType('Seconds', float)


class Flag(enum.IntFlag):

    def set_flag(self, flag: 'Flag') -> 'Flag':
        return self | flag

    def unset_flag(self, flag: 'Flag') -> 'Flag':
        return self & ~flag

    def has_flag(self, flag: 'Flag') -> bool:
        return self & flag == flag


def current_time() -> Seconds:
    return Seconds(time.time())
