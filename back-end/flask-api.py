import requests
import json

from flask import Flask
from flask_restful import Resource, Api
from flask.ext.jsonpify import jsonify
from requests_oauthlib import OAuth1

APP = Flask(__name__)
API = Api(APP)

def maptweet(tweet):
    if len(tweet['entities']['urls']) > 0 and tweet['entities']['urls'][0].get('url'):
        source_url = tweet['entities']['urls'][0].get('url')
    else:
        source_url = ''

    if tweet['entities'].get('media') and len(tweet['entities']['media']) > 0 and tweet['entities']['media'][0].get('media_url'):
        media_url = tweet['entities']['media'][0].get('media_url')
    else:
        media_url = ''

    reduced_tweet = {
        'text': tweet['text'],
        'source_url': source_url,
        'media_url': media_url
    }
    return reduced_tweet

class TwitterNewsData(Resource):
    def get(self):
        payload = {'q': 'news', 'lang': 'en', 'result_type': 'popular'}
        url = 'https://api.twitter.com/1.1/search/tweets.json'

        auth = OAuth1(
            'AGsVhqXmwc9fGM82xVcIpRUcj',
            'nN3HKcMOLlyy91RjOaFyoFe64GwRpSBObaC68fkJEVDHyjntfw',
            '826265268867432449-KLaZ2b8afiGmuINEPKmqA4DjWv4ENQT',
            'W3nJGED61ALQOerEC6Esl2A74hHeDI4Z8fRSqG9D1besv'
        )

        req_object = requests.get(url, params=payload, auth=auth)
        json_data = req_object.json()
        tweets = json_data["statuses"]
        
        top_tweets = self.filtertoptweets(tweets)
        reduced_tweets = self.reducetweetobjects(top_tweets)
        return json.dumps(list(reduced_tweets))

    def filtertoptweets(self, tweets):
        tweets.sort(key=lambda x: x["retweet_count"], reverse=True)

        return tweets[:5]

    def reducetweetobjects(self, tweets):
        return map(maptweet, tweets)

API.add_resource(TwitterNewsData, '/news_data')

if __name__ == '__main__':
    APP.run(debug=True)#, host='0.0.0.0')
