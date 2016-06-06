# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

# Convert description from markdown to reStructuredText
try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    description = ''


setup(
    name='ivona_api',
    url='https://github.com/Pythonity/python-ivona-api',
    download_url='https://github.com/Pythonity/python-ivona-api/releases/latest',
    bugtrack_url='https://github.com/Pythonity/python-ivona-api/issues',
    version='0.1.1',
    license='MIT License',
    author='Pythonity',
    author_email='pythonity@pythonity.com',
    maintainer='Paweł Adamczak',
    maintainer_email='pawel.adamczak@sidnet.info',
    description="Python library that helps you connect to Amazon's IVONA "
                "Speech Cloud from within your Python project.",
    long_description=description,
    packages=find_packages(),
    include_package_data=True,
    tests_require=['tox'],
    cmdclass={'test': Tox},
    install_requires=[
        'requests>=2.10.0',
        'requests-aws4auth>=0.9',
    ],
    extras_require={
        'testing': ['pytest', 'flaky'],
    },
    keywords='amazon ivona api text to speech',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
