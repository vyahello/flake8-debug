![Screenshot](icon.png)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Coverage Status](https://coveralls.io/repos/github/vyahello/flake8-debug/badge.svg?branch=master)](https://coveralls.io/github/vyahello/flake8-debug?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with flake8](https://img.shields.io/badge/flake8-checked-blue)](http://flake8.pycqa.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![PyPI version shields.io](https://img.shields.io/pypi/v/flake8-debug.svg)](https://pypi.python.org/pypi/flake8-debug/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/flake8-debug.svg)](https://pypi.python.org/pypi/flake8-debug)
[![PyPi downloads](https://img.shields.io/pypi/dm/flake8-debug.svg)](https://pypi.python.org/pypi/flake8-debug)
[![Downloads](https://pepy.tech/badge/flake8-debug)](https://pepy.tech/project/flake8-debug)
[![EO principles respected here](https://www.elegantobjects.org/badge.svg)](https://www.elegantobjects.org)

# flake8-debug

> A simple flake8 plugin that forbids the usage of `print`, `breakpoint` and `pdb.set_trace` functions in production code.

## Tools

### Production
- python 3.7+
- [flake8](http://flake8.pycqa.org/en/latest/)

### Development

- [black](https://black.readthedocs.io/en/stable/)
- [flake8](http://flake8.pycqa.org/en/latest/)
- [pytest](https://docs.pytest.org/en/7.0.x/)

## Installation

### PYPI

```bash
pip install flake8-debug
✨ 🍰 ✨
```

### Source code

```bash
git clone git@github.com:vyahello/flake8-debug.git
cd flake8-debug
python3 -m venv venv 
. venv/bin/activate
pip install -e .
```

## Errors

### Codes

- `DB100` - print function is detected.
- `DB200` - breakpoint function is detected.
- `DB201` - breakpointhook function is detected.
- `DB300` - set_trace function is detected.

### Sample

```python
# foo.py
import pdb
from pdb import set_trace
from sys import breakpointhook


def bar(*a):
    print(a)
    breakpoint()
    breakpointhook()
    set_trace()
    pdb.set_trace()
```

```bash
flake8 foo.py

foo.py:7:5: DB100 print() function usage is detected
foo.py:8:5: DB200 breakpoint() function usage is detected
foo.py:9:5: DB201 breakpointhook() function usage is detected
foo.py:10:5: DB300 set_trace() function usage is detected
foo.py:11:5: DB300 set_trace() function usage is detected
```

**[⬆ back to top](#flake8-debug)**

## Development notes

### Testing 

Please run the following script to start plugin tests:
```bash
pytest 
```

### CI

To be able to run code analysis, please execute command below:
```bash
./analyse-source-code.sh
```

### Meta

Author – _Vladimir Yahello_.

Distributed under the `MIT` license. See [license](LICENSE.md) for more information.

You can reach out me at:
* [vyahello@gmail.com](vyahello@gmail.com)
* [https://twitter.com/vyahello](https://twitter.com/vyahello)
* [https://www.linkedin.com/in/volodymyr-yahello-821746127](https://www.linkedin.com/in/volodymyr-yahello-821746127)

### Contributing

I would highly appreciate any contribution and support. If you are interested to add your ideas into project please follow next simple steps:

1. Clone the repository
2. Configure `git` for the first time after cloning with your `name` and `email`
3. `pip install -r requirements.txt` to install all project dependencies
4. `pip install -r requirements-dev.txt` to install all development project dependencies
5. Create your feature branch (git checkout -b feature/fooBar)
6. Commit your changes (git commit -am 'Add some fooBar')
7. Push to the branch (git push origin feature/fooBar)
8. Create a new Pull Request

### What's next

All recent activities and ideas are described at project [issues](https://github.com/vyahello/flake8-debug/issues) page. 
If you have ideas you want to change/implement please do not hesitate and create an issue.

**[⬆ back to top](#flake8-debug)**
