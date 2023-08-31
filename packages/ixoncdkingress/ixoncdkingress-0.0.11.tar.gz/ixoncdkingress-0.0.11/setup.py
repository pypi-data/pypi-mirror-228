#!/usr/bin/env python
from setuptools import find_packages, setup

development_requires = [
    'bandit==1.7.4',
    'dominate==2.7.0',
    'ixtest==0.0.20',
    'mock==4.0.3',
    'mypy==0.971',
    'pyfakefs==4.6.3',
    'pylint==2.15.0',
    'pytest==7.1.2',
    'pytest-cov==3.0.0',
    'pytest-integration==0.2.2',
    'pytest-mock==3.8.2',
    'types-requests>=2.28.11.5',
    'wouter==0.0.3',
]

setup(
    name='ixoncdkingress',
    version='0.0.11',
    description='IXON CDK Ingress used in Custom Backend Components(CBC) for the IXON Cloud',
    author='IXON',
    author_email='development@ixon.cloud',
    url='https://www.ixon.cloud/',
    packages=find_packages(exclude=['tests*', ]),
    package_data={
        '': ['py.typed', 'assets/*'],
    },
    python_requires='>=3.9',
    install_requires=[
        'cryptography~=38.0.3',
        'docker>=6.1.3',
        'pymongo>=4.4.0',
        'requests>=2.28.1',
    ],
    extras_require={
        'development': development_requires,
    },
)
