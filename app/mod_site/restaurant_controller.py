"""Controller for handeling the restaurants.
Naming convention worth noting is how handlers map to models:
Handler -> Model CRUD
1. new_restaurant -> create_restaurant
2. show_restaurants -> read_restaurants
3. edit_restaurant -> update_restaurant
4. remove_restaurant -> delete_restaurant

This holds true for menuitems aswell
"""

# Is there a better way to do this rather than circular imports?
from . import mod

from flask import render_template, url_for, request, flash, redirect

from flask import session as login_session

# database model imports for restaurants
from app.model.model_restaurants import create_restaurant, \
                                        read_restaurants, \
                                        update_restaurant, \
                                        delete_restaurant

from app.utils.auth import valid_login_session

# HANDLERS FOR RESTAURANTS ----------------------------------------------------


@mod.route('/restaurants/new', methods=['GET', 'POST'])
@valid_login_session
def new_restaurant():
    "Validates user login_session, gives user a form and handles http post"
    if request.method == 'GET':
        return render_template('restaurants/newrestaurant.html')
    elif request.method == 'POST':
        # Got post request -> First we get the request arguemnts
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zipCode = request.form['zipCode']
        user_id = login_session['user_id']
        # Next we call the create_resturant function from the model module
        create_restaurant(name, address, city, state, zipCode, user_id)
        flash("Successfully created your new restaurant")
        # Finally we return the success html
        return render_template("submitted.html")
    else:
        return "Invalid http method"


@mod.route('/restaurants')
@mod.route('/restaurants/<int:restaurant_id>/')
def show_restaurants(restaurant_id=None):
    "Gets the url restaurant id and lists out info on that or all restaurants"
    # If user not logged in we just show view only restaurants
    if 'username' not in login_session:
        return render_template('restaurants/public_restaurants.html',
                               restaurants=read_restaurants(restaurant_id)[0])
    # If user is logged in we render restaurants.html page with user data
    else:
        r = read_restaurants(restaurant_id, login_session['user_id'])
        restaurants = r[0]
        owner = r[1]
        return render_template('restaurants/restaurants.html',
                               restaurants=restaurants,
                               owner=owner)


@mod.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
@valid_login_session
def edit_restaurant(restaurant_id):
    """Gets the url restaurant id and handles editing"""
    user_id = login_session['user_id']
    r = read_restaurants(restaurant_id, user_id)
    if r[1] is True:  # Means if user is owner
        if request.method == 'GET':
            return render_template('restaurants/editrestaurant.html',
                                   restaurant=r[0][0])
        elif request.method == 'POST':
            # Got post request -> First we get the request arguemnts
            name = request.form['name']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            zipCode = request.form['zipCode']
            # Next we do the db edit
            update_restaurant(restaurant_id, name, address,
                              city, state, zipCode)
            # Finally we return the success html
            flash("Edited your restaurant")
            return render_template("submitted.html")
        else:
            return "Invalid http"
    else:
        flash("You need to be the owner of the restaurant to edit")
        return redirect(url_for('site.show_restaurants',
                                restaurant_id=restaurant_id))


@mod.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
@valid_login_session
def remove_restaurant(restaurant_id):
    """Handler for deleteing restaurants"""
    user_id = login_session['user_id']
    r = read_restaurants(restaurant_id, user_id)
    if r[1] is True:  # Means if user is owner
        if request.method == 'POST':
            # Next we do the db delete
            delete_restaurant(restaurant_id)
            # Finally we return the success html
            flash("Deleted your restaurant")
            return render_template("submitted.html")
        else:
            return render_template('restaurants/deleterestaurant.html',
                                   restaurant=r[0][0])
    else:
        flash("You need to be the owner of the restaurant to delete")
        return redirect(url_for('site.show_restaurants',
                                restaurant_id=restaurant_id))
