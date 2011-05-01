# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

import logging
import math

import grapher
import normalizer
import saver
from units import *

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
        self._logger = logging.getLogger(LOGNAME)
        self._logger.addHandler(logging.FileHandler(self._baseName + LOG_SUFFIX))
        self._rms = []
        self._orms = 0
        self._grapher.graph()

    def baseName(self):
        return self._baseName

    def drawable(self):
        return self._grapher.drawable()

    def neurons(self):
        return self._inputs + self._hidden1 + self._hidden2 + [self._output, self._end]

    def orig_data(self):
        return self._orig_data

    def learn_step(self):
        """
        Bootstraps the learning phase.
        """
        rms = self._do_one_learning_step()
        done = rms < self._MIN_RMS or abs(rms - self._orms) < self._MIN_DRMS
        self._orms = rms

        self._grapher.graph()
        f = (self._it + 0.0) / self._runs if not done else 1
        self._it += 1
        self._gui.notify_progress(f)

        if self._it >= self._runs or done:
            results, predicted = self._predict()
            s = saver.Save(self, results + [predicted])
            s.save_all()
            r = {'predicted':predicted, 'err': self._rms[-1]}
            return r
        return None

    def _predict(self):
        """
        After learning phase is ended, predict the next value and return the
        results for each pattern.
        """
        results = []
        for (inp, out) in self._data:
            self._end.set_desired(out)
            self._present_pattern(inp)
            results.append(self._normalizer.recast(self._end.value()))
        self._present_pattern(self._question)
        return (results, self._normalizer.recast(self._end.value()))

    def _present_pattern(self, pattern):
        """
        Presents a pattern to the neural network.
        """
        for (ineuron, ivalue) in zip(self._inputs, pattern):
            ineuron.set(ivalue)
        for n in self._hidden1:
            n.compute_output()
        for n in self._hidden2:
            n.compute_output()
        self._output.compute_output()

    def _backpropagate(self):
        """
        Does the backpropagation.
        """
        self._end.report_and_learn_from_error()
        self._output.report_and_learn_from_error()
        for n in self._hidden2:
            n.report_and_learn_from_error()
        for n in self._hidden1:
            n.report_and_learn_from_error()

    def _do_one_learning_step(self):
        """
        Does one learning step, controlling each neuron in the network and
        updating the weights and the logs.
        """
        rms = 0
        self._logger.info('Step {0} starting'.format(self._it))
        for (inp, out) in self._data:
            self._logger.info('input: {0}, expected: {1}'.format(inp, out))
            self._end.set_desired(out)
            self._present_pattern(inp)
            e = self._end.get_error()
            rms += e * e
            self._backpropagate()
        rms /= len(self._data)
        rms = math.sqrt(rms)

        self._logger.info('===================')
        self._logger.info('RMS: {0}'.format(rms))
        self._logger.info('===================')
        self._logger.info('')
        self._rms.append(rms)
        return rms

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

        # params
        self._eta = config['eta']
        self._alpha = config['alpha']

        # rms params
        self._MIN_RMS = config['min_rms']
        self._MIN_DRMS = config['min_delta_rms']

    def _prepare_data(self, config):
        """
        Reads learning set, normalizing it and preparing the auxiliary lists
        to be used while learning.
        """
        self._orig_data = data = config['data']

        # ranges
        data_max = max(data)
        data_min = min(data)
        self._normalizer = normalizer.Normalizer(
                data_min, data_max, self._dom_min, self._dom_max)

        ndata = map(lambda x: self._normalizer.normalize(x), data)

        self._data = map(
                lambda x: (ndata[x:x+self._N], ndata[x+self._N]),
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
            n = Neuron(self._mW, self._MW, self._f, self._df, self._momentum,
                    'h1{0}'.format(i), self._eta, self._alpha)
            n.set_recurrent(self._recurrent)
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
            n = Neuron(self._mW, self._MW, self._f, self._df, self._momentum,
                    'h2{0}'.format(i), self._eta, self._alpha)
            n.set_recurrent(self._recurrent)
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
        self._output = Neuron(self._mW, self._MW, self._f, self._df,
                self._momentum, 'o', self._eta, self._alpha)
        self._output.set_recurrent(self._recurrent)
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

