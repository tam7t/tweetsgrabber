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

Your web browser will be directed to twitter authentication page.  Once
authenticated, input the provided PIN to the console.  The script will then
create the following files:

* friends.csv
* followers.csv
* timeline.csv

The following elements have not been implemented:

* lists
* favorites
* direct messages

tweepy
------
  * timelines incorrectly use `page` for pagination.  According to latest
    twitter documentation, the parameter `max_id` should be used instead.
