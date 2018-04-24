from typing import Callable, Optional, List, Union, Any, Iterable
import enum

import sdl
import utils
import collision


GRAVITY = 0.001


MainLoopCallback = Callable[[utils.Seconds], None]


def main_loop(cb: MainLoopCallback) -> None:
    end = start = utils.current_time()

    while not sdl.quit_requested():
        delta = utils.Seconds(end - start)
        cb(delta)
        start = end
        end = utils.current_time()


class Animation:

    def __init__(self,
                 sprite_sheet: sdl.Texture,
                 frames: List[sdl.Rectangle],
                 frame_delay: utils.Seconds) -> None:
        self.sprite_sheet = sprite_sheet
        self.frames = frames
        self.frame_delay = frame_delay
        self.start_time = utils.current_time()

    def render(self,
               renderer: sdl.Renderer,
               position: complex,
               flip: Optional[sdl.Flip]=None) -> None:
        current_frame = self.current_frame()
        renderer.render_texture(self.sprite_sheet,
                                src=current_frame,
                                dst=sdl.Rectangle(int(position.real),
                                                  int(position.imag),
                                                  current_frame.width,
                                                  current_frame.height),
                                flip=flip)

    def done(self) -> bool:
        return self.time_since_start() > self.frame_delay * len(self.frames)

    def current_frame(self) -> sdl.Rectangle:
        i = int(self.time_since_start()/self.frame_delay) % len(self.frames)
        print(self.time_since_start())
        return self.frames[i]

    def time_since_start(self) -> utils.Seconds:
        return utils.Seconds(utils.current_time() - self.start_time)


class Image:

    def __init__(self,
                 sprite_sheet: sdl.Texture,
                 frame: sdl.Rectangle) -> None:
        self.sprite_sheet = sprite_sheet
        self.frame = frame

    def render(self,
               renderer: sdl.Renderer,
               position: complex,
               flip: Optional[sdl.Flip]=None) -> None:
        renderer.render_texture(self.sprite_sheet,
                                src=self.frame,
                                dst=sdl.Rectangle(int(position.real),
                                                  int(position.imag),
                                                  self.frame.width,
                                                  self.frame.height),
                                flip=flip)


Sprite = Union[Image, Animation]


# TODO We shouldn't need this in the future
def even_frames(first_frame: sdl.Rectangle,
                frame_count: int) -> List[sdl.Rectangle]:
    return [
        sdl.Rectangle(first_frame.width * i, 0,
                      first_frame.width, first_frame.height)
        for i in range(0, frame_count)
    ]


Box = sdl.Rectangle
Boxes = Iterable[Box]


def update_velocity(entity: Any, boxes: Boxes) -> None:
    pass


def will_collide(entity: Any, box: Box, delta) -> bool:
    pass


def update_physics(entity: Any, delta: utils.Seconds, boxes: Boxes) -> None:
    collision.update_velocity(entity, boxes)
    update_position(entity, delta)
    apply_gravity(entity, delta)


def update_position(entity: Any, delta: utils.Seconds, boxes: Boxes) -> None:
    entity.position += entity.velocity * delta


def apply_gravity(entity: Any, delta: utils.Seconds) -> None:
    entity.velocity += GRAVITY * delta * delta * 1j


@enum.unique
class Direction(enum.Enum):

    LEFT = enum.auto()
    RIGHT = enum.auto()

    def to_flip(self) -> sdl.Flip:
        if self == Direction.LEFT:
            return sdl.Flip.HORIZONTAL
        return sdl.Flip.NONE
