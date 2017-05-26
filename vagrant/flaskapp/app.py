"""This program routes the urls and requests to the correct handlers"""

from flask import Flask, url_for, render_template, request, flash, redirect
from model.model import list_resturants, list_menu, editname_resturant, delete_resturant

#Imports the handlers
from handlers.newresturant import insertresturant, render_newresturant

from handlers.newmenuitem import insertmenuitem, render_newmenuitem
from handlers.altermenuitem import  editmenuitem, render_editmenuitem, \
                                    deletemenuitem, render_deletemenuitem
from handlers.listmenujson import listmenujson, getitemjson


app = Flask(__name__)

# CRUD FOR RESTURANTS ----------------------------------------------------------

@app.route('/resturants/new', methods=['GET', 'POST'])
def NewResturants():
    """Gets the url resturant id and handles editing"""
    if request.method == 'POST':
        return insertresturant()
    else:
        return render_newresturant()

@app.route('/resturants')
@app.route('/resturants/<int:resturant_id>/')
def ListResturants(resturant_id=False):
    """Gets the url resturant id and lists out info on that or all resturants"""
    print resturant_id
    output = open("templates/resturants.html", "r")
    body = ""
    for r in list_resturants(resturant_id):
        body += """<div>Resturant: {} with id {id}</div> <a href='/resturant/{id}/edit'>
                Edit</a><br><a href='/resturant/{id}/delete'>Delete</a>
                """.format(r.name, id=r.id)
    output = (output.read().format(body))
    return output

@app.route('/resturants/<int:resturant_id>/edit')
def EditResturants(resturant_id=False):
    """Gets the url resturant id and handles editing"""
    output = open("views/editresturant.html", "r")
    output = output.read().format(id=resturant_id)
    return output

@app.route('/resturants/<int:resturant_id>/delete')
def DeleteResturant(resturant_id=0):
    output = open("views/deleteresturant.html", "r")
    output = output.read().format(id=resturant_id)
    return output

# CRUD FOR MENUITEMS -----------------------------------------------------------

@app.route('/menu/<int:resturant_id>/new', methods = ['GET', 'POST'])
def newmenuitem(resturant_id=False):
    if request.method == 'POST':
        success = insertnewmenuitem(resturant_id)
        if success:
            flash("New menuitem created!")
            return redirect(url_for("showmenu", resturant_id=resturant_id))
    else:
        return render_newmenuitem(resturant_id)

@app.route('/menu')
@app.route('/menu/<int:resturant_id>')
def showmenu(resturant_id=False):
    print "got request for resturantmenu"
    items = list_menu(resturant_id)
    resturant = list_resturants(resturant_id)
    return render_template('menu.html', resturant=resturant, items=items)

@app.route('/menu/<int:menuitem_id>/edit', methods = ['GET', 'POST'])
def editmenu(menuitem_id=False):
    print "Got request to edit"
    print menuitem_id
    if request.method == 'POST':
        resturant_id = editmenuitem(menuitem_id)
        if resturant_id:
            flash("Menuitem edited!")
            return redirect(url_for("showmenu", resturant_id=resturant_id))
    else:
        return render_editmenuitem(menuitem_id)

@app.route('/menu/<int:menuitem_id>/delete', methods=['GET', 'POST'])
def delmenuitem(menuitem_id=False):
    if request.method == 'POST':
        resturant_id = deletemenuitem(menuitem_id)
        if resturant_id:
            flash("Menuitem deleted!")
            return redirect(url_for("showmenu", resturant_id=resturant_id))
    else:
        return render_deletemenuitem(menuitem_id)

# JSON REST API

@app.route('/resturant/<int:resturant_id>/menu/json')
@app.route('/resturant/<int:resturant_id>/menu/<int:menuitem_id>/json')
def getjsondata(resturant_id=False, menuitem_id=False):
    print "got json request!"
    if menuitem_id == False:
        jsonfied = listmenujson(resturant_id)
        return jsonfied
    else:
        jsonfied = getitemjson(resturant_id, menuitem_id)
        return jsonfied


if __name__ == "__main__":
    app.secret_key = "my_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)
