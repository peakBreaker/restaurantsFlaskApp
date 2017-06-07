"""Contains models for doing CRUD on the restaurants table"""

from restaurants import Base, restaurants, MenuItems

from makesession import makesession

session = makesession(Base)

def testimport():
    print "Hello from the model_resturants module"

def list_restaurants(restaurantid, user_id=False):
    """
    Queries the database for restaurants and returns a list of
    restaurants objects ordered by name alphabetically.
    """
    if restaurantid == None:
        return (session.query(restaurants).order_by(restaurants.name).all(), False)
    else:
        restaurantlist = session.query(restaurants).filter_by(id=restaurantid).one()
        print "got the restaurantlist"
        print restaurantlist.name
        if restaurantlist.user_id == user_id:
            # Then we know that the user id is the owner of the restaurant
            print "user is owner"
            return ([restaurantlist], True)
        else:
            return ([restaurantlist], False)

def insert_restaurant(name, address, city, state, zipCode, user_id):
    """Gets parameters for a new restaurants and adds it into the db"""
    print "insert restaurant model running"
    restaurant = restaurants(
                            name=name,
                            address=address,
                            city=city,
                            state=state,
                            zipCode=zipCode,
                            user_id=user_id
                          )
    session.add(restaurant)
    session.commit()
    print "added new restaurant to db"
    return

def editname_restaurant(id, name):
    """
    Gets the id of the restaurant to be renamed and renames it to the name
    passed
    """
    restaurant = session.query(restaurants).filter_by(id=id).one()
    restaurant.name = name
    session.add(restaurant)
    session.commit()
    print "uprdated restaurant in db"
    return

def delete_restaurant(id):
    restaurant = session.query(restaurants).filter_by(id=id).one()
    session.delete(restaurant)
    session.commit()
    print "restaurant deleted"
    return
