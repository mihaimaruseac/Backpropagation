# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

import math

import grapher
import normalizer
from units import *
from globaldefs import *

def log(x):
    """
    Normal logistic function. Output in [0, 1].
    """
    return 1 / ( 1 + math.exp(-x))

def dlog(x):
    """
    Derivative of the above function.
    """
    return log(x) * (1 - log(x))

def log2(x):
    """
    Logistic function with output in [-1, 1].
    """
    return 1 - 2 * log(x)

def dlog2(x):
    """
    Derivative of the above function.
    """
    return -2 * log(x) * (1 - log(x))

def th(x):
    """
    tanh function.
    """
    return math.tanh(x)

def dth(x):
    """
    Derivative of the above function.
    """
    t = th(x)
    return 1 - t * t

class Network(object):
    """
    Represents an entire neural network.

    The constructor constructs the network, the learn method trains the
    network and predicts the next value (this is still used for a prediction
    problem). All other methods are auxiliary.
    """

    def __init__(self, config, gui, graph):
        """
        Builds the network.

        config  User configuration.
        """
        self._gui = gui
        self._parse_network(config)
        self._parse_activation(config)
        self._prepare_data(config)
        self._runs = config['runs']
        self._baseName = config['baseName']
        self._grapher = grapher.Grapher(graph, gui)
        self._do_build_nw()
        self._it = 0

    def learn_step(self):
        """
        Bootstraps the learning phase.
        """

        self._grapher.graph()
        f = (self._it + 0.0) / self._runs
        self._it += 1
        self._gui.notify_progress(f)

        if self._it >= self._runs:
            return True #TODO: return useful data
        return None

    def _parse_activation(self, config):
        """
        Gets the activation function, its derivative and domain.
        """
        self._dom_max = 1
        self._dom_min = -1

        if config['activation'] == 'log':
            self._f = log
            self._df = dlog
            self._dom_min = 0 # the single function with domain in [0, 1]
        elif config['activation'] == '2log':
            self._f = log2
            self._df = dlog2
        else:
            self._f = th
            self._df = dth

    def _parse_network(self, config):
        """
        Parses the network configuration options.
        """
        # inputs
        self._N = config['N']

        # hidden layers
        self._h1 = config['h1']
        self._h2 = config['h2']

        # weights bounds
        self._mW = config['minW']
        self._MW = config['maxW']

        # recurrent network?
        self._recurrent = config['recurrent']

        # momentum?
        self._momentum = config['momentum']

    def _prepare_data(self, config):
        """
        Reads learning set, normalizing it and preparing the auxiliary lists
        to be used while learning.
        """
        data = config['data']

        # ranges
        data_max = max(data)
        data_min = min(data)
        self._normalizer = normalizer.Normalizer(
                data_min, data_max, self._dom_min, self._dom_max)

        ndata = map(lambda x: self._normalizer.normalize(x), data)

        self._data = map(
                lambda x: (ndata[x:x+self._N], ndata[x+self._N-1]),
                range(len(ndata) - self._N))
        self._question = ndata[-self._N:]

    def _do_build_nw(self):
        """
        Builds the neural network, layer by layer.
        """
        self.__build_inputs()
        self.__build_hidden1()
        self.__build_hidden2()
        self.__build_output()
        self._grapher.build_basic_network(
                self._N, self._inputs,
                self._h1, self._hidden1,
                self._h2, self._hidden2,
                self._output, self._end)

    def __build_inputs(self):
        """
        Builds the input layer.
        """
        self._inputs = []
        for i  in range(self._N):
            self._inputs.append(Pattern('i{0}'.format(i)))

        self._inputs.append(Fixed('fi'))

    def __build_hidden1(self):
        """
        Builds the first hidden layer.
        """
        self._hidden1 = []
        for i in range(self._h1):
            n = Neuron(self._mW, self._MW, 'h1{0}'.format(i))
            for inp in self._inputs:
                n.connect(inp)
            self._hidden1.append(n)
        if self._h1:
            self._hidden1.append(Fixed('fh1'))

    def __build_hidden2(self):
        """
        Builds the second hidden layer.
        """
        self._hidden2 = []
        for i in range(self._h2):
            n = Neuron(self._mW, self._MW, 'h2{0}'.format(i))
            if self._h1:
                for inp in self._hidden1:
                    n.connect(inp)
            else:
                for inp in self._inputs:
                    n.connect(inp)
            self._hidden2.append(n)
        if self._h2:
            self._hidden2.append(Fixed('fh2'))

    def __build_output(self):
        """
        Builds the output layer and the end of the network.
        """
        self._output = Neuron(self._mW, self._MW, 'o')
        if self._h2:
            for inp in self._hidden2:
                self._output.connect(inp)
        elif self._h1:
            for inp in self._hidden1:
                self._output.connect(inp)
        else:
            for inp in self._inputs:
                self._output.connect(inp)

        self._end = Output(self._output, 'e')

