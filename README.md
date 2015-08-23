Crabigator
==========
[![Build Status](https://travis-ci.org/jonesinator/crabigator.svg)](https://travis-ci.org/jonesinator/crabigator) ![License](https://img.shields.io/github/license/jonesinator/crabigator.svg)

A very thin Python wrapper over the [WaniKani
API](https://www.wanikani.com/api) (WaniKani is a tool for leaning Japanese
vocabulary). The aim is to model the API as closely as possible while ensuring
the correct Python type is used for each field in the API. The syntax for using
the library has been made as simple as possible.

Installation
------------
### Stable Versions
To install for all users `sudo pip install crabigator`

To install for a single user `pip install --user crabigator`

### Development Versions
First clone this repository and cd to it.

To install for all users `sudo python setup.py install`

To install for a single user `python setup.py --user install`

Usage
-----
1. Import the WaniKani class. `from crabigator.wanikani import WaniKani`
2. Instantiate a WaniKani instance with your API key.
   `wanikani = WaniKani('my_api_key')`
3. Get any endpoint specified by the API docs (dashes replaced with
   underscores).
  * `wanikani.user_information`
  * `wanikani.study_queue`
  * `wanikani.level_progression`
  * `wanikani.srs_distribution`
  * `wanikani.recent_unlocks`
  * `wanikani.critical_items`
  * `wanikani.radicals`
  * `wanikani.kanji`
  * `wanikani.vocabulary`
4. From any of the above endpoints in #3 the output fields in the
   required-information key can be retrieved. For example:
  * `print(wanikani.user_information.username)`
  * `print(wanikani.study_queue.next_review_date)`
  * `print(wanikani.level_progression.kanji_total)`
  * `print(wanikani.srs_distribution.master.total)`
  * `print(wanikani.recent_unlocks[0])`
  * `print(wanikani.critical_items[0])`
  * `print(wanikani.radicals[0])`
  * `print(wanikani.kanji[0])`
  * `print(wanikani.vocabulary[0])`

Notes
-----
* Everything is a property of a Python object.
* All API responses can be easily printed for debugging.
* All dates in API responses are converted to datetime objects.
* All comma-separated lists in API responses are converted to arrays of strings
  for easier iteration over multiple readings and meanings.
