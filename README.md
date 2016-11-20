# python-ivona-api
[![Build Status](https://img.shields.io/travis/Pythonity/python-ivona-api.svg)][travis]
[![PyPI Version](https://img.shields.io/pypi/v/ivona_api.svg)][pypi]
[![Python Versions](https://img.shields.io/pypi/pyversions/ivona_api.svg)][pypi]
[![License](https://img.shields.io/github/license/Pythonity/python-ivona-api.svg)][license]

Python library that helps you connect to Amazon's [IVONA][ivona] Speech Cloud
from within your Python project. All you need to use it are the
[access keys][ivona keys].

It currently only implements `CreateSpeech` and `ListVoices` endpoints,
as they should cover the vast majority of use cases. Lexicons endpoints
may be added in the future.

If you're looking for out-of-the-box solution, have a look at 
[ivona-speak][ivona speak] - it's a script that uses this very
library and lets you use its functionality directly from your shell.

## Installation
With PyPI:
```
$ pip install ivona_api
```

## API
There's no documentation as of now, but the code is commented and
*should* be pretty straightforward to use.

But feel free to ask [me](mailto:pawel.adamczak@sidnet.info) if anything
is unclear.

## Tests
Package was tested with the help of `py.test` and `tox` on Python 2.7, 3.4
and 3.5 (see `tox.ini`).

To run tests yourself you need to set environment variables with secret
and access keys before running `tox`:
```shell
$ export IVONA_ACCESS_KEY="YOUR_ACTUAL_ACCESS_KEY"
$ export IVONA_SECRET_KEY="YOUR_ACTUAL_SECRET_KEY"
$ tox
```

## Contributions
Package source code is available at [GitHub][github].

Feel free to use, ask, fork, star, report bugs, fix them, suggest enhancements,
add functionality and point out any mistakes.

## Authors
Developed and maintained by [Pythonity][pythonity].

Written by [Paweł Adamczak][pawelad].


[github]: https://github.com/Pythonity/python-ivona-api
[ivona keys]: http://developer.ivona.com/en/speechcloud/introduction.html#Credentials
[ivona speak]: https://github.com/Pythonity/ivona-speak
[ivona]: https://www.ivona.com/
[license]: https://github.com/Pythonity/python-ivona-api/blob/master/LICENSE
[pawelad]: https://github.com/pawelad
[pythonity]: http://pythonity.com/
[travis]: https://travis-ci.org/Pythonity/python-ivona-api
[pypi]: https://pypi.python.org/pypi/ivona_api
