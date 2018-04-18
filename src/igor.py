import utils
import game
import enum


class Igor:

    @enum.unique
    class State(enum.Enum):

        STANDING = 0x01
        MOVING = 0x02
        ATTACKING = 0x04

    def __init__(self, position: complex) -> None:
        self.state = State.STANDING
        self.position = position
        self.animation = None
        # Have resources injected in here

    @property
    def time_since_state_change(self) -> Seconds:
        return utils.current_time() - self.state_change_time

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, s: State) -> None:
        self._state = s
        self.state_change_time = utils.current_time()

    def update(self) -> None:
        if self.state 
