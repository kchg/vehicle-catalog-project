from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

try:
    os.remove("vehiclecatalog.db")
except OSError: pass

from database_setup import Base, User, Category, Vehicle

engine = create_engine('sqlite:///vehiclecatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


owner = User(name="Kevin Chiang", email="kevinc9364@gmail.com")
session.add(owner)
session.commit()


luxurySedan = Category(user_id=1, name="Luxury Sedan")
session.add(luxurySedan)
session.commit()

bmw = Vehicle(user_id=1, year=2017, make="BMW", model="428i", price=15000.00 , category=luxurySedan)
session.add(bmw)
session.commit()

suv = Category(user_id=1, name="SUV")
session.add(suv)
session.commit()

jeep = Vehicle(user_id=1, year=2017, make="Jeep", model="Cherokee", price=35000.00 , category=suv)
session.add(jeep)
session.commit()

coupe = Category(user_id=1, name="Coupe")
session.add(coupe)
session.commit()

minivan = Category(user_id=1, name="Minivan")
session.add(minivan)
session.commit()

truck = Category(user_id=1, name="Truck")
session.add(truck)
session.commit()

motorcycle = Category(user_id=1, name="Motorcycle")
session.add(motorcycle)
session.commit()



print "added sample vehicles!"
