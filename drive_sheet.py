__author__ = 'jpatdalton'

import columns
from my_models import Artist, Track, Current_Spreadsheet
from sqlalchemy.sql import func
from datetime import datetime

def update_hourly(session, worksheet):
    end = str(int(session.query(func.max(Current_Spreadsheet.indice)).all()[0][0]) + 2)
    track_ids = session.query(Current_Spreadsheet).all()
    col_youtube = columns.youtube
    col_popularity = columns.spotify_popularity
    cell_list_popularity = worksheet.range(col_popularity+'2:'+col_popularity+end)
    cell_list_views = worksheet.range(col_youtube+'2:'+col_youtube+end)
    col = columns.shazams
    cell_list_zams = worksheet.range(col+'2:'+col+end)
    col = columns.shazam_chart_pos
    cell_list_chart_pos = worksheet.range(col+'2:'+col+end)
    for track_id in track_ids:
        track = session.query(Track).get(track_id.id)
        i = track_id.indice
        cell_list_views[i].value = track.youtube_views
        cell_list_popularity[i].value = track.spotify_popularity
        cell_list_chart_pos[i].value = track.shazam_chart_pos
        cell_list_zams[i].value = track.shazams

    worksheet.update_cells(cell_list_popularity)
    worksheet.update_cells(cell_list_views)
    worksheet.update_cells(cell_list_zams)
    worksheet.update_cells(cell_list_chart_pos)

def update_artists(session, worksheet):
    end = str(int(session.query(func.max(Current_Spreadsheet.indice)).all()[0][0]) + 7)

    col = columns.artists
    cell_list_artists = worksheet.range(col+'2:'+col+str(end))
    col = columns.fb_likes
    cell_list_fb_likes = worksheet.range(col+'2:'+col+end)
    col = columns.instagram
    cell_list_insta_likes = worksheet.range(col+'2:'+col+end)
    col = columns.vine
    cell_list_vine_likes = worksheet.range(col+'2:'+col+end)
    col = columns.soundcloud
    cell_list_sc_likes = worksheet.range(col+'2:'+col+end)
    col = columns.twitter
    cell_list_twitter_likes = worksheet.range(col+'2:' + col+end)

    n=0
    track_ids = session.query(Current_Spreadsheet).all()
    for track_id in track_ids:
        track = session.query(Track).get(track_id.id)
        #i = track_id.indice
        for artist in track.artists:
            cell_list_artists[n].value = artist.name
            cell_list_fb_likes[n].value = artist.fb_likes
            cell_list_insta_likes[n].value = artist.instagram
            cell_list_vine_likes[n].value = artist.vine
            cell_list_sc_likes[n].value = artist.soundcloud
            cell_list_twitter_likes[n].value = artist.twitter
            n+=1

    worksheet.update_cells(cell_list_artists)
    worksheet.update_cells(cell_list_fb_likes)
    worksheet.update_cells(cell_list_insta_likes)
    worksheet.update_cells(cell_list_vine_likes)
    worksheet.update_cells(cell_list_sc_likes)
    worksheet.update_cells(cell_list_twitter_likes)


def update_weekly(session, worksheet):
    end = int(session.query(func.max(Current_Spreadsheet.indice)).all()[0][0]) + 2
    col = columns.song_title
    cell_list_titles = worksheet.range(col+'2:'+col+str(end))
    col = columns.chart_position
    cell_list_nums = worksheet.range(col+'2:'+col+str(end))
    col = columns.chart_movement
    cell_list_chart_movement = worksheet.range(col+'2:'+col+str(end))
    col_writers = columns.writers
    col_producers = columns.producers
    col_label = columns.label
    cell_list_writers = worksheet.range(col_writers+'2:'+col_writers+str(end))
    cell_list_producers = worksheet.range(col_producers+'2:'+col_producers+str(end))
    cell_list_labels = worksheet.range(col_label+'2:'+col_label+str(end))
    n=0
    track_ids = session.query(Current_Spreadsheet).all()
    for track_id in track_ids:
        track = session.query(Track).get(track_id.id)
        i = track_id.indice
        cell_list_titles[i].value = track.title
        cell_list_chart_movement[i].value = track.chart_movement
        cell_list_nums[i].value = n+1

        cell_list_writers[i].value = track.writers
        cell_list_producers[i].value = track.producers
        cell_list_labels[i].value = track.label

        n+=1

    # Update in batch
    worksheet.update_cells(cell_list_nums)
    worksheet.update_cells(cell_list_titles)
    worksheet.update_cells(cell_list_chart_movement)
    worksheet.update_cells(cell_list_writers)
    worksheet.update_cells(cell_list_producers)
    worksheet.update_cells(cell_list_labels)


def update_daily(session, worksheet):
    today = datetime.today()
    end = str(int(session.query(func.max(Current_Spreadsheet.indice)).all()[0][0]) + 2)

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
    col = columns.release_date
    cell_list_dates = worksheet.range(col+'2:'+col+end)

    n=0
    track_ids = session.query(Current_Spreadsheet).all()
    for track_id in track_ids:
        track = session.query(Track).get(track_id.id)
        i = track_id.indice

        cell_list_spins[i].value = track.spins
        cell_list_aud[i].value = track.radio_audience
        cell_list_spins_pos[i].value = track.radio_position
        cell_list_spins_days[i].value = track.days_from_release
        cell_list_spins_pop_pos[i].value = track.spins_pop_pos
        cell_list_pop[i].value = track.spins_pop
        cell_list_rhythmic[i].value = track.spins_rhythmic
        cell_list_urban[i].value = track.spins_urban
        cell_list_itunes[i].value = track.itunes_chart_pos
        cell_list_spins_lw[i].value = track.spins_lw
        cell_list_spins_diff[i].value = track.spins_diff
        cell_list_dates[i].value = (today - track.itunes_release_date).days

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
    worksheet.update_cells(cell_list_dates)





