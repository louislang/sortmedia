#!/usr/bin/env python

from setuptools import setup

setup(name='mediasort',
      version='1.0',
      description='Dedupe and sort photo and video files based on the date ' +
                  'they were created.',
      author='Louis Lang',
      author_email='louis@lang.sh',
      url='https://github.com/LouisLang/mediasort',
      keywords='file-sorting media-manager photos videos',
      packages=['mediasort'],
      entry_points={
        'console_scripts': [
            'mediasort=mediasort.cli:main',
        ],
      },
     )
