[![PyPI version](https://badge.fury.io/py/import-wrappers.svg)](https://badge.fury.io/py/import-wrappers)
![PyPI pyversions](https://img.shields.io/pypi/pyversions/import-wrappers.svg)
[![Coverage Status](https://coveralls.io/repos/github/eyadgaran/import-wrappers/badge.svg)](https://coveralls.io/github/eyadgaran/import-wrappers)
![Build Status](https://github.com/eyadgaran/import-wrappers/actions/workflows/test.yml/badge.svg?branch=main)

# Import Wrappers
A simple set of utilities to make working with various import patterns easy.


# Installation
```pip install import-wrappers```

# Optional Dependencies
The original motivation for this library was the repetitive utilities I found myself authoring to
hack around supporting optional dependencies in other projects. Optional dependencies are a common
pattern where the core of a library does not depend on a dependency but some functionality may
require it. Most users may never interact with the code that requires the optional dependency but
without proper handling will still be required to install them and by extension inherit the overhead
of managing dependency versions and conflicts.

# Usage
### Wrapping Optional Dependencies

Typical import pattern - this fails on import whether or not the dependency is used
```python
from optional_dependency import SomeUnusedClass


def some_function_that_isnt_needed(*args, **kwargs):
    return SomeUnusedClass().some_method(*args, **kwargs)
```

Same functionality using import wrappers - only raise an error on USE, not import
```python
from import_wrappers.optional_dependencies import OptionalDependencyWrapper

SomeUnusedClass = OptionalDependencyWrapper('optional_dependency', 'SomeUnusedClass')

def some_function_that_isnt_needed(*args, **kwargs):
    return SomeUnusedClass().some_method(*args, **kwargs)
```
