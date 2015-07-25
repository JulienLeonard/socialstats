from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import selenium
import sys
import time
from utils import *

#
# login to faa
#
def faa_login(driver, faa_username, faa_password):
    driver.get("https://fineartamerica.com/loginartist.php")
    elem = driver.find_element_by_name("username")
    elem.send_keys(faa_username)
    elem.send_keys(Keys.RETURN)
    elem = driver.find_element_by_name("password")
    elem.send_keys(faa_password)
    elem.send_keys(Keys.RETURN)
    return driver
    
#
# get the number of visitors
#
def faa_nvisitors(driver):
    driver.get("http://fineartamerica.com/controlpanel/statistics.html?tab=visitors")
    nvisitors = ""
    elems = driver.find_elements(By.XPATH, '//p')
    for elem in elems:
        text = elem.text
        items = text.split(" ")
        if len(items) > 2 and items[0] == "Total" and items[1] == "Visitors:":
            nvisitors = items[2]
            break
    return nvisitors

#
# get the number of followers
#
def faa_nfollowers(driver):
    driver.get("http://fineartamerica.com/profiles/" + faa_profile + ".html")
    nfollowers = ""
    elems = driver.find_elements(By.XPATH,'//a')
    for elem in elems:
        # puts("a href",elem.get_attribute("href"))
        if elem.get_attribute("href") == u"http://fineartamerica.com/profiles/" + profiles + ".html?tab=watchlist&type=others":
            nfollowers = elem.text
            break
    return nfollowers

#
# get the number of views
#    
def faa_nviews(driver):
    driver.get("http://fineartamerica.com/profiles/" + faa_profile + ".html")
    nviews = ""
    elems = driver.find_elements(By.XPATH,'//p')
    viewfound = False
    for elem in elems:
        # puts("p",elem.text)
        if viewfound == False and elem.text == u'VIEWS:':
            viewfound = True
        elif viewfound == True:
            nviews = elem.text
            break
    return nviews

#
# format faa stats into xml string
#
def faa_xmlstats(nviews,nfollowers,nvisitors,timestamp):
    xmlcontent = "<fineartamerica nviews=\"" + nviews + "\" nfollowers=\"" + nfollowers + "\" nvisitors=\"" + nvisitors + "\" timestamp=\"" + timestamp + "\">\n"
    xmlcontent = xmlcontent + "</fineartamerica>\n"
    return xmlcontent

#
# fetch faa stats and dump them into xml file
#
def faa_dump(faa_username,faa_password,faa_profile,xmloutputfilepath):

    # create selenium webdriver
    driver = webdriver.Firefox()

    # faa login
    driver = faa_login(driver, faa_username, faa_password)

    # get stats
    nvisitors  = faa_nvisitors(driver)
    nfollowers = faa_nfollowers(driver)
    nviews     = faa_nviews(driver)

    driver.close()

    # format output content
    xmlcontent = faa_xmlstats(nviews,nfollowers,nvisitors,str(time.time()))

    # dump xml into xmloutputfilepath
    output=open(xmloutputfilepath, 'w+')
    output.write(xmlcontent.encode('utf8'))
    output.close()
    


