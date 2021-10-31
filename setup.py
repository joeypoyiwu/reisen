# sets up the CLI

from setuptools import setup

setup(
    name='reisen',
    version='0.1.0',
    py_modules=['main'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'reisen = main:organizeFiles',
        ],
    },
)