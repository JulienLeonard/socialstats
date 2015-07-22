import pytumblr
import time
from utils import *

#
# dump tumblr stats into a xml output file
#
def tumblr_dump(oAuthConsumerKey, secretKey, tumblr3addr, tumblr4addr, xmloutputfilepath):
    #
    # connect tumblr client
    #
    client = pytumblr.TumblrRestClient( oAuthConsumerKey,
                                        secretKey,
                                        tumblr3addr,
                                        tumblr4addr )
 
    #
    # get the stats and format xml content
    #
    
    # get the number of followers
    nfollowers = client.followers('julienleonard', offset=0, limit=20)['total_users'];

    # get all the posts with their count
    limit = 20
    posts = client.posts('julienleonard', offset=0, limit=limit)['posts'];
    index = 0
    offset = 0
    content = "<tumblr nfollowers=\"" + str(nfollowers) + "\" timestamp=\"" + str(time.time()) + "\">\n"
    while len(posts) > limit - 1:
        for post in posts:
            content = content + "\t<post name=\"" + post['slug'] + "\" \t timestamp=\"" + str(post['timestamp']) + "\" \t count=\"" + str(post['note_count']) + "\"/>\n"
            index += 1
        offset += limit
        posts = client.posts('julienleonard', offset=offset, limit=limit)['posts'];
    content = content + "</tumblr>\n"

    # dump content
    output=open(xmloutputfilepath, 'w+')
    output.write(content)
    output.close()

