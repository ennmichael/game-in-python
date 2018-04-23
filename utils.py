from typing import NewType
import time
import enum


Seconds = NewType('Seconds', float)


def current_time() -> Seconds:
    return Seconds(time.time())
