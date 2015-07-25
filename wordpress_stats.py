from utils import *
import urllib, json
import time
import datetime

def dump(blogid,filepath): 
    posts = []
    offset = 0
    while True:
        puts("offset",offset)
        url = "https://public-api.wordpress.com/rest/v1/sites/" + blogid + "/posts?number=100&offset=" + str(offset)
        response = urllib.urlopen(url);
        data = json.loads(response.read())
        for post in data['posts']:
            posts.append(post)
        if len(data['posts']) < 100:
            break
        offset += 100

    output=open(filepath, 'w+')
    content = "<wordpress nfollowers=\"" + "NA" + "\" timestamp=\"" + str(time.time()) + "\">\n"

    for post in posts:
        puts(post['title'],post['like_count'],post['date'])
        content = content + "\t<post name=\"" + post['title'] + "\" \t timestamp=\"" + str(post['date']) + "\" \t fav_count=\"" + str(post['like_count']) + "\"></post>\n"

    content = content + "</wordpress>\n"
    output.write(content.encode('utf8'))
    output.close()

# dump("wordpressexample.xml")
