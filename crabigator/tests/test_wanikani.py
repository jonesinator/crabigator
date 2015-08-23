from crabigator.wanikani import WaniKani
import os
from unittest import TestCase

api_key = os.environ['WANIKANI_API_KEY']

class TestWaniKani(TestCase):
    def test_wanikani(self):
        wk = WaniKani(api_key)
        print(wk.user_information)
        print(wk.study_queue)
        print(wk.level_progression)
        print(wk.srs_distribution)
        print(wk.recent_unlocks)
        print(wk.get_recent_unlocks(3))
        print(wk.critical_items)
        print(wk.get_recent_unlocks(65))
        print(wk.radicals)
        print(wk.get_radicals([1,2]))
        print(wk.kanji)
        print(wk.get_kanji([1,2]))
        print(wk.vocabulary)
        print(wk.get_vocabulary([1,2]))
