#!/usr/bin/env python
from setuptools import setup

setup(
    name='license-info',
    version='0.8.1',
    description='Show list of installed python packages with version and license info',
    author='Michal Odnous',
    author_email='odi.root@gmail.com',
    url='https://github.com/odiroot/license-info',
    py_modules=["license_info"],
    install_requires=["pkgtools", "pip"],
    entry_points={
        'console_scripts': [
            'li = license_info:main',
        ],
    },
    license="Unlicensed (Public Domain)"
)
