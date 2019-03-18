# -*- coding:utf-8 -*-

import json
from requests_oauthlib import OAuth1Session
import os
from os.path import join, dirname
from dotenv import load_dotenv

import sys
print(sys.getdefaultencoding())
# sys.setdefaultencoding('utf-8') # デフォルトの文字コードを変更する．
import requests

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Twitter:
    CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
    CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

    twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    def showtimeline(self):
        url = "https://api.twitter.com/1.1/search/tweets.json"
        params = {'count' : 5, 'q' : '@nega_deg_kun'}
        req = self.twitter.get(url, params = params)
        if req.status_code == 200:
            timeline = json.loads(req.text)
            print(timeline)
            for tweet in timeline['statuses']:
                #tweet = json.loads(tweet)
                print(tweet['user']['name']+'::'+tweet['text'])
                print(tweet['created_at'])
                print('----------------------------------------------------')
        else:
            print("ERROR: %d" % req.status_code)

    def get_screen_name(self):
        pass

    def reply_result(self, user_id, screen_name, tweet_id):
        tweet = "@"+screen_name+" "+"Reply Thanks you"
        url = "https://api.twitter.com/1.1/statuses/update.json"
        params = {
            "in_reply_to_status_id": tweet_id,
            "status": tweet
        }
        self.twitter.post(url, params=params)

    def streaming(self):
        url = "https://stream.twitter.com/1.1/statuses/filter.json"
        params = {"track": "@nega_deg_kun"}
        RLT = 180
        while(True):
            try:
                req = self.twitter.post(url, stream=True, params=params)
                #print(req.status_code)
                if req.status_code == 200:
                    if req.encoding is None:
                        req.encoding = "utf-8"
                    for js in req.iter_lines(chunk_size=1,decode_unicode=True):
                        try:
                            if js :
                                tweet = json.loads(js)
                                if 'text' in tweet:
                                    Name = (tweet["user"]["name"])
                                    user_id = tweet["user"]["id_str"]
                                    SC_N = (tweet["user"]["screen_name"])
                                    Text = (tweet["text"])
                                    tweet_id = tweet["id_str"]
                                    print ('----\n'+Name+"(@"+SC_N+"):"+'\n'+Text)

                                    self.reply_result(user_id, SC_N, tweet_id)

                                    continue
                                else:
                                    continue
                        except UnicodeEncodeError:
                            pass
                elif req.status_code == 420:
                    print('Rate Limit: Reload after', RLT, 'Sec.')
                    time.sleep(RLT)

                else:
                    print("HTTP ERRORE: %d" % req.status_code)
                    break
            except KeyboardInterrupt:
                print("End")
                break

            except:
                print("except Error:", sys.exc_info())
                pass
