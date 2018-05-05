import math
import unittest


from game import game


class TestMovingEntity(unittest.TestCase):

    def example_entity(position: complex, velocity: complex) -> MovingEntity:
        return game.MovingEntity(position,
                                 game.Direction.RIGHT,
                                 velocity,
                                 sprite=None)

    def test_physics(self) -> None:
        # La di da
