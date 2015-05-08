
from unittest import TestCase, main

from gates import *


class TestBuffer(TestCase):

    def test_cascade(self):
        buf1 = Buffer()
        buf2 = Buffer(buf1.get_out())
        buf3 = Buffer(buf2.get_out())
        self.assertFalse(buf3.get_out().get_state())
        buf1.get_in().set_state(True)
        self.assertTrue(buf3.get_out().get_state())


class TestNot(TestCase):

    def test_not(self):
        not0 = Not()
        not1 = Not(not0.get_out())
        not0.get_in().set_state(True)
        self.assertFalse(not0.get_out().get_state())
        self.assertTrue(not1.get_out().get_state())
        not0.get_in().set_state(False)
        self.assertTrue(not0.get_out().get_state())


class TestAnd(TestCase):
    def setUp(self):
        pass

    def test_and(self):
        and_gate = And()
        and_gate.get_in1().set_state(True)
        and_gate.get_in2().set_state(True)
        self.assertTrue(and_gate.get_out().get_state())
        and_gate.get_out().set_state(False)
        self.assertFalse(and_gate.get_out().get_state())

    def test_cascade(self):
        and0 = And()
        and1 = And()
        and2 = And(and0.get_out(), and1.get_out(), Link())
        self.assertFalse(and2.get_out().get_state())
        and0.get_in1().set_state(True)
        self.assertFalse(and2.get_out().get_state())
        and0.get_in2().set_state(True)
        self.assertFalse(and2.get_out().get_state())
        and1.get_in1().set_state(True)
        self.assertFalse(and2.get_out().get_state())
        and1.get_in2().set_state(True)
        # finally true
        self.assertTrue(and2.get_out().get_state())


class TestOr(TestCase):
    def test_or(self):
        gate = Or()
        self.assertFalse(gate.get_out().get_state())
        gate.get_in1().set_state(True)
        self.assertTrue(gate.get_out().get_state())
        gate.get_in1().set_state(False)
        self.assertFalse(gate.get_out().get_state())



class Tests(TestCase):

    def setUp(self):
        self.link = Link()


    def test_link(self):
        self.assertFalse(self.link.get_state())
        callback_data = {}
        def callback(state):
            callback_data['called'] = True
            callback_data['state'] = state
        self.link.set_callback(callback)
        self.link.set_state(True)
        self.assertTrue(self.link.get_state())
        self.assertTrue(callback_data['called'])
        self.assertTrue(callback_data['state'])
        self.link.set_state(False)
        self.assertFalse(callback_data['state'])


if __name__ == '__main__':
    main()
