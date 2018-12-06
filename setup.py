# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Genetic-Cars',
    version='0.0.1',
    description='ALHE project',
    long_description=readme,
    author='Daniel Bigos',
    author_email='D.Bigos@stud.elka.pw.edu.pl',
    url='https://github.com/pik694/genetic-cars',
    license=license,
    packages=find_packages(exclude='tests')
)
