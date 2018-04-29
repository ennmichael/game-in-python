import enum
import functools

import utils
import game
import sdl
import collision


class Wolfram:

    class Sprites:

        def __init__(self, textures: sdl.LoadedTextures) -> None:

            sprite_sheet = textures[b'sprites/igor.png']

            self.still = functools.partial(
                game.Image,
                sprite_sheet,
                frame=sdl.Rectangle(0 + 0j, sdl.Dimensions(100, 160)))

            self.running = functools.partial(
                game.Animation,
                sprite_sheet,
                frames=game.even_frames(
                    sdl.Rectangle(0 + 0j, sdl.Dimensions(100, 160)), 8),
                frame_delay=utils.Seconds(0.15))

    SPEED = 90

    @enum.unique
    class State(enum.Enum):

        STILL = enum.auto()
        RUNNING = enum.auto()

    def __init__(self,
                 position: complex,
                 textures: sdl.LoadedTextures) -> None:
        self.direction = game.Direction.RIGHT
        self.state = Wolfram.State.STILL
        self.position = position
        self.velocity = 0 + 0j
        self.sprites = Wolfram.Sprites(textures)
        self.sprite: game.Sprite = self.sprites.still()

    @property
    def checkbox(self) -> collision.Box:
        return self.sprite.checkbox

    def render(self, renderer: sdl.Renderer) -> None:
        self.sprite.render(renderer,
                           self.position,
                           self.direction.to_flip())

    def move_right(self) -> None:
        if (self.state != Wolfram.State.RUNNING
                or self.direction != game.Direction.RIGHT):
            self.state = Wolfram.State.RUNNING
            self.sprite = self.sprites.running()
            self.velocity = Wolfram.SPEED + self.velocity.imag * 1j
            self.direction = game.Direction.RIGHT

    def move_left(self) -> None:
        if (self.state != Wolfram.State.RUNNING
                or self.direction != game.Direction.LEFT):
            self.state = Wolfram.State.RUNNING
            self.sprite = self.sprites.running()
            self.velocity = -Wolfram.SPEED + self.velocity.imag * 1j
            self.direction = game.Direction.LEFT

    def stand_still(self) -> None:
        if self.state != Wolfram.State.STILL:
            self.state = Wolfram.State.STILL
            self.sprite = self.sprites.still()
            self.velocity = self.velocity.imag * 1j

    def can_jump(self) -> bool:
        pass

    def jump(self) -> None:
        pass

    def handle_keyboard(self, keyboard: sdl.Keyboard) -> None:
        if keyboard.key_down(sdl.Scancode.LEFT):
            self.move_left()
        elif keyboard.key_down(sdl.Scancode.RIGHT):
            self.move_right()
        else:
            self.stand_still()
