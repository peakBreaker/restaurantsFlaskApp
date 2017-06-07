
from context import Base, Resturants, MenuItems

import random

def randprice():
    """Generates a random price for menuitem"""
    return random.randint(30, 120) + 0.99

def getname():
    """Gets a random name from foodnames file"""
    # foodnames downloaded from http://eatingatoz.com/food-list/
    s = u'%s' % random.sample(open('data/foodnames', 'r').read().split('\n'), 1)[0]
    return s

def getdescr():
    """Generates a random deescription for menuitem"""
    s = u'%s' % random.sample(open('data/loremipsum', 'r').read().split('\n'), 1)[0]
    return s

def generateMenuItem(resturantid, session):
    """Generates a menuitem object and adds it to session"""
    try:
        for i in range(0, 10):
            print "adding item.."
            menuitem = MenuItems(
                                name = getname(),
                                description = getdescr(),
                                price = randprice(),
                                resturant_id = resturantid
                                )
            session.add(menuitem)
            session.commit()
        return "seeded menuitems"
    except Exception as e:
        print "Something went wrong"
        return e

def seedMenuItems(session):
    """Gets the resturants in the db and seeds each resturant with 10 menuitems"""
    for r in session.query(Resturants).all():
        print "adding menuitems for resturant with id " + str(r.id)
        mi = generateMenuItem(r.id, session)
        print mi


    print "Success! Menuitems seeded in db.. returning"
    return
