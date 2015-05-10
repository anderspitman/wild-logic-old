
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
            listener(self._state)


class Switch(Observable):
    pass


class Gate(Observable):
    def __init__(self, inputs=[]):
        super(Gate, self).__init__()
        self._inputs = inputs
        for input_ in inputs:
            input_.register_listener(self._callback)
            self._callback(input_.get_state())

    def _callback(self, state):
        pass


class Not(Gate):
    def _callback(self, state):
        self.set_state(not state)


class And(Gate):
    def _callback(self, state):
        temp_state = state
        for x in self._inputs:
            temp_state = temp_state and x.get_state()
        self.set_state(temp_state)


class Or(Gate):
    def _callback(self, state):
        for input_ in self._inputs:
            if input_.get_state():
                self.set_state(True)
                break

