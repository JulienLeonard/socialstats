from utils import *
import urllib, json
import time
import datetime

#
# get all wordpress stats data
#
def wordpress_stats():
    stats = []
    offset = 0
    baseurl = "https://public-api.wordpress.com/rest/v1/sites/" + blogid + "/posts?number=100&offset="
    while True:
        url = baseurl + str(offset)
        response = urllib.urlopen(url);
        data = json.loads(response.read())
        for post in data['posts']:
            stats.append((post['title'],post['date'],post['like_count']))
        if len(data['posts']) < 100:
            break
        offset += 100
        
    return stats

#
# format stats into xml
#
def wordpress_xmlstats(stats,timestamp):
    content = "<wordpress nfollowers=\"" + "NA" + "\" timestamp=\"" + str(timestamp) + "\">\n"
    for stat in stats:
        (title,data,nfavs) = stat
        content = content + "\t<post name=\"" + title + "\" \t timestamp=\"" + str(date) + "\" \t fav_count=\"" + str(nfavs) + "\"></post>\n"
    content = content + "</wordpress>\n"
    return content


#
# dump wordpress stats into xmloutputfilepath
#
def wordpress_dump(blogid,xmloutputfilepath): 

    # get all the posts
    posts = wordpress_postdata()

    # format the data 
    xmlcontent = wordpress_xmlstats(stats,time.time())

    # dump xmlcontent 
    output=open(xmloutputfilepath, 'w+')
    output.write(xmlcontent.encode('utf8'))
    output.close()

