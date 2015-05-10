
class Observable(object):
    count = 0

    def __init__(self):
        self._id = Observable.count
        Observable.count += 1
        self._name = "Observable {}".format(self._id)

        self._listeners = []
        self._state = True
        # also call method to trigger callbacks
        self.set_state(False)

    def get_state(self):
        return self._state

    def set_state(self, state):
        #print("setting state of {} to {}, {}".format(self._name, state, self))
        if state != self._state:
            #print("actually set")
            self._state = state
            self._notify_listeners()

    def register_listener(self, listener):
        self._listeners.append(listener)

    def _notify_listeners(self):
        for listener in self._listeners:
            listener()


class Switch(Observable):
    def __init__(self):
        super(Switch, self).__init__()

        self._name = "Switch"


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
