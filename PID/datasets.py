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