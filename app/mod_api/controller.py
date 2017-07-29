from flask import Blueprint, jsonify

from app.model.model_restaurants import read_restaurants
from app.model.model_menuitems import read_menuitems

mod = Blueprint('api', __name__)

# JSON REST API ---------------------------------------------------------------


@mod.route('/restaurants')
@mod.route('/restaurants/<int:resturant_id>')
def show_restaurants(restaurant_id=None):
    """Endpoint for getting json data on restaurants"""
    # First we get restaurant(s) as a list
    restaurants = read_restaurants(restaurant_id)[0]
    # Then we return it as json
    return jsonify(Restaurants=[r.serialize for r in restaurants])


@mod.route('/restaurants/<int:restaurant_id>/menu')
@mod.route('/restaurants/<int:restaurant_id>/menu/<int:menuitem_id>')
def show_menuitems(restaurant_id, menuitem_id=None):
    """Endpoint for getting json data on menuitems"""
    items = read_menuitems(restaurant_id, menuitem_id)
    return jsonify(MenuItems=[i.serialize for i in items])
