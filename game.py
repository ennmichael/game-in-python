from typing import Callable, Optional, List, Union, Any
import enum
import collision

import sdl
import utils


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
                                dst=sdl.Rectangle(position,
                                                  current_frame.dimensions),
                                flip=flip)

    def done(self) -> bool:
        return self.time_since_start() > self.frame_delay * len(self.frames)

    def current_frame(self) -> sdl.Rectangle:
        i = int(self.time_since_start()/self.frame_delay) % len(self.frames)
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
                                dst=sdl.Rectangle(position,
                                                  self.frame.dimensions),
                                flip=flip)


Sprite = Union[Image, Animation]


# TODO We shouldn't need this in the future
def even_frames(first_frame: sdl.Rectangle,
                frame_count: int) -> List[sdl.Rectangle]:
    return [
        sdl.Rectangle(first_frame.width * i, first_frame.dimensions)
        for i in range(0, frame_count)
    ]


def update_physics(entity: Any,
                   walls: collision.Walls,
                   delta: utils.Seconds) -> None:
    apply_gravity(entity, delta)
    update_position(entity, walls, delta)


def update_position(entity: Any,
                    walls: collision.Walls,
                    delta: utils.Seconds) -> None:
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
