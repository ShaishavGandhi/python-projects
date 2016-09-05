from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

access_token = "773911496-gjFt7FI0nYdsGH0RgW14Agoz5wXmIpOVtddbwy6b"
access_token_secret = "ZIE3lOOdKUGqJhhQvYtkj2cB3BlfvpE4SSsL6VFCpK1zx"
consumer_key = "jMncPH1y8l8hubkzxb7UD0ysb"
consumer_secret = "nsqLNiAhDqceEfnK7jF4SA6NgFBIYConP4WSXfk7MNTsv2e1t5"
mi=0
kkr=0
rcb=0

class StdOutListener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        text = data["text"]
        global mi,rcb,kkr
        if "Mumbai Indians" in text:
            mi+=1
        elif "KKR" in text:
            kkr+=1
        elif "RCB" in text:
            rcb+=1
        print "Mumbai Indians : "+str(mi)+"\nKKR : "+str(kkr)+"\nRCB : "+str(rcb)
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(track=['Mumbai Indians', 'KKR', 'RCB'])