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
        _checkHBox = gtk.HBox()
        self._build_topology_gui(_checkHBox)
        self._build_activation_gui(_checkHBox)
        _topVBox.pack_start(_checkHBox, False, False, 5)
        _checkHBox = gtk.HBox()
        self._build_params_gui(_checkHBox)
        self._build_extra_gui(_checkHBox)
        _topVBox.pack_start(_checkHBox, False, False, 5)
        self._d.vbox.add(_topVBox)

    def _build_topology_gui(self, _checkHBox):
        """
        Builds the GUI allowing to tweak network's topology.

        _checkHBox    HBox holding the widgets built by this function
        """
        _aVBox = self._build_compund_gui_box(_checkHBox, "Topology:")
        self._order = self._build_labeled_input('N: ', _aVBox)
        self._h1 = self._build_labeled_input('h1:', _aVBox)
        self._h2 = self._build_labeled_input('h2:', _aVBox)

    def _build_activation_gui(self, _checkHBox):
        """
        Builds the GUI allowing to select between activation functions.
        """
        _aVBox = self._build_compund_gui_box(_checkHBox, "Activations:")
        self._log = gtk.RadioButton(None, 'Simple logistic')
        self._2log = gtk.RadioButton(self._log, 'Logistic in [-1, 1]')
        self._tanh = gtk.RadioButton(self._log, 'Tanh')
        _aVBox.add(self._log)
        _aVBox.add(self._2log)
        _aVBox.add(self._tanh)

    def _build_params_gui(self, _checkHBox):
        """
        Builds the GUI for setting the parameters.
        """
        _aVBox = self._build_compund_gui_box(_checkHBox, "Parameters:")
        self._etaCounter = self._build_counter('learning rate:', .1, 5, _aVBox, .1, 1)
        self._alphaCounter = self._build_counter('momentum rate:', .2, .8, _aVBox, .1, 1, False)
        self._minRmsCounter = self._build_counter('minimum error:', 0, .1, _aVBox, .01)
        self._minRmsCounter.get_adjustment().set_value(.01)
        self._minDeltaRmsCounter = self._build_counter('minimum delta error:', 0, .1, _aVBox, .01)

    def _build_extra_gui(self, _checkHBox):
        """
        Builds the GUI part for extra options.
        """
        _aVBox = self._build_compund_gui_box(_checkHBox, "Extra:")
        self._minCounter = self._build_counter('min weight:', -1, 1, _aVBox)
        self._maxCounter = self._build_counter('max weight:', -1, 1, _aVBox)
        self._minCounter.get_adjustment().set_value(-1)
        self._maxCounter.get_adjustment().set_value(1)
        self._momentum = gtk.CheckButton('Use momentum')
        self._momentum.connect('clicked', self.__on_momentum)
        self._recurrent = gtk.CheckButton('Recurent network')
        _aVBox.add(self._momentum)
        _aVBox.add(self._recurrent)

    def _build_IO_gui(self, _topVBox):
        """
        Builds the GUI for the UI actions: what file to read and how many
        steps to learn.

        _topVBox    VBox holding the widgets built by this function
        """
        _fileHBox = gtk.HBox()
        _fileVBox = gtk.VBox()
        _topVBox.pack_start(_fileVBox, False, False, 5)
        _fileLabel = gtk.Label('Input filename:')
        _fileHBox.pack_start(_fileLabel, False, False, 5)
        self._fileChoose = gtk.FileChooserButton("Select input filename")
        _fileHBox.pack_start(self._fileChoose, True, True, 5)
        _fileVBox.pack_start(_fileHBox, False, False, 5)
        self._rCounter = self._build_counter('Max steps:', 1000, 3000, _fileVBox, 100, 0)

    def _build_compund_gui_box(self, _checkHBox, frame):
        """
        Builds the VBox used to construct a compund widget and adds it to the
        parent frame, adding that frame to the parent container.
        """
        _frame = gtk.Frame(frame)
        _checkHBox.pack_start(_frame, True, True, 5)
        _aVBox = gtk.VBox()
        _frame.add(_aVBox)
        return _aVBox


    def _build_labeled_input(self, text, parent, default='2'):
        """
        Builds a Edit TextBox with a Label to input one parameter.

        text    text explaining what the value stands for
        parent  parent widget
        """
        _hBox = gtk.HBox()
        _label = gtk.Label(text)
        _hBox.pack_start(_label, False, False, 5)
        w = gtk.Entry()
        w.set_width_chars(3)
        w.set_text(default)
        _hBox.pack_start(w, True, True, 5)
        parent.add(_hBox)
        return w

    def _build_counter(self, text, minv, maxv, parent, incr=.05, digits=2, enabled=True):
        """
        Builds a SpinButton used to represent a fixed value in a fixed
        interval (for values of parameters).

        text        text explaining what the value stands for
        minv        minimal value for the counter
        maxv        maximal value for the counter
        parent      parent box for this counter
        incr        increment value for the spin button
        digits      decimal places to show in the button
        enabled     is the SpinButton available when it is built?
        return      the SpinButton built
        """
        _hBox = gtk.HBox()
        _label = gtk.Label(text)
        _hBox.pack_start(_label, False, False, 5)
        sb = gtk.SpinButton(gtk.Adjustment(step_incr=incr), digits=digits)
        sb.set_numeric(True)
        sb.set_wrap(True)
        sb.set_range(minv, maxv)
        sb.set_sensitive(enabled)
        _hBox.pack_start(sb, True, True, 5)
        parent.add(_hBox)
        return sb

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
            self._report(gtk.MESSAGE_ERROR, "Invalid file!")
            # Try again, hopefully we won't recourse too many times.
            return self.display()

        # If everything is ok here, read info from the other widgets,
        # complete the dictionary and return
        if not self._complete_config():
            return self.display()

        # Check read values for consistency
        # if in error, display again

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

        self._configDict['baseName'] = fName

        try:
            with open(fName) as f:
                d = f.readline()
                p = d.split()
                self._configDict['data'] = map(float, p)
                self._configDict['N'] = len(self._configDict['data'])
        except Exception as e:
            return False
        return True

    def _complete_config(self):
        """
        Reads data from the dialog's widgets to complete the _configDict.
        """
        self._configDict['runs'] = int(self._rCounter.get_value())

        if not self._read_int_text_widget('N', self._order):
            return False
        if not self._read_int_text_widget('h1', self._h1):
            return False
        if not self._read_int_text_widget('h2', self._h2):
            return False

        if self._log.get_active():
            self._configDict['activation'] = 'log'
        elif self._2log.get_active():
            self._configDict['activation'] = '2log'
        else:
            self._configDict['activation'] = 'tanh'

        self._configDict['minW'] = self._minCounter.get_value()
        self._configDict['maxW'] = self._maxCounter.get_value()
        self._configDict['momentum'] = self._momentum.get_active()
        self._configDict['recurrent'] = self._recurrent.get_active()

        self._configDict['alpha'] = self._alphaCounter.get_value()
        self._configDict['eta'] = self._etaCounter.get_value()
        self._configDict['min_rms'] = self._minRmsCounter.get_value()
        self._configDict['min_delta_rms'] = self._minDeltaRmsCounter.get_value()

        if self._configDict['minW'] > self._configDict['maxW'] - .1:
            self._report(gtk.MESSAGE_WARNING, "Invalid interval for weights, ignored")
            self._configDict['minW'] = -1
            self._configDict['maxW'] = 1

        if self._configDict['h1'] == 0 and self._configDict['h2'] != 0:
            self._report(gtk.MESSAGE_WARNING, "Still a network with a single layer")

        if self._configDict['N'] < 1:
            self._report(gtk.MESSAGE_ERROR, "Order should be at least 1")
            return False

        return True

    def _read_int_text_widget(self, cfgName, widget):
        """
        Reads data from a text widget and tries to convert it to integer.
        """
        try:
            self._configDict[cfgName] = int(widget.get_text())
        except Exception as e:
            self._report(gtk.MESSAGE_ERROR, "Invalid option for {0}!".format(cfgName))
            return False
        return True

    def _report(self, msg_type, text):
        """
        Reports an error or a warning.
        """
        md = gtk.MessageDialog(self._d, gtk.DIALOG_DESTROY_WITH_PARENT,
                msg_type, gtk.BUTTONS_CLOSE, text)
        md.run()
        md.destroy()

    def __on_momentum(self, widget, data=None):
        self._alphaCounter.set_sensitive(not self._alphaCounter.get_sensitive())

