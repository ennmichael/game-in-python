import utils

import game
import enum
import sdl
import functools


class Igor:

    class Sprites:

        def __init__(self, textures: sdl.LoadedTextures) -> None:

            sprite_sheet = textures[b'sprites/igor.png']

            self.still = functools.partial(game.Animation, sprite_sheet)
            self.running = functools.partial(game.Animation, sprite_sheet)
            # TODO Other parameters too

    SPEED = 90

    @enum.unique
    class State(utils.Flag):

        NONE = 0x00
        ATTACKING = 0x01

    def __init__(self,
                 position: complex,
                 textures: sdl.LoadedTextures) -> None:
        self.direction = game.Direction.RIGHT
        self.state = Igor.State.NONE
        self.position = position
        self.velocity = 0 + 0j
        self.sprites = Igor.Sprites(textures)
        self.sprite = self.sprites.still()

    def render(self, renderer: sdl.Renderer) -> None:
        self.sprite.render(renderer,
                           self.position,
                           self.direction.to_flip())

    @property
    def time_since_state_change(self) -> utils.Seconds:
        return utils.Seconds(utils.current_time() - self.state_change_time)

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, s: State) -> None:
        self._state = s
        self.state_change_time = utils.current_time()

    def update(self, delta: utils.Seconds) -> None:
        self.update_position(delta)
        self.apply_gravity(delta)

    def update_position(self, delta: utils.Seconds) -> None:
        self.position += self.velocity * delta

    def apply_gravity(self, delta: utils.Seconds) -> None:
        pass

    def move_right(self) -> None:
        self.direction = game.Direction.RIGHT
        self.velocity = Igor.SPEED + self.velocity.imag * 1j

    def move_left(self) -> None:
        self.direction = game.Direction.LEFT
        self.velocity = -Igor.SPEED + self.velocity.imag * 1j

    def stand_still(self) -> None:
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
