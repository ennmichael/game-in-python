from typing import Callable, Optional, List
import enum
import abc

import sdl
import utils
import collision


GRAVITY = 0.001


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

    @abc.abstractmethod
    @property
    def checkbox(self) -> collision.Box:
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
    def checkbox(self) -> collision.Box:
        return self.current_frame

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
    def checkbox(self) -> collision.Box:
        return self.sprite.checkbox
    
    def update_sprite(self) -> None:
        self.sprite.update()


class MovingEntity(Entity):
    def __init__(self,
                 position: complex,
                 sprite: Sprite,
                 direction: Direction,
                 velocity: complex=0+0j) -> None:
        super().__init__(position, sprite)
        self.direction = direction
        self.velocity = velocity

    def update_physics(self,
                       walls: collision.Walls,
                       delta: utils.Seconds) -> None:
        self.apply_gravity(delta)
        self.update_velocity(walls, delta)
        self.update_position(delta)

    def apply_gravity(self, delta: utils.Seconds) -> None:
        self.velocity += GRAVITY * delta * delta * 1j

    def update_velocity(self,
                        walls: collision.Walls,
                        delta: utils.Seconds) -> None:
        col = collision.detect(self.checkbox,
                               self.velocity,
                               walls,
                               delta)

        if col:
            pass

    def update_position(self, delta: utils.Seconds) -> None:
        self.position += self.velocity * delta
