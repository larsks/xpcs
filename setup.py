from setuptools import setup, find_packages

with open('requirements.txt') as fd:
    requires = fd.readlines()

with open('requirements.txt') as fd:
    setup(name='xpcs',
          version='0.1',
          packages=find_packages(),
          install_requires=requires,
          entry_points={
              'console_scripts': [
                  'xpcs = xpcs.main:cli',
              ],
          }
          )
