__author__ = 'jpatdalton'

import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import columns

def get_details(worksheet, indices, end):
    driver = webdriver.Firefox()
    url = 'http://www.billboard.com/biz/charts/the-billboard-hot-100'
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html)
    driver.close()
    titles = soup.select(".details")
    col_writers = columns.writers
    col_producers = columns.producers
    col_label = columns.label
    cell_list_writers = worksheet.range(col_writers+'2:'+col_writers+str(end))
    cell_list_producers = worksheet.range(col_producers+'2:'+col_producers+str(end))
    cell_list_labels = worksheet.range(col_label+'2:'+col_label+str(end))

    writers = list()
    producers = list()
    labels = list()
    n=0
    for title in titles:
        try:
            arr = title.get_text().split('\n')
            text = arr[len(arr)-2].strip()
            text1 = text.split('(')
            producers.append(text1[0].strip())
            text2 = text1[1].split(')')
            writers.append(text2[0])
            text3 = text2[1].split()
            labels.append(' '.join(text3))
        except Exception, e:
            print e, 'Billboard Biz'
        n+=1
    print len(writers), len(producers), len(labels)
    n=0
    for ind in indices:
        try:
            cell_list_writers[ind].value = writers[n]
            cell_list_producers[ind].value = producers[n]
            cell_list_labels[ind].value = labels[n]
        except Exception, e:
            print e, 'Billboard Biz'

        n+=1


    worksheet.update_cells(cell_list_writers)
    worksheet.update_cells(cell_list_producers)
    worksheet.update_cells(cell_list_labels)

def get_writers_producers_labels():
    driver = webdriver.Firefox()
    url = 'http://www.billboard.com/biz/charts/the-billboard-hot-100'
    driver.get(url)
    time.sleep(11)
    login = driver.find_element_by_link_text('Log In')
    login.click()
    time.sleep(5)
    name = driver.find_element_by_id('edit-name')
    name.send_keys('steve@zeitlosent.com')
    time.sleep(1)
    password = driver.find_element_by_id('edit-pass')
    password.send_keys('steve')
    time.sleep(1)
    password.send_keys(Keys.ENTER)
    time.sleep(11)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    html = driver.page_source
    soup = BeautifulSoup(html)
    driver.close()
    titles = soup.select(".details")
    writers = list()
    producers = list()
    labels = list()
    n=0
    for title in titles:
        try:
            arr = title.get_text().split('\n')
            text = arr[len(arr)-2].strip()
            text1 = text.split('(')
            producers.append(text1[0].strip())
            text2 = text1[1].split(')')
            writers.append(text2[0])
            text3 = text2[1].split()
            labels.append(' '.join(text3))
        except Exception, e:
            print e, 'Billboard Biz'
        n+=1
    print len(writers), len(producers), len(labels)
    return writers, producers, labels