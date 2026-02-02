# Contributing to Midna

Thank you for your interest in contributing to Midna! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Procedures](#testing-procedures)
- [Commit Conventions](#commit-conventions)
- [Pull Request Process](#pull-request-process)
- [Security](#security)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and collaborative environment. Please be considerate and constructive in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/midna.git
   cd midna
   ```
3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/jassem-manita/midna.git
   ```

## Development Environment Setup

### Prerequisites

- Python 3.8 or newer
- pip (comes with Python)
- Git

### Installation Steps

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install the package in editable mode with dev dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

   This installs:
   - `pytest` and `pytest-cov` for testing
   - `black` for code formatting
   - `flake8` for linting
   - `isort` for import sorting
   - `mypy` for type checking
   - `build` and `twine` for packaging

3. **Verify the installation**:
   ```bash
   midna --version
   pytest tests/
   ```

## Code Style Guidelines

We follow standard Python conventions to maintain code quality and consistency.

### Formatting

- **Line Length**: Maximum 100 characters
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Prefer double quotes for strings

### Tools

1. **Black** (code formatter):
   ```bash
   black midna/ tests/
   ```

2. **isort** (import sorting):
   ```bash
   isort midna/ tests/
   ```

3. **Flake8** (linting):
   ```bash
   flake8 midna/ tests/ --max-line-length=100
   ```

4. **mypy** (type checking):
   ```bash
   mypy midna/ --ignore-missing-imports
   ```

### Docstrings

Use Google-style docstrings for all public functions, classes, and modules:

```python
def function_name(param1: str, param2: int) -> bool:
    """Brief description of the function.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: Description of when this error is raised
    """
    pass
```

### Naming Conventions

- **Functions and variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private members**: Prefix with single underscore `_private_method`

## Testing Procedures

### Running Tests

Run all tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest tests/ --cov=midna --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_midna.py
```

Run specific test function:
```bash
pytest tests/test_midna.py::test_function_name
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Name test functions with `test_` prefix
- Use descriptive test names that explain what is being tested
- Aim for at least 80% code coverage for new code

Example test structure:
```python
def test_function_does_expected_behavior():
    """Test that function_name handles input correctly."""
    # Arrange
    input_data = "test"
    
    # Act
    result = function_name(input_data)
    
    # Assert
    assert result == expected_output
```

### Security Testing

Before submitting a PR, run security checks:

1. **Bandit** (security linter):
   ```bash
   bandit -r midna/ -x tests,test
   ```

2. **pip-audit** (dependency vulnerability scanner):
   ```bash
   pip-audit
   ```

## Commit Conventions

We follow conventional commit messages for clarity and automatic changelog generation.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring without changing functionality
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build config, etc.)
- `perf`: Performance improvements
- `ci`: CI/CD changes

### Examples

```bash
feat(discovery): add support for Poetry pyproject.toml format

Implemented parser for Poetry-style pyproject.toml files to support
auto-discovery in Poetry-based projects.

Closes #123
```

```bash
fix(installer): handle network timeout errors gracefully

Added retry logic and better error messages when pip installation
fails due to network issues.
```

```bash
docs: update README with new CLI options
```

## Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines above

3. **Run all checks**:
   ```bash
   # Format code
   black midna/ tests/
   isort midna/ tests/
   
   # Run linting
   flake8 midna/ tests/ --max-line-length=100
   
   # Run tests
   pytest tests/ --cov=midna
   
   # Run security checks
   bandit -r midna/ -x tests,test
   ```

4. **Commit your changes** using conventional commit messages:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what was changed and why
   - Reference to any related issues (e.g., "Closes #123")
   - Screenshots or examples if applicable

7. **Respond to feedback** from maintainers and update your PR as needed

### PR Checklist

Before submitting, ensure:

- [ ] Code follows style guidelines (Black, isort, Flake8)
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated (README, docstrings, etc.)
- [ ] Security checks pass (Bandit, pip-audit)
- [ ] Commit messages follow conventions
- [ ] PR description is clear and complete

## Security

If you discover a security vulnerability, please follow our security policy:

1. **Do NOT** open a public issue
2. Review [SECURITY.md](https://github.com/jassem-manita/midna/blob/main/SECURITY.md)
3. Report the vulnerability privately through GitHub's security advisory feature

## Questions?

If you have questions or need help:

- Open a [GitHub Discussion](https://github.com/jassem-manita/midna/discussions)
- Check existing [Issues](https://github.com/jassem-manita/midna/issues)
- Reach out to the maintainer: Jassem Manita ([@jassem-manita](https://github.com/jassem-manita))

Thank you for contributing to Midna!
