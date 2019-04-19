######
Models
######

The core class of the ``spines`` package is the :class:`spines.Model`
class. All models have four primary functions in common: ``build``,
``fit``, ``predict`` and ``error``.  You can implement as many
additional functions as needed but these lie at the heart of the
``spines`` library.


build
=====

The ``build`` function is optional and called prior to any fitting or
predicting.  It's job is to do any initialization required for the model
prior to use.


fit
===

The ``fit`` function (aka train) takes input data and it's corresponding
output data and fits the model.  This function is not required (though
it is likely implemented for most use cases).


predict
=======

The ``predict`` function takes input data and generates it's
corresponding outputs based on the parameters of the model.


error
=====

The ``error`` function takes input and output data and calculates an
error measure for the model.

