#Reference: http://www.mikaelbrunila.fi/2017/03/27/scraping-extracting-mapping-geodata-twitter/
import tweepy
from tweepy import Stream
from tweepy import StreamListener 
from tweepy import OAuthHandler
import json

# Twitter API keys
consumer_key = 'PSstLBpnp1oEgCtJQGFzSoXs0'
consumer_secret = 'f5v36gPN2u0cuBVujLqa2NBH3b5uJRRVTaGcGGtn1tEcM377vp'
access_token = '998641782194933760-YCNSkx8udzUA5Yx5DLO3l2w4FjQfaVR'
access_secret = 'PsHZQL76UQzwxsw9HnNFSd7U2c6gIcD5odWvO1ihjgMc7'

# Authenticate
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
# Store stream twitters to the file
file = open('streamTwitter', 'a')

# This listener will print out all Tweets it receives
class PrintListener(tweepy.StreamListener):
    # Read data and store to file 
    def on_data(self, data):
        # Decode the JSON data
        tweet = json.loads(data)
        file.write(str(tweet))
        # Print out the Tweet
        print('@%s: %s' % (tweet['user']['screen_name'], tweet['text'].encode('ascii', 'ignore')))

    # Handle error
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

# Call self defined 
def start_stream():
    count = 0
    while True and count<5:
        try:
            sapi = tweepy.streaming.Stream(auth, PrintListener(api))
            sapi.sample()
            count=count+1
            # If want to filter by a certain word such as 'python', use the line below
            # stream.filter(track=['python'])
        except: 
            continue

if __name__ == '__main__':
    # Show system message
    print('Below are captured twitter ==>')

    # Connect the stream to our listener
    listener = PrintListener()
    stream = tweepy.Stream(auth, listener)

    # Collect data
    start_stream()
