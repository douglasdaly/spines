######
Spines
######

**Backbones for parameterized models.**

|travis| |nbsp| |cov| |nbsp| |docs| |nbsp| |pypi| |nbsp| |status| |nbsp|
|pyvers|


About
=====

Spines was built to provide a skeleton for Model classes: a common
interface for users to build models around (with some tools and
utilities which take advantage of those commonalities).  It's core Model
class is similar, in structure, to some of scikit-learn's underlying
Estimator classes - but with a single set of unified functions for all
models, namely:

- Build
- Fit
- Predict
- Score
- Error

The predict method is the only one that's required to be implemented,
though the others are likely useful most of the time (and often required
to take advantage of some of the additional utilities provided by
spines).

Spines also incorporates automatic version management for your models -
something akin to a very lightweight git - but for individual models.
It also caches results generated during various iterations of the
development/fitting process so that they're not lost during - something
that can (and often does) happen during very iterative model development
work.


Installing
==========

Install with your favorite package manager, like ``pipenv``:

.. code-block:: bash

    $ pipenv install spines


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
    :target: https://readthedocs.org/projects/spines/
    :alt: Documentation
.. |travis| image:: https://travis-ci.org/douglasdaly/spines.svg?branch=master
    :target: https://travis-ci.org/douglasdaly/spines
    :alt: Travis-CI
.. |cov| image:: https://coveralls.io/repos/github/douglasdaly/spines/badge.svg
    :target: https://coveralls.io/github/douglasdaly/spines
    :alt: Coverage
.. |nbsp| unicode:: 0xA0
   :trim:
