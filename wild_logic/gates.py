from core import Observable, Switch

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
