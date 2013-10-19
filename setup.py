#!/usr/bin/env python
from distutils.core import setup

setup(
    name='license-info',
    version='0.0.1',
    description='Show list of installed python packages with version and license info',
    author='Michal Odnous',
    author_email='odi.root@gmail.com',
    url='https://github.com/odiroot/license-info',
    py_modules = ["license_info"],
    entry_points={
        'console_scripts': [
            'li = license_info:main',
        ],
    },
)
