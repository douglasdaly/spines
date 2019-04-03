######
Spines
######

**Backbones for parameterized models.**

About
=====

Spines was built to provide a skeleton for Model classes: a common 
interface for users to build models around (with some tools and 
utilities which take advantage of having the commonalities).  It's 
similar, in structure, to some of scikit-learn's underlying Estimator 
classes - but with a single set of unified functions for all models, 
namely:

- Build
- Fit
- Transform

The transform method is the only one that's required, though the other 
two are likely useful most of the time.  Spines is **absolutely not** a 
replacement for scikit-learn (or any other data/machine-learning 
library) it's simply a useful framework for building your own models 
(leveraging *any* library) in a standardized and convenient way.


Installing
==========

Install with your favorite package manager, like ``pipenv``:

.. code-block:: bash

    $ pipenv install spines


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
    changelogs/changelogs
    license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
