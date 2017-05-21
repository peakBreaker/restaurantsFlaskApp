from sqlalchemy import create_engine #, func to aggregate
from sqlalchemy.orm import sessionmaker

from resturants import Base, Resturants

engine = create_engine('sqlite:///resturants.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

def list_resturants():
    """
    Queries the database for resturants and returns a list of
    resturants ordered by name alphabetically.
    """
    resturantlist = session.query(Resturants).order_by(Resturants.name).all()

    return resturantlist

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
