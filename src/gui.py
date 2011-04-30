# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

import gtk
import glib
import logging

import config
import network

from globaldefs import *

class MainWindow(gtk.Window):
    """
    Holds the definition for the main window from the GUI and all data
    associated with it.
    """

    def __init__(self):
        """
        Builds the window. Connects all the signals and displays all the
        widgets.
        """
        super(MainWindow, self).__init__()
        self.set_size_request(XXX, YYY)
        self.set_title(TITLE)
        self.set_icon_from_file(ICON_FILE)
        self.connect('delete_event', self.__on_exit)

        self._nw = None
        self._inhibit = False

        self._build_gui()

        self.show()
        self.show_all()

    def _build_gui(self):
        """
        Builds the interface of this window, the entire tree of widgets.
        """
        _vbox = gtk.VBox()
        self.add(_vbox)

        _toolbar = self._build_toolbar()
        _vbox.pack_start(_toolbar, False, False, 5)

        _sw = gtk.ScrolledWindow()
        self._graph = gtk.Image()
        self._graph.set_from_file(ICON_FILE)
        _sw.add_with_viewport(self._graph)
        _vbox.pack_start(_sw, True, True, 5)

    def _build_toolbar(self):
        """
        Builds the toolbar and the associated buttons used to control the
        application.

        return  the Toolbar
        """
        _toolbar = gtk.Toolbar()
        _toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        _toolbar.set_style(gtk.TOOLBAR_BOTH)
        _toolbar.set_border_width(5)

        _btnNew = self._build_toolbar_button(gtk.STOCK_NEW, "New",
                "Starts a new prediction", self.__on_new)
        _toolbar.insert(_btnNew, -1)

        _btnAbout = self._build_toolbar_button(gtk.STOCK_ABOUT, "About",
                "About this program", self.__on_about)
        _toolbar.insert(_btnAbout, -1)

        _toolbar.insert(gtk.SeparatorToolItem(), -1)
        self._pBar = gtk.ProgressBar()
        self._pBar.set_text('Learning progress')
        ti = gtk.ToolItem()
        b = gtk.HBox()
        b.pack_start(self._pBar, False, False, 5)
        ti.add(b)
        _toolbar.insert(ti, -1)

        return _toolbar

    def _build_toolbar_button(self, img_stock, label, tooltip, callback):
        """
        Adds a new button to a toolbar.

        img_stock   stock image to use
        label       label of button
        tooltip     tooltip for the button
        callback    callback when button is clicked

        return      the button
        """
        img = gtk.Image()
        img.set_from_stock(img_stock, gtk.ICON_SIZE_LARGE_TOOLBAR)
        btn = gtk.ToolButton(img, label)
        btn.set_tooltip_text(tooltip)
        btn.connect('clicked', callback)
        return btn

    def notify_progress(self, p):
        """
        Called from the neural network to notify the progress of the learning.
        """
        self._pBar.set_fraction(p)

    def __step(self):
        if self._inhibit:
            self._inhibit = False
            return False

        r = self._nw.learn_step()
        if r:
            self._md = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
                'Network predicts {0} ± {1:.2}%'.format(
                    r['predicted'], 100*r['err']))
            self._md.connect('response', self.__close_modal)
            self._md.show_all()
            self._md.show()
            self._nw = None
            return False
        return True

    def __close_modal(self, widget, data=None):
        """
        Closes the prediction result dialog.
        """
        self._md.destroy()
        self._pBar.set_fraction(0)
        self._graph.set_from_file(ICON_FILE)

    def __on_exit(self, widget, data=None):
        """
        Called when destroying the main window. Leave the gtk threads (and
        finish application).
        """
        gtk.main_quit()

    def __on_new(self, widget, data=None):
        """
        Called when the user issues a request for a new game.
        """
        if self._nw:
            self._inhibit = True

        cfg = config.Config(self, TITLE)
        cfg.display()
        r = cfg.get_settings()
        cfg.destroy()

        if r:
            self._nw = network.Network(r, self, self._graph)
            glib.timeout_add(100, self.__step)
        else:
            self._nw = None
            self._graph.set_from_file(ICON_FILE)

    def __on_about(self, widget, data=None):
        """
        Called when the user issues a request for the About dialog.
        """
        aboutDialog = gtk.AboutDialog()
        aboutDialog.set_name(TITLE)
        aboutDialog.set_authors(["Mihai Maruseac <mihai.maruseac@rosedu.org>"])
        aboutDialog.set_documenters(
                ["Mihai Maruseac <mihai.maruseac@rosedu.org>"])
        aboutDialog.set_artists(
                ["Art taken from Public Domain pictures on the web"])
        aboutDialog.set_comments(
            "Use backpropagation to forecast."
            "\nSee README and LICENSE for more information.")
        aboutDialog.set_copyright(
            "Copyright © 2011 - 2012 Mihai Maruseac <mihai.maruseac@rosedu.org>")
        aboutDialog.set_logo(self.get_icon())
        aboutDialog.set_icon(self.get_icon())
        aboutDialog.set_version("0.1")
        aboutDialog.run()
        aboutDialog.destroy()

def main():
    """
    Main function. Construct the windows and start all application threads.
    """
    l = logging.getLogger(LOGNAME)
    l.setLevel(logging.INFO)
    w = MainWindow()
    gtk.gdk.threads_init()
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
    logging.shutdown()

if __name__ == '__main__':
    main()

