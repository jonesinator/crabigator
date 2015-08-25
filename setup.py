import re
import setuptools
import shlex
import subprocess
import sys

def call(command):
    return subprocess.check_output(shlex.split(command))

# Get the latest version by looking at the highest-numbered git tag matching
# the version format exactly.
ver = list(sorted(
    [tuple(map(int, x.split('.'))) for x in call('git tag').splitlines()
    if re.match('^\d+\.\d+\.\d+$', x)])[-1])

class Publish(setuptools.Command):
    description = ('Bump the version number (major, minor, or micro) ' +
                   'and publish to pypi.')
    user_options = [('bump=', 'b',
                     'Which version to bump when publishing. ' +
                     'Major, minor, or micro.')]

    def initialize_options(self):
        self.bump = 'micro'

    def finalize_options(self):
        assert (self.bump == 'major' or
                self.bump == 'minor' or
                self.bump == 'micro')

    def run(self):
        # Determine the next version.
        if self.bump == 'major':
            new = '{0}.{1}.{2}'.format(ver[0] + 1, ver[1], ver[2])
        elif self.bump == 'minor':
            new = '{0}.{1}.{2}'.format(ver[0], ver[1] + 1, ver[2])
        elif self.bump == 'micro':
            new = '{0}.{1}.{2}'.format(ver[0], ver[1], ver[2] + 1)
        else:
            raise Exception("bump must be major, minor, or micro")

        # Create and publish the new distribution with the new version.
        call('git tag -a {new} -m "Publish version {new}"'.format(new=new))
        call('python setup.py sdist')
        call('python setup.py bdist_wheel')
        call('twine upload dist/*')
        call('git push origin {new}'.format(new=new))

class Test(setuptools.Command):
    description = 'Run all unit tests for the crabigator module.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        raise SystemExit(subprocess.call(
            [sys.executable, '-Wd', 'crabigator/tests/__init__.py']))

setuptools.setup(name='crabigator',
                 description='Python Library for WaniKani',
                 long_description=open('README.md').read(),
                 url='http://github.com/jonesinator/crabigator/',
                 author='Aaron Jones',
                 author_email='aaron@jonesinator.com',
                 license='MIT',
                 version='{0}.{1}.{2}'.format(ver[0], ver[1], ver[2]),
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
                 ],
                 **dict(cmdclass={'test':Test,'publish':Publish}))
