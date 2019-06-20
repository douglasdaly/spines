# Spines

*Skeletons for parameterized models.*

[![Build Status](https://travis-ci.org/douglasdaly/spines.svg?branch=master)](https://travis-ci.org/douglasdaly/spines)
[![Coverage Status](https://coveralls.io/repos/github/douglasdaly/spines/badge.svg)](https://coveralls.io/github/douglasdaly/spines)
[![Documentation Status](https://readthedocs.org/projects/spines/badge/?version=latest)](https://spines.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/spines.svg)](https://pypi.org/project/spines/)
[![Status](https://img.shields.io/pypi/status/spines.svg)](https://pypi.org/project/spines/)
[![Python Versions](https://img.shields.io/pypi/pyversions/spines.svg)](https://pypi.org/project/spines/)

<img width="20%" align="right" src="https://github.com/douglasdaly/spines/raw/master/docs/_static/images/spines_logo_256.png" alt="Spines Logo" style="margin-left: 10px;">

**Important:** This software is still in it's early alpha phase and is 
constantly in flux.  It will likely change significantly.


## Installation

To install spines use your package manager of choice, an example using 
`pipenv` would be:

```bash
$ pipenv install spines
```


## About

Spines is a library which provides a consistent (and hopefully familiar)
framework for building predictive models.  It's core `Model` class
is similar, in structure, to some of scikit-learn's underlying Estimator
classes - but with a single set of unified functions for all models,
namely:

- Construct
- Fit
- Predict
- Score

The `predict` method is the only one that's required to be
implemented, though the others are likely useful most of the time (and
often required to take advantage of some of the additional features
provided by spines).

Models act as an extension of `Transform` classes, which are, as
the name implies, used to transform one input to one output.  The
`Transform` class requires a definition for the `transform`
method (in the `Model` this simply calls `predict`), and also
contains the functions:

- Construct
- Fit
- Transform
- Score

The last core concept of spines is the `Parameter`, used in both
`Model` and `Transform` objects to specify some value (or
values) for a particular parameter.  Parameters (and hyper-parameters)
allow you to tweak your model without having to change the code.  They
are used like so:

```python
class MyModel(Model):
    beta = Parameter(float)

    ...
```

Which would specify a new Model with a single, float-valued parameter
named "beta", which can be used in the logic of the model just like
a normal object attribute:

```python
...

def predict(self, x):
    return self.beta * x

...
```

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


## Documentation

The latest documentation is hosted on 
[read the docs](https://spines.readthedocs.io/ "Spines ReadTheDocs").


## License

This project is licensed under the MIT License, for more information see 
the [LICENSE](https://github.com/douglasdaly/spines/blob/master/LICENSE) 
file.
