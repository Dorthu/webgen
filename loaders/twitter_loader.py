import tweepy


def load_content(config):
    t = tweepy.OAuthHandler(config['twitter_oauth_token'], config['twitter_oauth_secret'])
    t.set_access_token(config['twitter_access_token'], config['twitter_access_secret'])
    api = tweepy.API(t)

    tweets = api.user_timeline(config['user'])
    ret = []

    for t in tweets:
        if t.text[0] == '@':
            continue

        ret.append({
            "type": "tweet",
            "content": t.text,
            "stamp": t.created_at.timestamp(),
            "created": t.created_at,
            "tweet_url": "https://twitter.com/{}/status/{}".format(config['user'], t.id),
        })

    return ret
