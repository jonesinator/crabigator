from datetime import datetime
from json import loads
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

__all__ = ['WaniKani']

API_VERSION = '1.4'
URL_FORMAT = 'https://www.wanikani.com/api/v{vers}/user/{key}/{res}/{args}'


class WaniKani():

    def __init__(self, api_key, url_format=URL_FORMAT):
        (self.url_format, self.api_key) = (url_format, api_key)

    def get_user_information(self):
        return self._get('user-information', 'user_information', USER_INFO)
    user_information = property(get_user_information)

    def get_study_queue(self):
        return self._get('study-queue', 'requested_information', STUDY_QUEUE)
    study_queue = property(get_study_queue)

    def get_level_progression(self):
        return self._get('level-progression',
                         'requested_information',
                         LEVEL_PROG)
    level_progression = property(get_level_progression)

    def get_srs_distribution(self):
        return self._get('srs-distribution',
                         'requested_information',
                         SRS_DISTS)
    srs_distribution = property(get_srs_distribution)

    def get_recent_unlocks(self, limit=None):
        return self._get_meta_items('recent-unlocks', limit)
    recent_unlocks = property(get_recent_unlocks)

    def get_critical_items(self, percent=None):
        return self._get_meta_items('critical-items', percent)
    critical_items = property(get_critical_items)

    def get_radicals(self, levels=[]):
        return self._get_items(levels, 'radicals', RADICAL)
    radicals = property(get_radicals)

    def get_kanji(self, levels=[]):
        return self._get_items(levels, 'kanji', KANJI)
    kanji = property(get_kanji)

    def get_vocabulary(self, levels=[]):
        return self._get_items(levels, 'vocabulary', VOCABULARY)
    vocabulary = property(get_vocabulary)

    def _get(self, resource, key, fields):
        return ApiObj(self._raw_request(resource)[key], fields)

    def _get_items(self, lv, resource, fields):
        response = self._raw_request(resource,
                                     argument=','.join([str(lv) for lv in lv]))
        response = (response['requested_information']['general']
                    if 'general' in response['requested_information']
                    else response['requested_information'])
        item_list = []
        for item in response:
            item_list.append(ApiObj(item, fields))
        return item_list

    def _get_meta_items(self, resource, argument):
        argument = str(argument) if argument is not None else ''
        response = self._raw_request(resource, argument=argument)
        item_list = []
        for item in response['requested_information']:
            tmap = {'radical': RADICAL, 'kanji': KANJI,
                    'vocabulary': VOCABULARY}
            item_list.append(ApiObj(item, tmap[item['type']]))
        return item_list

    def _raw_request(self, resource, argument='', version=API_VERSION):
        url = self.url_format.format(vers=version, key=self.api_key,
                                     res=resource, args=argument)
        rsp = loads(urlopen(url).read().decode('utf-8'))
        if 'error' in rsp:
            c = rsp['error']['code'] if 'code' in resp['error'] else None
            m = rsp['error']['message'] if 'message' in resp['error'] else None
            raise ApiError(c, m)
        return rsp


class ApiError(Exception):

    def __init__(self, code, msg):
        super(ApiError, self).__init__('{c} - {m}'.format(c=code, m=msg))
        (self.code, self.message) = (code, msg)


class ApiObj:

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
             ('creation_date', lambda x: datetime.utcfromtimestamp(x)),
             ('vacation_date', lambda x: datetime.utcfromtimestamp(x))]
STUDY_QUEUE = [('lessons_available', lambda x: x),
               ('reviews_available', lambda x: x),
               ('reviews_available_next_hour', lambda x: x),
               ('reviews_available_next_day', lambda x: x),
               ('next_review_date', lambda x: datetime.utcfromtimestamp(x))]
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
             ('unlocked_date', lambda x: datetime.utcfromtimestamp(x)),
             ('available_date', lambda x: datetime.utcfromtimestamp(x)),
             ('burned', lambda x: x),
             ('burned_date', lambda x: datetime.utcfromtimestamp(x)),
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
