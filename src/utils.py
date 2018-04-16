from typing import NewType
import time


Seconds = NewType('Seconds', float)


def current_time() -> Seconds:
    return Seconds(time())
