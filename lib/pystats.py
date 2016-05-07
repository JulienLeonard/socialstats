#
# fetch all the data from the different social sites, to dump files in accordance
# create a dedicated dir under dump_directory()/%timestamp%/ to gather the different files
# analysed after by Tcl to generate graphs in svg and javascript
#

import os 
import time
import sys

import tumblr_stats
import flickr_stats
import twitter_stats
import wordpress_stats
import faa_stats

from mysocialids import *

#
# crate dump dir
#
def pystats_newnowdir(dump_directory,social_type):
    now = time.time()
    newdirectory = dump_directory + str(now) + social_type

    if not os.path.exists(newdirectory):
        os.makedirs(newdirectory)

    return newdirectory
    
#
# get stats from the specified social medium and dump it
#
def pystats_social(dump_directory,social_type):

    newdirectory = pystats_newnowdir(dump_directory,social_type)

    if social_type == "tumblr":
        print("start tumblr ...")
        tumblr_filepath = newdirectory + "/tumblr.xml"
        tumblr_stats.tumblr_dump(tumblr_consumer_key(), tumblr_secret_key(), tumblr_access_token(), tumblr_access_token_secret(), tumblr_userid(), tumblr_filepath)
        print("stop tumblr")

    if social_type == "flickr":
        print("start flickr ...")
        flickr_filepath = newdirectory + "/flickr.xml"
        flickr_stats.flickr_dump(flickr_api_secret(),flickr_api_key(),flickr_user_id(),flickr_filepath)
        print("stop flickr")

    if social_type == "twitter":
        print("start twitter ...")
        twitter_filepath = newdirectory + "/twitter.xml"
        twitter_stats.twitter_dump(twitter_consumer_key(), twitter_consumer_secret(), twitter_access_token(), twitter_access_token_secret(), twitter_screenname(), twitter_filepath)
        print("stop twitter")

    if social_type == "wordpress":
        print("start wordpress ...")
        wordpress_filepath = newdirectory + "/wordpress.xml"
        wordpress_stats.wordpress_dump(wordpress_blogid(),wordpress_filepath)
        print("stop wordpress")

    if social_type == "fineartamerica":
        print("start faa ...")
        faa_filepath = newdirectory + "/faa.xml"
        faa_stats.faa_dump(faa_username(),faa_password(),faa_profile(),faa_filepath)
        print("stop faa")

#
# main call: usage: main social_type (can be tumblr, flickr, twitter, wordpress, or fineartamerica)
#
def main():
    social_type  = sys.argv[1]
    pystats_social(pystats_output_dir(),social_type)

if __name__ == '__main__':
  main()

#
# usage
# dump_social("flickr")
#
