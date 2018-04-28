from typing import Iterable, Any
import sdl
import utils


Wall = utils.Vector
Box = sdl.Rectangle
Walls = Iterable[Wall]
Boxes = Iterable[Box]


def detect(entity: Any, walls: Walls, delta: utils.Seconds) -> Iterable[Wall]:
    yield from (wall for wall in walls if will_collide(entity.velocity,
                                                       wall,
                                                       delta))


def will_collide(entity: Any, wall: Wall, delta: utils.Seconds) -> bool:
    # Help in understanding this: https://stackoverflow.com/a/565282/5736791
    # Also keep in mind that the cross product of 2D vectors is actually a scalar,
    # which is the sourface of the parallelorgam formed by the two vectors.

    d = (utils.cross(entity.position - wall.position, entity.velocity)
         / utils.cross(entity.velocity, wall.free_vector)

    return 0 <= d <= 1
