# python-ivona-api
[![Build status](https://img.shields.io/travis/Pythonity/python-ivona-api.svg)][travis]
[![Test coverage](https://img.shields.io/coveralls/Pythonity/python-ivona-api.svg)][coveralls]
[![PyPI version](https://img.shields.io/pypi/v/ivona_api.svg)][pypi]
[![Python versions](https://img.shields.io/pypi/pyversions/ivona_api.svg)][pypi]
[![License](https://img.shields.io/github/license/Pythonity/python-ivona-api.svg)][license]

Python library that helps you connect to Amazon's [IVONA][ivona] Speech Cloud
from within your Python project. All you need to use it are the
[access keys][ivona keys].

It currently only implements `CreateSpeech` and `ListVoices` endpoints,
as they should cover the vast majority of use cases. Lexicons endpoints
may be added in the future.

If you're looking for out-of-the-box solution, you should probably use
[ivona-speak][ivona speak] - it's a script that uses this library and lets you
use its functionality directly from your shell.

## Installation
With PyPI:

```
$ pip install ivona_api
```

## API
There's no documentation as of now, but the code is commented and *should* be 
pretty straightforward to use.

That said - feel free to ask [me](mailto:pawel.adamczak@sidnet.info) if anything
is unclear.

## Tests
Package was tested with the help of `py.test` and `tox` on Python 2.7, 3.4, 3.5
and 3.6 (see `tox.ini`).

To run tests yourself you need to set environment variables with secret
and access keys before running `tox`:

Code coverage is available at [Coveralls][coveralls].

```shell
$ pip install -r requirements/dev.txt
$ export IVONA_ACCESS_KEY="YOUR_ACTUAL_ACCESS_KEY"
$ export IVONA_SECRET_KEY="YOUR_ACTUAL_SECRET_KEY"
$ tox
```

## Contributions
Package source code is available at [GitHub][github].

Feel free to use, ask, fork, star, report bugs, fix them, suggest enhancements,
add functionality and point out any mistakes. Thanks!

## Authors
Developed and maintained by [Pythonity][pythonity].

Written by [Paweł Adamczak][pawelad].


[coveralls]: https://coveralls.io/github/Pythonity/python-ivona-api
[github]: https://github.com/Pythonity/python-ivona-api
[ivona keys]: http://developer.ivona.com/en/speechcloud/introduction.html#Credentials
[ivona speak]: https://github.com/Pythonity/ivona-speak
[ivona]: https://www.ivona.com/
[license]: https://github.com/Pythonity/python-ivona-api/blob/master/LICENSE
[pawelad]: https://github.com/pawelad
[pypi]: https://pypi.python.org/pypi/ivona_api
[pythonity]: http://pythonity.com/
[travis]: https://travis-ci.org/Pythonity/python-ivona-api
