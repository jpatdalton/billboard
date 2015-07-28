__author__ = 'jpatdalton'

from splinter import Browser
import time
from bs4 import BeautifulSoup
import codecs

browser = Browser()
url = 'http://play.spotify.com'
browser.visit(url)
time.sleep(2)
button = browser.find_by_id('has-account')
button.click()
time.sleep(1)
browser.fill('username', 'patrick@theflowtilla.com')
browser.fill('password', 'easypassword')
buttons = browser.find_by_css('button')
visible_buttons = [button for button in buttons if button.visible]
login_button = visible_buttons[-1]
login_button.click()
time.sleep(1)
browser.visit('https://play.spotify.com/artist/5YGY8feqx7naU7z4HrwZM6')
time.sleep(30)

CORRECT_FRAME_INDEX = 6
with browser.get_iframe(CORRECT_FRAME_INDEX) as iframe:
    html = iframe.html
    soup = BeautifulSoup(html)
    output = soup.prettify()
    with codecs.open('test.html', 'w', 'utf-8') as output_f:
        output_f.write(output)
browser.quit()