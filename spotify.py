__author__ = 'jpatdalton'

import spotipy
import columns
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import math
url = 'http://www.spotify.com'

def spotify_search(titles, worksheet, indices, end):
    sp = spotipy.Spotify()
    col = columns.spotify_popularity
    cell_list_streams = worksheet.range(col+'2:'+col+end)
    n=0
    for ind in indices:
        results = sp.search(q=titles[n], limit=1)
        cell_list_streams[ind].value = results['tracks']['items'][0]['popularity']
        n+=1
    worksheet.update_cells(cell_list_streams)

def get_artist_id(name):
    the_id = ''
    try:
        sp = spotipy.Spotify()
        results = sp.search(q='artist:' + name, type='artist')
        the_id = results['artists']['items'][0]['id']
    except Exception, e:
        print e, 'Cant get Spotify artist id = ' + name
    return the_id


def get_id(title):
    the_id = ''
    try:
        sp = spotipy.Spotify()
        results = sp.search(q=title, limit=1)
        the_id = results['tracks']['items'][0]['id']
    except Exception, e:
        print e, 'Cant get Spotify id = ' + title
    return the_id

def get_popularity(id):
    popularity = -1
    try:
        url = 'https://api.spotify.com/v1/tracks/' + id
        data = requests.get(url).json()
        popularity = data["popularity"]
    except Exception, e:
        print e, 'Cant get Spotify id1 = ' + id
    return popularity

def login():
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(2)
    login = driver.find_element_by_class_name('user-link')
    login.click()
    time.sleep(3)
    name = driver.find_element_by_id('login-username')
    name.send_keys("patrick@theflowtilla.com")
    time.sleep(2.1)
    password = driver.find_element_by_id('login-password')
    password.send_keys('easypassword')
    time.sleep(1)
    password.send_keys(Keys.ENTER)
    time.sleep(3)
    driver.get("https://www.spotify.com/us/redirect/webplayer/?utm_source=www.spotify.com&utm_medium=www_footer")
    time.sleep(3)
    return driver



def get_streams(driver, title, artist_id):
    the_streams = 0

    try:
        driver.get("https://play.spotify.com/artist/" + artist_id)
        time.sleep(7)
        iframe = driver.find_elements_by_id('main')
        driver.switch_to_frame(iframe[0])
        time.sleep(3)
        iframe1 = driver.find_elements_by_id('app-artist')
        driver.switch_to_frame(iframe1[0])
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source)
        streams = soup.select(".tl-listen-count")
        songs = soup.select(".tl-highlight")
        print '### ', title

        n=1 # streams start at index 1, there is nothing in the first
        flag = 0
        tilt = title.lower()
        for song in songs:
            print n, song.text.lower()
            if tilt in song.text.lower():
                break
            n+=1
            if n == (len(songs)+1):
                flag = 1
                break
                #raise Exception(title)
                print 'CRITICAL ERROR IN SPOTIFY STREAMS'

        if flag:
            n=1
            size = len(tilt)
            mid = math.trunc(int(size/2))
            for song in songs:
                print n, song.text.lower()
                if tilt[0:mid] in song.text.lower():
                    break
                if tilt[mid:size] in song.text.lower():
                    break
                n+=1
                if n == (len(songs)+1):
                    break
        the_streams = int(streams[n].text.replace(',',''))
    except Exception, e:
        print e, 'spotify streams 1 ', title, artist_id

    return the_streams

