
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


class TestNor(TestCase):
    def test_truth_table(self):
        truth_table = {
            (0, 0) : 1,
            (0, 1) : 0,
            (1, 0) : 0,
            (1 ,1) : 0
        }
        self.assertTrue(verify_logic(Nor, truth_table))


class TestVerifier(TestCase):
    def test_verifier(self):
        truth_table = {
            (0, 0) : 0,
            (0, 1) : 0,
            (1, 0) : 0,
            (1 ,1) : 1
        }
        self.assertTrue(verify_logic(And, truth_table))


if __name__ == '__main__':
    main()
