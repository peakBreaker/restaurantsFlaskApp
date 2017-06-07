"""Contains functions for doing CRUD on the MenuItems table"""

from restaurants import Base, restaurants, MenuItems
from makesession import makesession

session = makesession(Base)

def list_menu(restaurantid=False):
    """
    Lists out menu for all restaurants if no arg is given, or a specific
    restaurant id if arg is given
    """
    if restaurantid == False:
        menulist = session.query(MenuItems).all()
    else:
        menulist = session.query(MenuItems).filter_by(restaurant_id=restaurantid).all()
    return menulist

def get_restaurantitem(restaurant_id, menuitem_id):
    menulist = session.query(MenuItems).filter_by(restaurant_id=restaurant_id).all()
    return menulist[int(menuitem_id)].serialize

def insert_menuitem(name, description, price, restaurant_id, user_id):
    """Inserts a new menuitem row in the db"""
    print "inserting new menuitem"
    item = MenuItems(
                    name=name,
                    description=description,
                    price=price,
                    restaurant_id=restaurant_id,
                    user_id=user_id
                    )
    session.add(item)
    session.commit()
    return "Successfully inserted into db"

def edit_menuitem(id, name, description, price):
    """Updates the values of a row in the MenuItems table to the args given"""
    # First we find the object from quering the db
    item = session.query(MenuItems).filter_by(id=id).one()
    # Next we update the values
    item.name=name
    item.description=description
    item.price=price
    # Then we add and commit the data to the session
    session.add(item)
    session.commit()
    # Finally we return the success statement
    return item.restaurant_id

def delete_menuitem(id):
    """Deletes the restaurant with the restaurant_id = passed argument"""
    # First we query the db
    item = session.query(MenuItems).filter_by(id=id).one()
    # Next we get the restaurant id
    restaurant_id = item.restaurant_id
    # Then we delete the item from db through the session
    session.delete(item)
    session.commit()
    # Finally we return the restaurant id
    return restaurant_id
