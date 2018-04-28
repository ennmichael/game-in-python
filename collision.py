from typing import Iterable, Any

import sdl
import utils


Wall = utils.BoundVector
Box = sdl.Rectangle
Walls = Iterable[Wall]
Boxes = Iterable[Box]


def detect(entity: Any, walls: Walls, delta: utils.Seconds) -> Iterable[Wall]:
    yield from (wall for wall in walls if will_collide(entity.velocity,
                                                       wall,
                                                       delta))


def will_collide(entity: Any, wall: Wall, delta: utils.Seconds) -> bool:
    v = utils.BoundVector(entity.position, entity.velocity * delta)
    return utils.vectors_intersect(v, wall)
