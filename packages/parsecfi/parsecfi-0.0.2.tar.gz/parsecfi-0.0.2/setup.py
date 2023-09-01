from setuptools import setup, find_packages

setup(
    name='parsecfi',
    version='0.0.2',
    description='Python SDK for the Parsec API',
    author='PARSEC FINANCE INC.',
    packages=['parsecfi'],
    license='MIT',
    install_requires=[
        'requests',
        'pandas'
    ]
)