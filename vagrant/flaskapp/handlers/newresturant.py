"""This module handles everything concerning new resturants"""

from flask import render_template, request
from context import insert_resturant

def insertresturant():
    """Handles POST request to insert a new resturant into db"""
    # First we get the request arguemnts
    name = request.form['name']
    address = request.form['description']
    city = request.form['price']
    state = request.form['state']
    zipCode = request.form['zipCode']
    # Next we call the insert_newresturant function
    # takes arguments name, address, city, state, zipCode
    s = insert_resturant(name, address, city, state, zipCode)
    print s
    # Finally we return the success html
    return render_template("submitted.html")


def render_newresturant():
    """Renders the newresturant.html for user input"""
    return render_template("newresturant.html")
