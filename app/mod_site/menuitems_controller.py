"""Holds handlers and controls flow for menuitems handeling"""

# Is there a better way to do this import rather than circular imports?
from . import mod
# Imports for flask
from flask import render_template, url_for, request, flash, redirect
# Imports for handeling sessions
from flask import session as login_session

from app.model.model_restaurants import read_restaurants

from app.model.model_menuitems  import  create_menuitem, \
                                        read_menuitems, \
                                        update_menuitem, \
                                        delete_menuitem

# HANDLERS FOR MENUITEMS -----------------------------------------------------------

@mod.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def new_menuitem(restaurant_id):
    """Checks user login, returns new menuitem form, and handles the post req"""
    # First check if user is logged in
    if 'username' not in login_session:
        flash("You need to be logged in to add items!")
        return redirect('/login')
    # Next we check the request type and handle it appropriately
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        success = create_menuitem(name, description, price, restaurant_id, login_session['user_id'])
        if success:
            flash("New menuitem created!")
            return redirect(url_for("site.show_menuitems", restaurant_id=restaurant_id))
    else:
        r = read_restaurants(restaurant_id, login_session['user_id'])
        restaurant = r[0][0]
        owner = r[1]
        if owner:
            return render_template('menuitems/newmenuitem.html', restaurant=restaurant)
        else:
            flash("You need to own the post to edit it!")
            return redirect(url_for('site.show_menuitems', restaurant_id=restaurant_id))

@mod.route('/restaurants/<int:restaurant_id>/menu')
@mod.route('/restaurants/<int:restaurant_id>/menu/<int:menuitem_id>')
def show_menuitems(restaurant_id, menuitem_id=None):
    """Lets user view all menuitems in db or for specific restaurant"""
    r = read_restaurants(restaurant_id, login_session['user_id'])
    restaurant = r[0][0]
    owner = r[1]
    items = read_menuitems(restaurant_id, menuitem_id)
    if 'username' not in login_session:
        return render_template  (
                                'menuitems/public_menuitems.html',
                                restaurant=restaurant, items=items
                                )
    else:
        # And return the data to the user
        return render_template('menuitems/menuitems.html', restaurant=restaurant, items=items, owner=owner)

@mod.route('/restaurants/<int:restaurant_id>/menu/<int:menuitem_id>/edit',\
            methods=['GET', 'POST'])
def edit_menuitem(restaurant_id, menuitem_id):
    """Handler which lets user edit a menutiem"""
    # First check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    # Next we check the request method and handle it appropriately
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        success = update_menuitem(menuitem_id, name, description, price)
        if success:
            flash("Menuitem edited!")
            return redirect(url_for("site.show_menuitems", restaurant_id=restaurant_id))
    else:
        menuitem = read_menuitems(restaurant_id, menuitem_id)[0]
        return render_template('menuitems/editmenuitem.html',
                                restaurant_id=restaurant_id,
                                item=menuitem)

@mod.route('/restaurants/<int:restaurant_id>/menu/<int:menuitem_id>/',\
            methods=['GET', 'POST'])
def remove_menuitem(restaurant_id, menuitem_id):
    """Handler which lets users delete menuitems"""
    # First check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    # Next we check if user is owner of restaurant
    user_id = login_session['user_id']
    r = read_restaurants(restaurant_id, user_id)
    if r[1] == True:
        if request.method == 'POST':
            deleted = delete_menuitem(menuitem_id)
            if deleted:
                flash("Menuitem deleted")
                return redirect(url_for("site.show_menuitems", restaurant_id=restaurant_id))
        else:
            return render_template('menuitems/deletemenuitem.html',
                                    restaurant_id=restaurant_id,
                                    menuitem_id=menuitem_id)
    else:
        # The user is not owner
        flash("You need to be the owner of the restaurant to delete menuitem")
        return redirect(url_for('site.show_restaurants', restaurant_id=restaurant_id))
