# python-ivona-api
Python (3) library that helps you connect to Amazon's [IVONA][ivona]
Speech Cloud from within your Python project. You need its
[access keys][ivona keys] to use it.

It currently only implements `CreateSpeech` and `ListVoices` endpoints,
as they should cover the vast majority of use cases. Lexicons endpoints
may be added in the future.

If you're looking for out-of-the-box solution, have a look at 
[ivona-speak][ivona speak github] - it's a script that uses this very
library and lets you use its functionality directly from your shell.

Packages required for running and testing are listed in `requirements`
directory.

## Installation
With `pip`:
```
$ pip3 install ivona_api
```

## API
There's no documentation as of now, but the code is commented and
*should* be pretty straightforward to use.

But feel free to ask [me](mailto:pawel.adamczak@sidnet.info) if anything
is unclear.

## Tests
Package was tested with `pytest` and `tox` on Python 3.4
(see `tox.ini`).

To run tests yourself you need to set environment variables with secret
and access keys before running `tox` inside the repository:
```
export IVONA_ACCESS_KEY="YOUR_ACTUAL_ACCESS_KEY"
export IVONA_SECRET_KEY="YOUR_ACTUAL_SECRET_KEY"
```

## Contributions
Package source code is available at [GitHub][ivona api github].

Feel free to use, ask, fork, star, report bugs, fix them, suggest 
enhancements and point out any mistakes.

## Authors
Developed and maintained by [Pythonity][pythonity].

Written by [Paweł Adamczak][pawelad].

[ivona]: https://www.ivona.com/
[ivona keys]: http://developer.ivona.com/en/speechcloud/introduction.html#Credentials
[ivona speak github]: https://github.com/Pythonity/ivona-speak
[ivona api github]: https://github.com/Pythonity/python-ivona-api
[pythonity]: http://pythonity.com/
[pawelad]: https://github.com/pawelad