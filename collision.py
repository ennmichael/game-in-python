from typing import NamedTuple, Any, Optional, Iterable, Tuple

import sdl
import utils


Wall = utils.BoundVector
Box = sdl.Rectangle
Walls = Iterable[Wall]
Boxes = Iterable[Box]


class Collision(NamedTuple):

    entity_offset: complex
    wall: Wall


def detect(entity: Any,
           walls: Walls,
           delta: utils.Seconds) -> Optional[Collision]:
    for wall in walls:
        offset = collision_offset(entity, wall, delta)
        if offset:
            return Collision(offset, wall)
    return None


def collision_offset(entity: Any,
                     wall: Wall,
                     delta: utils.Seconds) -> Optional[complex]:
    offsets: Tuple[complex, complex, complex, complex] = (
        0 + 0j,
        entity.checkbox.width + 0j,
        entity.checkbox.height * 1j,
        entity.checkbox.width + entity.checkbox.height * 1j
    )

    displacement = entity.velocity * delta

    for offset in offsets:
        v = utils.BoundVector(entity.position + offset, displacement)
        if utils.vectors_intersect(v, wall):
            return offset

    return None
