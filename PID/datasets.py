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
