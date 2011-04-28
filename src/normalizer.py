# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

DELTA = .1
EPS = .1
REPS = 1 / EPS

class Normalizer(object):
    """
    Used to normalize a set of examples.
    """

    def __init__(self, min_data, max_data, min_range, max_range):
        """
        Builds a normalizer object.
        """
        self._md = min_data
        self._Md = max_data
        self._mr = min_range
        self._Mr = max_range

        if self._md > self._Md - DELTA:
            self._md = self._Md - DELTA # ensure a valid normalization range

        self._ETA = (self._Mr - self._mr) / (self._Md - self._md)
        self._RETA = 1 / self._ETA

    def normalize(self, x):
        """
        Normalizes a value.
        """
        return EPS * (self._ETA * (x - self._md) + self._mr)

    def recast(self, x):
        """
        Retransforms a normalized value to its original value.
        """
        return self._md + self._RETA * REPS * (x - EPS * self._mr)

