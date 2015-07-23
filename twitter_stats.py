import tweepy
from utils import *
import time
import datetime

#
# dump twitter stats into a xml file
#
def twitter_dump(consumer_key, consumer_secret, access_token, access_token_secret, xmloutputfilepath): 


    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Creation of the actual interface, using authentication
    api = tweepy.API(auth)

    # check me
    user = api.me()

    print('Name: ' + user.name)
    print('Location: ' + user.location)
    print('Friends: ' + str(user.followers_count))

    content = "<twitter nfollowers=\"" + str(user.followers_count) + "\" timestamp=\"" + str(time.time()) + "\">\n"


    # public_tweets = api.home_timeline()
    # for tweet in public_tweets:
    #    print tweet.text

    #for follower in api.followers_ids('twitter'):
    #    print api.get_user(follower).screen_name

    #results = api.search(q='julleor')

    #for tweet in results:
    #    puts("date",(tweet.created_at - datetime.datetime(1970,1,1)).total_seconds())

    limit = 100
    timeline = api.user_timeline(screen_name='julleor', count=limit)
    index = 0
    maxid = ""
    while True:
        for tweet in timeline:
            content = content + "\t<post name=\"" + str(tweet.id) + "\" \t timestamp=\"" + str(tweet.created_at) + "\" \t fav_count=\"" + str(tweet.favorite_count) + "\" \t rt_count=\"" + str(tweet.retweet_count) + "\">" + tweet.text + "</post>\n"
            print ("Text:", tweet.text)
            #print ("Number", str(index))
            #print ("ID:", tweet.id)
            #print ("User ID:", tweet.user.id)
            #print ("Text:", tweet.text)
            #print ("Created:", tweet.created_at)
            #print ("Favorited:", tweet.favorited)
            #print ("Retweeted:", tweet.retweeted)
            #print ("Retweet count:", tweet.retweet_count)
            #print ("Favorite count:", tweet.favorite_count)
            index += 1
            maxid = tweet.id
        if len(timeline) < limit:
            break
        else:
            timeline = api.user_timeline(screen_name='julleor', count=limit, max_id=maxid)


    output=open(xmloutputfilepath, 'w+')
    content = content + "</twitter>\n"
    output.write(content.encode('utf8'))
    output.close()
