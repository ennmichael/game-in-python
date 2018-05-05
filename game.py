from typing import Callable, Optional, List, Iterable
import enum
import abc

import sdl
import utils


GRAVITY = 1000


# Redundant type aliases?
Checkbox = sdl.Rectangle
Checkboxes = Iterable[Checkbox]
MainLoopCallback = Callable[[utils.Seconds], None]


def main_loop(cb: MainLoopCallback, fps: int) -> None:
    end = start = utils.current_time()

    while not sdl.quit_requested():
        t = utils.current_time()
        delta = utils.Seconds(t - start)

        if delta < 1/fps:
            continue

        cb(delta)
        start = end
        end = t


class Sprite(abc.ABC):

    @abc.abstractmethod
    def render(self,
               renderer: sdl.Renderer,
               position: complex,
               flip: Optional[sdl.Flip]=None) -> None:
        pass

    @property
    @abc.abstractmethod
    def dimensions(self) -> sdl.Dimensions:
        pass

    def update(self) -> None:
        pass


class Animation(Sprite):

    def __init__(self,
                 sprite_sheet: sdl.Texture,
                 frames: List[sdl.Rectangle],
                 frame_delay: utils.Seconds) -> None:
        self.sprite_sheet = sprite_sheet
        self.frames = frames
        self.frame_delay = frame_delay
        self.start_time = utils.current_time()
        self.current_frame_num = 0

    def render(self,
               renderer: sdl.Renderer,
               position: complex,
               flip: Optional[sdl.Flip]=None) -> None:
        renderer.render_texture(
            self.sprite_sheet,
            src=self.current_frame,
            dst=sdl.Rectangle(position,
                              self.current_frame.dimensions),
            flip=flip)

    @property
    def current_frame(self) -> sdl.Rectangle:
        return self.frames[self.current_frame_num]

    @property
    def dimensions(self) -> sdl.Dimensions:
        return self.current_frame.dimensions

    def update(self) -> None:
        self.update_current_frame_num()

    def update_current_frame_num(self) -> None:
        t = self.time_since_start()
        self.current_frame_num = (int(t / self.frame_delay) % len(self.frames))

    def done(self) -> bool:
        return self.time_since_start() > self.frame_delay * len(self.frames)

    def time_since_start(self) -> utils.Seconds:
        return utils.Seconds(utils.current_time() - self.start_time)


class Image(Sprite):

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

    @property
    def dimensions(self) -> sdl.Dimensions:
        return self.frame.dimensions


# TODO We shouldn't need this in the future
def even_frames(first_frame: sdl.Rectangle,
                frame_count: int) -> List[sdl.Rectangle]:
    return [
        sdl.Rectangle(first_frame.width * i, first_frame.dimensions)
        for i in range(0, frame_count)
    ]


@enum.unique
class Direction(enum.Enum):

    LEFT = enum.auto()
    RIGHT = enum.auto()

    def to_flip(self) -> sdl.Flip:
        if self == Direction.LEFT:
            return sdl.Flip.HORIZONTAL
        return sdl.Flip.NONE


class Entity:
    def __init__(self, position: complex, sprite: Sprite) -> None:
        self.position = position
        self.sprite = sprite

    @property
    def checkbox(self) -> Checkbox:
        return sdl.Rectangle(self.position, self.sprite.dimensions)

    def update_sprite(self) -> None:
        self.sprite.update()


class MovingEntity(Entity):
    def __init__(self,
                 position: complex,
                 direction: Direction,
                 velocity: complex,
                 sprite: Sprite) -> None:
        super().__init__(position, sprite)
        self.direction = direction
        self.velocity = velocity

    def update_physics(self,
                       solid_boxes: Checkboxes,
                       delta: utils.Seconds) -> None:
        self.apply_gravity(delta)

        displacement = self.velocity * delta
        imag_position_delta = displacement.imag
        real_position_delta = displacement.real

        # Smarter way to do this without the slight glitching

        for box in solid_boxes:
            if self.checkbox.vertically_overlaps(box):
                if self.checkbox.is_above(box):
                    d = box.upper_left.imag - self.checkbox.lower_left.imag
                    if d < displacement.imag:
                        imag_position_delta = d
                else:
                    d = self.checkbox.upper_left.imag - box.lower_left.imag
                    if d < -displacement.imag:
                        imag_position_delta = -d
            elif self.checkbox.horizontally_overlaps(box):
                if self.checkbox.is_left_from(box):
                    d = box.upper_right.real - self.checkbox.upper_left.real
                    if d < displacement.real:
                        real_position_delta = d
                else:
                    d = self.checkbox.upper_left.real - box.upper_right.real
                    if d < -displacement.real:
                        real_position_delta = -d

        self.position += real_position_delta + imag_position_delta * 1j

    def apply_gravity(self, delta: utils.Seconds) -> None:
        self.velocity += GRAVITY * delta * delta * 1j
