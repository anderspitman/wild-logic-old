
class And(object):
    def __init__(self):
        self._in1 = False
        self._in2 = False

    def evaluate(self):
        return self._in1 and self._in2

    def set_in1(self, in1):
        self._in1 = in1

    def set_in2(self, in2):
        self._in2 = in2
