##
#                     GNU GENERAL PUBLIC LICENSE
#                        Version 3, 29 June 2007
#
#  Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
#  Everyone is permitted to copy and distribute verbatim copies
#  of this license document, but changing it is not allowed.
#
#                             Preamble
#
#   The GNU General Public License is a free, copyleft license for
# software and other kinds of works.
#
#   The licenses for most software and other practical works are designed
# to take away your freedom to share and change the works.  By contrast,
# the GNU General Public License is intended to guarantee your freedom to
# share and change all versions of a program--to make sure it remains free
# software for all its users.  We, the Free Software Foundation, use the
# GNU General Public License for most of our software; it applies also to
# any other work released this way by its authors.  You can apply it to
# your programs, too.
#
#   When we speak of free software, we are referring to freedom, not
# price.  Our General Public Licenses are designed to make sure that you
# have the freedom to distribute copies of free software (and charge for
# them if you wish), that you receive source code or can get it if you
# want it, that you can change the software or use pieces of it in new
# free programs, and that you know you can do these things.
#
#   To protect your rights, we need to prevent others from denying you
# these rights or asking you to surrender the rights.  Therefore, you have
# certain responsibilities if you distribute copies of the software, or if
# you modify it: responsibilities to respect the freedom of others.
#
#   For example, if you distribute copies of such a program, whether
# gratis or for a fee, you must pass on to the recipients the same
# freedoms that you received.  You must make sure that they, too, receive
# or can get the source code.  And you must show them these terms so they
# know their rights.
#
#   Developers that use the GNU GPL protect your rights with two steps:
# (1) assert copyright on the software, and (2) offer you this License
# giving you legal permission to copy, distribute and/or modify it.
#
#   For the developers' and authors' protection, the GPL clearly explains
# that there is no warranty for this free software.  For both users' and
# authors' sake, the GPL requires that modified versions be marked as
# changed, so that their problems will not be attributed erroneously to
# authors of previous versions.
#
#   Some devices are designed to deny users access to install or run
# modified versions of the software inside them, although the manufacturer
# can do so.  This is fundamentally incompatible with the aim of
# protecting users' freedom to change the software.  The systematic
# pattern of such abuse occurs in the area of products for individuals to
# use, which is precisely where it is most unacceptable.  Therefore, we
# have designed this version of the GPL to prohibit the practice for those
# products.  If such problems arise substantially in other domains, we
# stand ready to extend this provision to those domains in future versions
# of the GPL, as needed to protect the freedom of users.
#
#   Finally, every program is threatened constantly by software patents.
# States should not allow patents to restrict development and use of
# software on general-purpose computers, but in those that do, we wish to
# avoid the special danger that patents applied to a free program could
# make it effectively proprietary.  To prevent this, the GPL assures that
# patents cannot be used to render the program non-free.
#


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
