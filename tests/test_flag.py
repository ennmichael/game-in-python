import unittest
import enum

from game import utils


@enum.unique
class FlagExample(utils.Flag):

    A = enum.auto()
    B = enum.auto()
    C = enum.auto()


class FlagTest(unittest.TestCase):

    def test_everything(self) -> None:
        e = FlagExample.A

        self.assertTrue(e.has_flag(FlagExample.A))
        self.assertFalse(e.has_flag(FlagExample.B))
        self.assertFalse(e.has_flag(FlagExample.C))

        e.unset_flag(FlagExample.A)

        self.assertFalse(e.has_flag(FlagExample.A))
        self.assertFalse(e.has_flag(FlagExample.B))
        self.assertFalse(e.has_flag(FlagExample.C))

        e.set_flag(FlagExample.B)
        e.set_flag(FlagExample.C)

        self.assertFalse(e.has_flag(FlagExample.A))
        self.assertTrue(e.has_flag(FlagExample.B))
        self.assertTrue(e.has_flag(FlagExample.C))


if __name__ == '__main__':
    unittest.main()
