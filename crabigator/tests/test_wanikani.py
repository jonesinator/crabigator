from crabigator.wanikani import WaniKani
import os
from unittest import TestCase

api_key = os.environ['WANIKANI_API_KEY']


class TestWaniKani(TestCase):

    def test_wanikani(self):
        wanikani = WaniKani(api_key)
        print(wanikani.user_information)
        print(wanikani.study_queue)
        print(wanikani.level_progression)
        print(wanikani.srs_distribution)
        print(wanikani.recent_unlocks)
        print(wanikani.get_recent_unlocks(3))
        print(wanikani.critical_items)
        print(wanikani.get_recent_unlocks(65))
        print(wanikani.radicals)
        print(wanikani.get_radicals([1, 2]))
        print(wanikani.kanji)
        print(wanikani.get_kanji([1, 2]))
        print(wanikani.vocabulary)
        print(wanikani.get_vocabulary([1, 2]))
