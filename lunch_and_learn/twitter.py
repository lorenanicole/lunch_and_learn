import requests
from requests_oauthlib import OAuth1
import os
import json
import yaml

__author__ = 'lorenamesa'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TWITTER_API = 'https://api.twitter.com/1.1'

def auth():
    '''
    Define an app at - https://apps.twitter.com/
    Store credentials in config.yml
    '''

    with open('config.yml', 'r') as stream:
        credentials = yaml.load(stream)

    return OAuth1(credentials.get('client_id'),
                  credentials.get('client_secret'),
                  credentials.get('access_token'),
                  credentials.get('access_token_secret'))

def get_home_timeline(count=10):
    '''
    https://dev.twitter.com/rest/reference/get/statuses/home_timeline
    '''

    response = requests.get(TWITTER_API + '/statuses/home_timeline.json?count={0}'.format(count), auth=auth())
    return json.loads(response.content.decode('utf-8'))

def post_tweet(text):
    '''
    https://dev.twitter.com/rest/reference/post/statuses/update
    '''

    response = requests.post(TWITTER_API + '/statuses/update.json', auth=auth(), data={'status': text})
    return json.loads(response.content.decode('utf-8'))

def analyze_sources(tweets):
    types = ['hootsuite', 'sproutsocial', 'twitter', 'buffer']

    sources = {}
    for tweet in tweets:
        for type in types:
            if type in tweet.get('source'):
                if type in sources:
                    sources[type] += 1
                else:
                    sources[type] = 1
                break

    if sum(sources.values()) != len(tweets):
        sources['other'] = len(tweets) - sum(sources.values())

    return sources