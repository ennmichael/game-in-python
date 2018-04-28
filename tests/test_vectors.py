import unittest

from game import utils


class TestVectors(unittest.TestCase):

    def test_intersection(self) -> None:
        intersecting_vectors = [
            (utils.BoundVector(0j, 10 + 10j),
             utils.BoundVector(10 + 0j, 0 + 10j)),

            (utils.BoundVector(0j, 1 + 1j),
             utils.BoundVector(0 + 0j, -1 - 1j)),

            (utils.BoundVector(0j, 10j),
             utils.BoundVector(-1j, 2j)),

            (utils.BoundVector(0j, 10j),
             utils.BoundVector(-3j, 5j)),

            (utils.BoundVector(0j, 10j),
             utils.BoundVector(2j, 4j)),

            (utils.BoundVector(0 + 0j, 1 + 0j),
             utils.BoundVector(.5 + 0j, 2 + 0j)),

            (utils.BoundVector(-1 + 0j, 2 + 0j),
             utils.BoundVector(.5 + 0j, 1 + 0j)),

            (utils.BoundVector(-10 + 0j, 1 + 0j),
             utils.BoundVector(-9.5 + 0j, 0j))
        ]

        nonintersecting_vectors = [
            (utils.BoundVector(0j, 1 + 1j),
             utils.BoundVector(10 + 0j, 0 + 10j)),

            (utils.BoundVector(0j, 1 + 1j),
             utils.BoundVector(-.5 + 0j, -1 - 1j)),

            (utils.BoundVector(-10 + 0j, 1 + 0j),
             utils.BoundVector(1 + 0j, 2 + 0j)),

            (utils.BoundVector(-10 + 0j, 0j),
             utils.BoundVector(1 + 0j, 2 + 0j)),

            (utils.BoundVector(-10 + 0j, 1 + 0j),
             utils.BoundVector(-11 + 0j, 0j))
        ]

        for v1, v2 in intersecting_vectors:
            self.assertTrue(utils.vectors_intersect(v1, v2))

        for v1, v2 in nonintersecting_vectors:
            self.assertFalse(utils.vectors_intersect(v1, v2))
