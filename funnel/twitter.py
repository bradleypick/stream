#!/usr/bin/env python

import os
import csv
import json
import tweepy
import argparse

ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']
CONSUMER_KEY = os.environ['TWITTER_API_KEY']
CONSUMER_SECRET = os.environ['TWITTER_API_SECRET']

class StreamListener(tweepy.StreamListener):

    def __init__(self, outfile, api=None):
        super().__init__(api)
        self.outfile = outfile
        with open(outfile, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['time_created',
                            'time_created_orig',
                            'screen_name',
                            'verified',
                            'retweet',
                            'text'])

    def on_status(self, status):
        with open(self.outfile, 'a', newline='') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data = status._json
            if not hasattr(status, 'retweeted_status'):
                writer.writerow([data['created_at'],
                                data['created_at'],
                                data['user']['screen_name'],
                                data['user']['verified'],
                                False,
                                data['text']])
            else:
                writer.writerow([data['created_at'],
                                data['retweeted_status']['created_at'],
                                data['retweeted_status']['user']['screen_name'],
                                data['retweeted_status']['user']['verified'],
                                True,
                                data['retweeted_status']['text']])
                
                
    def on_error(self, status_code):
        if status_code == 420:
            return False

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Twitter Stream API interface to route data to <insert-destination-here>')
    parser.add_argument('--track', nargs='+', help='Terms to track in stream', required=True)
    args = parser.parse_args()

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

    stream_listener = StreamListener(outfile='data/test.csv')
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=args.track, languages=['en'])

