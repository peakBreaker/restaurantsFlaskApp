
from context import Resturants

def getseeddata():
    """Reads the addresses and names files and returns a list of tuples"""
    a = open("seed/addresses", "r") # File is from https://www.randomlists.com/random-addresses
    n = open("seed/names", "r") # File is from http://www.wordlab.com/archives/restaurant-names-list/
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

def populateResturants(session):
    """
    Queries the database for resturants and returns a list of names of
    resturants ordered by name alphabetically.
    """
    try:
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
    except Exception as e:
        return e
