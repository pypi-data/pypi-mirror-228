from setuptools import setup
try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()
setup(
    name='retryer',
    version='1.0.1',
    description='A retry decorator for error handling',
    author='Vishwanath Kannan',
    packages=['retryer'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'time',
        'functools'
    ],
)