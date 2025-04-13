# Testing the CV Optimizer

This directory contains the test suite for the CV Optimizer cloud function. The tests are organized into multiple categories and use pytest as the testing framework.

## Test Structure

- `tests/unit/`: Unit tests for individual modules
  - `test_document_processor.py`: Tests for the document processing functionality
  - `test_gemini_client.py`: Tests for the Gemini API client
  - `test_adk_client.py`: Tests for the ADK client
  - `test_storage.py`: Tests for the GCS storage utilities
  - `test_secret_manager.py`: Tests for the Secret Manager client
  - `test_schemas.py`: Tests for the Pydantic schema models

- `tests/integration/`: Integration tests that verify multiple components working together
  - `test_main_flow.py`: Tests for the main application flow (HTTP endpoints, authentication, etc.)

- `tests/fixtures/`: Test data files and fixtures
  - `sample_cv.txt`: A sample CV text file for testing
  - `sample_jd.txt`: A sample job description for testing

- `conftest.py`: Common pytest fixtures shared across tests

## Running Tests

### Setup

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Make sure you have any necessary environment variables set (or use mock objects in tests)

### Running All Tests

```bash
pytest
```

### Running Specific Test Categories

```bash
# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Run a specific test file
pytest tests/unit/test_document_processor.py

# Run a specific test function
pytest tests/unit/test_document_processor.py::TestDocumentProcessor::test_extract_text_from_pdf
```

### Running with Coverage

```bash
pytest --cov=. 
```

This will generate a coverage report showing which parts of the code are covered by tests.

For a more detailed HTML coverage report:

```bash
pytest --cov=. --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

## Best Practices

1. **Mock external dependencies**: Always mock external services like Google Cloud Storage, Secret Manager, and Gemini API.
2. **Use fixtures**: Create reusable test fixtures in `conftest.py` for common test dependencies.
3. **Test edge cases**: Include tests for error handling, invalid inputs, and edge cases.
4. **Keep tests independent**: Tests should not depend on the state left by previous tests.
5. **Use meaningful assertions**: Make assertion messages clear to understand test failures.

## Extending the Test Suite

When adding new functionality to the codebase, follow these steps:

1. Create unit tests for the new module or function
2. Update integration tests if the new functionality affects the main application flow
3. Add any new test fixtures if needed
4. Run the full test suite to ensure nothing breaks 