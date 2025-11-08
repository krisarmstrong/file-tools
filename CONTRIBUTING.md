# Contributing to File Tools

Thank you for your interest in contributing to File Tools! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/file-tools.git`
3. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
4. Install dependencies: `pip install -e .[test]`

## Development Process

### Setting Up Your Environment

```bash
# Install development dependencies
pip install -e .[test,dev]

# Run tests
pytest tests/ -v

# Check code formatting
ruff check .
```

### Making Changes

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass: `pytest tests/`
5. Commit your changes with a clear message

### Commit Messages

Follow conventional commit format:

```
feat: add new organize mode
fix: correct file path handling
docs: update README with new examples
test: add tests for rename functionality
```

### Pull Requests

1. Push your changes to your fork
2. Create a pull request against the main repository
3. Describe your changes clearly
4. Link any related issues
5. Wait for review and address feedback

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and concise
- Add comments for complex logic

## Testing

- Write tests for all new features
- Maintain or improve code coverage
- Test edge cases and error conditions
- Run the full test suite before submitting

```bash
# Run tests with coverage
pytest tests/ -v --cov=file_tools --cov-report=term
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update docs/ for significant features
- Include usage examples

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about the codebase
- Suggestions for improvements

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
