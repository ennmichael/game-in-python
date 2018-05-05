from typing import NewType, NamedTuple
import time


def cross(v1: complex, v2: complex) -> float:
    return v1.real * v2.imag - v1.imag * v2.real


def dot(v1: complex, v2: complex) -> float:
    return v1.real * v2.real + v1.imag * v2.imag


def cos_between(v1: complex, v2: complex) -> float:
    return dot(v1, v2) / abs(v1) / abs(v2)


def pairwise_multiply(a: complex, b: complex) -> complex:
    return a.real * b.real + a.imag * b.imag * 1j


Seconds = NewType('Seconds', float)


def current_time() -> Seconds:
    return Seconds(time.time())
