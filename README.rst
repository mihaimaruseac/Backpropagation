Backpropagation
===============

A. About
........

This is a homework for the Machine Learning Course that I am taking right now
at my University.

The homework uses backpropagation in order to forecast a value from a given set
of values, knowing that one value depends on the values of several of the
previous numbers in the series.

The assignment is done in Python.

B. Usage
........

Run ``./bp.py`` to start the main part of the application. The GUI is pretty
simple to use.

It will show a real time graph of the network while learning with edges
coloured according to their relevance: a red colour means inhibition while a
green color means a bonus.

The application does a logging of all steps in the learning phase.

The input is first normalized to the range of the activation function (-1 to 1
or 0 to 1). In fact, the normalization ensures that points outside the initial
range can still be somehow predicted (with a certain error if the data trend is
exponential but that is another problem).

At the end of the learning phase, the user sees the predicted value along with
an estiamtion of the error and the application saves the network in different
formats to disk. Also, a plot of all data (predicted and given) is saved.

