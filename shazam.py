__author__ = 'jpatdalton'

import urllib2
from bs4 import BeautifulSoup
import re


def shazam_search(titles, worksheet):
    url_zams = 'http://www.shazam.com/charts/top-100/united-states'
    response = urllib2.urlopen(url_zams)
    html = response.read()
    soup = BeautifulSoup(html)


    cell_list_zams = worksheet.range('I3:I102')

    for n in xrange(100):
        current_song = titles[n]
        index = len(current_song)
        found = 1
        while(found):
            try:
                #ind = soup.find(text = re.compile(current_song[0:index]+"*")).parent.parent.parent
                zams = soup.find(text=re.compile(current_song+"*")).parent.parent.parent.parent.span.string

                cell_list_zams[n].value = zams
                found = 0
            except Exception, e:
                print e, ' [' + current_song[0:index] + ']'
                index -= 1
                found = 0
    # Update in batch
    worksheet.update_cells(cell_list_zams)