import urllib, json
import time
import datetime

#
# get all wordpress stats data
#
def wordpress_stats(blogid):
    result = []
    offset = 0
    baseurl = "https://public-api.wordpress.com/rest/v1/sites/" + blogid + "/posts?number=100&offset="
    while True:
        url = baseurl + str(offset)
        response = urllib.urlopen(url);
        data = json.loads(response.read())
        for post in data['posts']:
            result.append((post['title'],post['date'],post['like_count']))
        if len(data['posts']) < 100:
            break
        offset += 100
        
    return result

#
# format stats into xml
#
def wordpress_xmlstats(stats,timestamp):
    xmlcontent = "<wordpress nfollowers=\"" + "NA" + "\" timestamp=\"" + str(timestamp) + "\">\n"
    for stat in stats:
        (title,date,nfavs) = stat
        xmlcontent = xmlcontent + "\t<post name=\"" + title + "\" \t timestamp=\"" + str(date) + "\" \t fav_count=\"" + str(nfavs) + "\"></post>\n"
    xmlcontent = xmlcontent + "</wordpress>\n"
    return xmlcontent


#
# dump wordpress stats into xmloutputfilepath
#
def wordpress_dump(blogid,xmloutputfilepath): 

    # get all the posts
    stats = wordpress_stats(blogid)

    # format the data 
    xmlcontent = wordpress_xmlstats(stats,time.time())

    # dump xmlcontent 
    output=open(xmloutputfilepath, 'w+')
    output.write(xmlcontent.encode('utf8'))
    output.close()

