import sys
sys.path.insert(0, 'libs')
from twitter import *
from settings import *
import datetime
from dateutil import parser, tz


def get_trucks():
    # authenticate to twitter
    t = Twitter(
            auth=OAuth(
                OAUTH_TOKEN,
                OAUTH_SECRET,
                CONSUMER_KEY,
                CONSUMER_SECRET)
    )
    results = []
    for truck in FOOD_TRUCK_HANDLES:
        out = FOOD_TRUCK_HANDLES[truck].copy()
        result = parse_tweets(t.statuses.user_timeline(screen_name=out['username'],
                                              exclude_replies=True,
                                              contributor_details=False,
                                              include_rts=False))
        out['tweet'] = result[0]
        out['geo'] = result[1]
        results.append(out)

    return results

def get_truck(truck_handle):
    """ GET a single truck by its name"""
    t = Twitter(
            auth=OAuth(
                OAUTH_TOKEN,
                OAUTH_SECRET,
                CONSUMER_KEY,
                CONSUMER_SECRET)
    )
    if truck_handle in FOOD_TRUCK_HANDLES:
        out = FOOD_TRUCK_HANDLES[truck_handle].copy()
        result = parse_tweets(t.statuses.user_timeline(screen_name=out['username'],
                                                exclude_replies=True,
                                                contributor_details=False,
                                                include_rts=False))
        out['tweet'] = result[0]
        out['geo'] = result[1]

        return out
    else:
        return {'error':'Couldnt find Truck'}


def parse_tweets(tweets):
    """ Parse an array of tweets
        The bits we care about look like this:
            tweet['text'] # the tweet
            tweet['geo']={u'type': u'Point', u'coordinates': [41.8169215, -71.4063959]}
            tweet['entities']['hashtags']=[{u'indices': [11, 18], u'text': u'double'}, {u'indices': [19, 24], u'text': u'hash'}]

            Since the api orders tweets like the timeline does, return
    """
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(TZ)
    now = datetime.datetime.now()
    now = now.replace(tzinfo=from_zone)
    now = now.astimezone(to_zone)

    for tweet in tweets:
        # Thanks Stack Overflow: http://stackoverflow.com/questions/4770297/python-convert-utc-datetime-string-to-local-datetime
        twitter_date = parser.parse(tweet["created_at"])
        twitter_date.replace(tzinfo=from_zone)
        local_date = twitter_date.astimezone(to_zone)
        # we only care about today's tweets.
        if now.day == local_date.day:
            hashtags = [tag['text'] for tag in tweet['entities']['hashtags']]
            if tweet['geo'] != None:
                if HASHTAG_TRIGGER in hashtags:
                    return tweet['text'], tweet['geo']
            else:
                pass # since this has no geo data for us
    return None, None

