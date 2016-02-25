import requests
import json
import yaml
import os
from requests_oauthlib import OAuth1
from pprint import pprint

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

# def analyze_sources(tweets):
#     sources = {}
#     for tweet in timeline:
#     # pprint(tweet)
#         print(tweet.get('created_at') + " " + tweet.get('user').get('screen_name') + " : " + tweet.get('text') + "\n")
#         if 'hootsuite' in tweet.get('source'):
#             if 'hootsuite' in sources:
#                 sources['hootsuite'] += 1
#             else:
#                 sources['hootsuite'] = 1
#             continue
#
#         if 'sproutsocial' in tweet.get('source'):
#             if 'sproutsocial' in sources:
#                 sources['sproutsocial'] += 1
#             else:
#                 sources['sproutsocial'] = 1
#             continue
#
#         if 'twitter' in tweet.get('source'):
#             if 'twitter' in sources:
#                 sources['twitter'] += 1
#             else:
#                 sources['twitter'] = 1
#             continue
#     return sources

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

if __name__ == '__main__':

    # Get home timeline and display
    timeline = get_home_timeline()

    for tweet in timeline:
        print(tweet.get('created_at') + " " + tweet.get('user').get('screen_name') + " : " + tweet.get('text') + "\n")

    # Find sources from home timeline and display
    sources = analyze_sources(timeline)

    print('Twitter sources: ')
    for source, qty in sources.items():
        print('{0} - qty {1}'.format(source, qty))

    # Post a tweet and display result
    tweet = post_tweet('Example of me tweeting!')

    if tweet.get('errors'):
        print("Couldn't post to Twitter: {0}".format(tweet.get('errors')[0].get('message')))
    else:
        print("Successfully posted! View tweet at: https://twitter.com/{0}/status/{1}"
              .format(tweet.get('user').get('id')), tweet.get('id'))

    # Get home timeline and display
    # timeline = get_home_timeline()
    # print timeline
    # timeline = map(lambda t: {'created_at': t.get('created_at'),
    #                           'screen_name': t.get('user').get('screen_name'),
    #                           'id': t.get('id'),
    #                           'url': 'https://twitter.com/{0}/status/{1}'.format(t.get('user').get('id'), t.get('id')),
    #                           'source': t.get('source'),
    #                           'text': t.get('text')}, timeline)
    #
    # import csv
    #
    # with open('my_home_timeline.csv', 'rw') as timeline:
    #     fieldnames = ['created_at', 'screen_name', 'id', 'text', 'source', 'url']
    #     writer = csv.DictWriter(timeline, fieldnames=fieldnames)
    #
    #     for tweet in timeline:
    #         print tweet
    #         writer.writerow(tweet)


    # Find sources from home timeline and display
    # sources = analyze_sources(timeline)
    #
    # print('Twitter sources: ')
    # for source, qty in sources.items():
    #     print('{0} - qty {1}'.format(source, qty))
    #
    # # Post a tweet and display result
    # tweet = post_tweet('Example of me tweeting!')
    #
    # if tweet.get('errors'):
    #     print("Couldn't post to Twitter: {0}".format(tweet.get('errors')[0].get('message')))
    # else:
    #     print("Successfully posted! View tweet at: https://twitter.com/{0}/status/{1}"
    #           .format(tweet.get('user').get('id')), tweet.get('id'))
