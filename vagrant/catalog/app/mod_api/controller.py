from flask import Blueprint

mod = Blueprint('api', __name__)

@mod.route('/getstuff')
def getstuff():
    return '{"result" : "You are accessing the api"}'


# JSON REST API ----------------------------------------------------------------

@mod.route('/resturant/<int:resturant_id>/menu/json')
@mod.route('/resturant/<int:resturant_id>/menu/<int:menuitem_id>/json')
def getjsondata(resturant_id=False, menuitem_id=False):
    print "got json request!"
    if menuitem_id == False:
        jsonfied = listmenujson(resturant_id)
        return jsonfied
    else:
        jsonfied = getitemjson(resturant_id, menuitem_id)
        return jsonfied
