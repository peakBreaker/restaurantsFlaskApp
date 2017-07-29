"""Contains models for doing CRUD for restaurants"""

from restaurants import Base, Restaurants, MenuItems

from makesession import makesession

session = makesession(Base)


def read_restaurants(restaurantid, user_id=None):
    """
    Queries the database for restaurants. Takes restaurantid and userid args,
    and returns:
    1. If restaurantid = None -> Returns tuple ([restaurants], None)
    2. Else returns tuple of restaurant (as a list) and bool of user ownership
        -> return ([restaurant], owner)
    """
    if restaurantid is None:
        # Getting all restaurants
        return (session.query(Restaurants).order_by(Restaurants.name).all(), None)
    else:
        restaurant = session.query(Restaurants).filter_by(id=restaurantid).one()
        if restaurant.user_id == user_id:
            # Then we know that the user id is the owner of the restaurant
            return ([restaurant], True)
        else:
            # If user is not owner, or not logged in at all
            return ([restaurant], False)


def create_restaurant(name, address, city, state, zipCode, user_id):
    "Gets parameters for a new restaurants and adds it into the db"
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
    return True


def update_restaurant(restaurantid, name, address, city, state, zipCode):
    "Updates a restaurant in the db, returns a string if successful"
    restaurant = session.query(Restaurants).filter_by(id=restaurantid).one()
    restaurant.name = name
    restaurant.address = address
    restaurant.city = city
    restaurant.state = state
    restaurant.zipCode = zipCode
    session.add(restaurant)
    session.commit()
    return True


def delete_restaurant(restaurantid):
    "Deletes restaurant with belonging menuitems with passed restautant id"
    restaurant = session.query(Restaurants).filter_by(id=restaurantid).one()
    menuitems = session.query(MenuItems).\
        filter_by(restaurant_id=restaurantid).all()
    session.delete(menuitems)
    session.delete(restaurant)
    session.commit()
    return True
