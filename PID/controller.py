import time
from PID.datasets import ListValue, SerialValue


class ControllerBase:
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


class Controller(ControllerBase):
    WindupGuard = 20.0
    threshold = ListValue()

    def integral_windup_guard(self):
        if self.integral < -self.WindupGuard:
            self.integral = -self.WindupGuard

        if self.integral > self.WindupGuard:
            self.integral = self.WindupGuard
