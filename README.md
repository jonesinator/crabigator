Crabigator
==========
A very thin Python wrapper over the [WaniKani
API](https://www.wanikani.com/api). The aim is to model the API as closely as
possible while ensuring the correct Python type is used for each field in the
API. The syntax for using the library has been made as simple as possible.

Status
------
[![Build Status](https://travis-ci.org/jonesinator/crabigator.svg)](https://travis-ci.org/jonesinator/crabigator)

Installation
------------
### Stable Versions
To install for all users `sudo pip install crabigator`
To install for a single user `pip install --user crabigator`

### Development Versions
To install for all users `sudo python setup.py install`
To install for a single user `python setup.py --user install`

Usage
-----
1. Import the wanikani module. `from crabigator.wanikani import wanikani`
2. Instantiate a WaniKani object with your API key.
   `wk = wanikani.WaniKani('my_api_key')`
3. Get any endpoint specified by the API docs.
  * `wk.user_information`
  * `wk.study_queue`
  * `wk.level_progression`
  * `wk.srs_distribution`
  * `wk.recent_unlocks`
  * `wk.critical_items`
  * `wk.radicals`
  * `wk.kanji`
  * `wk.vocabulary`
4. From any of the above in #4 the fields in required-information can be
   retrieved. For example:
  * `print(wk.user_information.username)`
  * `print(wk.study_queue.next_review_date)`
  * `print(wk.level_progression.kanji_total)`
  * `print(wk.srs_distribution.master.total)`
  * `print(wk.recent_unlocks[0])`
  * `print(wk.critical_items[0])`
  * `print(wk.radicals[0])`
  * `print(wk.kanji[0])`
  * `print(wk.vocabulary[0])`

Notes
-----
* Everything is a property of a Python object.
* All API responses can be easily printed for debugging.
* All dates in API responses are converted to datetime objects.
* All comma-separated lists in API responses are converted to arrays of strings
  for easier iteration.
