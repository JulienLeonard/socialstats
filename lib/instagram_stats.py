from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import selenium
import os
import sys
import time
import win32api, win32con
from win32key import *
from basics import *
from timeutils import *

def instagram_get_current_post_data(driver):
    # get instagram link
    #linkpin = driver.find_elements(By.XPATH, '//link[@rel="canonical"]')[0]
    #link = pin.linkget_attribute("href")
    # get title and nfavs
    pins = driver.find_elements(By.XPATH, '//span')
    isnumberoflikes = False
    istitle = False
    title = "Unknown"
    nlikes = "Unknown"
        
    for pin in pins:
        # puts("pin text " + pin.text.encode('utf-8'))
        
        if isnumberoflikes:
            pieces = pin.text.encode('utf-8').split()
            if len(pieces) > 0:
                nlikes = pieces[0]
            else:
                nlikes = "0"
            isnumberoflikes = False
                
        if istitle:
            pieces = pin.text.encode('utf-8').split()
            title = []
            for piece in pieces:
                if not piece[0] == "#":
                    title.append(piece)
                else:
                    break
            title = " ".join(title)
            istitle = False
            
        if pin.text.encode('utf-8') == "Follow":
            # next is number of likes
            isnumberoflikes = True

        if pin.text.encode('utf-8') == "likes" or pin.text.encode('utf-8') == "like this":
            # next is title
            istitle = True

    link = "/".join(driver.current_url.split("/")[:-1])
    # puts("link",link)
            
    title = title.decode("utf-8")
    # puts("pin title " + title)
    puts("pin title " + title + " nlikes " + nlikes + " link " + link)
    return (title,nlikes,link)
    

def instagram_dump(instagram_username,orgoutputfilepath):

    os.system("taskkill /f /im chromedriver.exe")

    content = ["* Instagram"]
    
    # create selenium webdriver
    driver = webdriver.Chrome('C:/Home/chromedriver.exe')

    driver.get("https://www.instagram.com/" + instagram_username + "/")
    time.sleep(2)
    
    # get number of posts
    pins = driver.find_elements(By.XPATH, '//span')
    nfollowers = None
    nposts = None
    
    for pin in pins:
        # puts("pin text " + pin.text.encode('utf-8'))
        pieces = pin.text.encode('utf-8').split()
        if len(pieces) > 1:
            if pieces[1] == "posts":
                nposts = pieces[0]
            if pieces[1] == "followers":
                nfollowers = pieces[0]

    content.append("nposts : " + nposts)
    content.append("nfollowers : " + nfollowers)
    puts("nposts",nposts,"nfollowers",nfollowers)

    # go through all the posts
    press('tab')
    press('tab')
    press('tab')
    press('enter')


    # for i in range(int(nposts)):
    for i in range(int(40)):
        time.sleep(2)

        (title,nlikes,link) = instagram_get_current_post_data(driver)

        content.append("** " + title)
        content.append("instagram_nlikes : " + nlikes)
        content.append("instagram_link : " + link)
        
        press('enter')

    driver.close()
    
    os.system("taskkill /f /im chromedriver.exe")
    
    fput(orgoutputfilepath,"\n".join(content).encode("utf-8"))
    
    

def test():
    from distimport import *
    mmydb = distimport("c:/PROJECTS/MYDB","mydb")
    #import sys
    #sys.path.append("c:/PROJECTS/MYDB")
    #from mydb import *
    mydb = mmydb.MYDB()
    userid         = mydb.property("INSTAGRAM-USERID")
    outputstatsdir = mydb.property("STATS-OUTPUTDIR")
    puts("userid",userid,"outputstatsdir",outputstatsdir)

    
    newstatdirpath = outputstatsdir + "/instagram." + date4filename(utcnow())
    if not os.path.exists(newstatdirpath):
        os.makedirs(newstatdirpath)
    
    instagram_dump(userid, newstatdirpath + "/instagram." + date4filename(utcnow()) + ".org")

    # driver = webdriver.Chrome('C:/Home/chromedriver.exe')

    # driver.get("https://www.instagram.com/p/BEdbIk0SlKg/?taken-by=julleor")
    # time.sleep(2)

    # (title,nlikes,link) = instagram_get_current_post_data(driver)

    # # puts("title " + title.decode("utf-8") + " nlikes " + nlikes + " link " + link)

    # content = ["toto titi"]
    # content.append("title " + title + " nlikes " + nlikes + " link " + link)
    # puts("content","\n".join(content))

    # fput("sandbox.org","\n".join(content).encode("utf-8"))
    

test()
    

