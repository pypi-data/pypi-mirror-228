# Your python setup file. An example can be found at:
# https://github.com/pypa/sampleproject/blob/master/setup.py
from setuptools import setup

setup(name='graphframes_latest',
      version='0.8.3',
      description='GraphFrames: DataFrame-based Graphs',
      license='MIT',
      url='https://github.com/graphframes/graphframes',
      packages=['graphframes', 'graphframes.lib', 'graphframes.examples'],
      install_requires=[
          'nose==1.3.7',
          'numpy>=1.7'
		],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
		],
 )
