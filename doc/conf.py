# Sphinx configuration for smoek documentation

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "smoek"
copyright = "2026, Sandia National Laboratories"
author = "smoek developers"
version = "1.0"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = []

autodoc_member_order = "bysource"
autosummary_generate = True
