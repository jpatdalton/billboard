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
import logging
import db_setup
import itunes
import billboard_biz
import drive_sheet
from my_models import Artist, Track, Current_Spreadsheet
from sqlalchemy.sql import exists, text

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
        logging.info('Refined name - ['+ str(r)+']')
    return main_artists, song_titles, indices

def validate_artists(artists, session):

    for art_name in artists:
        stmt = exists().where(Artist.name == art_name)
        query = session.query(Artist).filter(stmt)
        if len(query.all()) is 0:
            fb_id, insta_id, twitter_id, vine_id, sc_id = get_artists_ids(art_name)
            session.add(Artist(name=art_name, fb_id=fb_id, instagram_id=insta_id, twitter_id=twitter_id, vine_id=vine_id, soundcloud_id=sc_id))
    print 'NEW ARTISTS: ', session.new

def validate_tracks(tracks, artists, writers, producers, labels, indices, session):
    n = 0
    next_ind = 0
    for title in tracks:
        results = session.query(Track).filter_by(title=title).all()
        if len(results) is 1:
            print 'Track exists'
            populated_track = results[0]
            populated_track.writers = writers[n]
            populated_track.producers = producers[n]
            populated_track.label = labels[n]
            session.add(populated_track)
        elif len(results) is 0:
            print 'Creating this new track - ' + title
            new_track = Track(title=title)
            populated_track = populate_track_info(new_track)
            if n == 99:
                next_ind = len(artists)
            else:
                next_ind = indices[n+1]
            for i in xrange(next_ind - indices[n]):
                try:
                    the_artist = session.query(Artist).filter(Artist.name == artists[indices[n]+i]).all()
                    artist = the_artist[0]
                    populated_track.artists.append(artist)
                    populated_track.writers = writers[n]
                    populated_track.producers = producers[n]
                    populated_track.labels = labels[n]
                except Exception, e:
                    print e, 'No artist for the track! -', title
            session.add(populated_track)
        else:
            print 'This track has multiple results uh oh! FIXME $$$ - ' + title
        n+=1

def populate_track_info(track):
    try:
        id = itunes.get_song_id(track.title)
        track.itunes_id = id
        release_dt = itunes.get_release_date(id)
        track.itunes_release_date = release_dt
        track.days_from_release = itunes.calculate_days_from_release(release_dt)
        track.youtube_id = youtube.get_id(track.title)
        track.spotify_id = spotify.get_id(track.title)
        track.shazam_id = shazam.get_id(track.title)
    except Exception, e:
        print e, 'populate_track_info', track.title
    return track

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
                diff = "+"+str(diff)
        movements.append(diff)
        n+=1
    return movements

def put_artists(artists, worksheet, indices):
    end = 2+len(artists)
    col = columns.artists
    cell_list_artists = worksheet.range(col+'2:'+col+str(end))

    for n in xrange(len(artists)):
        cell_list_artists[n].value = artists[n]

    worksheet.update_cells(cell_list_artists)

def put_titles(titles, movements, worksheet, indices, end):
    # Select a range
    col = columns.song_title
    cell_list_titles = worksheet.range(col+'2:'+col+str(end))
    col = columns.chart_position
    cell_list_nums = worksheet.range(col+'2:'+col+str(end))
    col = columns.chart_movement
    cell_list_chart_movement = worksheet.range(col+'2:'+col+str(end))
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
    session = db_setup.get_session()

    worksheet = oauth.open_spreadsheet()

    make_spreadsheet(session, worksheet)

    #ARTIST STUFF
    '''
    #artists, titles, indices = get_top100()
    try:
        validate_artists(artists, session)
        session.commit()
    except Exception, e:
        session.rollback()
        print e, '120'
    '''
    '''
    try:
        update_artists(session)
        session.commit()
    except Exception, e:
        session.rollback()
        print e, '121'

     #TRACK STUFF
    try:
        validate_tracks(titles, artists, indices, session)
        session.commit()
    except Exception, e:
        session.rollback()
        print e, '122'
    '''
    '''
    try:
        # updates table 'current spreadsheet' with ids of the week's tracks
        populate_current_spreadsheet(titles, session)
        session.commit()
    except Exception, e:
        session.rollback()
        print e, '123'
    '''
    '''
    try:
        update_tracks_hourly(session)
        session.commit()
    except Exception, e:
        session.rollback()
        print e
    '''

    '''
    try:
        update_tracks_daily(session)
        session.commit()
    except Exception, e:
        session.rollback()
        print e

    try:
        update_tracks_weekly(session)
    except Exception, e:
        session.rollback()
        print e

    '''
    #movements = get_movements()
    #num = len(artists)
    #end = str(2+num)
    #billboard_biz.get_details(worksheet, indices, end)
    #put_titles(titles, movements, worksheet, indices, end)
    #put_artists(artists, worksheet, indices)
    #spins.get_spins(artists, titles, worksheet, indices, end)
    #itunes.itunes_search(titles, worksheet, indices, end)
    #youtube.youtube_search(titles, worksheet, indices, end)
    #spotify.spotify_search(titles, worksheet, indices, end)
    #shazam.shazam_search(titles, worksheet, indices, end)

    #myfacebook.get_likes(artists, worksheet, end)
    #instagram.get_instas(artists, worksheet, end)
    #mytwitter.get_twitter_stats(artists, worksheet, end)
    #vine.get_vine_stats(artists, worksheet, end)
    #sc.get_followers(artists, worksheet, end)

    session.close()

def update_tracks_hourly(session):
    track_ids = session.query(Current_Spreadsheet).all()
    for track_id in track_ids:
        track = session.query(Track).get(track_id.id)
        if track.youtube_id != ('None' or None):
            track.youtube_views = youtube.get_views(track.youtube_id)
        if track.shazam_id != ('None' or None):
            track.shazams, track.shazam_chart_pos = shazam.get_shazam_stats(track.shazam_id) #verified support
        if track.spotify_id != ('None' or None):
            track.spotify_popularity = spotify.get_popularity(track.spotify_id)
        session.add(track)

def update_tracks_daily(session):
    track_ids = session.query(Current_Spreadsheet).all()
    try:
        spins.update_tracks(track_ids, session)
        session.commit()
    except Exception, e:
        session.rollback()
        print e, 'Couldnt update SPINS $$$'
    '''
    tracks = session.query(Track).all()
    for track in tracks:
        track.days_from_release = track.days_from_release + 1
    session.add(track)
    '''



def update_tracks_weekly(session):
    artists, titles, indices = get_top100()
    #ARTIST STUFF
    '''
    try:
        validate_artists(artists, session)
        session.commit()
    except Exception, e:
        session.rollback()
        print e, '120'
    '''
     #TRACK STUFF
    writers, producers, labels = billboard_biz.get_writers_producers_labels()
    if not(len(writers) == len(producers) == len(labels) == 100):
        print 'couldnt get writers, producers, or labels!!! $$$ FIXME'
        raise Exception


     #TRACK STUFF
    try:
        # used to populate track billboard info
        validate_tracks(titles, artists, writers, producers, labels, indices, session)
        session.commit()
    except Exception, e:
        session.rollback()
        print e, '122'
    movements = get_movements()
    try:
        # updates table 'current spreadsheet' with ids of the week's tracks
        # puts chart position and movements for all current tracks
        populate_current_spreadsheet(titles, movements, session)
        session.commit()
    except Exception, e:
        session.rollback()
        print e, '123'


def update_artists(session):
    artists = session.query(Artist).all()
    for artist in artists:
        print artist.name
        if artist.fb_id != ('None' or None):
            artist.fb_likes = myfacebook.get_fb_likes(artist.fb_id)
        if artist.instagram_id != ('None' or None):
            artist.instagram = instagram.get_followers(artist.instagram_id)
        if artist.twitter_id != ('None' or None):
            artist.twitter = mytwitter.get_followers(artist.twitter_id) #verified support
        if artist.vine_id != ('None' or None):
            print artist.vine_id
            artist.vine = vine.get_user_data(artist.vine_id) #verified support
        if artist.soundcloud_id is not ('None' or None):
            artist.soundcloud = sc.get_num_followers(artist.soundcloud_id)
        session.add(artist)

def get_artists_ids(name):
    fb_id = myfacebook.get_page_id(name)
    instagram_id = instagram.get_id(name)
    twitter_id = mytwitter.get_id(name) #verified support
    vine_id = vine.get_id(name) #verified support
    soundcloud_id = sc.get_id(name)
    return fb_id, instagram_id, twitter_id, vine_id, soundcloud_id

def get_release_dates(titles, worksheet, indices, end, session):
    col = columns.release_date
    cell_list_dates = worksheet.range(col+'2:'+col+end)
    n=0
    for ind in indices:
        name = titles[n]
        id = itunes.get_song_id(name)
        cell_list_dates[ind].value = itunes.calculate_days_from_release(itunes.get_release_date(id))
        n+=1
    worksheet.update_cells(cell_list_dates)

def populate_current_spreadsheet(titles, movements, session):
    session.execute(text('TRUNCATE table current_spreadsheet'))
    n = 1
    for title in titles:
        results = session.query(Track).filter(Track.title == title).all()
        if len(results) == 1:
            track = results[0]
            session.add(Current_Spreadsheet(id = track.id))
            track.chart_position = n
            track.chart_movement = movements[n-1]
            session.add(track)
        elif len(results) > 1:
            print 'MORE THAN ONE TRACK IS BEING RETURNED FIXME $$$'
        else:
            print 'NO TRACK, FIXME $$$'
        n += 1

'''
            populated_track = results[0]
            if n == 99:
                next_ind = len(artists)
            else:
                next_ind = indices[n+1]
            for i in xrange(next_ind - indices[n]):
                try:
                    the_artist = session.query(Artist).filter(Artist.name == artists[indices[n]+i]).all()
                    artist = the_artist[0]
                    populated_track.artists.append(artist)
                except Exception, e:
                    print e, 'No artist for the track! -', title
            session.add(populated_track)
'''
def do_days_from_release(session):
    tracks = session.query(Track).all()
    for track in tracks:
        release_dt = itunes.get_release_date(track.itunes_id)
        track.days_from_release = itunes.calculate_days_from_release(release_dt)
        session.add(track)
    session.commit()

'''
import billboard_top100
billboard_top100.run_the_jewels()


import db_setup
from my_models import Artist, Track, Current_Spreadsheet
from sqlalchemy.sql import exists, text
session = db_setup.get_session()

query = session.query(Track).filter(Track.title == 'Nasty Freestyle').all()
query[0].shazam_id is 'None'
session.close()


import billboard_biz
billboard_biz.get_writers_producers_labels()


from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
url = 'http://www.billboard.com/biz/charts/the-billboard-hot-100'
driver.get(url)
time.sleep(11)
login = driver.find_element_by_link_text('Log In')
login.click()
time.sleep(2)
name = driver.find_element_by_id('edit-name')
name.send_keys('steve@zeitlosent.com')
time.sleep(1)
password = driver.find_element_by_id('edit-pass')
password.send_keys('steve')
time.sleep(1)
password.send_keys(Keys.ENTER)
login = driver.find_element_by_id('edit-submit--3')
login.submit()

'''

