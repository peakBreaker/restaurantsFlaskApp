"""Contains the classes for the database models"""

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class restaurants(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    user_id = Column(Integer, ForeignKey('users.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class MenuItems(Base):
    __tablename__ = 'menuitems'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(1000))
    price = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
        }

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    email = Column(String(80), nullable = False)
    picture = Column(String(250))



engine = create_engine('sqlite:///restaurantmenuwithusers.db')

Base.metadata.create_all(engine)
