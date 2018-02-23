#!/usr/bin/env python
from setuptools import setup, find_packages
from pip.req import parse_requirements


setup(
    name='fintech',
    version='0.0.1',
    packages=find_packages(exclude=('tests', '*.tests', '*.tests.*')),
    include_package_data=True,
    scripts=['manage.py'],
    install_requires=[str(ir.req) for ir in parse_requirements('requirements.txt', session='hack')],
)
