__author__ = 'jpatdalton'

import urllib2
from bs4 import BeautifulSoup
import re
import oauth
import spins
import youtube
import spotify
import shazam
import myfacebook
import instagram
import mytwitter
import vine
import sc
import columns

def get_top100():

    url = 'http://www.billboard.com/charts/hot-100'
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)

    titles = soup.select(".row-title")
    song_titles = list()
    song_artists = list()
    indices = list()
    for title in titles:
        song_titles.append(title.find("h2").get_text().strip())
        song_artists.append(title.find("h3").get_text().strip())
    main_artists = list()

    total = 0
    for artist in song_artists:
        refined_names = artist.split('Featuring')
        count = 0
        for refined_name in refined_names:
            refined_name1 = refined_name.split('&')
            if len(refined_name1) > 1:
                refined_name2 = refined_name1[0].split(',')
                for n in refined_name2:
                    count+=1
                    main_artists.append(n.strip())
                count+=1
                main_artists.append(refined_name1[1].strip())
            else:
                refined_name2 = refined_name1[0].split('With')
                for n in refined_name2:
                    count+=1
                    main_artists.append(n.strip())
        indices.append(total)
        total+=count

    for r in main_artists:
        print 'Refined name - ['+ str(r)+']'


    return main_artists, song_titles, indices


def get_movements():
    movements = list()
    url = 'http://www.billboard.com/charts/hot-100'
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)

    moves = soup.select(".row-rank")
    n = 0
    for move in moves:
        last_week = move.select('.last-week')[0].string[11:].strip()
        if last_week == '--':
            diff = 'N/A'
        else:
            diff = int(last_week) - (n+1)
            if int(diff) > 0:
                diff = "'+"+str(diff)
        movements.append(diff)
        n+=1
    return movements

def put_artists(artists, worksheet, indices):
    end = 2+len(artists)
    col = columns.artists
    cell_list_artists = worksheet.range(col+'3:'+col+str(end))

    for n in xrange(len(artists)):
        cell_list_artists[n].value = artists[n]

    worksheet.update_cells(cell_list_artists)

def put_titles(titles, movements, worksheet, indices, end):
    # Select a range
    col = columns.song_title
    cell_list_titles = worksheet.range(col+'3:'+col+str(end))
    col = columns.chart_position
    cell_list_nums = worksheet.range(col+'3:'+col+str(end))
    col = columns.chart_movement
    cell_list_chart_movement = worksheet.range(col+'3:'+col+str(end))
    n=0
    for ind in indices:
        cell_list_titles[ind].value = titles[n]
        cell_list_chart_movement[ind].value = movements[n]
        cell_list_nums[ind].value = n+1
        n+=1

    # Update in batch
    worksheet.update_cells(cell_list_nums)
    worksheet.update_cells(cell_list_titles)
    worksheet.update_cells(cell_list_chart_movement)


def run_the_jewels():
    worksheet = oauth.open_worksheet()
    artists, titles, indices = get_top100()
    #movements = get_movements()
    num = len(artists)
    end = str(2+num)
    #put_titles(titles, movements, worksheet, indices, end)
    #put_artists(artists, worksheet, indices)
    #spins.get_spins(artists, titles, worksheet, indices, end)
    #youtube.youtube_search(titles, worksheet, indices, end)
    #spotify.spotify_search(titles, worksheet, indices, end)
    #shazam.shazam_search(titles, worksheet, indices, end)
    #myfacebook.get_likes(artists, worksheet, end)
    instagram.get_instas(artists, worksheet, end)
    #mytwitter.get_twitter_stats(artists, worksheet, end)
    #vine.get_vine_stats(artists, worksheet, end)
    #sc.get_followers(artists, worksheet, end)


'''
import billboard_top100
billboard_top100.run_the_jewels()
'''


