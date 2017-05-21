from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from puppies import Base, Shelter, Puppy

import datetime

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

newchallenge = "--------------------------- NEW CHALLENGE! --------------------"

def Challenge_one():
    """
    Queries all puppies in the puppy table and prints out names
    alphabetically
    """
    print newchallenge
    q = session.query(Puppy).order_by(Puppy.name).all()
    namelist = []
    for pup in q:
        pupname = pup.name
        namelist.append(pupname)
    return namelist

print Challenge_one()

def Challenge_two():
    """
    Queries all the puppies, filters out those older than approx 6 months and order
    by age
    """
    print newchallenge
    today = datetime.date.today()
    # 6 months is 30*6 to simplify. Might revisit to calc months and leap years
    six_months_ago = today - datetime.timedelta(days = 30*6)
    print "Six months ago: " + str(six_months_ago)
    q = session.query(Puppy).filter(Puppy.dateOfBirth > six_months_ago).\
                        order_by(Puppy.dateOfBirth).all()
    namelist = []
    for pup in q:
        pupname = pup.name
        namelist.append(pupname)
    return namelist

print Challenge_two()

def Challenge_three():
    """Queries all puppies and orders by weight"""
    print newchallenge
    q = session.query(Puppy).order_by(Puppy.weight).all()
    namelist = []
    for pup in q:
        pupname = pup.name
        namelist.append(pupname)
    return namelist

print Challenge_three()

def Challenge_four():
    """Queries all the puppies and groups them by the shelter they are staying"""
    print newchallenge
    q = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
    namelist = []
    for pup in q:
        namelist.append((pup[0].name, pup[1]))
    return namelist

print Challenge_four()
