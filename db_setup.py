'''
This file is not currently used
'''

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

def get_session():
    session = Session()
    return session

    chart_position = Column(Integer)
    chart_movement = Column(String(3))
    title = Column(String(45))
    alt_title = Column(String(45))
    spins_lw = Column(Integer)
    radio_position = Column(Integer)
    radio_days = Column(Integer)
    radio_audience = Column(Integer)

    artists = relationship('Artist', secondary=track_artists,
                            backref=backref('tracks', lazy='dynamic'))
