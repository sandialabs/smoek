"""
Legacy setup.py for backward compatibility.

This file is deprecated. New installations should use:
    pip install .

This file will be removed in smoek version 2.0.
All package configuration is now in pyproject.toml (PEP 621).
"""

import warnings
from setuptools import setup

warnings.warn(
    "setup.py is deprecated. Use 'pip install .' instead. "
    "setup.py will be removed in smoek 2.0.",
    DeprecationWarning,
    stacklevel=2,
)

setup()
