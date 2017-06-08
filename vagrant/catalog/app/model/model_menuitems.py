"""Contains functions for doing CRUD on the MenuItems table"""

from restaurants import Base, Restaurants, MenuItems
from makesession import makesession

session = makesession(Base)

def read_menuitems(restaurant_id=None, menuitem_id=None):
    """
    Lists out menuitems depending on args:
    1. A specific menuitem if menuitem_id is given
    2. All menuitems if no args is given
    3. All menuitems for a specific restaurant if restaurantid is given
    """
    if menuitem_id != None:
        # Then we show info about the selected item
        return session.query(MenuItems).filter_by(id=menuitem_id).one().serialize
    elif restaurantid == None:
        # Then we list all menuitems
        return session.query(MenuItems).order_by(MenuItems.name).all()
    else:
        # Then we list all menuitems for selected restaurant
        return session.query(MenuItems).filter_by(restaurant_id=restaurant_id).order_by(MenuItems.name).all()

def get_restaurantitem(restaurant_id, menuitem_id):
    menulist = session.query(MenuItems).filter_by(restaurant_id=restaurant_id).order_by(MenuItems.name).all()
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
