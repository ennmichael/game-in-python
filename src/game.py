from typing import Callable, NamedTuple
import sdl
import utils


MainLoopCallback = Callable[[utils.Seconds], None]


def main_loop(cb: MainLoopCallback) -> None:
    end = start = utils.current_time()

    while not sdl.quit_requested():
        delta = utils.Seconds(end - start)
        start = end
        cb(delta)
        end = utils.current_time()


class Sprite(NamedTuple):

    frame_count: int
    frame_delay: utils.Seconds
    dimensions: sdl.Dimensions


class SpriteSheet:

    def __init__(self, texture: sdl.Texture) -> None:
        self.texture = texture

    def render_sprite(self,
                      renderer: sdl.Renderer,
                      position: complex,
                      sprite: Sprite,
                      frame: int) -> None:
        width, height = sprite.dimensions
        renderer.render_texture(self.texture,
                                src=sdl.Rectangle(frame * width, 0,
                                                  width, height),
                                dst=sdl.Rectangle(int(position.real),
                                                  int(position.imag),
                                                  width, height))


class Animation:

    def __init__(self,
                 sprite_sheet: SpriteSheet,
                 sprite: Sprite) -> None:
        self.sprite_sheet = sprite_sheet
        self.change_sprite(sprite)

    def change_sprite(self, sprite: Sprite) -> None:
        self.sprite = sprite
        self.done = False
        self.start_time = utils.current_time()

    def render(self, renderer: sdl.Renderer, position: complex) -> None:
        frame = 0
        self.sprite_sheet.render_sprite(renderer,
                                        position,
                                        self.sprite,
                                        frame)

        # TODO This is where I stopped
        # What is needed next is to test the animation
        # and then implement keyboard handling
        # and then we can start implementing the game
