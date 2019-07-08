#!/usr/bin/env python

from setuptools import setup, find_packages


setup(name='gflask',
      version='0.1.0',
      description='simple way to run flask app in gunicorn server',
      author='Mario Wang',
      author_email='xp.wang@bigsec.com',
      url='https://www.bigsec.com',
      packages=find_packages(exclude=["test",'*.pyc']),
      install_requires=[
          'gunicorn', 'flask', 'gevent'
      ],
      extras_require = {
          'protobuf':  ["google-apputils"]
      },
      )
