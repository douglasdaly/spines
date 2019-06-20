######
Spines
######

.. image:: ./_static/images/spines_logo_256.png
    :scale: 30 %
    :alt: Spines Logo
    :align: right

*Skeletons for parameterized models.*

|travis| |nbsp| |cov| |nbsp| |docs| |nbsp| |pypi| |nbsp| |status| |nbsp|
|pyvers|

.. important::

    This software is still in it's early alpha phase and is constantly
    in flux.  It will likely change significantly.


Installation
============

Install with your favorite package manager, like ``pipenv``:

.. code-block:: bash

    $ pipenv install spines


About
=====

Spines is a library which provides a consistent (and hopefully familiar)
framework for building predictive models.  It's core :obj:`Model` class
is similar, in structure, to some of scikit-learn's underlying Estimator
classes - but with a single set of unified functions for all models,
namely:

- Construct
- Fit
- Predict
- Score

The ``predict`` method is the only one that's required to be
implemented, though the others are likely useful most of the time (and
often required to take advantage of some of the additional features
provided by spines).

Models act as an extension of :obj:`Transform` classes, which are, as
the name implies, used to transform one input to one output.  The
:obj:`Transform` class requires a definition for the :obj:`transform`
method (in the :obj:`Model` this simply calls :obj:`predict`), and also
contains the functions:

- Construct
- Fit
- Transform
- Score

The last core concept of spines is the :obj:`Parameter`, used in both
:obj:`Model` and :obj:`Transform` objects to specify some value (or
values) for a particular parameter.  Parameters (and hyper-parameters)
allow you to tweak your model without having to change the code.  They
are used like so:

.. code-block:: python

    class MyModel(Model):
        beta = Parameter(float)

        ...

Which would specify a new Model with a single, float-valued parameter
named "beta", which can be used in the logic of the model just like
a normal object attribute:

.. code-block:: python

    ...

    def predict(self, x):
        return self.beta * x

    ...


Spines was built because the process of developing a model could be
significantly aided by an intelligent framework keeping tabs on changes,
storing results and helping you iterate. The purpose of spines was to
give a simple (and not *too* opinionated) interface/skeleton for models
(which was not *too* unfamiliar) as well as provide some helpful
utilities for the model building process which take advantage of the
(minimal) structure imposed.  To accomplish this spines provides some
useful key features:

- Automatic version management.
- Storing intermediate/iterative results during the model development
  and fitting process.
- A unified storage format for models to facilitate collaboration,
  fitting and deployment.
- The ability to easily compose together transforms and models into a
  pipeline.
- The ability to deploy a model (or pipeline), with a single command, as
  a RESTful API endpoint.


Simple Example
==============

To demonstrate how to build a model with spines we'll use a toy example
of a simple linear regression model.  First we import what we'll need:

.. code-block:: python

    import numpy as np

    from spines import Model, Parameter


Now we'll create the model class:

.. code-block:: python

    class LinearRegression(Model):
        """
        Simple linear regression model

            y = mx + b

        """
        m = Parameter(float)
        b = Parameter(float)

        def fit(self, x, y):
            covs = np.cov(x, y)
            self.m = (covs[0, 1] / np.var(x))
            self.b = np.mean(y) - (self.m * np.mean(x))

        def predict(self, x):
            return (self.m * x) + self.b

Now that we have the model we can generate some random data to fit it
with:

.. code-block:: python

    x = np.random.rand(10)
    y = 3.0 * x
    x += np.random.normal(scale=0.05, size=(10,))

Then create and fit the model:

.. code-block:: python

    model = LinearRegression()
    model.fit(x, y)

If we look at the ``model.parameters`` attribute we should see something
like ``b`` being a small-ish number around 0 and ``m`` being close to
3.

See the :doc:`quick start <quickstart>` page for a slightly more
in-depth example.


.. toctree::
    :maxdepth: 2
    :caption: Getting Started
    :hidden:

    installation
    quickstart


.. toctree::
    :maxdepth: 2
    :caption: Usage
    :hidden:

    usage/parameters
    usage/models


.. toctree::
    :maxdepth: 2
    :caption: Reference
    :hidden:

    api/modules
    contributing
    conduct
    authors
    development/development.main
    changelogs/changelogs
    license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. |pyvers| image:: https://img.shields.io/pypi/pyversions/spines.svg
    :target: https://pypi.org/projects/spines/
    :alt: Supported Python Versions
.. |pypi| image:: https://img.shields.io/pypi/v/spines.svg
    :target: https://pypi.org/projects/spines/
    :alt: PyPI
.. |status| image:: https://img.shields.io/pypi/status/spines.svg
    :target: https://pypi.org/projects/spines/
    :alt: Status
.. |docs| image:: https://readthedocs.org/projects/spines/badge/?version=latest
    :target: https://spines.readthedocs.io/en/latest/
    :alt: Documentation
.. |travis| image:: https://travis-ci.org/douglasdaly/spines.svg?branch=master
    :target: https://travis-ci.org/douglasdaly/spines
    :alt: Travis-CI
.. |cov| image:: https://coveralls.io/repos/github/douglasdaly/spines/badge.svg
    :target: https://coveralls.io/github/douglasdaly/spines
    :alt: Coverage
.. |nbsp| unicode:: 0xA0
   :trim:
