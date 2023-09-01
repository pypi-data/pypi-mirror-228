"""
This file is used to build your package. It is used by the command
`python setup.py install` or `python setup.py develop`.
"""

from setuptools import setup, find_packages


setup(
    name='hexarchsetup',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        # Your dependencies here
    ],
    package_data={
        'src': ['templates/*.json'],
    },
    entry_points={
        'console_scripts': [
            # This allows you to run your main function from the command line.
            'hexsetup=src.main:main',
        ],
    },
    author='Éric Dominguez Morales',
    author_email='ericdominguezm@gmail.com',
    description='Automatically generate a hexagonal architecture project structure in Python. \
        Easily customizable to include user-defined modules.',
)
