# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

"""
Holds all kind of neurons and their description.
"""

import random

class Unit(object):
    """
    Simple unit from network. Holds a single value and doesn't learn anything
    at all.
    """
    def __init__(self, name='', value=None):
        self._name = name
        self._value = value

    def value(self):
        return self._value

class Fixed(Unit):
    """
    A unit holding a fixed value, keeping that value constant and not
    learning.
    """
    pass

class Pattern(Unit):
    """
    A unit for pattern feeding the neural network.
    """
    def set(self, value):
        self._value = value

class Output(Unit):
    """
    A unit for feeding the desired output to the neural network and starting
    the backpropagation phase.

    self.value() will return the actual output
    self.desired() / self.set_desired() work with desired values.
    """
    def __init__(self, n, name='', value=None):
        super(Unit, self).__init__(name, value)
        self._n = n
        self._desired = None

    def desired(self):
        return self._desired

    def set_desired(self, desired):
        self._desired = desired

class Neuron(Unit):
    """
    Actual neuron.

    self.value() will return the output of the neuron
    """
    def __init__(self, minW, maxW, name=''):
        super(Unit, self).__init__(name, None)
        self._min = minW
        self._max = maxW
        self._weights = []
        self._inputs = []

    def connect(self, i):
        """
        Connects a unit to the input of this neuron.
        """
        self._inputs.append(i)
        self._weights.append(random.uniform(self._min, self._max))

