#from distutils.core import setup
from setuptools import setup
from ibapi import get_version_string

import sys

if sys.version_info < (3,1):
    sys.exit("Only Python 3.1 and greater is supported")

setup(
    name='dolos',
    version=get_version_string(),
    packages=['ibapi'],
    url='',
    license='',
    author='',
    author_email='',
    description='Python IB API'
)
