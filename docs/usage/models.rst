######
Models
######

The core class of the ``spines`` package is the :class:`spines.Model` class.
All models have three primary functions in common: ``build``, ``fit`` and
``transform``.  You can implement as many additional functions as needed but
these three lie at the heart of the ``spines`` library.


build
=====

The ``build`` function is optional and called prior to any fitting or
predicting.  It's job is to do any initialization required for the model
prior to use.


fit
===

The ``fit`` function (aka train) takes input data and it's corresponding
output data and fits the model.  This function is not required (though it
is likely implemented for most use cases).


transform
=========

The ``transform`` function (aka predict) takes input data and generates
it's corresponding outputs based on the parameters of the model.
