#!/usr/bin/env python
# Automate Facebook Posting 
# Auther: Tauseed Zaman

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4
from bs4 import BeautifulSoup as soup 
from urllib.request import Request, urlopen
from time import sleep
import requests

#getting news from different pakistani's websites

# get latest news from DailyPakistan
def get_DailyPakistan_News():
    html_text=requests.get("https://en.dailypakistan.com.pk/latest").text
    soupp = soup(html_text, 'lxml')
    main_container = soupp.find_all("div",{'class':["col-xs-12 col-sm-4 col-lg-3 verticle-widget-col news3"]})
    output=[]
    for i,item in enumerate(main_container):
       heading = item.find("small").text
       link = item.find("a").get("href")
       output.append({heading,link})
    return output

#get news from thenews.com.pk
def get_TheNews_News():
    html_text=requests.get("https://www.thenews.com.pk/latest-stories").text
    soupp = soup(html_text, 'lxml')
    main_container = soupp.find_all("div",{'class':["writter-list-item-story"]})
    output = []
    for i,item in enumerate(main_container):
        heading = item.find("h2").text.strip()
        link = item.find("a").get("href")
        output.append(heading,link)
        i=i+1
    return output

# get news from geo news
def get_Geo_News():
    html_text=requests.get("https://www.geo.tv/").text
    soupp = soup(html_text, 'lxml')
    main_container = soupp.find_all("article")
    output = []
    for i,item in enumerate(main_container):
        a_tage = item.find("a")
        output.append(a_tage.text.strip(),a_tage.get('href'))
    return output

#fetching hashtags for facebook post
def hashtags(hash_idea):
    url = 'http://best-hashtags.com/hashtag/' + hash_idea

    try:
        req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
        page = urlopen(req, timeout=10)
        page_html = page.read()
        page.close()
        page_soup = soup(page_html, 'html.parser')
        result = page_soup.find('div',{'class':'tag-box tag-box-v3 margin-bottom-40'})
        tags = result.decode()
        start_index = tags.find('#')
        end_index = tags.find('</p1>')
        tags = tags[start_index:end_index]

        return tags
    except:
        print('Something went wrong While Fetching hashtags')


# login to facebook account
def login(username, password):
    try:
        url = 'https://facebook.com'
        driver.get(url)
        user = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.NAME, 'email')))
        user.send_keys(username)
        pas = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.NAME, 'pass')))
        pas.send_keys(password)
        login_btn = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.NAME,'login')))
        login_btn.click()

    except:
        print('Something went wrong while login process')



def post(caption):
    for post_link,post_title in caption:
        try:
            # click on + button
            add = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[2]/div[4]/div[1]/div[3]/div[2]/span/div/i')))
            add.click()
            # click on post
            click_add_post = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[2]/div[4]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div[2]/div[1]/div/div[1]/div[2]/div/div/div/div[1]/span')))
            click_add_post.click()

            sleep(5)
            print(caption)
            # select text box
            cap = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[11]/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div/div/div[2]/div/div/div/div')))
            cap.send_keys(post_title)
            cap.send_keys(post_link)
                
            sleep(5) # this is mandatory while doing some thing with bot
            btn_post = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[11]/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div/div[3]/div[2]/div/div/div[1]/div/span/span')))
            btn_post.click()
            sleep(5)
        except:
            print('Something Went Wrong While posting ')

    
if __name__== "__main__":
    #turn for credentials, driver, and caption
    username = "" #input('ENTER USERNAME : ')
    password = "" #input('ENTER PASSWORD : ')
    hash_idea = "" #input('ENTER ONE HASH : ')
    driver = webdriver.Chrome("path to chrome driver")
    login(username,password)
    post(get_DailyPakistan_News())