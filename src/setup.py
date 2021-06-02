#!/usr/bin/env python

from distutils.core import setup

setup(
      name='TrainManagement',
      version='1.0',
      description='TrainManagement software',
      author='Pierre Contri',
      author_email='pierre.contri@free.fr',
      url='https://github.com/pierrecontri/TrainManagement',
      packages=['Controller', 'ElectronicComponents', 'ElectronicController', 'ElectronicModel', 'Model', 'TrainIO'],
)
