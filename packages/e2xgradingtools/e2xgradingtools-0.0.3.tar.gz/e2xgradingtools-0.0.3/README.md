# E2X Grading Tools

[![PyPi](https://img.shields.io/pypi/v/e2xgradingtools)](https://pypi.org/project/e2xgradingtools)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/e2x-grading-tools/badge/?version=latest)](https://e2x-grading-tools.readthedocs.io/en/latest/?badge=latest)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

e2xgradingtools provides a structured approach to execute tests using the global namespace of Jupyter notebooks, with the following highlights:

- Convenient variable and function existence checks
- Continued execution of remaining tests even if one test fails
- Hiding of student’s print statements during test execution
- Built-in type checking for robust testing
- Ability to reference implementation for comparison testing
- Customizable to suit specific needs
- Test output can be parsed by e2xgrader for partial point extraction

Please consult the [docs](https://e2x-grading-tools.readthedocs.io/en/latest) and look at the example notebook in this repository.
