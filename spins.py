__author__ = 'jpatdalton'

import urllib2
from bs4 import BeautifulSoup
import re
import columns
from datetime import date
import datetime

def get_spins(main_artists, song_titles, worksheet, indices, end):
    url_spins = 'http://kworb.net/radio/'
    response = urllib2.urlopen(url_spins)
    html = response.read()
    soup = BeautifulSoup(html)

    week_ago = date.today() - datetime.timedelta(days = 7)
    fd = week_ago.strftime("%Y%m%d")
    url_spins = 'http://kworb.net/radio/pop/archives/' + fd + '.html'
    response = urllib2.urlopen(url_spins)
    html = response.read()
    soup_lw = BeautifulSoup(html)

    col = columns.spins
    col_audience = columns.audience
    col_spins_pos = columns.spins_pos
    col_spins_days = columns.spins_days

    cell_list_spins = worksheet.range(col+'2:'+col+end)
    cell_list_aud = worksheet.range(col_audience+'2:'+col_audience+end)
    cell_list_spins_pos = worksheet.range(col_spins_pos+'2:'+col_spins_pos+end)
    cell_list_spins_days = worksheet.range(col_spins_days+'2:'+col_spins_days+end)

    col_spins_lw = columns.spins_last_week
    col_spins_diff = columns.spins_diff
    cell_list_spins_lw = worksheet.range(col_spins_lw+'2:'+col_spins_lw+end)
    cell_list_spins_diff = worksheet.range(col_spins_diff+'2:'+col_spins_diff+end)


    n=0
    for indice in indices:
        current_song = song_titles[n]
        index = len(current_song)
        found = 1
        while(found):
            if index<4:
                found = 0
                print 'Cant find the spins for [' + current_song + ']'
                break
            try:
                ind = soup.find(text = re.compile(current_song[0:index]+"*")).parent.parent.parent

                print str(len(ind)) + ' - [' + current_song + ']'
                #if len(ind) > 1:
                #    print 'Too many returns for [' + current_song + ']'
                    #search for artist in the line
                indx = ind.find_all("td")

                spins = indx[4].get_text()

                cell_list_spins_pos[indice].value = indx[0].get_text()
                cell_list_spins[indice].value = spins
                cell_list_aud[indice].value = indx[8].get_text()
                cell_list_spins_days[indice].value = indx[10].get_text()

                ind_lw = soup_lw.find(text = re.compile(current_song[0:index]+"*")).parent.parent.parent

                indx_lw = ind_lw.find_all("td")
                spins_lw = indx_lw[4].get_text()
                cell_list_spins_lw[indice].value = spins_lw
                diff = int(spins) - int(spins_lw)
                if diff > 0:
                    diff = "'+" + str(diff)
                cell_list_spins_diff[indice].value = diff

                found = 0
            except Exception, e:
                print e, ' [' + current_song[0:index] + ']'
                index -= 1
                found = 0
        n+=1
    # Update in batch
    worksheet.update_cells(cell_list_spins)
    worksheet.update_cells(cell_list_aud)
    worksheet.update_cells(cell_list_spins_pos)
    worksheet.update_cells(cell_list_spins_days)
    worksheet.update_cells(cell_list_spins_diff)
    worksheet.update_cells(cell_list_spins_lw)

