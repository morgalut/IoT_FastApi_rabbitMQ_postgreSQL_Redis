# Running Tests with Pytest

This guide explains how to run tests for the IoT Event Ingestion Service using **pytest**.

## Prerequisites

1. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Confirm that PostgreSQL is running and the database is properly configured using the `.env` file:
   ```env
POSTGRES_PORT=5432
POSTGRES_PASSWORD=newer_password
POSTGRES_USER=new_admin
POSTGRES_DB=iot_events

REDIS_HOST=redis
REDIS_PORT=6379
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=user
RABBITMQ_PASSWORD=guest
   ```

## Running Tests

To execute the tests, use the following command:

```bash
pytest tests/test_app.py
```

### Output
Pytest will display the test results, indicating which tests passed, failed, or were skipped.

### Example
```bash
=================================== test session starts ===================================
collected 3 items

tests/test_app.py ....                                                               [100%]

==================================== 4 passed in 2.13s ====================================
```

## Debugging Failures

1. If a test fails, pytest will display the failure details. Fix the issue in the application or test code and re-run the tests.

2. To run a specific test, use:
   ```bash
   pytest tests/test_app.py::test_register_device_success
   ```

3. For detailed output, add the `-v` flag:
   ```bash
   pytest -v tests/test_app.py
   ```

## Cleaning the Database

The `setup_database` fixture ensures that the database is reset before each test. If you encounter unexpected test failures, confirm that the database is being reset correctly.

## Additional Options

- Run all tests with detailed output:
  ```bash
  pytest -v
  ```

- Display a short summary of test results:
  ```bash
  pytest --tb=short
  ```

