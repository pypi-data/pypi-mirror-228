from setuptools import setup, find_packages

setup(
    name='parsecfi',
    version='0.0.1',
    description='Python SDK for the Parsec API',
    author='PARSEC FINANCE INC.',
    packages=find_packages(),
    license='MIT',
    install_requires=[
        'requests',
        'pandas'
    ]
)