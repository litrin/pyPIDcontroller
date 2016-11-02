import time


class BaseMovingValue:
    current = None
    last = None

    def __init__(self, current=None, last=None):
        raise NotImplementedError("Class BaseMovingValue is a abstract class!")

    def __len__(self):
        return 0

    def value(self, value):
        pass

    @property
    def delta(self):
        return self.current - self.last


class SerialValue(BaseMovingValue):
    current = 0
    last = 0

    length = 0

    def __init__(self, current=None, last=None):
        if last is not None:
            self.last = last

        if current is not None:
            self.current = current

    def value(self, value):
        self.length += 1
        self.last = self.current
        self.current = value

    def __len__(self):
        return self.length


class ListValue(list, BaseMovingValue):
    def __init__(self, current=None, last=None):
        if last is not None:
            self.value(last)

        if current is not None:
            self.value(current)

    def value(self, value):
        self.append(value)

    @property
    def current(self):
        return self[-1]

    @property
    def last(self):
        return self[-2]


class PIDControllerBase:
    Interval = 0.0

    P = 0.2
    I = 0.0
    D = 0.0

    time = SerialValue()
    diff = SerialValue()
    threshold = SerialValue()
    error_value = SerialValue()

    integral = 0.0
    length = 0

    def set_PID(self, P=0.2, I=0.0, D=0.0):
        self.P = P
        self.I = I
        self.D = D

    def set_target(self, target):
        self.Target = target

    def set_threshold(self, threshold):
        self.threshold.value(threshold)

    # time step generator
    def serial_time(self):
        return time.time()

    # Keep this method, set a range for controller
    def integral_windup_guard(self):
        pass

    def update(self, threshold):

        """
        previous_error = 0
        integral = 0
        start:
          error = setpoint - measured_value
          integral = integral + error*dt
          derivative = (error - previous_error)/dt
          output = Kp*error + Ki*integral + Kd*derivative
          previous_error = error
          wait(dt)
          goto start
        """
        self.set_threshold(threshold)
        self.time.value(self.serial_time())

        self.error_value.value(self.Target - self.threshold.current)
        if (self.time.delta < self.Interval or
                    self.error_value.current is 0.0):
            self.output = 0.0

        else:
            self.output = self.P * self.threshold.delta

            self.integral += self.time.delta * self.error_value.delta
            self.integral_windup_guard()
            self.output += self.I * self.integral / len(self.threshold)

            derivative = self.error_value.delta / self.time.delta
            self.output += self.D * derivative

    def get_output(self, threshold):
        self.update(threshold)

        return self.output


class PIDController(PIDControllerBase):
    WindupGuard = 20.0
    threshold = ListValue()

    def integral_windup_guard(self):
        if self.integral < -self.WindupGuard:
            self.integral = -self.WindupGuard

        if self.integral > self.WindupGuard:
            self.integral = self.WindupGuard
