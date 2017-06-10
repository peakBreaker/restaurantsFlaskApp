"""Contains models for doing CRUD on the restaurants table"""

from restaurants import Base, Restaurants, MenuItems

from makesession import makesession

session = makesession(Base)

def read_restaurants(restaurantid, user_id=None):
    """
    Queries the database for restaurants. Takes restaurantid and userid args,
    and returns:
    1. If restaurantid = None -> Returns all list of restaurants in a tuple
    2. Else returns tuple of restaurant (as a list) and bool of user ownership
        -> return ([restaurant], owner)
    """
    print "User id is " + str(user_id)
    if restaurantid == None:
        print "Getting all restaurants!"
        return (session.query(Restaurants).order_by(Restaurants.name).all(), None)
    else:
        restaurant = session.query(Restaurants).filter_by(id=restaurantid).one()
        print "got the restaurant"
        print restaurant
        if restaurant.user_id == user_id:
            # Then we know that the user id is the owner of the restaurant
            print "user is owner"
            return ([restaurant], True)
        else:
            # If user is not owner, or not logged in at all
            return ([restaurant], False)

def create_restaurant(name, address, city, state, zipCode, user_id):
    """Gets parameters for a new restaurants and adds it into the db"""
    print "insert restaurant model running"
    restaurant = Restaurants(
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

def update_restaurant(restaurantid, name, address, city, state, zipCode):
    """
    Gets the id of the restaurant to be renamed and renames it to the name
    passed
    """
    print "edit restaurant model running!"
    restaurant = session.query(Restaurants).filter_by(id=restaurantid).one()
    restaurant.name = name
    restaurant.address = address
    restaurant.city = city
    restaurant.state = state
    restaurant.zipCode = zipCode
    session.add(restaurant)
    session.commit()
    print "uprdated restaurant in db"

def delete_restaurant(restaurantid):
    print "deleting restaurant"
    restaurant = session.query(Restaurants).filter_by(id=restaurantid).one()
    session.delete(restaurant)
    session.commit()
    return "restaurant deleted"
