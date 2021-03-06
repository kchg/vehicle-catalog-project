import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'catalog_user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


    def is_authenticated(self):
        return True
    
    def get_id(self):
        return unicode(self.id)

class Category(Base):
    __tablename__ = 'category'
    name = Column(String(250), primary_key=True)
    user_id = Column(Integer, ForeignKey('catalog_user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
        }

class Vehicle(Base):
    __tablename__ = 'vehicle'
    id = Column(Integer, primary_key=True)

    year = Column(Integer, nullable=False)
    make = Column(String(80), nullable=False)
    model = Column(String(80), nullable=False)
    trim = Column(String(80))
    price = Column(Float, nullable = False)
    mileage = Column(Integer, nullable = False)
    description = Column(String(10000))
    
    image_url = Column(String(250))

    category_name = Column(String(80), ForeignKey('category.name'))
    category = relationship(Category, single_parent=True)

    user_id = Column(Integer, ForeignKey('catalog_user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'year': self.year,
            'make': self.make,
            'model': self.model,
            'trim': self.trim,
            'price': self.price,
            'mileage': self.mileage,
            'image_url': self.image_url,
            'description': self.description,
            'category_name': self.category_name,
            'id': self.id,
        }






engine = create_engine('postgresql://catalog:password@localhost/catalog')


Base.metadata.create_all(engine)
