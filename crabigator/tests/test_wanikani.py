"""Tests for crabigator.wanikani."""

from __future__ import print_function
import os
from unittest import TestCase

from crabigator.wanikani import WaniKani, WaniKaniError


# TestCase exposes too many public methods. Disable the pylint warning for it.
# pylint: disable=too-many-public-methods
class TestWaniKani(TestCase):
    """Unit test cases for the WaniKani API wrapper."""

    @classmethod
    def test_wanikani(cls):
        """Test all public methods in crabigator.wanikani."""
        wanikani = WaniKani(os.environ['WANIKANI_API_KEY'])
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
        try:
            wanikani.get_vocabulary([9999])
        except WaniKaniError as ex:
            print(ex)
