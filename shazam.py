__author__ = 'jpatdalton'

import urllib2
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import oauth
import columns


def shazam_search(titles, worksheet, indices, end):
    url_zams = 'http://www.shazam.com/charts/top-100/united-states'
    response = urllib2.urlopen(url_zams)
    html = response.read()
    soup = BeautifulSoup(html)

    col = columns.shazams
    cell_list_zams = worksheet.range(col+'2:'+col+end)
    col = columns.shazam_chart_pos
    cell_list_chart_pos = worksheet.range(col+'2:'+col+end)
    n=0
    driver = webdriver.Firefox()
    for ind in indices:
        current_song = titles[n]
        index = len(current_song)
        found = 1
        while(found):
            try:
                zams = soup.find(text=re.compile(current_song+"*")).parent.parent.parent.parent.span.string
                cell_list_zams[ind].value = zams
                chart_pos = 'Not Charted'
                try:
                    chart_pos = soup.find(text = re.compile(current_song+"*")).parent.parent.parent.parent.attrs['data-chart-position']
                except Exception, e:
                    print e, 'Error in getting chart position - ' + current_song
                cell_list_chart_pos[ind].value = chart_pos
                found = 0
            except Exception, e:
                try:
                    cell_list_zams[ind].value = scrape(current_song, driver)
                    cell_list_chart_pos[ind].value = 'Not Charted'
                except Exception, e:
                    print e, 'Error in scrape in Shazam on song ' + current_song
                print e, ' [' + current_song[0:index] + ']'
                index -= 1
                found = 0
        #if (n == 50):
        #    worksheet.update_cells(cell_list_zams)
        #    cell_list_zams = worksheet.range('H3:H'+end)
        n+=1
    try:
        worksheet.update_cells(cell_list_zams)
        worksheet.update_cells(cell_list_chart_pos)
    except Exception, e:
        print e, 'SHAZAM'
        # many exceptions result from an closed connection 'bad status line', try again
        wkst = oauth.open_spreadsheet()
        wkst.update_cells(cell_list_zams)
        wkst.update_cells(cell_list_chart_pos)
    driver.close()

def get_id(title):
    the_id = ''
    try:
        driver = webdriver.Firefox()
        driver.get("http://www.shazam.com/search/"+title)
        time.sleep(2)
        pat = driver.page_source
        soup = BeautifulSoup(pat)
        data = soup.find_all(href=re.compile("www.shazam.com/track/"))[0]["href"]
        the_id = data.split('/')[4]
    except Exception, e:
        print e, 'Shazam ids - ', title
    finally:
        driver.close()
    return the_id

def scrape(title, driver):

    driver.get("http://www.shazam.com/search")
    inputs = driver.find_elements(By.TAG_NAME, "input")
    input = inputs[2]
    input.send_keys(title)
    time.sleep(1.5)
    input.submit()
    time.sleep(3)
    pat = driver.page_source
    soup = BeautifulSoup(pat)
    data = soup.find_all(href=re.compile("shazam.com/track/"))[0]
    link = data.get("href")
    return lookup_zams(link)

def lookup_zams(link):
    url_zams = link
    response = urllib2.urlopen(url_zams)
    html = response.read()
    soup = BeautifulSoup(html)
    data1 = soup.select(".trd-tag-count")[0].span.text
    return data1



