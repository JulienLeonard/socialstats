#
# use flickrapi to dump stats about pictures in a flickr account
# use time sleep to prevent automatic flickr rejection
#
import sys
import flickrapi
import time
import sys
from basics import *
import xml.etree.ElementTree

#
# method to dump social stats about the flickr user account
# args:
# - api_secret : your flickr api secret
# - api_key    : your flickr api key
# - user_id    : your flickr user id
# - filepath   : the path of the xml file where the data will be dumped into
#
def flickr_dump(api_secret,api_key,user_id,filepath):

    #
    # connect to flickr with flick api
    #
    flickr=flickrapi.FlickrAPI(api_key,api_secret)
    flickr.web_login_url("read")
    (token,frob)= flickr.get_token_part_one(perms='read')
    if not token: time.sleep(20)
    flickr.get_token_part_two((token, frob))

    #
    # get the photo data
    #
    myphotos = []
    perpage = 10
    pageindex = 1
    rsp = flickr.people_getPhotos(api_key=api_key,user_id=user_id,per_page=perpage,page=pageindex)
    photoss = list(rsp.iter("photos"))[0];

    while int(photoss.attrib['page']) < int(photoss.attrib['pages']):
        puts("page index",pageindex)
        time.sleep(10)
        photolist = list(photoss.iter("photo"));
        photoindex = 0
        for photo in photolist:
            time.sleep(1)

            # get the title
            phototitle = photo.attrib['title']

            # get timestamp of the photo
            photoinfo      = flickr.photos_getInfo(api_key=api_key,photo_id=photo.attrib['id'])
            photoxml       = list(photoinfo.iter("photo"))[0]
            dates          = list(photoxml.iter("dates"))[0]
            phototimestamp = dates.attrib['posted']
            
            # get the list of favorites for the photo
            time.sleep(1)
            favs       = flickr.photos_getFavorites(api_key=api_key,photo_id=photo.attrib['id'])
            favxml     = list(favs.iter("photo"))[0]
            favcount   = favxml.attrib['total']
            personlist = list(favxml.iter("person"))
            favedates  = [person.attrib['favedate'] for person in personlist]

            # add data to cache structure
            myphotos.append((phototitle, phototimestamp, favcount, favedates))

            # stdout info
            puts("photo",photo.attrib['id'],phototitle,"favedates",favedates)

            # iter to the next photo
            photoindex += 1
            
        # iter to the next page
        pageindex += 1
        rsp = flickr.people_getPhotos(api_key=api_key,user_id="22283623@N00",per_page=perpage,page=pageindex)
        photoss = list(rsp.iter("photos"))[0];

    #
    # format the data into xml
    #
    result = "<flickr timestamp=\"" + str(time.time()) + "\">\n"
    for photo in myphotos:
        (title,timestamp,total,favdates) = photo
        result += "   <photo title=\"" + title + "\" \t timestamp=\"" + timestamp + "\" \t count=\"" + total + "\" >\n"
        for favdate in favedates:
            result += "      <favedate timestamp=\"" + favdate + "\"/>\n"
        result += "   </photo>\n"
    result += "</flickr>\n"

    # dump the xml result in a file
    output=open(filepath, 'w+')
    output.write(result.encode('utf8'))
    output.close()


# flickr_dump("123456789abcdef0","123456789abcdef0123456789abcdef0","12345678@N01","C:/stats/flickr_stats.xml")
