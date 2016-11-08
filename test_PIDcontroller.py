import unittest, random, time
from PID.datasets import SerialValue, ListValue
from PID.controllers import Controller

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


class TestController(unittest.TestCase):
    def prepare_controller(self):
        p = Controller()
        p.set_PID(0.7, 0.1, 0.002)

        return p

    def test_controller(self):
        controller = self.prepare_controller()
        target = 0
        controller.set_target(target)

        feedback = 0.0

        for i in range(1, 0xff):
            time.sleep(0.001)
            controller.update(feedback)
            output = controller.get_output(True)

            serial = SerialValue()

            feedback += output

            if i & 0x8 is 0x8:
                target = random.random()
                controller.set_target(target)
            elif i & 0x8 > 0x2:
                serial.value(feedback)
                self.assertLessEqual(abs(serial.current - target),
                                     abs(serial.previous - target))


if __name__ == '__main__':
    unittest.main()
