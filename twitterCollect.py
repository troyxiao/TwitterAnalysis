#Reference: http://www.mikaelbrunila.fi/2017/03/27/scraping-extracting-mapping-geodata-twitter/
import tweepy
from tweepy import Stream
from tweepy import StreamListener 
from tweepy import OAuthHandler
import json
import time

# Twitter API keys
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
    
    def __init__(self, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        self.saveFile = open('streamTwitter.json', 'a')
        super(MyStreamListener, self).__init__()

    def on_status(self, status):
        if (time.time() - self.start_time) < self.limit:
            # filter twitter with geo info
            if status.geo is not None:
                self.saveFile.write(status.text)
                self.saveFile.write('\n')

                # print coordinates to screen
                dictCoords = status.geo
                listCoords = dictCoords['coordinates']
                latitude = listCoords[0]
                longitude = listCoords[1]
                print(str(listCoords[0]) + "," + str(listCoords[1]))
                print(status.place)

                return True
        else:
            self.saveFile.close()
            return False

    # Handle error
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream


if __name__ == '__main__':
    # set the length of time to collect data
    time_limit = 600
    print('Collecting twitters...Wait time is '+ str(time_limit)+ ' seconds.'+'\n')

    # Collect data
    myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener(time_limit))
    myStream.sample()

    print('Done.')
