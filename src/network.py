# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

import math

def log(x):
    """
    Normal logistic function. Output in [0, 1].
    """
    return 1 / ( 1 + math.exp(-x))

def log2(x):
    """
    Logistic function with output in [-1, 1].
    """
    e = math.exp(-x)
    return (1 - e) / (1 + e)

def th(x):
    """
    tanh function.
    """
    return math.tanh(x)

class Network(object):
    """
    Represents an entire neural network.

    The constructor constructs the network, the learn method trains the
    network and predicts the next value (this is still used for a prediction
    problem). All other methods are auxiliary.
    """

    def __init__(self, config):
        """
        Builds the network.

        config  User configuration.
        """
        self.runs = config['runs']

        # inputs
        self.N = config['N']

        # activation function
        if config['activation'] == 'log':
            self.f = log
        elif config['activation'] == '2log':
            self.f = log2
        else:
            self.f = th

        # hidden layers
        self.h1 = config['h1']
        self.h2 = config['h2']

        # weights bounds
        self.mW = config['minW']
        self.MW = config['maxW']

        # recurrent network?
        self.recurrent = config['recurrent']

        # momentum?
        self.momentum = config['momentum']

        # learning set
        data = config['data']
        self.data = map(lambda x: (data[x:x+self.N], data[x+self.N-1]),
                range(len(data) - self.N))
        self.question = data[-self.N:]

    def learn(self):
        return None

