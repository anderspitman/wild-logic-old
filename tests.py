
from unittest import TestCase, main

from gates import And

class Tests(TestCase):

    def setUp(self):
        self.and_gate = And()

    def test_and(self):
        self.and_gate.set_in1(True)
        self.and_gate.set_in2(True)
        self.assertTrue(self.and_gate.evaluate());
        self.and_gate.set_in2(False)
        self.assertFalse(self.and_gate.evaluate());

if __name__ == '__main__':
    main()
