"""Contains functions for doing CRUD on the MenuItems table"""

from restaurants import Base, Restaurants, MenuItems
from makesession import makesession

session = makesession(Base)

def read_menuitems(restaurant_id, menuitem_id=None):
    """
    Lists out menuitems depending on args:
    1. A specific menuitem if menuitem_id is given or
    2. All menuitems for a specific restaurant
    """
    if menuitem_id != None:
        # Then we show info about the selected item
        return [session.query(MenuItems).filter_by(id=menuitem_id).one()]
    else:
        # Then we list all menuitems for selected restaurant
        return session.query(MenuItems).filter_by(restaurant_id=restaurant_id).order_by(MenuItems.name).all()

def create_menuitem(name, description, price, restaurant_id, user_id):
    """Inserts a new menuitem row in the db"""
    item = MenuItems(
                    name=name,
                    description=description,
                    price=price,
                    restaurant_id=restaurant_id,
                    user_id=user_id
                    )
    session.add(item)
    session.commit()
    return True

def update_menuitem(menuitem_id, name, description, price):
    """Updates the values of a row in the MenuItems table to the args given"""
    # First we find the object from quering the db
    item = session.query(MenuItems).filter_by(id=menuitem_id).one()
    # Next we update the values
    item.name=name
    item.description=description
    item.price=price
    # Then we add and commit the data to the session
    session.add(item)
    session.commit()
    # Finally we return the success statement
    return True

def delete_menuitem(menuitem_id):
    """Deletes the restaurant with the restaurant_id = passed argument"""
    # First we query the db
    item = session.query(MenuItems).filter_by(id=menuitem_id).one()
    # Next we get the restaurant id
    restaurant_id = item.restaurant_id
    # Then we delete the item from db through the session
    session.delete(item)
    session.commit()
    # Finally we return the restaurant id
    return True
