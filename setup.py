#!/usr/bin/env python
from setuptools import setup

setup(
    name='license-info',
    version='0.8.6',
    description='Show list of installed python packages with version and license info',
    author='Michal Odnous',
    author_email='odi.root@gmail.com',
    url='https://github.com/odiroot/license-info',
    py_modules=["license_info"],
    install_requires=["pkgtools", "pip"],
    extras_require={
        "colors": ["termcolor"],
    },
    entry_points={
        'console_scripts': [
            'li = license_info:main',
        ],
    },
    license="BSD",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    tests_require=['mock', 'termcolor'],
    test_suite='tests',
)
