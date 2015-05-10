
class Observable(object):
    def __init__(self):
        self._listeners = []
        self.set_state(False)

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state
        self._notify_listeners()

    def register_listener(self, listener):
        self._listeners.append(listener)

    def _notify_listeners(self):
        for listener in self._listeners:
            listener()


class Switch(Observable):
    pass


class Gate(Observable):
    def __init__(self, inputs=[]):
        super(Gate, self).__init__()
        self._inputs = inputs
        for input_ in inputs:
            input_.register_listener(self._callback)
            self._callback()

    def _callback(self):
        raise Exception("Abstract method _callback not implemented")


class Not(Gate):
    def _callback(self):
        self.set_state(not self._inputs[0].get_state())


class And(Gate):
    def _callback(self):
        temp_state = True
        for x in self._inputs:
            temp_state = temp_state and x.get_state()
        self.set_state(temp_state)


class Or(Gate):
    def _callback(self):
        temp_state = False
        for input_ in self._inputs:
            if input_.get_state():
                temp_state = True
                break
        self.set_state(temp_state)


class Nand(Gate):
    def __init__(self, inputs=[]):
        self._and = And(inputs=inputs)
        self._not = Not(inputs=[self._and])
        super(Nand, self).__init__(inputs)

    def _callback(self):
        self.set_state(self._not.get_state())


class Nor(Gate):
    def __init__(self, inputs=[]):
        self._or = Or(inputs=inputs)
        self._not = Not(inputs=[self._or])
        super(Nor, self).__init__(inputs)

    def _callback(self):
        self.set_state(self._not.get_state())

class TruthTableException(Exception):
    def __init__(self, message):
        super(TruthTableException, self).__init__(message)


def verify_logic(gate_class, truth_table):
    num_columns = len(truth_table.keys()[0])
    switches = [ Switch() for x in range(num_columns) ]
    gate = gate_class(inputs=switches)
    for row in truth_table.keys():
        for i, in_val in enumerate(row):
            switches[i].set_state(in_val)
        if gate.get_state() != truth_table[row]:
            raise TruthTableException(
                "Failed on {}. Expected {}, Got {}".format(row,
                                                           truth_table[row],
                                                           gate.get_state()))
            return False
    return True


