from sqlalchemy.ext.declarative import declarative_base, declared_attr
import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from db_setup import Base
'''
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    #__table_args__ = {'mysql_engine': 'InnoDB'}

    id =  Column(Integer, primary_key=True)
    updated_at = Column(DateTime, default=datetime.datetime.now())
    created_at = Column(DateTime, default=datetime.datetime.now())
'''

track_artists = Table('track_artists', Base.metadata,
    Column('track_id', Integer, ForeignKey('track.id')),
    Column('artist_id', Integer, ForeignKey('artist.id'))

)


class Track(Base):
    __tablename__ = 'track'
    id =  Column(Integer, primary_key=True)
    updated_at = Column(DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now)
    created_at = Column(DateTime, default=datetime.datetime.now())

    chart_position = Column(Integer)
    chart_movement = Column(String(3))
    title = Column(String(45))
    alt_title = Column(String(45))
    spins_lw = Column(Integer)
    radio_position = Column(Integer)
    radio_days = Column(Integer)
    radio_audience = Column(Integer)
    days_from_release = Column(Integer)
    youtube_views = Column(Integer)
    youtube_id = Column(String(20))
    spotify_id = Column(String(30))
    spotify_popularity = Column(Integer)
    spotify_streams = Column(Integer)
    shazam_id = Column(Integer)
    shazams = Column(Integer)
    shazam_chart_pos = Column(Integer)
    itunes_id = Column(Integer)
    itunes_release_date = Column(DateTime)

    artists = relationship('Artist', secondary=track_artists,
                            backref=backref('tracks', lazy='dynamic'))

class Artist(Base):
    __tablename__ = 'artist'
    id =  Column(Integer, primary_key=True)
    updated_at = Column(DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now)
    created_at = Column(DateTime, default=datetime.datetime.now())
    name = Column(String(45), unique=True)
    alt_name = Column(String(45))
    fb_likes = Column(Integer)
    fb_id = Column(String(20))
    instagram = Column(Integer)
    instagram_id = Column(String(20))
    soundcloud = Column(Integer)
    soundcloud_id = Column(String(20))
    twitter = Column(Integer)
    twitter_id = Column(String(20))
    vine = Column(Integer)
    vine_id = Column(String(20))


