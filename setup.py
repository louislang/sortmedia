#!/usr/bin/env python

from os import path
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='sortmedia',
      version='1.2.1',
      description='Dedupe and sort photo and video files based on the date ' +
                  'they were created.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Louis Lang',
      author_email='louis@lang.sh',
      url='https://github.com/LouisLang/sortmedia',
      keywords='file-sorting media-manager photos videos',
      packages=['sortmedia'],
      entry_points={
        'console_scripts': [
            'sortmedia=sortmedia.cli:main',
        ],
      },
      install_requires=requirements,
     )
