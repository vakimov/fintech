#!/usr/bin/env python
from setuptools import setup, find_packages
from pip.req import parse_requirements


setup(
    name='fintech',
    version='0.1',
    # packages=['fintech'],
    packages=find_packages(exclude=('tests', '*.tests', '*.tests.*')),
    include_package_data=True,
    # exclude_package_data={'fintech': ['*.pyc']},
    scripts=['manage.py'],
    package_data={
        '': ['templates/*', ],
    },
    install_requires=[str(ir.req) for ir in parse_requirements('requirements.txt', session='hack')],
)
