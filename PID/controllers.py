import time
from PID.datasets import ListValue, SerialValue


class BaseController:
    """
    The base algorithm for PID
    """

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
        """
        Set P I D params for the controller

        :param P: number
        :param I: number
        :param D: number

        :return: None
        """
        self.P = P
        self.I = I
        self.D = D

    def set_target(self, target):
        """
        set the target

        :param target: number

        :return: None
        """
        self.Target = target

    def set_threshold(self, threshold):
        """
        Set the value from sensor or dash

        :param threshold: numbet

        :return: None
        """
        self.threshold.value(threshold)

    # time step generator
    def serial_time(self):
        """
        This method will generate a timestamp as real clock time mapping,
        sometime it can be replaced by cycle time counter or increase function.

        :return: number
        """
        return time.time()

    # Keep this method, in order to manage integral
    def integral_windup_guard(self):
        """
        Add moving avgerage here to defence shake

        :return: None
        """

        self.integral /= len(self.threshold)

    def update(self, threshold):
        """
        This is the main function for PID controller

        attach main logic below:
        --------
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


        :param threshold: number
        :return: None
        """

        # update threshold and time
        self.set_threshold(threshold)
        self.time.value(self.serial_time())
        # update error
        self.error_value.value(self.Target - self.threshold.current)
        if self.time.delta < self.Interval:
            # time too short, need not output
            self.output = 0.0

        else:
            # Kp * error
            self.output = self.P * self.error_value.current
            # Ki * integral = Ki * ( integral + error * dt )
            self.integral += self.error_value.current * self.time.delta
            self.integral_windup_guard()  # shake defence
            self.output += self.I * self.integral
            # Kd * derivative = Kd * ( error - previous_error ) / dt
            derivative = self.error_value.delta / self.time.delta
            self.output += self.D * derivative

    def get_output(self):
        """
        Get the output from controller

        :return: number
        """
        return self.output


class Controller(BaseController):
    # integral values' range
    WindupGuard = 20.0

    # change threshold param to ListValue
    threshold = ListValue()

    def integral_windup_guard(self):
        """
        set integral a range for controller,
        integral will between WindupGuard and -WindupGuard

        :return: None
        """
        if self.integral < -self.WindupGuard:
            self.integral = -self.WindupGuard

        if self.integral > self.WindupGuard:
            self.integral = self.WindupGuard


class AutoController(Controller):
    """
    AutoController is working for auto control scenario
    """
    valve = None

    Switch = True

    def __init__(self, auto_valve, target):
        """
        Object initialization

        :param auto_valve: BaseAutoValve
        :param target: number
        """
        self.valve = auto_valve
        self.set_target(target)

    def start(self):
        """
        Start auto control

        :return: None
        """
        for threshold in self.valve.get_sensor():
            # read current threshold from iterator
            self.update(threshold)
            self.valve.operate(self.get_output())

            if self.Switch:
                time.sleep(self.Interval)
            else:
                break

    def stop(self):
        """
        Stop auto control

        :return: None
        """
        self.Switch = False
