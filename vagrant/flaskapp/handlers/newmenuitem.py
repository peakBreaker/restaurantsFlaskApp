"""This module handles everything concerning new menu items"""

from flask import render_template, request
from context import insert_menuitem

def insertmenuitem(resturant_id):
    """Handles the POST request to submit new menuitems"""
    # First we get the forum arguments
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    # Then we insert the data into the db
    s = insert_menuitem(name, description, price, resturant_id)
    print s
    # If successful, we render the success template
    return render_template('submitted.html')

def render_newmenuitem(resturant_id):
    """Renders the newmenuitem for user input"""
    return render_template('newmenuitem.html', resturant_id=resturant_id)
