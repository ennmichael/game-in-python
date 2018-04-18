import unittest
import enum

from game import utils


@enum.unique
class FlagExample(utils.Flag):

    A = 0x01
    B = 0x02
    C = 0x04


class FlagTest(unittest.TestCase):

    def test_everything(self) -> None:
        e = FlagExample.A

        self.assertTrue(e.has_flag(FlagExample.A))
        self.assertFalse(e.has_flag(FlagExample.B))
        self.assertFalse(e.has_flag(FlagExample.C))

        e = e.unset_flag(FlagExample.A)

        self.assertFalse(e.has_flag(FlagExample.A))
        self.assertFalse(e.has_flag(FlagExample.B))
        self.assertFalse(e.has_flag(FlagExample.C))

        e = e.set_flag(FlagExample.B)
        e = e.set_flag(FlagExample.C)

        self.assertFalse(e.has_flag(FlagExample.A))
        self.assertTrue(e.has_flag(FlagExample.B))
        self.assertTrue(e.has_flag(FlagExample.C))


if __name__ == '__main__':
    unittest.main()
