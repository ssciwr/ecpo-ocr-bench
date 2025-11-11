# Welcome to ecpo-ocr-bench

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ssciwr/ecpo-ocr-bench/ci.yml?branch=main)](https://github.com/ssciwr/ecpo-ocr-bench/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/ecpo-ocr-bench/badge/)](https://ecpo-ocr-bench.readthedocs.io/)
[![codecov](https://codecov.io/gh/ssciwr/ecpo-ocr-bench/branch/main/graph/badge.svg)](https://codecov.io/gh/ssciwr/ecpo-ocr-bench)

## Installation

The Python package `ecpo_ocr_bench` can be installed from PyPI:

```
python -m pip install ecpo_ocr_bench
```

## Development installation

If you want to contribute to the development of `ecpo_ocr_bench`, we recommend
the following editable installation from this repository:

```
git clone git@github.com:ssciwr/ecpo-ocr-bench.git
cd ecpo-ocr-bench
python -m pip install --editable .[tests]
```

Having done so, the test suite can be run using `pytest`:

```
python -m pytest
```

## Acknowledgments

This repository was set up using the [SSC Cookiecutter for Python Packages](https://github.com/ssciwr/cookiecutter-python-package).
