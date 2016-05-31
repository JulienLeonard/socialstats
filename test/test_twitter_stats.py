from distimport import *
twitter_stats = distimport("./../lib",'twitter_stats')
from mysocialids import *
from basics import *

twitter_stats.twitter_dump(twitter_consumer_key(), twitter_consumer_secret(), twitter_access_token(), twitter_access_token_secret(), twitter_screenname(), "twitter_stats.xml")




