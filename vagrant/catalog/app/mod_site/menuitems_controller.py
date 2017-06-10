# Is there a better way to do this import rather than circular imports?
from . import mod
# Imports for flask
from flask import render_template, url_for, request, flash, redirect
# Imports for handeling sessions
from flask import session as login_session

from app.model.model_menuitems  import  insert_menuitem, \
                                        read_menuitems, \
                                        edit_menuitem, \
                                        delete_menuitem
print "running menuitems controller"
# HANDLERS FOR MENUITEMS -----------------------------------------------------------

@mod.route('/restaurants/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def new_menuitem(restaurant_id=False):
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

@mod.route('/menuitems')
@mod.route('/restaurants/<int:restaurant_id>/menu/<int:menuitem_id>')
def show_menu(restaurant_id=None, menuitem_id=None):
    """Lets user view all menuitems in db or for specific restaurant"""
    # We read the database to get manuitems and restaurant data
    items = read_menuitems(restaurant_id, menuitem_id)
    # And return the data to the user
    return render_template('menu.html', restaurant=restaurant, items=items)

@mod.route('/menu/<int:menuitem_id>/edit', methods = ['GET', 'POST'])
def edit_menuitem(menuitem_id=False):
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
def delete_menuitem(menuitem_id=False):
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
