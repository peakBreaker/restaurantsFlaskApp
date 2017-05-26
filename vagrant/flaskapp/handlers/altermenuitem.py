"""This module handles everything concerning new menu items"""

from flask import render_template, request
from context import edit_menuitem, delete_menuitem

def editmenuitem(menuitem_id):
    """Handles the POST request to edit menuitem"""
    # First we get the forum arguments
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    # Then we insert the data into the db, this returns the resturant id
    resturant_id = edit_menuitem(menuitem_id, name, description, price)
    # If successful, we render the success template
    return resturant_id

def render_editmenuitem(menuitem_id):
    """Renders the newmenuitem for user input"""
    return render_template('editmenu.html', menuitem_id=menuitem_id)

def deletemenuitem(menuitem_id):
    """Handles the POST request to delete a menuitem"""
    # We pass it to the appropriate model function
    resturant_id = delete_menuitem(menuitem_id)
    print resturant_id
    # Finally, if all went well we render the success templates
    return resturant_id

def render_deletemenuitem(menuitem_id):
    return render_template('deletemenuitem.html', menuitem_id=menuitem_id)
