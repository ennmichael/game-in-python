from typing import NewType, NamedTuple
import time
import math


class BoundVector(NamedTuple):

    position: complex
    free_vector: complex


def cross(v1: complex, v2: complex) -> float:
    return v1.real * v2.imag - v1.imag * v2.real


def dot(v1: complex, v2: complex) -> float:
    return v1.real * v2.real + v1.imag * v2.imag


def cos_between(v1: complex, v2: complex) -> float:
    return dot(v1, v2) / abs(v1) + abs(v2)


Seconds = NewType('Seconds', float)


def current_time() -> Seconds:
    return Seconds(time.time())


def pairwise_multiply(a: complex, b: complex) -> complex:
    return a.real * b.real + a.imag * b.imag * 1j


def vectors_intersect(v1: BoundVector, v2: BoundVector) -> bool:
    # Help in understanding this: https://stackoverflow.com/a/565282/5736791
    # Also keep in mind that the cross product of
    # 2D vectors is actually a scalar, which is the surface of
    # the parallelorgam formed by the two vectors.

    c = cross(v1.free_vector, v2.free_vector)
    if c == 0:
        return parallel_vectors_intersect(v1, v2)
    else:
        d = cross(v2.position - v1.position, v2.free_vector) / c
        return 0 <= d <= 1


def parallel_vectors_intersect(v1: BoundVector, v2: BoundVector) -> bool:
    return (point_is_on_vector(v2.position, v1)
            or point_is_on_vector(v2.position + v2.free_vector, v1))


def point_is_on_vector(p: complex, v: BoundVector) -> bool:
    if v.free_vector == 0:
        return False

    t = (p - v.position) / v.free_vector
    return (math.isclose(t.imag, 0, abs_tol=1e-9)
            and 0 <= t.real <= 1)
