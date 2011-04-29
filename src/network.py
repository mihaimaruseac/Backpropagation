# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

import math
from threading import Thread

import normalizer

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

class Network(Thread):
    """
    Represents an entire neural network.

    The constructor constructs the network, the learn method trains the
    network and predicts the next value (this is still used for a prediction
    problem). All other methods are auxiliary.
    """

    def __init__(self, config, gui):
        """
        Builds the network.

        config  User configuration.
        """
        Thread.__init__(self)
        self._gui = gui
        self._runs = config['runs']
        self._parse_network(config)
        self._parse_activation(config)
        self._prepare_data(config)
        self._stopped = False

    def learn(self):
        """
        Bootstraps the learning phase.
        """
        self._gui.notify_progress(0)
        self.start()

    def stop(self):
        """
        Stops learning.
        """
        self._stopped = True

    def run(self):
        """
        Learning phase.
        """
        for i in range(self._runs):
            if self._stopped:
                return
            self._gui.notify_progress((i + 0.0) / self._runs)
#            import time
#            time.sleep(1)
        self._gui.notify_progress(1, True)

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

