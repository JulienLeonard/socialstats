import pytumblr
import time
from utils import *

#
# get tumblr stats
# format (nfollowers, timestamp, [(postname,posttimestamp,postcount)])
#
def tumblr_stats(client,userid):
    # get the number of followers
    nfollowers = client.followers(userid, offset=0, limit=20)['total_users'];

    # get all the posts with their count
    poststats = []
    limit = 20
    posts = client.posts(userid, offset=0, limit=limit)['posts'];
    offset = 0
    while len(posts) > limit - 1:
        for post in posts:
            poststats.append((post['slug'],post['timestamp'],post['note_count']))
        offset += limit
        posts = client.posts(userid, offset=offset, limit=limit)['posts'];

    return (nfollowers, time.time(), poststats)

#
# get tumblr stats and format them into xml
#
def tumblr_xmlstats(stats):
    (nfollowers,timestamp,poststats) = stats

    xmlcontent = "<tumblr nfollowers=\"" + str(nfollowers) + "\" timestamp=\"" + str(timestamp) + "\">\n"
    for poststat in poststats:
        (postname,posttimestamp,postcount) = poststat
        xmlcontent = xmlcontent + "\t<post name=\"" + postname + "\" \t timestamp=\"" + str(posttimestamp) + "\" \t count=\"" + str(postcount) + "\"/>\n"
    xmlcontent = xmlcontent + "</tumblr>\n"
    
    return xmlcontent

#
# dump tumblr stats into a xml output file
#
def tumblr_dump(consumer_key, secret_key, access_token, access_token_secret, userid, xmloutputfilepath):
    #
    # connect tumblr client
    #
    client = pytumblr.TumblrRestClient( consumer_key, secret_key, access_token, access_token_secret )
 
    #
    # get the stats and format xml content
    #
    stats = tumblr_stats(client,userid)

    #
    # format stats to xml
    #
    xmlstats = tumblr_xmlstats(stats)

    # dump content
    output=open(xmloutputfilepath, 'w+')
    output.write(xmlstats)
    output.close()

