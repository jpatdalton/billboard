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
import sys
import datetime
from my_models import Artist, Track, Current_Spreadsheet
from sqlalchemy.sql import exists, text, func
import smtplib
from email.mime.text import MIMEText
import os.path

recipients = []
today = datetime.datetime.today()
td = today.strftime("%m-%d-%y")
artists_file = 'new_tracks_and_artists/new_artists_' + td + '.txt'
tracks_file = 'new_tracks_and_artists/new_tracks_' + td + '.txt'

def get_top100():

    url = 'http://www.billboard.com/charts/hot-100'
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)

    titles = soup.select(".chart-row__song")
    artists = soup.select('.chart-row__artist')
    song_titles = list()
    song_artists = list()
    indices = list()
    for title in titles:
        song_titles.append(title.get_text().strip())
    for artist in artists:
        song_artists.append(artist.find("a").get_text().strip())
    main_artists = list()

    total = 0
    for artist in song_artists:
        refined_names = artist.split('Featuring')
        count = 0
        for refined_name in refined_names:
            refined_name1 = refined_name.split('&')
            if len(refined_name1) > 1:
                refined_name2 = refined_name1[0].split(',')
                #refined_name3 = [i.split('With') for i in refined_name2]
                '''
                refined_name2 = [i.split(',') for i in refined_name1]
                refined_name2 = [j for i in refined_name2 for j in i]
                refined_name3 = [i.split('With') for i in refined_name2]
                refined_name4 = [j for i in refined_name3 for j in i]
                '''
                for n in refined_name2:
                    count+=1
                    main_artists.append(n.strip())
                #count+=1
                refined_name3 = refined_name1[1].split('With')
                for n in refined_name3:
                    count+=1
                    main_artists.append(n.strip())
                #main_artists.append(refined_name1[1].strip())
            else:
                refined_name2 = refined_name1[0].split('With')
                for n in refined_name2:
                    count+=1
                    main_artists.append(n.strip())
        indices.append(total)
        total+=count
    print main_artists
    print indices
    for r in main_artists:
        logging.info('Refined name - ['+ str(r)+']')
    return main_artists, song_titles, indices

def validate_artist(art_name, session):

    query = session.query(Artist).filter(Artist.name == art_name).all()
    if len(query) is 0:
        fb_id, insta_id, twitter_id, vine_id, sc_id, spotify_id = get_artists_ids(art_name)
        art = Artist(name=art_name, fb_id=fb_id, instagram_id=insta_id, twitter_id=twitter_id, vine_id=vine_id, soundcloud_id=sc_id, spotify_id=spotify_id)
        session.add(art)
        session.commit()
        print 'Made new artist - ' + art_name
        try:
            f = open(artists_file, 'a')
            f.write(art_name + '\n')
            if fb_id != 'None':
                f.writelines('Facebook: https://www.facebook.com/profile.php?id=' + str(fb_id) + '\n')
            if insta_id != 'None':
                uname = instagram.get_username(insta_id)
                f.write('Instagram: https://instagram.com/' + uname  + '\n')
            if twitter_id != 'None':
                f.write('Twitter: https://twitter.com/intent/user?user_id=' + str(twitter_id) + '\n')
            if vine_id != 'None':
                f.write('Vine: https://vine.co/u/' + str(vine_id) + '\n')
            if sc_id != 'None':
                url = sc.get_page(sc_id)
                f.write('Soundcloud: ' + url + '\n')
            f.write('\n\n')
            f.close()
        except Exception, e:
            print e

        return art
    return query[0]



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
            populated_track = Track(title=title)

            try:
                populated_track.writers = writers[n]
                populated_track.producers = producers[n]
                populated_track.label = labels[n]
            except Exception, e:
                print 'Trouble with writers, producers, labels'
            if n == 99:
                next_ind = len(artists)
            else:
                next_ind = indices[n+1]
            for i in xrange(next_ind - indices[n]):
                try:
                    the_artist = validate_artist(artists[indices[n]+i], session)
                    populated_track.artists.append(the_artist)
                except Exception, e:
                    print e, 'Problem appending artists to track - ', title
            populated_track = populate_track_info(populated_track)
            session.add(populated_track)
            session.commit()
            add_new_track(populated_track)
        else:
            print 'This track has multiple results uh oh! FIXME $$$ - ' + title
        n+=1

def add_new_track(track):
    try:
        f = open(tracks_file, 'a')
        f.write(track.title + '\n')
        if track.shazam_id != 'None':
            f.write('Shazam: http://www.shazam.com/track/' + str(track.shazam_id) + '\n')
        f.write('\n\n')
    finally:
        f.close()


def populate_track_info(track):
    try:
        id = itunes.get_song_id(track.title)
        track.itunes_id = id
        release_dt = itunes.get_release_date(id)
        track.itunes_release_date = release_dt
        track.days_from_release = itunes.calculate_days_from_release(release_dt)
        track.youtube_id = youtube.get_id(track.title)
        track.spotify_id = spotify.get_id(track.title)
        track.shazam_id = shazam.get_id(track.title + ' ' + track.artists[0].name)
    except Exception, e:
        print e, 'populate_track_info', track.title
    return track

def get_movements():
    movements = list()
    url = 'http://www.billboard.com/charts/hot-100'
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)

    moves = soup.select(".chart-row__last-week")
    n = 0
    for i in range(0, 199, 2):
        last_week = moves[i].string[11:].strip()
        if last_week == '--':
            diff = 'N/A'
        else:
            diff = int(last_week) - (n+1)
            if int(diff) > 0:
                diff = "+"+str(diff)
        movements.append(diff)
        n+=1
    return movements


def run_the_jewels():
    session = db_setup.get_session()

    session.close()

def update_tracks_hourly():
    session = db_setup.get_session()
    try:
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
        session.commit()
    except Exception, e:
        session.rollback()
        print e, '119'
    session.close()

def update_tracks_daily():
    session = db_setup.get_session()
    try:
        track_ids = session.query(Current_Spreadsheet).all()
        spins.update_tracks(track_ids, session)
        session.commit()
    except Exception, e:
        session.rollback()
        print e, 'Couldnt update SPINS $$$'
    session.close()
    '''
    tracks = session.query(Track).all()
    for track in tracks:
        track.days_from_release = track.days_from_release + 1
    session.add(track)
    '''

#populate_current_spreadsheet(titles, movements, session)

def update_tracks_weekly():
    session = db_setup.get_session()
    try:
        artists, titles, indices = get_top100()

        #ARTIST STUFF
        #TODO: only validate the artists from tracks
        '''
        try:
            validate_artist(artists, session)
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
            tt = open(artists_file, 'w+')
            ta = open(tracks_file, 'w+')
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

        session.commit()
    except Exception, e:
        session.rollback()
        print e, '117'
    session.close()
    try:
        send_email()
    except Exception,e:
        print '$$$ Couldnt send email!', e

def update_artists():
    session = db_setup.get_session()
    try:
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
                #print artist.vine_id
                artist.vine = vine.get_user_data(artist.vine_id) #verified support
            if artist.soundcloud_id != ('None' or None):
                artist.soundcloud = sc.get_num_followers(artist.soundcloud_id)
            else:
                artist.soundcloud = 0
            session.add(artist)
        session.commit()
    except Exception, e:
        session.rollback()
        print e, '122'
    session.close()

def get_artists_ids(name):
    fb_id = myfacebook.get_page_id(name)
    instagram_id = instagram.get_id(name)
    twitter_id = mytwitter.get_id(name) #verified support
    vine_id = vine.get_id(name) #verified support
    soundcloud_id = sc.get_id(name)
    spotify_id = spotify.get_artist_id(name)
    return fb_id, instagram_id, twitter_id, vine_id, soundcloud_id, spotify_id

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
    index = 0
    for title in titles:
        results = session.query(Track).filter(Track.title == title).all()
        if len(results) == 1:
            track = results[0]
            session.add(Current_Spreadsheet(id = track.id, indice = index))
            index += len(track.artists)
            track.chart_position = n
            track.chart_movement = movements[n-1]
            session.add(track)
        elif len(results) > 1:
            print 'MORE THAN ONE TRACK IS BEING RETURNED FIXME $$$'
        else:
            print 'NO TRACK, FIXME $$$'
        n += 1

def do_days_from_release(session):
    tracks = session.query(Track).all()
    for track in tracks:
        release_dt = itunes.get_release_date(track.itunes_id)
        track.days_from_release = itunes.calculate_days_from_release(release_dt)
        session.add(track)
    session.commit()

def send_email():
    message = ''
    tp = open(tracks_file, 'rb')
    message += '     -- NEW TRACKS --\n\n'
    message += tp.read()
    tp.close()
    fp = open(artists_file, 'rb')
    message += '     -- NEW ARTISTS --\n\n'
    message += fp.read()
    fp.close()
    # me == the sender's email address
    # you == the recipient's email address
    msg = MIMEText(message)
    msg['Subject'] = 'New Artists and Tracks for Billboard Metrics to Verify'
    msg['From'] = 'jpatdalton@gmail.com'
    msg['To'] = ", ".join(recipients)

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail('jpatdalton@gmail.com', recipients, msg.as_string())
    print 'email sent yo'
    s.quit()
'''
import billboard_top100
billboard_top100.send_email()
python -m smtpd -n -c DebuggingServer localhost:1025

billboard_top100.run_the_jewels()

billboard_top100.validate_artist()
import db_setup
from my_models import Artist, Track, Current_Spreadsheet
from sqlalchemy.sql import exists, text, func
session = db_setup.get_session()

query = session.query(Track).filter(Track.title=="Where Are U Now").all()[0]
query[0].shazam_id is 'None'
session.close()

import db_setup
session = db_setup.get_session()
import billboard_top100
billboard_top100.validate_artist('Wiz Khalifa', session)
session.close()

'''
'''
%%% ADD ARTIST TO TRACK %%%
import db_setup
session = db_setup.get_session()
import billboard_top100
from my_models import Artist, Track, Current_Spreadsheet
query = session.query(Track).filter(Track.title=="My Way").all()[0]
billboard_top100.validate_artist("Monty", session)
art = session.query(Artist).filter(Artist.name=="Monty").all()[0]
query.artists.append(art)

'''
#print sys.argv
if len(sys.argv) == 2:
    if sys.argv[1] == 'artists':
        print 'updating artists...'
        update_artists()
    elif sys.argv[1] == 'hourly':
        print 'updating hourly...'
        update_tracks_hourly()
    elif sys.argv[1] == 'daily':
        print 'updating daily...'
        update_tracks_daily()
    elif sys.argv[1] == 'weekly':
        print 'updating weekly...'
        update_tracks_weekly()
    elif sys.argv[1] == 'us':
        print 'updating drive spreadsheet spotify'
        drive_sheet.update_spotify()
    elif sys.argv[1] == 'uw':
        print 'updating drive spreadsheet weekly'
        drive_sheet.update_weekly()
    elif sys.argv[1] == 'ua':
        print 'updating drive spreadsheet artists'
        drive_sheet.update_artists()
    elif sys.argv[1] == 'uh':
        print 'updating drive spreadsheet hourly'
        drive_sheet.update_hourly()
    elif sys.argv[1] == 'ud':
        print 'updating drive spreadsheet daily'
        drive_sheet.update_daily()
elif len(sys.argv) == 3:
    if sys.argv[1] == 'artists' and sys.argv[2] == 'ua':
        print 'updating artists...'
        update_artists()
        print 'updating drive spreadsheet artists'
        drive_sheet.update_artists()
    if sys.argv[1] == 'hourly' and sys.argv[2] == 'uh':
        print 'updating hourly...'
        update_tracks_hourly()
        print 'updating drive spreadsheet hourly'
        drive_sheet.update_hourly()
    if sys.argv[1] == 'daily' and sys.argv[2] == 'ud':
        print 'updating daily...'
        update_tracks_daily()
        print 'updating drive spreadsheet daily'
        drive_sheet.update_daily()
    if sys.argv[1] == 'weekly' and sys.argv[2] == 'uw':
        print 'updating weekly...'
        update_tracks_weekly()
        print 'updating drive spreadsheet weekly'
        drive_sheet.update_weekly()

def get_artist_spotify_ids():
    session = db_setup.get_session()
    try:
        artists = session.query(Artist).all()
        for artist in artists:
            art_id = spotify.get_artist_id(artist.name)
            artist.spotify_id = art_id
            print artist.name + ' ' + str(art_id)
            session.add(artist)
        session.commit()
    except Exception, e:
        session.rollback()
        print e, '119'
    session.close()

def get_spotify_streams():
    session = db_setup.get_session()
    try:
        track_ids = session.query(Current_Spreadsheet).all()
        driver = spotify.login()
        for track_id in track_ids:
            art_id = ''
            streams = 0
            track = session.query(Track).get(track_id.id)
            art_id = track.artists[0].spotify_id
            if track.artists[0].name != 'Taylor Swift':
                streams = spotify.get_streams(driver, track.title, art_id)
                track.spotify_streams = streams
                session.add(track)
                session.commit()
    except Exception, e:
        session.rollback()
        print e, '119'
    finally:
        session.close()
        driver.close()



