__author__ = 'jpatdalton'

chart_position='A'
chart_movement='B'
song_title='C'
artists='D'
writers='E'
producers='F'
label='G'
itunes_chart_pos='H'
release_date='I'
spins_pos='J'
spins='K'
spins_last_week='L'
spins_diff='M'
spins_pop_pos='N'
spins_pop='O'
spins_rhythmic='P'
spins_urban='Q'
spins_days='R'
audience='S'
youtube='T'
spotify_popularity='U'
spotify_streams='V'
shazams='W'
shazam_chart_pos='X'
fb_likes='Y'
instagram='Z'
twitter='AA'
soundcloud='AB'
vine='AC'

headers = [
    "Chart Position (w)",
    "Chart Movement (w)",
    "Song Title (w)",
    "Artists (w)",
    "Writers (w)",
    "Producers (w)",
    "Label (w)",
    "Itunes Chart Position (d)", #
    "Days Since Release (d)", #
    "Overall Radio Position (d)", #
    "Overall Radio Spins (d)", #
    "Overall Spins Last Week (d)", #
    "Spins Difference Week to Week (d)", #
    "Pop Position (d)", #
    "Pop Spins (d)", #
    "Rhythmic Spins (d)", #
    "Urban Spins (d)", #
    "Radio Days [Pop] (d)", #
    "Audience [Millions] (d)", #
    "Youtube Views (h)", #
    "Spotify Popularity (h)", #
    "Spotify Streams (w)",
    "Shazams (h)", #
    "Shazam Chart Position (h)", #
    "Facebook Likes (h)", #
    "Instagram Followers (h)", #
    "Twitter Followers (h)", #
    "Soundcloud Followers (h)", #
    "Vine Followers (h)" #
]

'''import db_setup
from my_models import Artist, Track, Current_Spreadsheet
from sqlalchemy.sql import exists, text
session = db_setup.get_session()
query = session.query(Track).filter(Track.title == 'See You Again').all()
session.close()
'''