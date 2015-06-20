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
    "Chart Position",
    "Chart Movement",
    "Song Title",
    "Artists",
    "Writers",
    "Producers",
    "Label",
    "Itunes Chart Position", #
    "Days Since Release", #
    "Radio Position", #
    "Overall Radio Spins", #
    "Overall Spins Last Week", #
    "Spins Difference", #
    "Pop Position", #
    "Pop Spins", #
    "Rhythmic Spins", #
    "Urban Spins", #
    "Radio Days (Pop)", #
    "Audience (Millions)", #
    "Youtube Views", #
    "Spotify Popularity", #
    "Spotify Streams",
    "Shazams", #
    "Shazam Chart Position", #
    "Facebook Likes", #
    "Instagram Followers", #
    "Twitter Followers", #
    "Soundcloud Followers", #
    "Vine Followers" #
]

'''import db_setup
from my_models import Artist, Track, Current_Spreadsheet
from sqlalchemy.sql import exists, text
session = db_setup.get_session()
query = session.query(Track).filter(Track.title == 'See You Again').all()
session.close()
'''