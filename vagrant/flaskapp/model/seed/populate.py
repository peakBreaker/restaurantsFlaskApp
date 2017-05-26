from sqlalchemy import create_engine #, func to aggregate
from sqlalchemy.orm import sessionmaker

from resturants import Base, Resturants

from populateResturants import populateResturants
from populateMenuItems import seedMenuItems

engine = create_engine('sqlite:///resturants.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

p = populateResturants(session)
print p

s = seedMenuItems(session)
print s
