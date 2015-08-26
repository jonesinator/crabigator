"""Packaging/Publishing script for the crabigator python library."""

import base64
import datetime
import json
import re
import setuptools
import shlex
import subprocess
import sys

try:
    import urllib.request as url
except ImportError:
    import urllib2 as url


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


# setuptools.Command exposes too many public methods. Disable the pylint
# warning for it.
# pylint: disable=too-many-public-methods, attribute-defined-outside-init
class Publish(setuptools.Command):
    """A setup.py command that can be used to publish to pypi.python.org."""

    description = ('Bump the version number (major, minor, or micro) ' +
                   'and publish to pypi.')
    user_options = [('bump=', None, 'Which version to bump.'),
                    ('github-user=', None, 'The github username.'),
                    ('github-token=', None, 'The github auth token.'),
                    ('github-slug=', None, 'The github repo slug.'),
                    ('pypi-user=', None, 'The pypi username.'),
                    ('pypi-pass=', None, 'The pypi password.'),
                    ('pypi-repo=', None, 'The pypi repository.')]

    def initialize_options(self):
        self.bump = None
        self.github_user = None
        self.github_token = None
        self.github_slug = None
        self.pypi_user = None
        self.pypi_pass = None
        self.pypi_repo = None

    def finalize_options(self):
        assert (self.bump == 'major' or
                self.bump == 'minor' or
                self.bump == 'micro')
        assert self.github_user is not None
        assert self.github_token is not None
        assert self.github_slug is not None
        assert self.pypi_user is not None
        assert self.pypi_pass is not None
        assert self.pypi_repo is not None

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
        encode = base64.b64encode(self.github_user + b':' + self.github_token)
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
        response = url.urlopen(request, json.dumps(tagdata))

        # Create the tag reference.
        refdata = {'ref': 'refs/tags/' + new, 'sha' : sha}
        request = url.Request("https://api.github.com/repos/{0}/git/refs"
                              .format(self.github_slug))
        request.add_header("Authorization", b'Basic ' + encode)
        request.add_header("Content-Type", "application/json")
        response = url.urlopen(request, json.dumps(refdata))

        call('git pull')
        call('python setup.py sdist')
        call('python setup.py bdist_wheel')
        call('twine -r {0} -u {1} -p {2} upload dist/*'.format(
            self.pypi_repo, self.pypi_user, self.pypi_pass))


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
