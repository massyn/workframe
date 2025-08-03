# WorkFrame Test Suite

This directory contains the test suite for WorkFrame.

## Running Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=workframe

# Run specific test
pytest tests/test_core.py
```

## Test Structure

- `test_core.py` - Core WorkFrame functionality
- `test_crud.py` - CRUD operations and field types
- `test_auth.py` - Authentication and authorization
- `test_admin.py` - Admin interface functionality
- `test_database.py` - Database operations and migrations

## Writing Tests

Tests should follow these conventions:
- Use pytest fixtures for test setup
- Test both success and error cases
- Use meaningful test names that describe what is being tested
- Include docstrings for complex test scenarios