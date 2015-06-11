import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://unrestricted:untothetoprestricted@billboard.cehafzitzdxd.us-west-2.rds.amazonaws.com:3306/Billboard', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
'''
def __init__(self):
    {}
    #self.Base = declarative_base()
'''


def get_session():
    session = Session()
    return session


