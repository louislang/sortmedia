#!/usr/bin/env python

from setuptools import setup

setup(name='sortmedia',
      version='1.0',
      description='Dedupe and sort photo and video files based on the date ' +
                  'they were created.',
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
     )
