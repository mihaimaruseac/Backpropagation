# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

from globaldefs import *

import gtk
import os

class Save(object):
    """
    This will save all data gathered while learning and predicting.
    """
    def __init__(self, network, results):
        self._nw = network
        self._baseName = self._nw.baseName()
        self._rs = results

    def save_all(self):
        """
        Saves all data.
        """
        self._save_nw_to_img()
        self._save_nw_to_matrix()
        self._save_rms()
        self._save_values()

    def _save_nw_to_img(self):
        """
        Saves the network to a png file.
        """
        fName = self._baseName + NETWORK_SUFFIX
        drawable = self._nw.drawable()
        cmap = drawable.get_colormap()
        pbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8,
                *drawable.get_size())
        pbuf = pbuf.get_from_drawable(drawable, cmap, 0, 0, 0, 0,
                *drawable.get_size())
        pbuf.save(fName, 'png')

    def _save_nw_to_matrix(self):
        """
        Saves the weights from the network to a file.
        """
        ns = self._nw.neurons()
        lname = max(map(lambda n:len(n.name()), ns)) + 4
        l = max(lname, 7)
        t = (1 + len(ns)) * (l + 1) + 1
        sep = '{0:-^{1}}'.format('',t)
        fName =self._baseName + NETWORK_MATRIX_SUFFIX

        with open(fName, 'w') as f:
            f.write(sep + '\n')
            s = "|{0:^{1}}|".format('', lname)
            for n in ns:
                s += "{0:^{1}}|".format(n.name(), l)
            f.write(''.join(s) + '\n')
            f.write(sep + '\n')

            for n in ns:
                nd = {}
                for (nn, w) in zip(n.inputs(), n.weights()):
                    nd[nn.name()] = w + 0.0
                s = "|{0:^{1}}|".format(n.name(), lname)
                for nn in ns:
                    if nn in n.inputs():
                        s += "{0:^+{1}.2}|".format(nd[nn.name()], l)
                    else:
                        s += "{0:^{1}}|".format('', l)
                f.write(s + '\n')
                f.write(sep + '\n')

    def _save_rms(self):
        """
        Saves a list of errors per epoch and does a plot of them. The plot is
        done via gnuplot, which must be installed.
        """
        rms = self._nw._rms
        l = len(rms)
        fName = self._baseName + RMS_FILE_SUFFIX

        with open(fName, 'w') as f:
            for (i, r) in zip(range(l), rms):
                f.write('{0}\t{1:.5}\n'.format(i + 1, r))

        pngName = self._baseName + RMS_PLOT_SUFFIX
        cmd = \
            'echo \'set term png; plot "{0}" using 1:2 title "Error" ' \
            'with lines\' | gnuplot > {1}'.format(fName, pngName)
        os.system(cmd)

    def _save_values(self):
        """
        Saves the original values and the obtained values and does a plot of
        them. Plot done via gnuplot, see above method.
        """
        N = self._nw._N
        odata = self._nw.orig_data()
        n = len(odata)
        fName = self._baseName + VAL_SUFFIX

        with open(fName, 'w') as f:
            for (i, d) in zip(range(N), odata):
                f.write('{0}\t{1:.5}\t-\n'.format(i + 1, d))

            for (i, d, r) in zip(range(N, n+1), odata[N:], self._rs):
                f.write('{0}\t{1:.5}\t{2:.5}\n'.format(i + 1, d, r))

            f.write('{0}\t-\t{1:.5}\n'.format(n + 2, self._rs[-1]))

        pngName = self._baseName + VAL_PLOT_SUFFIX
        cmd = \
            'echo \'set term png; plot "{0}" using 1:2 title "Inputs", ' \
            '"{0}" using 1:3 title "Outputs" with lines \' | gnuplot ' \
            '> {1}'.format(fName, pngName)
        os.system(cmd)

