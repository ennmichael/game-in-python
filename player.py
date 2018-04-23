import utils

import game
import enum
import sdl
import functools


class Igor:

    class Sprites:

        def __init__(self, textures: sdl.LoadedTextures) -> None:

            sprite_sheet = textures[b'sprites/igor.png']

            self.still = functools.partial(game.Image,
                                           sprite_sheet,
                                           frame=sdl.Rectangle(0, 0,
                                                               100, 160))

            self.running = functools.partial(
                game.Animation,
                sprite_sheet,
                frames=game.even_frames(sdl.Rectangle(0, 0, 100, 160), 8),
                frame_delay=utils.Seconds(0.15))

    SPEED = 90

    @enum.unique
    class State(enum.Enum):

        STILL = enum.auto()
        ATTACKING = enum.auto()
        RUNNING = enum.auto()

    def __init__(self,
                 position: complex,
                 textures: sdl.LoadedTextures) -> None:
        self.direction = game.Direction.RIGHT
        self.state = Igor.State.STILL
        self.position = position
        self.velocity = 0 + 0j
        self.sprites = Igor.Sprites(textures)
        self.sprite: game.Sprite = self.sprites.still()

    def render(self, renderer: sdl.Renderer) -> None:
        self.sprite.render(renderer,
                           self.position,
                           self.direction.to_flip())

    def move_right(self) -> None:
        if self.state != Igor.State.RUNNING:
            self.state = Igor.State.RUNNING
            self.sprite = self.sprites.running()
            self.velocity = Igor.SPEED + self.velocity.imag * 1j
        self.direction = game.Direction.RIGHT

    def move_left(self) -> None:
        if self.state != Igor.State.RUNNING:
            self.state = Igor.State.RUNNING
            self.sprite = self.sprites.running()
            self.velocity = -Igor.SPEED + self.velocity.imag * 1j
        self.direction = game.Direction.LEFT

    def stand_still(self) -> None:
        if self.state != Igor.State.STILL:
            self.state = Igor.State.STILL
            self.sprite = self.sprites.still()
            self.velocity = self.velocity.imag * 1j

    def jump(self) -> None:
        pass

    def handle_keyboard(self, keyboard: sdl.Keyboard) -> None:
        if keyboard.key_down(sdl.Scancode.LEFT):
            self.move_left()
        elif keyboard.key_down(sdl.Scancode.RIGHT):
            self.move_right()
        else:
            self.stand_still()