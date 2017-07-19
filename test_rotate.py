from unittest import TestCase
from main import rotate


class TestRotate(TestCase):
    def test(self):
        self.assertEqual(0, rotate([0, 0]))

    def up_test(self):
        self.assertEqual(90, rotate([0, 1]))

    def right_test(self):
        self.assertEqual(0, rotate([1, 0]))

    def down_test(self):
        self.assertEqual(-90, rotate([0, -1]))

    def left_test(self):
        self.assertEqual(180, rotate([-1, 0]))
