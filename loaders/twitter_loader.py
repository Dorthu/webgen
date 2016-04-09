tweets = [
    {
        "content": "THis is #words @people",
        "type":"tweet",
        "stamp": 3
    }
]

import tweepy


def load_content(config):
    t = tweepy.OAuthHandler(config['twitter_oauth_token'], config['twitter_oauth_secret'])
    t.set_access_token(config['twitter_access_token'], config['twitter_access_secret'])
    api = tweepy.API(t)

    tweets = api.user_timeline(config['user'])
    ret = []

    for t in tweets:
        ret.append({
            "type": "tweet",
            "content": t.text,
            "stamp": t.created_at.timestamp()
        })

    return ret
