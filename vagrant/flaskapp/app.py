from flask import Flask
from model.model import list_resturants, list_menu, insert_resturant, editname_resturant, delete_resturant

app = Flask(__name__)

@app.route('/resturants')
@app.route('/resturants/<int:resturant_id>/')
def ListResturants(resturant_id=False):
    """Gets the url resturant id and lists out info on that or all resturants"""
    print resturant_id
    output = open("views/resturants.html", "r")
    body = ""
    for r in list_resturants(resturant_id):
        body += """<div>Resturant: {} with id {id}</div> <a href='/resturant/{id}/edit'>
                Edit</a><br><a href='/resturant/{id}/delete'>Delete</a>
                """.format(r.name, id=r.id)
    output = (output.read().format(body))
    return output

@app.route('/resturants/new')
def NewResturants():
    """Gets the url resturant id and handles editing"""
    output = open("views/newresturant.html", "r")
    output = output.read()
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

@app.route('/menu')
def listmenus():
    output = open("views/resturants.html", "r")
    body = ""
    for r in list_menu():
        body += """<div>Fooditem: {name}</div> <div> <b>Description: </b> {desc} </div> <br>
                <div> <b>Price: </b> {price} </div> <br> <div> {id}</div>
                <a href='/resturant/{id}/edit'>
                Edit</a><br><a href='/resturant/{id}/delete'>Delete</a>
                """.format(name = r.name, desc = r.description, price = r.price, id=r.id)
    output = (output.read().format(body))
    return output

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)
