from typing import Callable, Optional, Any
import enum

import sdl
import utils


GRAVITY = 0.001


MainLoopCallback = Callable[[utils.Seconds], None]


def main_loop(cb: MainLoopCallback) -> None:
    end = start = utils.current_time()

    while not sdl.quit_requested():
        delta = utils.Seconds(end - start)
        start = end
        cb(delta)
        end = utils.current_time()


class Animation:

    def __init__(self,
                 sprite_sheet: sdl.Texture,
                 frame_count: int,
                 frame_delay: utils.Seconds,
                 frame_width: int,
                 start_x: int=0) -> None:
        self.sprite_sheet = sprite_sheet
        self.start_x = start_x
        self.frame_count = frame_count
        self.frame_delay = frame_delay
        frame_height = sprite_sheet.height
        self.frame_dimensions = sdl.Dimensions(frame_width, frame_height)
        self.start_time = utils.current_time()

    def render(self,
               renderer: sdl.Renderer,
               position: complex,
               flip: Optional[sdl.Flip]=None) -> None:
        renderer.render_texture(self.sprite_sheet,
                                self.src_rectangle(),
                                self.dst_rectangle(position),
                                flip)

    def rewind(self) -> None:
        self.start_time = utils.current_time()

    @property
    def done(self) -> bool:
        return self.time_since_start > self.frame_delay * self.frame_count

    @property
    def current_frame(self) -> int:
        return int(self.time_since_start/self.frame_delay) % self.frame_count

    @property
    def time_since_start(self) -> utils.Seconds:
        return utils.Seconds(utils.current_time() - self.start_time)

    def src_x(self) -> int:
        delta_x = self.current_frame * self.frame_dimensions.width
        return self.start_x + delta_x

    def src_rectangle(self) -> sdl.Rectangle:
        return sdl.Rectangle(self.src_x(),
                             0,
                             self.frame_dimensions.width,
                             self.frame_dimensions.height)

    def dst_rectangle(self, position: complex) -> sdl.Rectangle:
        return sdl.Rectangle(int(position.real), int(position.imag),
                             self.frame_dimensions.width,
                             self.frame_dimensions.height)


@enum.unique
class Direction(enum.IntEnum):

    LEFT = enum.auto()
    RIGHT = enum.auto()


class Entity:

    def __init__(self, position: complex) -> None:
        self.position = position

    def apply_gravity(self, delta: utils.Seconds) -> None:
        pass

    def update_position(self, delta: utils.Seconds) -> None:
        pass


class DynamicEntity(Entity):
    
    def __init__(self, position: complex, velocity: complex) -> None:
        super().__init__(position)
        self.velocity = velocity
    
    def apply_gravity(self, delta: utils.Seconds) -> None:
        self.velocity += GRAVITY * (delta ** 2) * 1j

    def update_position(self, delta: utils.Seconds) -> None:
        self.position += self.velocity * delta
