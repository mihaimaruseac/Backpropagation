# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

import gtk

from globaldefs import *

SIZE = 40
PAD = 80

class Grapher(object):
    """
    Will produce a nice graph of the neural network using Dot.
    """
    def __init__(self, img, w):
        self._img = img
        self._w = w
        self.__pixmap = None

    def graph(self):
        """
        Called when network graph needs to be updated.
        """
        self._do_cleanup_draw()
        gc = self._w.get_style().black_gc
        pcon = self._w.get_pango_context()
        for n in self._neurons:
            n.draw(self.__pixmap, gc, SIZE, pcon)
        self._img.set_from_pixmap(self.__pixmap, None)

    def build_basic_network(self, N, inputs, h1, hidden1, h2, hidden2,
            output, end):
        """
        Places the nodes from the neural network at specific positions, being
        ready to draw them afterwards.
        """
        m = max(N, h1, h2) + 1
        self._W = m * (SIZE + PAD) + PAD
        m = 5 if (h1 and h2) else 4 if (h1 or h2) else 3
        self._H = m * (SIZE + PAD) + PAD
        self._do_cleanup_draw()

        x = PAD
        self._place(inputs, x)
        x += PAD + SIZE
        self._place(hidden1, x)
        x += PAD + SIZE if h1 else 0
        self._place(hidden2, x)
        x += PAD + SIZE if h2 else 0
        self._place([output], x)
        x += PAD + SIZE
        self._place([end], x)

        self._neurons = inputs + hidden1 + hidden2 + [output, end]

    def _place(self, elems, x):
        """
        Generates the positions for each neuron.
        """
        a = len(elems) * (SIZE + PAD) + PAD
        y = (self._W - a) / 2 + PAD
        for n in elems:
            n.place(x, y)
            y += SIZE + PAD

    def _do_cleanup_draw(self):
        """
        Does the initial drawing of the network, cleaning the drawing area.
        """
        if not self.__pixmap:
            self.__pixmap = gtk.gdk.Pixmap(self._w.get_window(), self._H, self._W)
        gc = self._w.get_style().bg_gc[gtk.STATE_NORMAL]
        self.__pixmap.draw_rectangle(gc, True, 0, 0, self._H, self._W)

