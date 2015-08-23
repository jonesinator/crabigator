from setuptools import setup, Command
import subprocess
import sys

class TestCommand(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        raise SystemExit(subprocess.call(
            [sys.executable, '-Wd', 'crabigator/tests/__init__.py']))

setup(name='crabigator',
      description='Python Library for WaniKani',
      long_description=open('README.md').read(),
      url='http://github.com/jonesinator/crabigator/',
      author='Aaron Jones',
      author_email='aaron@jonesinator.com',
      license='MIT',
      version='0.1.3',
      packages=['crabigator', 'crabigator.tests'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.0',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5'
      ], **dict(cmdclass=dict(test=TestCommand)))
