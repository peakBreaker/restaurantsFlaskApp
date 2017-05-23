from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Resturants(Base):
    __tablename__ = 'resturants'
    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))

class MenuItems(Base):
    __tablename__ = 'menuitems'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(1000))
    price = Column(Integer)
    resturant_id = Column(Integer, ForeignKey('resturants.id'))

engine = create_engine('sqlite:///resturants.db')

Base.metadata.create_all(engine)
