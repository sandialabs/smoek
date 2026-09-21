# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Migrated from setup.py to modern pyproject.toml build system (PEP 621)
- Updated Python version support to 3.10-3.13 (dropped EOL Python 3.9)
- setup.py now deprecated in favor of pip install, will be removed in v2.0

### Added
- Comprehensive CI/CD via GitHub Actions with auto-formatting, linting, and matrix testing
- Codecov integration for test coverage tracking (80% target)
- ReadTheDocs integration for documentation automation
- Conda environment files (environment.yml for users, dev_environment.yml for development)
- Optional dependency groups: test, poek, coek, backends, dev
- Black auto-formatting configuration (line-length=100)
- Flake8 linting configuration
- Pytest configuration in pyproject.toml
- Documentation infrastructure with Sphinx
- CONTRIBUTING.md with development guidelines
- This CHANGELOG.md

## [1.0.0] - 2024

Initial release

### Added
- Core optimization modeling functionality
- Pyomo backend support
- Optional poek and coek backends
- Model transformation capabilities
- Compact abstract model expressions
- Deferred model instantiation
- Code generation for multiple backends
