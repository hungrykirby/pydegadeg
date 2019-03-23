# -*- coding:utf-8 -*-

import json
from requests_oauthlib import OAuth1Session
import os
import re
from os.path import join, dirname
from dotenv import load_dotenv
import emoji
from janome.tokenizer import Tokenizer
import pandas as pd

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

    t = None
    twitter = None
    pnja_dic = None

    def __init__(self):
        self.t = Tokenizer()
        self.twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.pnja_dic = self.__make_dict()


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

    def reply_result(self, user_id, screen_name, tweet_id, text):
        point = self.__get_negaposi_point(user_id)
        tweet = "@"+screen_name + " " + "あなたの最近のポジティブ度は" + point + "点(100点~-100点)だよ。また診断してね！" 
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

                                    self.reply_result(user_id, SC_N, tweet_id, Text)

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

    def __make_dict(self):
        pn_ja = pd.read_csv('./dict/pn_ja.dic', sep=':',encoding='cp932', names=('Tango','Yomi','Hinshi', 'Score'))
        word = pn_ja['Tango']
        score = pn_ja['Score']

        return dict(zip(word, score))

    def __calc_score(self, point):
        result = 0
        indexes = [0, -0.927, 24.59, -46.7, -11.75, 86.67, -38.1, -36.8, 24]
        for i in len(indexes):
            result += indexes[i]*(point ** i)
        
        result = result*200.0 - 100
        if result > 100:
            result = 100
        elif result < -100:
            result -100
        return result

    def __get_negaposi_point(self, text):
        point = 0
        for token in self.t.tokenize(text):
            #print(token)
            if token in self.pnja_dic:
                print(token, ':', self.__calc_score(self.pnja_dic[token]))
                point = point + self.__calc_score(self.pnja_dic[token])
        return point

    def __return_tweets_points(self, user_id):
        point = 0
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        params = {
            "count":26,
            "user_id";user_id
        }
        tweets = self.twitter.get(url, params=params)
        for tweet in tweets:
            point = point + self.__get_negaposi_point(self.__shape_tweet(tweet))
        return point

    def __shape_tweet(self, tweet):
        shaped_tweet = tweet

        #URLを除去
        s = re.sub(r"(\s*https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "" ,shaped_tweet)
        
        #ハッシュタグを除去
        s = re.sub(r"(\s*#\S+\s*)", "", s)

        #リプライを除去
        s = re.sub(r"(\s*@\S+\s*)", "", s)

        #「診断して」を除去
        s = re.sub(r"診断して", "", s)

        #タブ、インデント、改行を除去
        s = re.sub(r"\s+", " ", s)

        #数字、英語を除去
        s = re.sub(r"[a-zA-Z0-9]+", "", s)

        #全角数字を除去
        s = re.sub(r"[０-９]+", "", s)

        s = self.__remove_emoji(s)

        if(s == ''):
            s = 'すもも'

        return s

    
    def __remove_emoji(self, src_str):
        return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)