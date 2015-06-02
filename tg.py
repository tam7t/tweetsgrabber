import tweepy
import time
import webbrowser
import secret
import cgi

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="your key"
consumer_secret="your secret"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth_url = auth.get_authorization_url()

# Open web browser to complete OAuth authentication
webbrowser.open(auth_url)
time.sleep(2)

# Accept PIN from user
verifier = raw_input('PIN: ').strip()
auth.get_access_token(verifier)

api = tweepy.API(auth)

def print_people(people, name):
    f = open(name,'w')
    f.write("\"name\",\"screen name\",\"url\",\"description\"\n")
    for user in tweepy.Cursor(people).items():
        line = (user.name, user.screen_name, user.url, user.description)
        str = "\"%s\",\"%s\",\"%s\",\"%s\"\n" % line
        f.write(str.encode("utf-8"))
    f.close()

def print_timeline(timeline, name):

    f = open(name,'w')

    headers = ('text',
               'created_at',
               'retweet_count',
               'source',
               'source_url',
               'lat',
               'long',
               'place_country',
               'place_country_code',
               'place_full_name',
               'place_name',
               'place_type',
               'place_url')
    str = "\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n" % headers
    f.write(str.encode("utf-8"))

    all = []
    max_id=-1

    statuses = timeline(count=200, include_rts=True)
    for status in statuses:
        if max_id < 0 or status.id < max_id:
            max_id = status.id
        all.append(status)

    while True:
        statuses = timeline(max_id=max_id, count=200, include_rts=True)
        prev_id = max_id
        for status in statuses:
            if status.id < max_id:
                max_id = status.id
        if max_id == prev_id:
            break
        else:
            for status in statuses:
                all.append(status)

    for status in all:
    # for status in tweepy.Cursor(timeline).items():
        place = {}
        place['country'] = ''
        place['country_code'] = ''
        place['full_name'] = ''
        place['name'] = ''
        place['place_type'] = ''
        place['url'] = ''

        if status.place:
            place['country'] = status.place.country
            place['country_code'] = status.place.country_code
            place['full_name'] = status.place.full_name
            place['name'] = status.place.name
            place['place_type'] = status.place.place_type
            place['url'] = status.place.url

        coordinates = {}
        coordinates[0] = ''
        coordinates[1] = ''

        if status.coordinates:
            coordinates[0] = status.coordinates[0]
            coordinates[1] = status.coordinates[1]

        line = (cgi.escape(status.text, quote=True),
                status.created_at,
                status.retweet_count,
                status.source,
                status.source_url,
                coordinates[0],
                coordinates[1],
                place['country'],
                place['country_code'],
                place['full_name'],
                place['name'],
                place['place_type'],
                place['url'])

        str = "\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n" % line
        f.write(str.encode("utf-8"))

    f.close()

print_timeline(api.user_timeline,'timeline.csv')
print_people(api.followers, 'followers.csv')
print_people(api.friends, 'friends.csv')

