"""Contains models for doing CRUD on the resturants table"""

from resturants import Base, Resturants, MenuItems

from makesession import makesession

session = makesession(Base)

def list_resturants(resturantid, user_id=False):
    """
    Queries the database for resturants and returns a list of
    resturants objects ordered by name alphabetically.
    """
    if resturantid == None:
        return (session.query(Resturants).order_by(Resturants.name).all(), False)
    else:
        resturantlist = session.query(Resturants).filter_by(id=resturantid).one()
        print "got the resturantlist"
        print resturantlist.name
        if resturantlist.user_id == user_id:
            # Then we know that the user id is the owner of the resturant
            print "user is owner"
            return ([resturantlist], True)
        else:
            return ([resturantlist], False)

def insert_resturant(name, address, city, state, zipCode, user_id):
    """Gets parameters for a new resturants and adds it into the db"""
    print "insert resturant model running"
    resturant = Resturants(
                            name=name,
                            address=address,
                            city=city,
                            state=state,
                            zipCode=zipCode,
                            user_id=user_id
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
