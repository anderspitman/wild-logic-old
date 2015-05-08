
class Link(object):
    def __init__(self):
        self._state = False
        self._callback = None

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state
        if self._callback:
            self._callback(self._state)

    def set_callback(self, callback):
        self._callback = callback


class Gate(object):
    def _callback(self, state):
        pass


class OneInputGate(Gate):
    def __init__(self, newIn=None, out=None):
        self._in = newIn if newIn is not None else Link()
        self._in.set_callback(self._callback)
        self._out = out if out is not None else Link()


    def get_in(self):
        return self._in

    def get_out(self):
        return self._out


class Buffer(OneInputGate):
    def _callback(self, state):
        self._out.set_state(self._in.get_state())


class Not(OneInputGate):
    def _callback(self, state):
        self.get_out().set_state(not self.get_in().get_state())


class TwoInputGate(Gate):
    def __init__(self, in1=None, in2=None, out=None):
        self._in1 = in1 if in1 is not None else Link()
        self._in2 = in2 if in2 is not None else Link()
        self._out = out if out is not None else Link()
        self._in1.set_callback(self._callback)
        self._in2.set_callback(self._callback)

    def get_out(self):
        return self._out

    def get_in1(self):
        return self._in1
        
    def set_in1(self, in1):
        self._in1 = in1

    def get_in2(self):
        return self._in2

    def set_in2(self, in2):
        self._in2 = in2


class Or(TwoInputGate):
    def _callback(self, state):
        self._out.set_state(self.get_in1().get_state() or 
                            self.get_in2().get_state())


class And(TwoInputGate):
    def _callback(self, state):
        self._out.set_state(self._in1.get_state() and self._in2.get_state())

