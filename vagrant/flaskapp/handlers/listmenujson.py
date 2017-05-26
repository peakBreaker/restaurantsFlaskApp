"""This module handles listing out menuitems as json for the restapi"""

from flask import jsonify
from context import list_menu, get_resturantitem, MenuItems

def listmenujson(resturant_id):
    items = list_menu(resturant_id)
    return jsonify(MenuItems=[i.serialize for i in items])

def getitemjson(resturant_id, menuitem_id):
    item = get_resturantitem(resturant_id, menuitem_id)
    return jsonify(item)
