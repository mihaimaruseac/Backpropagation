# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

import gtk

class Config(object):
    """
    Configuration dialog.
    """

    def __init__(self, parent, title=''):
        """
        Constructs the config dialog, always with the same initial values.

        parent  Parent window for the dialog
        title   Title for the dialog
        """
        btn = (gtk.STOCK_OK, gtk.RESPONSE_NONE,
                gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT)
        self._d = gtk.Dialog(title, parent,
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, btn)
        self._d.set_deletable(False)
        self._d.set_size_request(420, 220)
        self._d.set_resizable(False)
        self._build_gui()
        self._d.show_all()

        # holds the settings (uses to be a dictionary if everything is ok)
        self._configDict = None

    def _build_gui(self):
        """
        Builds the entire GUI for this dialog.
        """
        _topVBox = gtk.VBox()
        self._build_IO_gui(_topVBox)
#        _checkHBox = gtk.HBox()
#        self._build_action_gui(_checkHBox)
#        self._build_learning_gui(_checkHBox)
#        _topVBox.pack_start(_checkHBox, False, False, 5)
        self._d.vbox.add(_topVBox)

    def _build_IO_gui(self, _topVBox):
        """
        Builds the GUI for the UI actions: what file to read and how many
        steps to take on each learning iteration.

        _topVBox    VBox holding the widgets built by this function
        """
        _fileHBox = gtk.HBox()
        _topVBox.pack_start(_fileHBox, False, False, 5)
        _fileLabel = gtk.Label('Input filename:')
        _fileHBox.pack_start(_fileLabel, False, False, 5)
        self._fileChoose = gtk.FileChooserButton("Select input filename")
        _fileHBox.pack_start(self._fileChoose, True, True, 5)

    def display(self):
        """
        Displays this dialog, letting the user to chose the options. After the
        dialog is closed, check the user inputs and construct the settings
        dictionary.
        """
        if self._d.run() == gtk.RESPONSE_REJECT:
            self._configDict = None # nothing to return
            return None
        self._configDict = {}

        # Try to read the file provided
        if not self._read(self._fileChoose.get_filename()):
            md = gtk.MessageDialog(self._d, gtk.DIALOG_DESTROY_WITH_PARENT,
                    gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "Invalid file!")
            md.run()
            md.destroy()
            # Try again, hopefully we won't recourse too many times.
            return self.display()

        # If everything is ok here, read info from the other widgets,
        # complete the dictionary and return (the other widgets always
        # return good values).
        self._complete_config()

    def get_settings(self):
        """
        Returns the user's options. To be called only after hiding the dialog.
        Simply returns the dictionary.
        """
        d = self._configDict
        self._configDict = None
        return d

    def destroy(self):
        """
        Destroys this window. Should be called after reading user options with
        the above function. After this call, any access to this instance can
        result in bugs.
        """
        self._d.destroy()

    def _read(self, fName):
        """
        Reads the user provided filename to obtain information about the
        simulation. Completes the _configDict.

        return  True if everything is ok
        """
        if not fName:
            return False

#        try:
#            with open(fName) as f:
#                d = f.readline()
#                p = d.split()
#                if len(p) != 2:
#                    return False
#                self._configDict['N'] = int(p[0])
#                self._configDict['M'] = int(p[1])
#                d = f.readline()
#                self._configDict['D'] = int(d)
#                d = f.readline()
#                p = d.split()
#                if len(p) != 2:
#                    return False
#                self._configDict['xs'] = int(p[0])
#                self._configDict['ys'] = int(p[1])
#                d = f.readline()
#                self._configDict['d1'] = int(d)
#                d = f.readline()
#                self._configDict['d2'] = int(d)
#        except Exception as e:
#            return False
        return True

    def _complete_config(self):
        """
        Reads data from the dialog's widgets to complete the _configDict.
        """
#        self._configDict['greedy?'] = b = self._greedyAction.get_active()
#        if b:
#            self._configDict['ε/τ'] = self._eCounter.get_value()
#        else:
#            self._configDict['ε/τ'] = self._tCounter.get_value()
#        self._configDict['Q?'] = self._ql.get_active()
#        self._configDict['α'] = self._aCounter.get_value()
#        self._configDict['γ'] = self._gCounter.get_value()
#        self._configDict['runs'] = self._rCounter.get_value()

