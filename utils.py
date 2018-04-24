from typing import NewType
import time
import enum


Seconds = NewType('Seconds', float)


def current_time() -> Seconds:
    return Seconds(time.time())


def pairwise_multiply(a: complex, b: complex) -> complex:
    return a.real * b.real + a.imag * b.imag * 1j
