# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='vSporn-Python',
    version='1.0.0',
    description='Package to visualize football results in flask',
    long_description=readme,
    author='Martin Stan',
    author_email='martin.stan@gmx.de',
    url='https://github.com/stanman71/Python_Projects/Football',
    license=license,
    packages=find_packages(exclude=('CSV', 'templates'))
)
