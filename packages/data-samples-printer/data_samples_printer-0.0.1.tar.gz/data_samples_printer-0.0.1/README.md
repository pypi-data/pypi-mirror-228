# Data Samples Printer

[![PyPI](https://img.shields.io/pypi/v/data-samples-printer?style=flat-square)](https://pypi.python.org/pypi/data-samples-printer/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/data-samples-printer?style=flat-square)](https://pypi.python.org/pypi/data-samples-printer/)
[![PyPI - License](https://img.shields.io/pypi/l/data-samples-printer?style=flat-square)](https://pypi.python.org/pypi/data-samples-printer/)
[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)


---

**Documentation**: [https://ernestum.github.io/data-samples-printer](https://ernestum.github.io/data-samples-printer)

**Source Code**: [https://github.com/ernestum/data-samples-printer](https://github.com/ernestum/data-samples-printer)

**PyPI**: [https://pypi.org/project/data-samples-printer/](https://pypi.org/project/data-samples-printer/)

---

Don't be just mean and standart, print histograms as unicode instead!

## Installation

```sh
pip install data-samples-printer
```

## Basic Usage

```python
import data_samples_printer as dsp
import numpy as np

s1 = np.random.normal(size=100)
s2 = np.random.normal(size=100, scale=0.2)

# Plain printing
dsp.print(s1)
> ▁   ▃ ▁▃▁  ▃▃▅▇▅█▄▄▄▇▃▃█▄▅▇▄▃▃▁█▅█ ▁▃▃▁▃▁        ▁

# Printing multiple samples aligns their range
dsp.print(s1, s2)
> ▁   ▃ ▁▃▁  ▃▃▅▇▅█▄▄▄▇▃▃█▄▅▇▄▃▃▁█▅█ ▁▃▃▁▃▁        ▁
>                   ▁▂▃█▄▅▃▂▁

# Printing with labels
dsp.print(normal=s1, squeezed=s2)
> ▁   ▃ ▁▃▁  ▃▃▅▇▅█▄▄▄▇▃▃█▄▅▇▄▃▃▁█▅█ ▁▃▃▁▃▁        ▁ normal
>                    ▁▂▃█▄▅▃▂▁                       squeezed

# Pretty printing
dsp.pprint(s1, s2)
> ▂ ▂▁▁ ▁▂▄▃▁▁▂▂▂▄▃▂█▃▃▂▃▂▂▂▁▃▂▄▃▂ ▁▂▁ ▁▁▂       ▁ ▁ 0.00 ±1.00
>                 ▁▂▃▆█▅▆▄▁                          0.04 ±0.20

dsp.mprint(normal=s1, squeezed=s2)
> dist | mean | std | name
> -----|------|-----|-----
> `▕▁ ▂▁▁▁▁▁▃▁ ▂▆▂▁▅▅▅█▂▅▃▅█▃▇▆▂▂▂▂▂▂▅▃▁ ▁     ▁   ▂ ▁▏` | -0.04 | ±0.85 | normal
> `▕                ▁ ▁▄▃█▆█▆▂▂                       ▏` | 0.01 | ±0.19 | squeezed
> `▕-1.93                                         2.41▏` |
```

renders as:

dist | mean | std | name
-----|------|-----|-----
`▕▁ ▂▁▁▁▁▁▃▁ ▂▆▂▁▅▅▅█▂▅▃▅█▃▇▆▂▂▂▂▂▂▅▃▁ ▁     ▁   ▂ ▁▏` | -0.04 | ±0.85 | normal
`▕                ▁ ▁▄▃█▆█▆▂▂                       ▏` | 0.01 | ±0.19 | squeezed
`▕-1.93                                         2.41▏` |

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.7+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
pytest
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [Github project page
 ](https://pages.github.com/) automatically as part each release.

### Releasing

Trigger the [Draft release workflow](https://github.com/ernestum/data-samples-printer/actions/workflows/draft_release.yml)
(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.

Find the draft release from the
[GitHub releases](https://github.com/ernestum/data-samples-printer/releases) and publish it. When
 a release is published, it'll trigger [release](https://github.com/ernestum/data-samples-printer/blob/master/.github/workflows/release.yml) workflow which creates PyPI
 release and deploys updated documentation.

### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---

This project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.
