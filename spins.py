__author__ = 'jpatdalton'

import urllib2
from bs4 import BeautifulSoup
import re
import columns
from datetime import date
import datetime

def get_spins(main_artists, song_titles, worksheet, indices, end):
    today = date.today()
    yesterday = date.today() - datetime.timedelta(days = 1)
    week_ago = date.today() - datetime.timedelta(days = 7)
    fd = week_ago.strftime("%Y%m%d")
    td = today.strftime("%Y%m%d")

    url_spins = 'http://kworb.net/radio/'
    response = urllib2.urlopen(url_spins)
    html = response.read()
    pop_soup = BeautifulSoup(html)

    url_spins = 'http://kworb.net/airadio/'
    response = urllib2.urlopen(url_spins)
    html = response.read()
    soup = BeautifulSoup(html)

    url_spins = 'http://kworb.net/radio/urban/archives/' + td + '.html'
    response = urllib2.urlopen(url_spins)
    html = response.read()
    urban_soup = BeautifulSoup(html)

    url_spins = 'http://kworb.net/radio/rhythmic/archives/' + td + '.html'
    response = urllib2.urlopen(url_spins)
    html = response.read()
    rhythmic_soup = BeautifulSoup(html)

    url_spins = 'http://kworb.net/airadio/archives/' + fd + '.html'
    response = urllib2.urlopen(url_spins)
    html = response.read()
    soup_lw = BeautifulSoup(html)

    col = columns.spins
    col_audience = columns.audience
    col_spins_pos = columns.spins_pos
    col_spins_days = columns.spins_days
    col_spins_pop_pos = columns.spins_pop_pos
    col_spins_pop = columns.spins_pop
    col_spins_rhythmic = columns.spins_rhythmic
    col_spins_urban = columns.spins_urban
    col_spins_itunes = columns.itunes_chart_pos

    cell_list_spins = worksheet.range(col+'2:'+col+end)
    cell_list_aud = worksheet.range(col_audience+'2:'+col_audience+end)
    cell_list_spins_pos = worksheet.range(col_spins_pos+'2:'+col_spins_pos+end)
    cell_list_spins_days = worksheet.range(col_spins_days+'2:'+col_spins_days+end)
    cell_list_spins_pop_pos = worksheet.range(col_spins_pop_pos+'2:'+col_spins_pop_pos+end)
    cell_list_pop = worksheet.range(col_spins_pop+'2:'+col_spins_pop+end)
    cell_list_rhythmic = worksheet.range(col_spins_rhythmic+'2:'+col_spins_rhythmic+end)
    cell_list_urban = worksheet.range(col_spins_urban+'2:'+col_spins_urban+end)
    cell_list_itunes = worksheet.range(col_spins_itunes+'2:'+col_spins_itunes+end)

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

                spins = indx[6].get_text()

                cell_list_spins_pos[indice].value = indx[0].get_text()
                cell_list_spins[indice].value = spins
                cell_list_aud[indice].value = indx[4].get_text()

                cell_list_itunes[indice].value = indx[8].get_text()

                ind_lw = soup_lw.find(text = re.compile(current_song[0:index]+"*")).parent.parent.parent

                indx_lw = ind_lw.find_all("td")
                spins_lw = indx_lw[6].get_text()
                cell_list_spins_lw[indice].value = spins_lw
                diff = int(spins) - int(spins_lw)
                if diff > 0:
                    diff = "'+" + str(diff)
                cell_list_spins_diff[indice].value = diff

                try:
                    ind_pop = pop_soup.find(text = re.compile(current_song[0:index]+"*")).parent.parent.parent
                    indx_pop = ind_pop.find_all("td")
                    cell_list_spins_pop_pos[indice].value = indx_pop[0].get_text()
                    cell_list_pop[indice].value = indx_pop[4].get_text()
                    cell_list_spins_days[indice].value = indx_pop[10].get_text()
                except Exception, e:
                    print e, 'pop'
                try:
                    ind_urban = urban_soup.find(text = re.compile(current_song[0:index]+"*")).parent.parent.parent
                    indx_urban = ind_urban.find_all("td")
                    cell_list_urban[indice].value = indx_urban[4].get_text()
                except Exception, e:
                    print e, 'urban'
                try:
                    ind_rhythmic = rhythmic_soup.find(text = re.compile(current_song[0:index]+"*")).parent.parent.parent
                    indx_rhythmic = ind_rhythmic.find_all("td")
                    cell_list_rhythmic[indice].value = indx_rhythmic[4].get_text()
                except Exception, e:
                    print e, 'rhythmic'

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
    worksheet.update_cells(cell_list_spins_pop_pos)
    worksheet.update_cells(cell_list_pop)
    worksheet.update_cells(cell_list_rhythmic)
    worksheet.update_cells(cell_list_urban)
    worksheet.update_cells(cell_list_itunes)

