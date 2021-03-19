# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in totall/__init__.py
from totall import __version__ as version

setup(
	name='totall',
	version=version,
	description='d',
	author='d',
	author_email='d',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
