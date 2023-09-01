#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="habib ezatabadi",
    author_email='habibezati88@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Using Direct Method for estimate effect of covariates in Cumulative Incidnece Function",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pysurv_cmp1',
    name='pysurv_cmp1',
    packages=find_packages(include=['pysurv_cmp1', 'pysurv_cmp1.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/stats9/pysurv_cmp1',
    version='0.1.1',
    zip_safe=False,
)
