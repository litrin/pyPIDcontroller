import unittest

from PID.datasets import SerialValue, ListValue


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)


class TestSerialValue(unittest.TestCase):
    def test_sv(self):
        sv = SerialValue()
        self.main_testcase(sv)

    def test_lv(self):
        lv = ListValue()
        self.main_testcase(lv)

    def main_testcase(self, v):
        v.value(1)
        v.value(2)

        self.assertEqual(v.current, 2)
        self.assertEqual(v.previous, 1)
        self.assertEqual(v.delta, 2 - 1)
        self.assertEqual(len(v), 2)


if __name__ == '__main__':
    unittest.main()
