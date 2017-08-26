"""Initiates a database session"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def makesession(Base):
    "Initiatees a new session with database, returns the session object "
    # Init the engine obj
    # postgresql: "postgresql+pg8000://user:password@host/database"
    engine = create_engine('postgresql+pg8000://catalog:culinaryadventure443@localhost:5432/restaurantswithusers')
    # Bind engine and the base obj
    Base.metadata.bind = engine
    # Init the session
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # Return session obj
    return session
