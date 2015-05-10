
from unittest import TestCase, main

from gates import *

class TestObservable(TestCase):

    def test_listeners(self):
        obs = Observable()
        callback0_data = { 'called': False }
        callback1_data = { 'called': False }
        def callback0():
            callback0_data['called'] = True
        def callback1():
            callback1_data['called'] = True
        obs.register_listener(callback0)
        obs.register_listener(callback1)
        obs._notify_listeners()
        self.assertTrue(callback0_data['called'])
        self.assertTrue(callback1_data['called'])

class TestAnd(TestCase):
    def test_truth_table(self):
        truth_table = {
            (0, 0) : 0,
            (0, 1) : 0,
            (1, 0) : 0,
            (1 ,1) : 1
        }
        self.assertTrue(verify_logic(And, truth_table))

    def test_and(self):
        switches = [ Switch() for x in range(2) ]
        gate = And(inputs=switches)
        map(lambda x: x.set_state(True), switches)
        self.assertTrue(gate.get_state())

    def test_cascade(self):
        switches = [ Switch() for x in range(4) ]
        gate0 = And(inputs=switches[0:2])
        gate1 = And(inputs=switches[2:4])
        gate2 = And(inputs=[gate0, gate1])
        self.assertFalse(gate2.get_state())
        map(lambda x: x.set_state(True), switches)
        self.assertTrue(gate2.get_state())

class TestNot(TestCase):
    def setUp(self):
        self.switch = Switch()

    def test_truth_table(self):
        truth_table = {
            (0,) : 1,
            (1,) : 0
        }
        self.assertTrue(verify_logic(Not, truth_table))

    def test_not_switch_start_false(self):
        self.switch.set_state(False)
        gate = Not(inputs=[self.switch])
        self.assertTrue(gate.get_state())

    def test_not(self):
        self.assertFalse(self.switch.get_state())
        gate = Not(inputs=[self.switch])
        self.switch.set_state(False)
        self.assertTrue(gate.get_state())
        self.switch.set_state(True)
        self.assertFalse(gate.get_state())

    def test_cascade_not(self):
        not0 = Not(inputs=[self.switch])
        not1 = Not(inputs=[not0])
        self.assertFalse(not1.get_state())
        self.switch.set_state(True)
        self.assertTrue(not1.get_state())


class TestSwitch(TestCase):
    def setUp(self):
        self.callback_data = { 'called': False }
        def callback():
            self.callback_data['called'] = True
        self.callback = callback

    def test_switch(self):
        switch = Switch()
        self.assertFalse(switch.get_state())
        switch.set_state(True)
        self.assertTrue(switch.get_state())

    def test_switch_listener(self):
        switch = Switch()
        switch.register_listener(self.callback)
        switch.set_state(True)
        self.assertTrue(self.callback_data['called'])
        switch.set_state(False)
        self.assertTrue(self.callback_data['called'])

    def test_switch_to_and(self):
        switch0 = Switch()
        switch1 = Switch()
        gate = And(inputs=[switch0, switch1])
        self.assertFalse(gate.get_state())
        switch0.set_state(True)
        self.assertFalse(gate.get_state())
        switch1.set_state(True)
        self.assertTrue(gate.get_state())
        switch1.set_state(False)
        self.assertFalse(gate.get_state())


class TestOr(TestCase):
    def test_truth_table(self):
        truth_table = {
            (0, 0) : 0,
            (0, 1) : 1,
            (1, 0) : 1,
            (1 ,1) : 1
        }
        self.assertTrue(verify_logic(Or, truth_table))

    def test_or(self):
        switches = [ Switch() for x in range(2) ]
        gate = Or(inputs=switches)
        self.assertFalse(gate.get_state())
        switches[0].set_state(True)
        self.assertTrue(gate.get_state())
        switches[0].set_state(False)
        self.assertFalse(gate.get_state())


class TestNand(TestCase):
    def test_truth_table(self):
        truth_table = {
            (0, 0) : 1,
            (0, 1) : 1,
            (1, 0) : 1,
            (1 ,1) : 0
        }
        self.assertTrue(verify_logic(Nand, truth_table))

    def test_add_input(self):
        switches = [ Switch() for x in range(3) ]
        map(lambda x: x.set_state(True), switches)
        gate = Nand(switches[0:2])
        self.assertFalse(gate.get_state())
        gate.add_input(switches[2])
        switches[2].set_state(False)
        self.assertTrue(gate.get_state())


class TestNor(TestCase):
    def test_truth_table(self):
        truth_table = {
            (0, 0) : 1,
            (0, 1) : 0,
            (1, 0) : 0,
            (1 ,1) : 0
        }
        self.assertTrue(verify_logic(Nor, truth_table))

    def test_add_input(self):
        switches = [ Switch() for x in range(3) ]
        map(lambda x: x.set_state(False), switches)
        gate = Nor(switches[0:2])
        self.assertTrue(gate.get_state())
        gate.add_input(switches[2])
        switches[2].set_state(True)
        self.assertFalse(gate.get_state())


class TestGate(TestCase):
    def test_add_input(self):
        gate = Not()
        self.assertEquals(0, len(gate.get_inputs()))
        switch = Switch()
        gate.add_input(switch)
        self.assertEquals(1, len(gate.get_inputs()))
        self.assertTrue(switch in gate.get_inputs())

    def test_add_input_registers_listener(self):
        # using not gate since it's simple but has callback
        switch = Switch()
        gate = Not([switch])
        gate.add_input(switch)
        switch.set_state(False)
        self.assertTrue(gate.get_state())
        switch.set_state(True)
        self.assertFalse(gate.get_state())


class TestVerifier(TestCase):
    def test_verifier(self):
        truth_table = {
            (0, 0) : 0,
            (0, 1) : 0,
            (1, 0) : 0,
            (1 ,1) : 1
        }
        self.assertTrue(verify_logic(And, truth_table))

class TestSRLatch(TestCase):
    def test_sr_latch(self):
        r = Switch()
        s = Switch()
        latch = SRLatch(inputs=[r,s])
        s.set_state(True)
        r.set_state(False)
        self.assertTrue(latch.get_output('Q'))
        self.assertFalse(latch.get_output('Q_not'))
        s.set_state(False)
        r.set_state(False)
        self.assertTrue(latch.get_output('Q'))
        self.assertFalse(latch.get_output('Q_not'))
        r.set_state(True)
        self.assertFalse(latch.get_output('Q'))
        self.assertTrue(latch.get_output('Q_not'))


if __name__ == '__main__':
    main()
