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

class BaseMovingValue:
    """
    This is the abstrace object for serial value object,
    please do not use it directly
    """
    current = None
    previous = None

    length = 0

    def __init__(self, current=None, last=None):
        """
        Object initialization, may input 2 values at the beginning.

        :param current:
        :param last:
        """
        raise NotImplementedError("Class BaseMovingValue is a abstract class!")

    def __len__(self):
        """
        The data set length

        :return: int
        """
        return self.length

    def value(self, value):
        """
        set current value to date set

        :param value: void

        :return: None
        """
        self.length += 1
        pass

    @property
    def delta(self):
        """
        provide the diffrential for last 2 values

        :return: void
        """
        return self.current - self.previous

    def __str__(self):
        """
        x.__str__() <==> str(x)
        :return: string
        """
        return "Previous: %s, Current: %s" % (self.previous, self.current)


class SerialValue(BaseMovingValue):
    """
    This object contained 2 values for history sets, current and previous
    """
    current = 0
    previous = 0

    length = 0

    def __init__(self, current=None, previous=None):
        if previous is not None:
            self.previous = previous

        if current is not None:
            self.current = current

    def value(self, value):
        BaseMovingValue.value(self, value)
        self.previous = self.current
        self.current = value

    def __len__(self):
        return self.length


class ListValue(list, BaseMovingValue):
    """
    This object may provide full history record for all values
    """

    def __init__(self, current=None, previous=None):
        if previous is not None:
            self.value(previous)

        if current is not None:
            self.value(current)

    def value(self, value):
        self.append(value)

    @property
    def current(self):
        return self[-1]

    @property
    def previous(self):
        return self[-2]


class BaseAutoValve:
    """
    This object has 2 method
    """

    def get_sensor(self):
        """
        Return a iterator which may provide the threshold continuously

        :return: iterator
        """
        pass

    def operate(self, value):
        """
        Response to the controller output value to valve

        :param value: number
        :return: None
        """
        pass


class FakeAutoValve(BaseAutoValve):
    pass
