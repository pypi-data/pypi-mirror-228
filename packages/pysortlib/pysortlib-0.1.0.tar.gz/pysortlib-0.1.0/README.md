# Sorting algorithms

[![Coverage Status](https://coveralls.io/repos/github/slimreaper35/pysortlib/badge.svg?branch=main)](https://coveralls.io/github/slimreaper35/pysortlib?branch=main)

- Insert sort
- Bubble sort
- Merge sort
- Selection sort
- Quick sort
- Heap sort
- Counting sort
- Radix sort

## Install

```bash
pip install pysortlib
```

## Usage

```python
from pysortlib import insert_sort

array = [3, 5, 2, 1, 7, 4, 6]
insert_sort(array)  # set a breakpoint
print(array)
```

## Development

#### Virtual environment

```bash
pip install --user poetry
poetry config virtualenvs.in-project true
poety shell
poetry install
```

#### Pre-commit

```bash
pre-commit install --hook-type pre-commit
pre-commit install --hook-type commit-msg
pre-commit autoupdate
```

#### Coding standards

- black
- ruff
- mypy
- pytest
