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
    for i in range(int(30)):
        time.sleep(2)

        # get instagram link
        #linkpin = driver.find_elements(By.XPATH, '//link[@rel="canonical"]')[0]
        #link = pin.linkget_attribute("href")
        link = "/".join(driver.current_url.split("/")[:-1])
        
        # get title and nfavs
        pins = driver.find_elements(By.XPATH, '//span')
        isnumberoflikes = False
        istitle = False
        title = "Unknown"
        nlikes = "Unknown"
        
        for pin in pins:
            # puts("pin text " + pin.text.encode('utf-8'))
        
            if isnumberoflikes:
                nlikes = pin.text.encode('utf-8').split()[0]
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

            if pin.text.encode('utf-8') == "likes":
                # next is title
                istitle = True

        puts("pin title " + title)
        # puts("pin title " + title + " nlikes " + nlikes + " link " + link)

        content.append("** " + title)
        content.append("instagram_nlikes : " + nlikes)
        content.append("instagram_link : " + link)
        
        press('enter')

    driver.close()
    
    os.system("taskkill /f /im chromedriver.exe")
    
    fput(orgoutputfilepath,"\n".join(content))
    
    

def test():
    instagram_dump("julleor","instagram.org")

test()
    

