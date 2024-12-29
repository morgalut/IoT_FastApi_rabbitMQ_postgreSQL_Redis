

# Running Tests for the Alerting Service

This document provides step-by-step instructions to run tests for the Alerting Service, which ensures the application functions as expected. Before proceeding, ensure you have Python and pytest installed along with the necessary coverage plugin.

## Prerequisites

1. **Python**: Ensure Python is installed on your system.
2. **pytest**: This is the testing framework used. Install pytest and pytest-cov for coverage reports if not already installed:
   ```bash
   pip install pytest pytest-cov
   ```
3. **Environment Setup**: The PYTHONPATH environment variable needs to be set correctly for pytest to find and run the tests.

## Running the Tests

Follow these steps to execute the tests:

### Step 1: Navigate to the Service Directory

Change your current directory to the alerting service directory:

```bash
cd "IoT\ametos-backend-engineer-assignment\alerting_service"
```

### Step 2: Execute the Tests

Run the tests along with coverage reporting:

```bash
set PYTHONPATH=%CD% && pytest --cov=alerting_service tests/
```

This command sets the `PYTHONPATH` to the current directory (ensuring the alerting_service modules are discoverable by Python) and runs pytest across all tests in the `tests/` directory while collecting coverage data specifically for the `alerting_service` package.

## Interpreting Test Results

- **Test Results**: After running the command, pytest will provide a report on which tests passed and which failed along with the reason for failures if any.
- **Coverage Report**: The coverage report summarizes the percentage of the code base tested, helping identify any parts of the code not covered by tests.

By following these instructions, you can effectively test and validate the functionality of the Alerting Service within your IoT backend infrastructure.

