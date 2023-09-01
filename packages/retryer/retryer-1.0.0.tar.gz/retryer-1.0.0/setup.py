from setuptools import setup

setup(
    name='retryer',
    version='1.0.0',
    description='A retry decorator for error handling',
    author='Vishwanath Kannan',
    packages=['retryer'],
    install_requires=[
        'time',
        'functools'
    ],
)