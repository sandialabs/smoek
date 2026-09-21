# Contributing to Smoek

Thank you for your interest in contributing to Smoek!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sandialabs/smoek.git
   cd smoek
   ```

2. Create development environment:
   ```bash
   conda env create -f dev_environment.yml
   conda activate smoek_dev
   ```

3. Install package in editable mode:
   ```bash
   pip install -e ".[dev]"
   ```

## Running Tests

Run all tests:
```bash
pytest smoek
```

Run with coverage:
```bash
pytest --cov=smoek --cov-report=term smoek
```

Run with detailed coverage report showing missing lines:
```bash
pytest --cov=smoek --cov-report=term-missing smoek
```

## Code Style

We use Black for code formatting and Flake8 for linting.

Format code:
```bash
black .
```

Check linting:
```bash
# Check for critical errors
flake8 smoek --select=E9,F63,F7,F82 --show-source --statistics

# Check for all issues
flake8 smoek --max-line-length=100 --statistics
```

## Building Documentation

Build the documentation locally:
```bash
cd doc
make html
```

View the documentation:
```bash
# The built documentation will be in doc/_build/html/
# Open doc/_build/html/index.html in your browser
```

## Pull Request Process

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and ensure:
   - All tests pass
   - Code is formatted with Black
   - Linting checks pass
   - Documentation is updated if needed

3. Commit your changes with clear, descriptive commit messages

4. Push to your fork and submit a pull request

The CI will automatically:
- Format your code with Black (commits changes back to your PR)
- Run linting checks
- Run tests across Python 3.10-3.14
- Test with different backend configurations
- Generate coverage reports

## Optional Dependencies

To test with optional backends:

```bash
# Install poek backend
pip install poek

# Install coek backend
pip install coek

# Install all backends
pip install -e ".[backends]"
```

Note: If optional backends are not installed, tests for those backends will be skipped automatically.

## CI/CD Pipeline

Our GitHub Actions workflow includes:

1. **Format & Lint**: Auto-formats with Black and checks with Flake8
2. **Tests**: Matrix testing across Python 3.10-3.14
3. **Backend Tests**: Tests with pyomo-only, poek, and coek configurations
4. **Coverage**: Generates coverage reports and uploads to Codecov

## Repository Secrets

If you're a maintainer, ensure these secrets are configured:

- `CODECOV_TOKEN`: Token for uploading coverage reports to Codecov

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to maintain a welcoming and inclusive community.

## Questions?

If you have questions about contributing, feel free to:
- Open an issue on GitHub
- Check existing issues for similar questions
- Review the documentation at https://smoek.readthedocs.io

## License

By contributing, you agree that your contributions will be licensed under the BSD 3-Clause License.
