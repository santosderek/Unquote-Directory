from setuptools import setup, find_packages

setup(name='Unquote Directory',
      version='0.1',
      description='Unquote a directory of filenames with url encoding.',
      author='Derek Santos',
      license='The MIT License (MIT)',
      url='https://github.com/santosderek/Unquote-Directory',
      packages=['unquote-directory'],
      scripts=['unquote-directory/main.py'],
      entry_points={
          'console_scripts':
              ['unquote = unquote-directory.main:main']
      }
      )
