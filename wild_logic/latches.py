from gates import Gate, Nor, Nand

class SRLatch(Gate):
    count = 0

    def __init__(self, r, s):
        super(SRLatch, self).__init__([r, s])
        self._id = SRLatch.count
        SRLatch.count +=1
        self._name = "SRLatch {}".format(self._id)

        self._nor0 = Nor(inputs=[r])
        self._nor1 = Nor(inputs=[s])

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


class GatedSRLatch(Gate):
    def __init__(self, s, r, enable):
        super(GatedSRLatch, self).__init__([s,r,enable])

        self._nand0 = Nand(inputs=[s, enable])
        self._nand1 = Nand(inputs=[enable, r])

        self._nand2 = Nand(inputs=[self._nand0])
        self._nand3 = Nand(inputs=[self._nand1])

        self._nand2.add_input(self._nand3)
        self._nand3.add_input(self._nand2)

    def get_output(self, name):
        if name == 'Q':
            return self._nand2.get_state()
        elif name == 'Q_not':
            return self._nand3.get_state()
        else:
            raise Exception("invalid SR latch output name")

    def _callback(self):
        pass



