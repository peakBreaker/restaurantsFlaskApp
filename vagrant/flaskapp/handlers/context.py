import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(
                        os.path.dirname(__file__), '..')))

from model.model_menuitems import list_menu, \
    insert_menuitem, edit_menuitem, delete_menuitem, get_resturantitem

from model.model_resturants import insert_resturant

from model.resturants import MenuItems
