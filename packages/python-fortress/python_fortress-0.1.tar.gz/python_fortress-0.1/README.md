# Python Fortress

Python Fortress is a library designed to facilitate interaction with an API to retrieve an .env file. It's designed for securely and efficiently loading environment variables from a remote source.

[![codecov](https://codecov.io/gh/magestree/python_fortress/branch/develop/graph/badge.svg)](https://codecov.io/gh/magestree/python_fortress)

## Features

- Easy loading of credentials and configurations from environment variables.
- Secure retrieval of the `.env` file content from an API.
- Simple and efficient usage with intuitive methods.

## Installation

To install the project dependencies, run:

```bash
pip install -r requirements.txt
```

## Basic usage

The main module `fortress.py` provides the `Fortress` class and a convenience function `load_env()`.

## Example:

```python
from python_fortress.fortress import load_env

load_env()
```

## Tests
The project comes with a set of tests to ensure everything works as expected. You can run the tests using pytest:

```bash
pytest
```

To obtain a coverage report:
```bash
coverage run -m pytest
coverage report
```

## CI/CD
Thanks to GitHub Actions, each push or pull request will trigger the CI pipeline which will run tests and calculate code coverage.


## Contribution
If you're interested in contributing to the project, please follow these steps:

1. Fork repository.
2. Create a new branch for your feature or fix.
3. Implement your change or fix.
4. Run the tests to make sure everything is working as expected.
5. Open a pull request.


## Licencia
MIT
