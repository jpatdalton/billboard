__author__ = 'jpatdalton'

import urllib2
from bs4 import BeautifulSoup
import re
import columns
from datetime import date
import datetime
from my_models import Track

'''
pat = driver.page_source
driver.get(url_spins)
url_spins = 'https://play.spotify.com/artist/137W8MRPWKqSmrBGDBFSop'
response = urllib2.urlopen(url_spins)
html = response.read()
pop_soup = BeautifulSoup(html)
'''

today = date.today()
yesterday = date.today() - datetime.timedelta(days = 1)
week_ago = date.today() - datetime.timedelta(days = 7)
fd = week_ago.strftime("%Y%m%d")
td = today.strftime("%Y%m%d")
yd = yesterday.strftime("%Y%m%d")

url_spins = 'http://kworb.net/radio/'
response = urllib2.urlopen(url_spins)
html = response.read()
pop_soup = BeautifulSoup(html)

url_spins = 'http://kworb.net/airadio/'
response = urllib2.urlopen(url_spins)
html = response.read()
soup = BeautifulSoup(html)
try:
    url_spins = 'http://kworb.net/radio/urban/archives/' + td + '.html'
    response = urllib2.urlopen(url_spins)
    html = response.read()
    urban_soup = BeautifulSoup(html)
except Exception, e:
    print e, 'Couldnt get archived spins'
    td = yd
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

def get_spins(main_artists, song_titles, worksheet, indices, end):
    '''
    today = date.today()
    yesterday = date.today() - datetime.timedelta(days = 1)
    week_ago = date.today() - datetime.timedelta(days = 7)
    fd = week_ago.strftime("%Y%m%d")
    td = today.strftime("%Y%m%d")
    yd = yesterday.strftime("%Y%m%d")

    url_spins = 'http://kworb.net/radio/'
    response = urllib2.urlopen(url_spins)
    html = response.read()
    pop_soup = BeautifulSoup(html)

    url_spins = 'http://kworb.net/airadio/'
    response = urllib2.urlopen(url_spins)
    html = response.read()
    soup = BeautifulSoup(html)
    try:
        url_spins = 'http://kworb.net/radio/urban/archives/' + td + '.html'
        response = urllib2.urlopen(url_spins)
        html = response.read()
        urban_soup = BeautifulSoup(html)
    except Exception, e:
        print e, 'Couldnt get archived spins'
        td = yd
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
    '''
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

#def get_soups():

    #return pop_soup, soup, urban_soup, rhythmic_soup, soup_lw

def find_in_soup(title):
    results = [None] * 11
    current_song = title
    try:
        ind = soup.find(text = re.compile(current_song+"*")).parent.parent.parent

        #print str(len(ind)) + ' - [' + current_song + ']'
        indx = ind.find_all("td")

        spins = indx[6].get_text()

        results[0] = indx[0].get_text()
        results[1] = spins
        results[10] = indx[4].get_text()

        results[9] = indx[8].get_text()

        ind_lw = soup_lw.find(text = re.compile(current_song+"*")).parent.parent.parent

        indx_lw = ind_lw.find_all("td")
        spins_lw = indx_lw[6].get_text()
        results[2] = spins_lw
        diff = int(spins) - int(spins_lw)
        #if diff > 0:
            #diff = "'+" + str(diff)
        results[3] = diff

        try:
            ind_pop = pop_soup.find(text = re.compile(current_song+"*")).parent.parent.parent
            indx_pop = ind_pop.find_all("td")
            results[4] = indx_pop[0].get_text()
            results[5] = indx_pop[4].get_text()
            results[8] = indx_pop[10].get_text()
        except Exception, e:
            {}
            #print e, 'pop'
        try:
            ind_urban = urban_soup.find(text = re.compile(current_song+"*")).parent.parent.parent
            indx_urban = ind_urban.find_all("td")
            results[7] = indx_urban[4].get_text()
        except Exception, e:
            {}
            #print e, 'urban'
        try:
            ind_rhythmic = rhythmic_soup.find(text = re.compile(current_song+"*")).parent.parent.parent
            indx_rhythmic = ind_rhythmic.find_all("td")
            results[6] = indx_rhythmic[4].get_text()
        except Exception, e:
            {}
            #print e, 'rhythmic'

        found = 0
    except Exception, e:
        print e, ' [' + current_song + '] FIXME $$$'

    return results

def update_tracks(track_ids, session):
    for track_id in track_ids:
        track = session.query(Track).get(track_id.id)
        if track.spins_id is not None:
            title = track.spins_id
        else:
            title = track.title
        spins_results = find_in_soup(title)
        if len(spins_results) is not 0:
            if spins_results[0] is not None:
                track.radio_position = int(spins_results[0])
            else:
                track.radio_position = 0
            if spins_results[1] is not None:
                track.spins = int(spins_results[1])
            else:
                track.spins = 0
            if spins_results[2] is not None:
                track.spins_lw = int(spins_results[2])
            else:
                track.spins_lw = 0
            if spins_results[3] is not None:
                track.spins_diff = int(spins_results[3])
            else:
                track.spins_diff = 0
            if spins_results[4] is not None:
                track.spins_pop_pos = str(spins_results[4])
            else:
                track.spins_pop_pos = '--'
            if spins_results[5] is not None:
                track.spins_pop = str(spins_results[5])
            else:
                track.spins_pop = '--'
            if spins_results[6] is not None:
                track.spins_rhythmic = str(spins_results[6])
            else:
                track.spins_rhythmic = '--'
            if spins_results[7] is not None:
                track.spins_urban = str(spins_results[7])
            else:
                track.spins_urban = '--'
            if spins_results[8] is not None:
                track.radio_days = int(spins_results[8])
            else:
                track.radio_days = 0
            if spins_results[9] is not None:
                track.itunes_chart_pos = str(spins_results[9])
            else:
                track.itunes_chart_pos = '--'
            if spins_results[10] is not None:
                track.radio_audience = spins_results[10]
            else:
                track.radio_audience = 0
            #track.days_from_release = track.days_from_release + 1
            session.add(track)

    #return radio_position, spins, spins_lw, spins_diff, spins_pop_pos, spins_pop, spins_rhythmic, spins_urban, radio_days, itunes_chart_pos