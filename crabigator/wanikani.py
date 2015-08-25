"""A very thin Python wrapper over the WaniKani API.

The aim of this module is to model the API as closely as possible while
ensuring the correct Python type is used for each field in the API. The syntax
for using the library has been made as simple as possible.

Usage
-----
1. Import the WaniKani class. `from crabigator.wanikani import WaniKani`

2. Instantiate a WaniKani instance with your API key.
   `wanikani = WaniKani('my_api_key')`

3. Get any endpoint specified by the API docs (dashes replaced with
   underscores).
  * wanikani.user_information
  * wanikani.study_queue
  * wanikani.level_progression
  * wanikani.srs_distribution
  * wanikani.recent_unlocks
  * wanikani.critical_items
  * wanikani.radicals
  * wanikani.kanji
  * wanikani.vocabulary

4. From any of the above endpoints in #3 the output fields in the
   required-information key can be retrieved. For example:
  * print(wanikani.user_information.username)
  * print(wanikani.study_queue.next_review_date)
  * print(wanikani.level_progression.kanji_total)
  * print(wanikani.srs_distribution.master.total)
  * print(wanikani.recent_unlocks[0])
  * print(wanikani.critical_items[0])
  * print(wanikani.radicals[0])
  * print(wanikani.kanji[0])
  * print(wanikani.vocabulary[0])

5. If you need to pass arguments to the API then the following functions will
   do that.
  * wanikani.get_recent_unlocks(limit=10)
  * wanikani.get_critical_items(percent=75)
  * wanikani.get_radicals(levels=[2, 3, 4])
  * wanikani.get_kanji(levels=[5, 6, 7])
  * wanikani.get_vocabulary(levels=[8, 9, 10])

Notes
-----
* Everything is a property of a Python object.
* All API responses can be easily printed for debugging.
* All dates in API responses are converted to datetime objects.
* All comma-separated lists in API responses are converted to arrays of strings
  for easier iteration over multiple readings and meanings.

"""

from __future__ import print_function
from datetime import datetime
from json import loads
try:
    # pylint: disable=no-name-in-module, import-error
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

__all__ = ['WaniKani']

API_VERSION = '1.4'
URL_FORMAT = 'https://www.wanikani.com/api/v{vers}/user/{key}/{res}/{args}'


class WaniKani(object):
    """Main class for interacting with the WaniKani API.

    Each API endpoint has a property of the same name (with dashes replaced by
    underscores), and also a get_<endpoint> method which takes an optional
    argument specified by the API documentation.
    """

    def __init__(self, api_key, url_format=URL_FORMAT):
        (self.url_format, self.api_key) = (url_format, api_key)

    def get_user_information(self):
        """Retrieves the information in the user-information API endpoint."""
        return self._get('user-information', 'user_information', USER_INFO)
    user_information = property(get_user_information)

    def get_study_queue(self):
        """Retrieves the information in the study-queue API endpoint."""
        return self._get('study-queue', 'requested_information', STUDY_QUEUE)
    study_queue = property(get_study_queue)

    def get_level_progression(self):
        """Retrieves the information in the level-progression API endpoint."""
        return self._get('level-progression',
                         'requested_information',
                         LEVEL_PROG)
    level_progression = property(get_level_progression)

    def get_srs_distribution(self):
        """Retrieves the information in the srs-distribution API endpoint."""
        return self._get('srs-distribution',
                         'requested_information',
                         SRS_DISTS)
    srs_distribution = property(get_srs_distribution)

    def get_recent_unlocks(self, limit=None):
        """Retrieves the information in the recent-unlocks API endpoint."""
        return self._get_meta_items('recent-unlocks', limit)
    recent_unlocks = property(get_recent_unlocks)

    def get_critical_items(self, percent=None):
        """Retrieves the information in the critical-items API endpoint."""
        return self._get_meta_items('critical-items', percent)
    critical_items = property(get_critical_items)

    def get_radicals(self, levels=None):
        """Retrieves the information in the radicals API endpoint."""
        return self._get_items(levels, 'radicals', RADICAL)
    radicals = property(get_radicals)

    def get_kanji(self, levels=None):
        """Retrieves the information in the kanji API endpoint."""
        return self._get_items(levels, 'kanji', KANJI)
    kanji = property(get_kanji)

    def get_vocabulary(self, levels=None):
        """Retrieves the information in the vocabulary API endpoint."""
        return self._get_items(levels, 'vocabulary', VOCABULARY)
    vocabulary = property(get_vocabulary)

    def _get(self, resource, key, fields):
        """Gets an ApiObj representing some object returned by the API."""
        return ApiObj(self._raw_request(resource)[key], fields)

    def _get_items(self, levels, resource, fields):
        """Gets an array of ApiObj representing radicals, kanji, or
        vocabulary.
        """
        arg = ','.join([str(x) for x in levels]) if levels is not None else ''
        response = self._raw_request(resource=resource, argument=arg)
        response = (response['requested_information']['general']
                    if 'general' in response['requested_information']
                    else response['requested_information'])
        item_list = []
        for item in response:
            item_list.append(ApiObj(item, fields))
        return item_list

    def _get_meta_items(self, resource, argument):
        """Gets an array of ApiObj representing radicals, kanji, and/or
        vocabulary.
        """
        argument = str(argument) if argument is not None else ''
        response = self._raw_request(resource, argument=argument)
        item_list = []
        for item in response['requested_information']:
            tmap = {'radical': RADICAL, 'kanji': KANJI,
                    'vocabulary': VOCABULARY}
            item_list.append(ApiObj(item, tmap[item['type']]))
        return item_list

    def _raw_request(self, resource, argument='', version=API_VERSION):
        """Issue an HTTP GET request to the API and return the response."""
        url = self.url_format.format(vers=version, key=self.api_key,
                                     res=resource, args=argument)
        rsp = loads(urlopen(url).read().decode('utf-8'))
        if 'error' in rsp:
            code = rsp['error']['code'] if 'code' in rsp['error'] else None
            msg = rsp['error']['message'] if 'message' in rsp['error'] else None
            raise ApiError(code, msg)
        return rsp


class ApiError(Exception):
    """Errors returned by the WaniKani API itself.

    Contains all of the information in the "error" field returned by the API.
    """

    def __init__(self, code, msg):
        super(ApiError, self).__init__('{c} - {m}'.format(c=code, m=msg))
        (self.code, self.message) = (code, msg)

# Disable the too few public methods warning from pylint. Pylint may have a
# point, but ignore it on purpose...
# pylint: disable=too-few-public-methods
class ApiObj(object):
    """Generic object representing anything returned by the WaniKani API.

    This really just acts like a dict, but has a little nicer syntax. The
    fields are specified by the constants below. Each field has a name and a
    function used to retrieve the name from a provided JSON object.
    """

    def __init__(self, info, fields):
        for field, fun in fields:
            if info is not None and field in info and info[field] is not None:
                setattr(self, field, fun(info[field]))
            else:
                setattr(self, field, None)

    def __repr__(self):
        return str(self.__dict__)

USER_INFO = [('username', lambda x: x),
             ('gravatar', lambda x: x),
             ('level', lambda x: x),
             ('title', lambda x: x),
             ('about', lambda x: x),
             ('twitter', lambda x: x),
             ('topics_count', lambda x: x),
             ('posts_count', lambda x: x),
             ('creation_date', datetime.utcfromtimestamp),
             ('vacation_date', datetime.utcfromtimestamp)]
STUDY_QUEUE = [('lessons_available', lambda x: x),
               ('reviews_available', lambda x: x),
               ('reviews_available_next_hour', lambda x: x),
               ('reviews_available_next_day', lambda x: x),
               ('next_review_date', datetime.utcfromtimestamp)]
LEVEL_PROG = [('radicals_progress', lambda x: x),
              ('radicals_total', lambda x: x),
              ('kanji_progress', lambda x: x),
              ('kanji_total', lambda x: x)]
SRS_DIST = [('radicals', lambda x: x),
            ('kanji', lambda x: x),
            ('vocabulary', lambda x: x),
            ('total', lambda x: x)]
SRS_DISTS = [('apprentice', lambda x: ApiObj(x, SRS_DIST)),
             ('guru', lambda x: ApiObj(x, SRS_DIST)),
             ('master', lambda x: ApiObj(x, SRS_DIST)),
             ('enlighten', lambda x: ApiObj(x, SRS_DIST)),
             ('burned', lambda x: ApiObj(x, SRS_DIST))]
USER_SPEC = [('srs', lambda x: x),
             ('srs_numeric', lambda x: x),
             ('unlocked_date', datetime.utcfromtimestamp),
             ('available_date', datetime.utcfromtimestamp),
             ('burned', lambda x: x),
             ('burned_date', datetime.utcfromtimestamp),
             ('meaning_correct', lambda x: x),
             ('meaning_incorrect', lambda x: x),
             ('meaning_max_streak', lambda x: x),
             ('meaning_current_streak', lambda x: x),
             ('reading_correct', lambda x: x),
             ('reading_incorrect', lambda x: x),
             ('reading_max_streak', lambda x: x),
             ('reading_current_streak', lambda x: x),
             ('meaning_note', lambda x: x),
             ('user_synonyms', lambda x: x),
             ('reading_note', lambda x: x)]
RADICAL = [('character', lambda x: x),
           ('meaning', lambda x: x.split(', ')),
           ('image', lambda x: x),
           ('level', lambda x: x),
           ('user_specific', lambda x: ApiObj(x, USER_SPEC))]
KANJI = [('character', lambda x: x),
         ('meaning', lambda x: x.split(', ')),
         ('onyomi', lambda x: x.split(', ')),
         ('kunyomi', lambda x: x.split(', ')),
         ('nanori', lambda x: x.split(', ')),
         ('important_reading', lambda x: x),
         ('level', lambda x: x),
         ('user_specific', lambda x: ApiObj(x, USER_SPEC))]
VOCABULARY = [('character', lambda x: x),
              ('kana', lambda x: x.split(', ')),
              ('meaning', lambda x: x.split(', ')),
              ('level', lambda x: x),
              ('user_specific', lambda x: ApiObj(x, USER_SPEC))]
