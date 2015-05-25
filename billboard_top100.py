__author__ = 'jpatdalton'

import urllib2
from bs4 import BeautifulSoup
import re
import oauth
import youtube
import spotify
import shazam
import myfacebook
import instagram
import mytwitter
import vine

def get_top100():

    url = 'http://www.billboard.com/charts/hot-100'
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)

    titles = soup.select(".row-title")
    song_titles = list()
    song_artists = list()
    for title in titles:
        song_titles.append(title.find("h2").get_text().strip())
        song_artists.append(title.find("h3").get_text().strip())
    main_artists = list()
    for artist in song_artists:
        refined_name = artist.lower().split('featuring')[0]
        refined_name = refined_name.split('&')[0]
        refined_name = refined_name.split(' with ')[0]
        main_artists.append(refined_name)
        print 'Refined name = ' + refined_name
    return main_artists, song_titles


def get_spins(main_artists, song_titles, worksheet):
    url_spins = 'http://kworb.net/airadio/'
    response = urllib2.urlopen(url_spins)
    html = response.read()
    soup = BeautifulSoup(html)
    d0 = soup.select(".d0")
    d1 = soup.select(".d1")

    cell_list_spins = worksheet.range('D3:D102')
    cell_list_aud = worksheet.range('E3:E102')


    for n in xrange(100):
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
                cell_list_spins[n].value = indx[6].get_text()
                cell_list_aud[n].value = indx[4].get_text()
                found = 0
            except Exception, e:
                print e, ' [' + current_song[0:index] + ']'
                index -= 1
    # Update in batch
    worksheet.update_cells(cell_list_spins)
    worksheet.update_cells(cell_list_aud)

def put_titles_and_artists(artists, titles, worksheet):
    # Select a range
    cell_list_titles = worksheet.range('B3:B102')
    cell_list_artists = worksheet.range('C3:C102')

    for n in xrange(100):
        cell_list_titles[n].value = artists[n]
        cell_list_artists[n].value = titles[n]


    # Update in batch
    worksheet.update_cells(cell_list_titles)
    worksheet.update_cells(cell_list_artists)


    worksheet.acell('B4').value

def run_the_jewels():
    worksheet = oauth.open_worksheet()
    artists, titles = get_top100()
    #put_titles_and_artists(artists, titles, worksheet)
    #get_spins(artists, titles, worksheet)
    #youtube.youtube_search(titles, worksheet)
    #spotify.spotify_search(titles, worksheet)
    #shazam.shazam_search(titles, worksheet)
    #myfacebook.get_likes(artists, worksheet)
    #instagram.get_instas(artists, worksheet)
    #mytwitter.get_twitter_stats(artists, worksheet)
    vine.get_vine_stats(artists, worksheet)


'''
import billboard_top100
billboard_top100.run_the_jewels()
'''


