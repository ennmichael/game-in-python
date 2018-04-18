import utils
import game
import enum


class Igor:

    @enum.unique
    class State(utils.Flag):

        NONE = 0x00
        MOVING = 0x01
        ATTACKING = 0x02

    def __init__(self, position: complex) -> None:
        self.state = Igor.State.NONE
        self.position = position
        self.animation = None
        # Have resources injected in here

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

    def update(self) -> None:
        pass

    @property
    def standing_still(self) -> bool:
        return not self.state.has_flag(Igor.State.MOVING)
        # TODO This is a bug, we need to check if Igor is mid-air here too

    def move_left(self) -> None:
        if not self.state.has_flag(Igor.State.MOVING):
            self.state.set_flag(Igor.State.MOVING)
            self.direction = game.Direction.LEFT

    def move_right(self) -> None:
        if not self.state.has_flag(Igor.State.MOVING):
            self.state.set_flag(Igor.State.MOVING)
            self.direction = game.Direction.LEFT

    def move_in_direction(self, direction: game.Direction) -> None:
        pass

    def stand_still(self) -> None:
        pass
