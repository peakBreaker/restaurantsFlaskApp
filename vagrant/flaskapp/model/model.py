from sqlalchemy import create_engine #, func to aggregate
from sqlalchemy.orm import sessionmaker

from resturants import Base, Resturants, MenuItems

engine = create_engine('sqlite:///resturants.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

def list_resturants(resturantid):
    """
    Queries the database for resturants and returns a list of
    resturants objects ordered by name alphabetically.
    """
    if resturantid == False:
        resturantlist = session.query(Resturants).order_by(Resturants.name).all()
    else:
        resturantlist = session.query(Resturants).filter_by(id=resturantid).all()
    return resturantlist

def list_menu(resturantid=False):
    """
    Lists out menu for all resturants if no arg is given, or a specific
    resturant id if arg is given
    """
    if resturantid == False:
        menulist = session.query(MenuItems).all()
    else:
        menulist = session.query(MenuItems).filter_by(resturant_id=resturantid).all()
    return menulist

def insert_resturant(name, address, city, state, zipCode):
    """Gets parameters for a new resturants and adds it into the db"""
    resturant = Resturants(
                            name=name,
                            address=address,
                            city=city,
                            state=state,
                            zipCode=zipCode
                          )
    session.add(resturant)
    session.commit()
    print "added new resturant to db"
    return

def editname_resturant(id, name):
    """
    Gets the id of the resturant to be renamed and renames it to the name
    passed
    """
    resturant = session.query(Resturants).filter_by(id=id).one()
    resturant.name = name
    session.add(resturant)
    session.commit()
    print "uprdated resturant in db"
    return

def delete_resturant(id):
    resturant = session.query(Resturants).filter_by(id=id).one()
    session.delete(resturant)
    session.commit()
    print "resturant deleted"
    return
