"""Packaging/Publishing script for the crabigator python library."""

# pylint: disable=no-name-in-module, import-error
# pylint: disable=too-many-public-methods, attribute-defined-outside-init

from __future__ import print_function
import base64
import datetime
import json
import os
import re
import setuptools
import shlex
import subprocess
import sys


try:
    import ConfigParser as configparser
except ImportError:
    import configparser

try:
    import urllib2 as url
except ImportError:
    import urllib.request as url


def call(command):
    """Simple wrapper for running shell commands and getting the output"""
    return subprocess.check_output(shlex.split(command)).decode("utf-8")

# Get the latest version by looking at the highest-numbered git tag matching
# the version format exactly.
VER = sorted(
    [tuple([int(y) for y in x.split('.')])
     for x in call('git tag').splitlines()
     if re.match(r'^\d+\.\d+\.\d+', x)]
    )[-1]


class Publish(setuptools.Command):
    """A setup.py command that can be used to publish to pypi.python.org."""

    description = ('Bump the version number (major, minor, or micro) ' +
                   'and publish to pypi.')
    user_options = [('bump=', None, 'Which version to bump.'),
                    ('github-user=', None, 'The github username.'),
                    ('github-token=', None, 'The github auth token.'),
                    ('github-slug=', None, 'The github repo slug.'),
                    ('pypi-user=', None, 'The pypi username.'),
                    ('pypi-pass=', None, 'The pypi password.')]

    def initialize_options(self):
        self.bump = None
        self.github_user = None
        self.github_token = None
        self.github_slug = None
        self.pypi_user = None
        self.pypi_pass = None

    def finalize_options(self):
        assert (self.bump == 'major' or
                self.bump == 'minor' or
                self.bump == 'micro')
        assert self.github_user is not None
        assert self.github_token is not None
        assert self.github_slug is not None
        assert self.pypi_user is not None
        assert self.pypi_pass is not None

    def run(self):
        # Determine the next version.
        if self.bump == 'major':
            new = '{0}.{1}.{2}'.format(VER[0] + 1, 0, 0)
        elif self.bump == 'minor':
            new = '{0}.{1}.{2}'.format(VER[0], VER[1] + 1, 0)
        elif self.bump == 'micro':
            new = '{0}.{1}.{2}'.format(VER[0], VER[1], VER[2] + 1)
        else:
            raise Exception('bump must be major, minor, or micro')

        # Assemble the API request for creating a new tag on GitHub.
        user = self.github_user.encode('utf-8')
        token = self.github_token.encode('utf-8')
        encode = base64.b64encode(user + b':' + token)
        call('git pull')
        sha = call('git rev-parse HEAD').strip()
        name = call('git log --format="%an" -n 1 {0}'.format(sha)).strip()
        email = call('git log --format="%ae" -n 1 {0}'.format(sha)).strip()
        tagdata = {'tag': new,
                   'message': 'Publishing version ' + new,
                   'object': sha,
                   'type': 'commit',
                   'tagger': {
                       'name': name,
                       'email': email,
                       'date': datetime.datetime.utcnow().isoformat() + 'Z'}}

        # Create the tag object.
        request = url.Request("https://api.github.com/repos/{0}/git/tags"
                              .format(self.github_slug))
        request.add_header("Authorization", b'Basic ' + encode)
        request.add_header("Content-Type", "application/json")
        response = url.urlopen(request, json.dumps(tagdata).encode('utf-8'))
        print(response)

        # Create the tag reference.
        refdata = {'ref': 'refs/tags/' + new, 'sha': sha}
        request = url.Request("https://api.github.com/repos/{0}/git/refs"
                              .format(self.github_slug))
        request.add_header("Authorization", b'Basic ' + encode)
        request.add_header("Content-Type", "application/json")
        response = url.urlopen(request, json.dumps(refdata).encode('utf-8'))

        call('git pull')
        call('python setup.py sdist')
        call('python setup.py bdist_wheel')
        if not os.path.exists(os.path.expanduser('~/.pypirc')):
            config = configparser.RawConfigParser()
            config.add_section('distutils')
            config.set('distutils', 'index-servers', 'pypi')
            config.add_section('pypi')
            config.set('pypi', 'repository', 'https://pypi.python.org/pypi')
            config.set('pypi', 'username', self.pypi_user)
            config.set('pypi', 'password', self.pypi_pass)
            with open(os.path.expanduser('~/.pypirc'), 'w') as pypirc_file:
                config.write(pypirc_file)
        call('twine upload dist/*')


class Test(setuptools.Command):
    """A setup.py command that can be used to run unit tests."""

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
                 version='{0}.{1}.{2}'.format(VER[0], VER[1], VER[2]),
                 packages=['crabigator', 'crabigator.tests'],
                 classifiers=[
                     'Development Status :: 3 - Alpha',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Natural Language :: English',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3.4'
                 ],
                 cmdclass={'test': Test, 'publish': Publish})
