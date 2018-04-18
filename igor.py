import utils

import game
import enum
import sdl


class Igor:

    MAX_SPEED = 90
    ACCELERATION = 0.2

    @enum.unique
    class State(utils.Flag):

        NONE = 0x00
        ATTACKING = 0x02

    def __init__(self,
                 position: complex,
                 textures: sdl.LoadedTextures) -> None:
        self.direction = game.Direction.RIGHT
        self.state = Igor.State.NONE
        self.position = position
        self.velocity = 0 + 0j
        self.animation = game.Animation(textures[b'sprites/running.png'],
                                        frame_count=8,
                                        frame_delay=utils.Seconds(0.15),
                                        frame_width=100,
                                        start_x=0)

    def render(self, renderer: sdl.Renderer) -> None:
        self.animation.render(renderer,
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

    def move_right(self) -> None:
        self.direction = game.Direction.RIGHT
        if self.velocity.real < self.max_speed:
            self.velocity += self.acceleration

    def move_left(self) -> None:
        self.direction = game.Direction.LEFT
        if self.velocity.real > -self.max_speed:
            self.velocity -= self.acceleration

    def jump(self) -> None:
        pass

    def handle_keyboard(self, keyboard: sdl.Keyboard) -> None:
        if keyboard.key_down(sdl.Scancode.LEFT):
            self.move_left()
        elif keyboard.key_down(sdl.Scancode.RIGHT):
            self.move_right()
        else:
            self.slow_down()

    def slow_down(self) -> None:
        if self.velocity.real != 0:
            mult = self.velocity.real / abs(self.velocity.real)
            self.velocity -= mult * self.acceleration * 2
            if abs(self.velocity.real) < 0:
                self.velocity = 0 + self.velocity.imag * 1j
