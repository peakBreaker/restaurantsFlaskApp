"""Initiates a database session"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def makesession(Base):
    "Initiatees a new session with database, returns the session object "
    # Init the engine obj
    engine = create_engine('sqlite:///restaurantmenuwithusers.db')
    # Bind engine and the base obj
    Base.metadata.bind = engine
    # Init the session
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # Return session obj
    return session
