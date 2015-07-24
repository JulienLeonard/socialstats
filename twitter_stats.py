import tweepy
import time
import datetime

#
# get twitter stats
# result in the form (nfollowers,timestamp,[(tweetid,tweettimestamp,tweetnfavs,tweetnretweets,tweettext)])
#
def twitter_stats(api,user,screenname):
    
    nfollowers = user.followers_count
    timestamp  = time.time()

    limit = 100
    timeline = api.user_timeline(screen_name=screenname, count=limit)
    maxid = ""
    tweetstats = []
    while True:
        for tweet in timeline:
            tweetid         = tweet.id
            tweettimestamp  = tweet.created_at
            tweetnfavs      = tweet.favorite_count
            tweetnretweets  = tweet.retweet_count
            tweettext       = tweet.text
            tweetstats.append((tweetid,tweettimestamp,tweetnfavs,tweetnretweets,tweettext))
            maxid = tweet.id
        if len(timeline) < limit:
            break
        else:
            timeline = api.user_timeline(screen_name=screenname, count=limit, max_id=maxid)

    return (nfollowers,timeline,tweetstats)

#
# format stats into xml string
#
def twitter_xmlstats(stats):    
    (nfollowers,timeline,tweetstats) = tweetstats

    content = "<twitter nfollowers=\"" + str(nfollowers) + "\" timestamp=\"" + str(timestamp) + "\">\n"
    for tweetstat in tweetstats:
        (tweetid,tweettimestamp,tweetnfavs,tweetnretweets,tweettext) = tweetstat
        content = content + "\t<post name=\"" + str(tweetid) + "\" \t timestamp=\"" + str(tweettimestamp) + "\" \t fav_count=\"" + str(tweetnfavs) + "\" \t rt_count=\"" + str(tweetnretweets) + "\">" + tweettext + "</post>\n"
    content = content + "</twitter>\n"

    return content
    
    

#
# dump twitter stats into a xml file
#
def twitter_dump(consumer_key, consumer_secret, access_token, access_token_secret, screenname, xmloutputfilepath): 
    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    user = api.me()

    # get the stats
    stats = twitter_stats(api,user,screenname)

    # format the stats
    xmlcontent = twitter_xmlstats(stats)

    # dump the stats
    output=open(xmloutputfilepath, 'w+')
    output.write(xmlcontent.encode('utf8'))
    output.close()
