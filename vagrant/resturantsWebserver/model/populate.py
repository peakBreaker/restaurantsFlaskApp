from sqlalchemy import create_engine #, func to aggregate
from sqlalchemy.orm import sessionmaker

from resturants import Base, Resturants

engine = create_engine('sqlite:///resturants.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

def getseeddata():
    """Reads the addresses and names files and returns a list of tuples"""
    a = open("seed/addresses", "r")
    n = open("seed/names", "r")
    i = 1
    seedlist = []
    while i < 11:
        num = 1
        name = n.readline()
        while num < 3:
            if num == 1:
                address = a.readline()
            else:
                s = a.readline().split(", ")
                city = s[0]
                s2 = s[1].split(" ")
                state = s2[0]
                zipcode = s2[1]
            num += 1
        seedlist.append((name[:-1], address[:-1], city[:-1], state[:-1], zipcode[:-1]))
        i += 1
    return seedlist


def populate_resturants():
    """
    Queries the database for resturants and returns a list of names of
    resturants ordered by name alphabetically.
    """
    for s in getseeddata():
        print s[0]
        resturant = Resturants(
                                name = s[0],
                                address = s[1],
                                city = s[2],
                                state = s[3],
                                zipCode = s[4]
                              )
        session.add(resturant)
        session.commit()
    return "Populated resturants"

print populate_resturants()
