#!/usr/bin env python
# -*- coding: utf-8 -*-
import sys
import re
import datetime
import tweepy
import myConf
from myFunc import *

def write_log(var):
    fout= str(datetime.datetime.today().strftime('%x %X')) + ' ; '
    fout+= str(var)
    print (fout)
    return None

def do_select_function(cmd, api):
    func= re.split(' +', cmd)

    if len(func) < 2:
        ans= ' '
        return ans

    try:
        fid= myConf.myFunctionKeyword.index(func[1].lower())
    except:
        write_log('--> no function...')
        ans= myConf.reply_noFunction
        return ans

    ans= eval(myConf.myFunctionDo[fid])(func[2:], api)
    return ans

def do_oauth():
    consumer_key= myConf.consumer_key
    consumer_secret= myConf.consumer_secret
    access_token= myConf.access_token
    access_token_secret= myConf.access_token_secret

    try:
        auth= tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
    except:
        write_log('*Authentication error...')
        sys.exit()

    write_log('*Authenticated...')
    return auth

class Listener(tweepy.StreamListener):
    def __init__(self):
        write_log('-> created Listener object...')
        super(Listener,self).__init__()
        return None

    def __del__(self):
        write_log('-> __del__...')
        return None

    def on_connect(self):
        write_log('-> connected streaming...')
        return None

    # def on_data(self, data):
    #     print(data)
    #     f= open('tweet.log','a')
    #     f.write(data)
    #     f.close()
    #     return

    def on_status(self, status):
        write_log('-> updated status...')
        status.created_at += datetime.timedelta(hours=9)

        if str(status.in_reply_to_screen_name) == str(myConf.myAccount):
            tweet= '@' + str(status.user.screen_name) + ' '

            if str(status.user.screen_name) in str(myConf.okAccount):
                write_log('-> access registered user @' + str(status.user.screen_name))
                ans= do_select_function(status.text, api)
                tweet+= ans
            else:
                write_log('-> access non registered user @' + str(status.user.screen_name))
                tweet+= myConf.reply_ngAccount
 
            tweet+= '\n' + str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            api.update_status(status= tweet, in_reply_to_status_id= status.id)

        return
      
    def on_error(self, status_code):
        var= '-> error status code= ' + str(status_code)
        write_log(var)
        return

    def on_timeout(self):
        write_log('-> timeout...')
        return

if __name__ == '__main__':
  #C... Initialaze
    auth= do_oauth()
    api= tweepy.API(auth)

  #C... Create Object
    listener= Listener()
    stream= tweepy.Stream(auth, listener)

  #C...
    write_log('*Start listening...')
    stream.userstream()