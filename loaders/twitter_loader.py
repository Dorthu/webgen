tweets = [
    {
        "content": "THis is #words @people",
        "type":"tweet",
        "stamp": 3
    }
]

import tweepy

t = tweepy.OAuthHandler(twitter_oauth_token, twitter_oauth_secret)
t.set_access_token(twitter_access_token, twitter_access_secret)
api = tweepy.API(t)

u = api.get_user('dorthu22')


def load_content():
    return tweets
