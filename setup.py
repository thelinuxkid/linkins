#!/usr/bin/python
from setuptools import setup, find_packages

EXTRAS_REQUIRES = dict(
    test=[
        'pytest>=2.2.4',
        'mock>=0.8.0',
        'tempdirs>=0.0.1',
        ],
    dev=[
        'ipython>=0.13',
        ],
    )

# Tests always depend on all other requirements, except dev
for k,v in EXTRAS_REQUIRES.iteritems():
    if k == 'test' or k == 'dev':
        continue
    EXTRAS_REQUIRES['test'] += v

setup(
    name='linkins',
    version='0.0.1',
    description='linkins -- Safely link directory structures',
    long_description=(
        "linkins is a command line tool which allows users to link a "
        "directory structure. It provides the ability to execute "
        "user-defined scripts at each level of the directory hierarchy "
        "and a safe way to backup existing files or directories."
        ),
    license='GPL',
    author='Andres Buritica',
    author_email='andres@thelinuxkid.com',
    maintainer='Andres Buritica',
    maintainer_email='andres@thelinuxkid.com',
    url='https://github.com/andresburitica/linkins',
    packages = find_packages(),
    test_suite='nose.collector',
    install_requires=[
        'setuptools',
        ],
    extras_require=EXTRAS_REQUIRES,
    entry_points={
        'console_scripts': [
            'linkins = linkins.cli:main',
            ],
        },
    )
