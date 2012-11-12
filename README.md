TweetsGrabber
=============
*Backup your Twitter*

Installation
------------
Pull a copy of this repo.  Included is a copy of the `tweepy` library.
`tweepy` is available from [github](https://github.com/tweepy/tweepy).

Usage
-----
    python tg.py

tweepy
------
  * timelines incorrectly use `page` for pagination.  According to latest
    twitter documentation, the parameter `max_id` should be used instead.
