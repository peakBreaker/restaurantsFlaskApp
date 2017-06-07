# Imports for flask
from flask import Blueprint, render_template, url_for, request, flash, redirect
# Imports for handeling sessions
from flask import session as login_session
import random, string
# Imports for dbmodels
from app.model.model_restaurants import  list_restaurants, \
                                        editname_restaurant, \
                                        delete_restaurant
from app.model.model_menuitems  import  list_menu
from app.model.model_users      import  createUser, getUserInfo, getUserID

mod = Blueprint('site', __name__)

# HANDLERS FOR RESTAURANTS -----------------------------------------------------

@mod.route('/restaurants/new', methods=['GET', 'POST'])
def Newrestaurants():
    """Validates user login_session, gives user a form and handles http post"""
    # First we validate user login
    if 'username' not in login_session:
        return redirect('/login')
    # Next we check weather user sends http get or post, and then do appropriate thing
    if request.method == 'POST':
        return insertrestaurant(login_session['user_id'])
    else:
        return render_template()

@mod.route('/restaurants')
@mod.route('/restaurants/<int:restaurant_id>/')
def Listrestaurants(restaurant_id=None):
    """Gets the url restaurant id and lists out info on that or all restaurants"""
    # First check if user is logged in
    if 'username' not in login_session:
        return render_template(
                                'restaurants/public.html',
                                restaurants=list_restaurants(restaurant_id)
                                )
    # If user is logged in we render restaurants.html page with appropriate data
    else:
        r = list_restaurants(restaurant_id, login_session['user_id'])
        restaurant = r[0]
        owner = r[1]
        print "checked restaurant in db.. restaurant is and user is owner?"
        print restaurant
        print owner
        return render_template(
                                'restaurants.html',
                                restaurants=restaurant,
                                owner=owner
                                )

@mod.route('/restaurants/<int:restaurant_id>/edit')
def Editrestaurants(restaurant_id=False):
    """Gets the url restaurant id and handles editing"""
    # First check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    else:
        return render_template('editrestaurants.html')

@mod.route('/restaurants/<int:restaurant_id>/delete')
def Deleterestaurant(restaurant_id=0):
    """Handler for deleteing restaurants"""
    if 'username' not in login_session:
        return redirect('/login')
    output = open("views/deleterestaurant.html", "r")
    output = output.read().format(id=restaurant_id)
    return output

# HANDLERS FOR MENUITEMS -----------------------------------------------------------

@mod.route('/restaurants/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def newmenuitem(restaurant_id=False):
    """Checks user login, returns new menuitem form, and handles the post req"""
    # First check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    # Next we check the request type and handle it appropriately
    if request.method == 'POST':
        success = insertnewmenuitem(restaurant_id, login_session['user_id'])
        if success:
            flash("New menuitem created!")
            return redirect(url_for("showmenu", restaurant_id=restaurant_id))
    else:
        return render_newmenuitem(restaurant_id)

@mod.route('/menu')
@mod.route('/restaurants/<int:restaurant_id>/menu')
def showmenu(restaurant_id=False):
    """Lets user view all menuitems in db or for specific restaurant"""
    # We read the database to get manuitems and restaurant data
    items = list_menu(restaurant_id)
    restaurant = list_restaurants(restaurant_id)
    # And return the data to the user
    return render_template('menu.html', restaurant=restaurant, items=items)

@mod.route('/menu/<int:menuitem_id>/edit', methods = ['GET', 'POST'])
def editmenu(menuitem_id=False):
    """Handler which lets user edit a menutiem"""
    # First check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    # Next we check the request method and handle it appropriately
    if request.method == 'POST':
        restaurant_id = editmenuitem(menuitem_id)
        if restaurant_id:
            flash("Menuitem edited!")
            return redirect(url_for("showmenu", restaurant_id=restaurant_id))
    else:
        return render_editmenuitem(menuitem_id)

@mod.route('/menu/<int:menuitem_id>/delete', methods=['GET', 'POST'])
def delmenuitem(menuitem_id=False):
    """Handler which lets users delete menuitems"""
    # First check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    # Next we check the request method and handle it appropriately
    if request.method == 'POST':
        restaurant_id = deletemenuitem(menuitem_id)
        if restaurant_id:
            flash("Menuitem deleted!")
            return redirect(url_for("showmenu", restaurant_id=restaurant_id))
    else:
        return render_deletemenuitem(menuitem_id)
