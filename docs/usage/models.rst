######
Models
######

The core class of the ``spines`` package is the :class:`spines.Model` class.
A model has three primary functions:

construct
    The ``construct`` function is optional and called prior to any fitting or
    predicting.  It's job is to do any initialization required for the model
    prior to use.


fit
    The ``fit`` function takes input data and it's corresponding output data
    and fits the model.


predict
    The ``predict`` function takes input data after a model has been fitted and
    generates it's predictions for the output predictions.
