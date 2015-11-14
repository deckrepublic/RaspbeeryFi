import unittest
from raspberrypifi import *


class UtilityTest(unittest.TestCase):
    def test_find_true_offset(self):
        string = 'line 1 stuff \nline 2 stuff'
        self.assertEqual(find_true_offset(string, 1, 3), 3)

    def test_find_true_offset2(self):
        string = 'line 1 stuff \nline 2 stuff'
        self.assertEqual(find_true_offset(string, 2, 3), 17)

    def test_find_true_offset3(self):
        string = 'line 1 stuff \nline 2 stuff'
        self.assertEqual(find_true_offset(string, 1, 0), 0)

    def test_find_true_offset4(self):
        string = 'line 1 stuff \nline 2 stuff'
        # aren't enough lines in the string
        with self.assertRaises(ValueError):
            find_true_offset(string, 3, 1)


if __name__ == '__main__':
    unittest.main()
