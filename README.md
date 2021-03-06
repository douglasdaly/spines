# Spines

<img width="20%" align="right" src="./docs/_static/images/spines_logo_256.png" alt="Spines Logo" style="margin-left: 10px;">

*Skeletons for parameterized models.*

[![Build Status](https://travis-ci.org/douglasdaly/spines.svg?branch=master)](https://travis-ci.org/douglasdaly/spines)
[![Coverage Status](https://coveralls.io/repos/github/douglasdaly/spines/badge.svg)](https://coveralls.io/github/douglasdaly/spines)
[![Documentation Status](https://readthedocs.org/projects/spines/badge/?version=latest)](https://spines.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/spines.svg)](https://pypi.org/project/spines/)
[![Status](https://img.shields.io/pypi/status/spines.svg)](https://pypi.org/project/spines/)
[![Python Versions](https://img.shields.io/pypi/pyversions/spines.svg)](https://pypi.org/project/spines/)

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
framework for building predictive models.  It's core Model class is 
similar, in structure, to some of scikit-learn's underlying Estimator 
classes - but with a single set of unified functions for all models, 
namely:

- Construct
- Fit
- Train
- Predict
- Error
- Score

The ```predict``` method is the only one that's required to be 
implemented, though the others are likely useful most of the time (and 
often required to take advantage of some of the additional features 
provided by spines).

Spines was built because the process of developing a model could be 
significantly aided by an intelligent framework keeping tabs on changes, 
storing results and helping you iterate. The purpose of spines was to 
give a simple (and not too opinionated) interface/skeleton for models as 
well as provide some helpful utilities for the model building process.
To accomplish this spines provides some useful key features:

- Standardized format for models of all types.
- Automatic version management.
- Storing intermediate/iterative results during the model development
  and training/fitting process.
- A unified storage format for models to facilitate collaboration,
  training and deployment.


## Documentation

The latest documentation is hosted on 
[read the docs](https://spines.readthedocs.io/ "Spines ReadTheDocs").


## License

This project is licensed under the MIT License, for more information see 
the [LICENSE](https://github.com/douglasdaly/spines/blob/master/LICENSE) 
file.
