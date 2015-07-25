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
# dump faa stats into xml file
#
def faa_dump(username,password,faa_profile,filepath):
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.implicitly_wait(3)

    
    driver.get("https://fineartamerica.com/loginartist.php")

    elem = driver.find_element_by_name("username")
    elem.send_keys(username)
    elem.send_keys(Keys.RETURN)
    elem = driver.find_element_by_name("password")
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)

    # get nvisitors
    driver.get("http://fineartamerica.com/controlpanel/statistics.html?tab=visitors")
    nvisitors = "-1"
    elems = driver.find_elements(By.XPATH, '//p')
    for elem in elems:
        text = elem.text
        items = text.split(" ")
        if len(items) > 2 and items[0] == "Total" and items[1] == "Visitors:":
            nvisitors = items[2]
            break

    # get nfollowers
    driver.get("http://fineartamerica.com/profiles/" + faa_profile + ".html")

    nfollowers = "-1"
    elems = driver.find_elements(By.XPATH,'//a')
    for elem in elems:
        # puts("a href",elem.get_attribute("href"))
        if elem.get_attribute("href") == u"http://fineartamerica.com/profiles/" + profiles + ".html?tab=watchlist&type=others":
            nfollowers = elem.text
            break

    # get nviews
    nviews = "-1"
    elems = driver.find_elements(By.XPATH,'//p')
    viewfound = False
    for elem in elems:
        # puts("p",elem.text)
        if viewfound == False and elem.text == u'VIEWS:':
            viewfound = True
        elif viewfound == True:
            nviews = elem.text
            break

    content = "<fineartamerica nviews=\"" + nviews + "\" nfollowers=\"" + nfollowers + "\" nvisitors=\"" + nvisitors + "\" timestamp=\"" + str(time.time()) + "\">\n"
    content = content + "</fineartamerica>\n"

    output=open(filepath, 'w+')
    output.write(content.encode('utf8'))
    output.close()
    driver.close()
    


