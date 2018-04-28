from typing import NewType, NamedTuple
import time


class BoundVector(NamedTuple):

    position: complex
    free_vector: complex


def cross(v1: complex, v2: complex) -> float:
    return v1.real * v2.imag - v1.imag * v2.real


Seconds = NewType('Seconds', float)


def current_time() -> Seconds:
    return Seconds(time.time())


def pairwise_multiply(a: complex, b: complex) -> complex:
    return a.real * b.real + a.imag * b.imag * 1j
