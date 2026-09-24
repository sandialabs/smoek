# Smoek Documentation

This directory contains the end-user documentation for smoek, built with Sphinx.

## Documentation Files

The documentation consists of 5 main sections:

1. **overview.rst** - Introduction to smoek's architecture, key concepts, and when to use it
2. **quickstart.rst** - Getting started guide with progressive examples
3. **api.rst** - Comprehensive API reference organized by functionality
4. **backends.rst** - Guide to backend transformations (Pyomo, Coek, etc.)
5. **examples.rst** - Comprehensive examples from simple to complex models

## Key Features

- **End-user focused**: Emphasis on practical usage rather than implementation details
- **Example-driven**: Examples from `smoek/core/tests/models.py` throughout
- **Data loading coverage**: Detailed documentation of `load_data_from_json` and `store_data_to_json`
- **Progressive learning**: Simple examples first, building to complex optimization problems

## Building the Documentation

### Install dependencies

```bash
pip install -r requirements.txt
```

### Build HTML

```bash
make html
```

Or directly:

```bash
sphinx-build -b html . _build/html
```

The generated HTML will be in `_build/html/index.html`.

### Run Tests

Run doctest on code examples:

```bash
make doctest
```

Or:

```bash
sphinx-build -b doctest . _build/doctest
```

Check for broken links:

```bash
make linkcheck
```

### Other Formats

```bash
make latexpdf  # Build PDF via LaTeX
make epub      # Build EPUB
make text      # Build plain text
```

## Documentation Structure

```
doc/
├── index.rst           # Main entry point with toctree
├── overview.rst        # What is smoek, architecture, concepts
├── quickstart.rst      # Getting started tutorial
├── api.rst            # Complete API reference
├── backends.rst       # Backend transformation guide  
├── examples.rst       # Comprehensive examples
├── conf.py           # Sphinx configuration
├── Makefile          # Build commands
└── requirements.txt  # Sphinx dependencies
```

## API Documentation Highlights

The API reference (`api.rst`) provides comprehensive coverage of:

- Model definition (`@model`, `Model`)
- Variables and domains (`variable()`, `Binary`, `Integers`, etc.)
- Parameters and data (`parameter()`, `data()`)
- Sets and indices (`set()`, `range()`, `sequence()`, `index()`)
- Constraints (`constraint()`, `inequality()`)
- Objectives (`objective()`, `minimize()`, `maximize()`)
- Mathematical expressions (`sum()`, `prod()`, `forall()`, trig functions)
- **Data loading and storage** (detailed section):
  - `load_data_from_json()` with all parameters
  - `store_data_to_json()` for creating data files
  - `JsonDataPortal`/`DataPortal` classes
  - Complete JSON schema format documentation
- Utilities (`expr_to_string()`, `model_to_dict()`, etc.)

## Configuration

The `conf.py` file is pre-configured with:

- `sphinx.ext.autodoc` - API documentation
- `sphinx.ext.napoleon` - NumPy/Google docstrings
- `sphinx.ext.mathjax` - Mathematical notation
- `sphinx.ext.viewcode` - Source code links
- `sphinx.ext.doctest` - Testable examples
- `sphinx_rtd_theme` - Read the Docs theme

No configuration changes needed.
