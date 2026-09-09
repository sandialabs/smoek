A lightweight optimization modeling library.

--------------------------------------------------------------------------------

#[![Pytest Tests](https://github.com/sandialabs/smoek/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/sandialabs/smoek/actions/workflows/pytest.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/sandialabs/smoek/branch/main/graph/badge.svg)](https://codecov.io/gh/sandialabs/smoek)
[![Documentation Status](https://readthedocs.org/projects/smoek/badge/?version=latest)](http://smoek.readthedocs.org/en/latest/)
[![GitHub contributors](https://img.shields.io/github/contributors/sandialabs/smoek.svg)](https://github.com/sandialabs/smoek/graphs/contributors)
[![Merged PRs](https://img.shields.io/github/issues-pr-closed-raw/sandialabs/smoek.svg?label=merged+PRs)](https://github.com/sandialabs/smoek/pulls?q=is:pr+is:merged)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Overview

Smoek is an experimental Python modeling environment that uses a
compact abstract model expression to enable fast transformation of model structure, deferred model
instantiation, and code generation. Smoek was designed to support lightweight model declarations
that can be transformed into back-end implementations such as Pyomo, Poek, Coek, and other
modeling languages or specialized solver interfaces. 
Abstract
model descriptions can be written compactly in Python, transformed quickly, and used to generate
efficient concrete optimization models in lower-level or performance-oriented modeling systems.
The overhead for Smoek declarations and problem transformations is minimal, and low-
level modeling libraries like Coek can be leveraged to significantly accelerate model generation.

## Testing

Smoek tests can be executed using pytest:

```
cd smoek
pytest .
```

If the pytest-cov package is installed, pytest can provide coverage statistics:

```
cd smoek
pytest --cov=smoek .
```

The following options list the lines that are missing from coverage tests:
```
cd smoek
pytest --cov=smoek --cov-report term-missing .
```

Note that pytest coverage includes coverage of test files themselves.  This gives a somewhat skewed sense of coverage for the code base, but it helps identify tests that are omitted or not executed completely.

