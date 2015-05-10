
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


class Gate(Observable):
    def __init__(self, inputs=None):
        super(Gate, self).__init__()
        self._name = "Gate"

        self._inputs = inputs if inputs is not None else []
        for input_ in self._inputs:
            input_.register_listener(self._callback)
            self._callback()

    def add_input(self, new_input):
        self._inputs.append(new_input)
        new_input.register_listener(self._callback)
        self._callback()

    def get_inputs(self):
        return self._inputs

    def _callback(self):
        raise Exception("Abstract method _callback not implemented")


class Not(Gate):
    count = 0

    def __init__(self, inputs=[]):
        super(Not, self).__init__(inputs)

        self._id = Not.count
        Not.count += 1
        self._name = "Not {}".format(self._id)

    def _callback(self):
        self.set_state(not self._inputs[0].get_state())


class And(Gate):
    def _callback(self):
        temp_state = True
        for x in self._inputs:
            temp_state = temp_state and x.get_state()
        self.set_state(temp_state)


class Or(Gate):
    count = 0

    def __init__(self, inputs=[]):
        super(Or, self).__init__(inputs)

        self._id = Or.count
        Or.count += 1
        self._name = "Or {}".format(self._id)

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

    def add_input(self, new_input):
        self._and.add_input(new_input)
        super(Nand, self).add_input(new_input)

    def _callback(self):
        self.set_state(self._not.get_state())


class Nor(Gate):
    count = 0

    def __init__(self, inputs=[]):
        self._or = Or(inputs=inputs)
        self._not = Not(inputs=[self._or])
        super(Nor, self).__init__(inputs)
        self._id = Nor.count
        Nor.count += 1
        self._name = "Nor {}".format(self._id)

    def add_input(self, new_input):
        self._or.add_input(new_input)
        super(Nor, self).add_input(new_input)

    def _callback(self):
        new_state = self._not.get_state()
        self.set_state(self._not.get_state())


class SRLatch(Gate):
    count = 0

    def __init__(self, inputs=[]):
        super(SRLatch, self).__init__(inputs)
        self._id = SRLatch.count
        SRLatch.count +=1
        self._name = "SRLatch {}".format(self._id)

        self._nor0 = Nor(inputs=[inputs[0]])
        self._nor1 = Nor(inputs=[inputs[1]])

        print("nor0 init: {}".format(self._nor0.get_state()))
        print("nor1 init: {}".format(self._nor0.get_state()))

        self._nor0.add_input(self._nor1)
        self._nor1.add_input(self._nor0)

    def get_output(self, name):
        if name == 'Q':
            return self._nor0.get_state()
        elif name == 'Q_not':
            return self._nor1.get_state()
        else:
            raise Exception("invalid SR latch output name")

    def _callback(self):
        pass







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


