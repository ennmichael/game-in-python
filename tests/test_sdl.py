import unittest

from game import sdl


class TestRectangles(unittest.TestCase):

    TRUE_HORIZONTAL_CASES = [
        (sdl.Rectangle(10 + 1j, sdl.Dimensions(10, 10)),
         sdl.Rectangle(10 + 2j, sdl.Dimensions(20, 20))),

        (sdl.Rectangle(10 + -3j, sdl.Dimensions(10, 30)),
         sdl.Rectangle(20 + -4j, sdl.Dimensions(5, 40))),

        (sdl.Rectangle(0 + 5j, sdl.Dimensions(10, 50)),
         sdl.Rectangle(-3 + -6j, sdl.Dimensions(5, 60))),

        (sdl.Rectangle(0 + 7j, sdl.Dimensions(10, 70)),
         sdl.Rectangle(-5 + 8j, sdl.Dimensions(5, 880))),

        (sdl.Rectangle(0 + -9j, sdl.Dimensions(10, 3210)),
         sdl.Rectangle(5 + 123236j, sdl.Dimensions(3, 123220)))
    ]

    FALSE_HORIZONTAL_CASES = [
        (sdl.Rectangle(10 + 112j, sdl.Dimensions(10, 64740)),
         sdl.Rectangle(-25 + -223j, sdl.Dimensions(20, 7720)))
    ]

    def test_horizontally_overlaps(self) -> None:
        for r1, r2 in TestRectangles.TRUE_HORIZONTAL_CASES:
            self.assertTrue(r1.horizontally_overlaps(r2))
            self.assertTrue(r2.horizontally_overlaps(r1))

        for r1, r2 in TestRectangles.FALSE_HORIZONTAL_CASES:
            self.assertFalse(r1.horizontally_overlaps(r2))
            self.assertFalse(r2.horizontally_overlaps(r1))

    def test_vertically_overlaps(self) -> None:
        def invert_rectangle(r: sdl.Rectangle) -> sdl.Rectangle:
            return sdl.Rectangle(r.upper_left.imag + r.upper_left.real * 1j,
                                 sdl.Dimensions(r.dimensions.height,
                                                r.dimensions.width))

        for r1, r2 in ((invert_rectangle(r1), invert_rectangle(r2))
                       for r1, r2 in TestRectangles.TRUE_HORIZONTAL_CASES):
                self.assertTrue(r1.vertically_overlaps(r2))
                self.assertTrue(r2.vertically_overlaps(r1))

        for r1, r2 in ((invert_rectangle(r1), invert_rectangle(r2))
                       for r1, r2 in TestRectangles.FALSE_HORIZONTAL_CASES):
            self.assertFalse(r1.vertically_overlaps(r2))
            self.assertFalse(r2.vertically_overlaps(r1))
