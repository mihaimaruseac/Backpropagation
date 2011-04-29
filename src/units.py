# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

"""
Holds all kind of neurons and their description.
"""

from globaldefs import *

import logging
import pango
import random

_logger = logging.getLogger(LOGNAME)

class Unit(object):
    """
    Simple unit from network. Holds a single value and doesn't learn anything
    at all.
    """
    def __init__(self, name='', value=None):
        self._name = name
        self._value = value
        self._x = 0
        self._y = 0
        self._err = 0

    def value(self):
        return self._value

    def place(self, x, y):
        self._x = x
        self._y = y

    def draw(self, pbuff, gc, size, pcon):
        self._draw_image(pbuff, gc, size)
        self._draw_label(pbuff, gc, size, pcon)

    def compute_output(self):
        pass

    def report_and_learn_from_error(self):
        pass

    def report_error(self, err):
        pass

    def _draw_image(self, pbuff, gc, size):
        pbuff.draw_arc(gc, False, self._x, self._y, size, size, 0, 64 * 360)

    def _draw_label(self, pbuff, gc, size, pcon):
        l = pango.Layout(pcon)
        self._draw_label_text(l)
        pbuff.draw_layout(gc, self._x + size / 4, self._y + size / 4, l)

    def _draw_label_text(self, l):
        l.set_text(self._name)

    def exit_point(self, size):
        return (self._x + size, self._y + size / 2)

    def entry_point(self, size):
        return (self._x, self._y + size / 2)

class Fixed(Unit):
    """
    A unit holding a fixed value, keeping that value constant and not
    learning.
    """
    def __init__(self, name='', value=1):
        super(Fixed, self).__init__(name, value)
        self._inputs = []
        self._weights = []

    def _draw_label_text(self, l):
        l.set_text("1")

    def _draw_image(self, pbuff, gc, size):
        pbuff.draw_rectangle(gc, False, self._x, self._y, size, size)

class Pattern(Unit):
    """
    A unit for pattern feeding the neural network.
    """
    def set(self, value):
        self._value = value

    def _draw_label_text(self, l):
        l.set_text(">")

    def _draw_image(self, pbuff, gc, size):
        ps = [(self._x, self._y),
                (self._x + size, self._y + size / 2),
                (self._x, self._y + size)]
        pbuff.draw_polygon(gc, False, ps)

class Output(Unit):
    """
    A unit for feeding the desired output to the neural network and starting
    the backpropagation phase.

    self.value() will return the actual output
    self.desired() / self.set_desired() work with desired values.
    """
    def __init__(self, n, name=''):
        super(Output, self).__init__(name, None)
        self._n = n
        self._desired = None

    def desired(self):
        return self._desired

    def set_desired(self, desired):
        self._desired = desired

    def value(self):
        return self._n.value()

    def get_error(self):
        """
        Returns the error in this output. Starts the backpropagation phase.
        """
        self._err = self._n.value() - self._desired
        return self._err

    def report_and_learn_from_error(self):
        """
        Reports the error to the output neuron and finishes execution (there's
        nothing to learn here).
        """
        self._n.report_error(self._err)

    def _draw_label_text(self, l):
        l.set_text("=")

    def _draw_image(self, pbuff, gc, size):
        ps = [(self._x + size - 10, self._y),
                (self._x - 10, self._y + size / 2),
                (self._x + size - 10, self._y + size)]
        pbuff.draw_polygon(gc, False, ps)

    def entry_point(self, size):
        return (self._x - 10, self._y + size / 2)

class Neuron(Unit):
    """
    Actual neuron.

    self.value() will return the output of the neuron
    """
    def __init__(self, minW, maxW, f, df, name=''):
        super(Neuron, self).__init__(name, None)
        self._min = minW
        self._max = maxW
        self._weights = []
        self._inputs = []
        self._f = f
        self._df = df

    def connect(self, i):
        """
        Connects a unit to the input of this neuron.
        """
        self._inputs.append(i)
        self._weights.append(random.uniform(self._min, self._max))

    def compute_output(self):
        """
        Computes the output of this neuron, depending on its inputs and its
        weights.
        """
        s = 0
        for (w, i) in zip(self._weights, self._inputs):
            s += w * i.value()
        self._value = self._f(s)
        _logger.info('Neuron {0}: activation: {1}'.format(self._name, self._value))

    def report_error(self, err):
        """
        Receives an error from the next layer. Acummulate all values before
        trying to learn something and report the error to the previous layer.
        """
        self._err += err
        _logger.info('Neuron {0}: Received error: {1}'.format(self._name, err))

    def report_and_learn_from_error(self):
        """
        Reports the total error to the previous layer, learns from the error
        and resets it.
        """
        _logger.info('Neuron {0}: Total error: {1}'.format(self._name, self._err))

        for (w, i) in zip(self._weights, self._inputs):
            i.report_error(w * self._err)

        self._err = 0

    def _draw_label_text(self, l):
        l.set_text("")

