from sqlalchemy import create_engine #, func to aggregate
from sqlalchemy.orm import sessionmaker

def makesession(Base):
    #Initiate the engine obj
    engine = create_engine('sqlite:///resturants.db')
    # Bind engine and the base obj
    Base.metadata.bind = engine
    # Init the session
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    #return session obj
    return session
