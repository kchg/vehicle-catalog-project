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

sample_description = """
PREMIUM PACKAGE. ONE OWNER. CARFAX CERTIFIED. LOW MILES. BACK UP CAMERA. PARK ASSIST. PREMIUM RED LEATHER INTERIOR. STEERING WHEEL CONTROLS. BLUETOOTH. PWR SUNROOF. DUAL CLIMATE CONTROL. AUTO START/STOP. PADDLE SHIFTERS. SPORT/ECO DRIVE. This BMW 4 Series has a strong Intercooled Turbo Premium Unleaded I-4 2.0 L/122 engine powering this Automatic transmission. Window Grid Diversity Antenna, Wheels: 18 x 8 Lt Alloy Double-Spoke (Style 397), Valet Function. Carfax One-Owner.*These Packages Will Make Your BMW 4 Series 428i the Envy of Onlookers*Trunk Rear Cargo Access, Trip Computer, Transmission: Sport Automatic, Tracker System, Tires: P225/45R18 All Season, Tire Specific Low Tire Pressure Warning, Tailgate/Rear Door Lock Included w/Power Door Locks, Systems Monitor, SULEV Emissions, Strut Front Suspension w/Coil Springs, Sport seats, Sport Leather Steering Wheel, Speed Sensitive Rain Detecting Variable Intermittent Wipers w/Heated Jets, Sliding Front Center Armrest and Rear Center Armrest, Single Stainless Steel Exhaust w/Dark Chrome Tailpipe Finisher.*Know You're Making a Reliable Purchase *Carfax reports: Carfax One-Owner Vehicle, No Damage Reported, No Accidents Reported.*Visit Us Today *Stop by Gravity Autos Duluth located at 2960 Satellite Blvd, Duluth, GA 30096 for a quick visit and a great vehicle!

Additional Information
TECHNOLOGY PACKAGE -inc: Head-Up Display Navigation System Remote Services Advanced Real-Time Traffic Information BMW Online & BMW Apps Instrument Cluster w/Extended Contents,CORAL RED/BLACK DAKOTA LEATHER UPHOLSTERY,ALPINE WHITE,PARKING ASSISTANT,ALUMINUM HEXAGON TRIM W/HIGH GLOSS BLACK HIGHLIGHT,Turbocharged,Rear Wheel Drive,Power Steering,ABS,4-Wheel Disc Brakes,Brake Assist,Aluminum Wheels,Tires - Front Performance,Tires - Rear Performance,Sun/Moonroof,Generic Sun/Moonroof,Heated Mirrors,Power Mirror(s),Integrated Turn Signal Mirrors,Power Folding Mirrors,Rear Defrost,Intermittent Wipers,Variable Speed Intermittent Wipers,Rain Sensing Wipers,Power Door Locks,Daytime Running Lights,HID headlights,Automatic Headlights,Headlights-Auto-Leveling,Fog Lamps,AM/FM Stereo,CD Player,MP3 Player,HD Radio,Steering Wheel Audio Controls,Auxiliary Audio Input,Bluetooth Connection,Power Driver Seat,Power Passenger Seat,Bucket Seats,Seat Memory,Pass-Through Rear Seat,Rear Bench Seat,Adjustable Steering Wheel,Trip Computer,Telematics,Leather Steering Wheel,Keyless Start,Keyless Entry,Universal Garage Door Opener,Cruise Control,Climate Control,Multi-Zone A/C,Rear A/C,Woodgrain Interior Trim,Premium Synthetic Seats,Auto-Dimming Rearview Mirror,Driver Vanity Mirror,Passenger Vanity Mirror,Driver Illuminated Vanity Mirror,Passenger Illuminated Visor Mirror,Floor Mats,Mirror Memory,Power Windows,Security System,Engine Immobilizer,Traction Control,Stability Control,Front Side Air Bag,Tire Pressure Monitor,Driver Air Bag,Passenger Air Bag,Front Head Air Bag,Rear Head Air Bag,Passenger Air Bag Sensor,Knee Air Bag
"""


convertible = Category(user_id=1, name="Convertible")
session.add(convertible)
session.commit()

camaro = Vehicle(user_id=1, year=2015, make="Chevrolet", model="Camaro", trim="LT Convertible",
mileage = 12000, description=sample_description, price=18345, category=convertible,
image_url="https://images.autotrader.com/scaler/653/490/hn/c/bf94417e357a4320abb5bb4357a9ffd2.jpg")
session.add(camaro)
session.commit()


lambo = Vehicle(user_id=2, year=2017, make="Lamborghini" ,model="Huracan", trim="LP 580-2 Spyder",
mileage=1254, description=sample_description, price=229533, category=convertible,
image_url="https://images.autotrader.com/scaler/653/490/hn/c/5e6f409af44f47bdb30ffaeff501c7e1.jpg")
session.add(lambo)
session.commit()


coupe = Category(user_id=1, name="Coupe")
session.add(coupe)
session.commit()

bmw = Vehicle(user_id=2, year=2017, make="BMW", model="428i", trim="Coupe",
  mileage=15000, description=sample_description, price=15000.00 , 
  image_url="https://images.autotrader.com/scaler/653/490/hn/c/fa0576661fb0455a9e507658549332a9.jpg",
  category=coupe)
session.add(bmw)
session.commit()

cadillac = Vehicle(user_id=1, year=2011, make="Cadillac", model="CTS", trim="Premium AWD Coupe",
  mileage=15000, description=sample_description, price=17345 , 
  image_url="https://images.autotrader.com/scaler/653/490/hn/c/05987a9c388341b28fc800bd17b25aa6.jpg",
  category=coupe)
session.add(cadillac)
session.commit()

bugatti = Vehicle(user_id=1, year=2010, make="Bugatti", model="Veyron", trim="",
mileage=6060, description=sample_description, price=1899950, category=coupe,
image_url="https://images.autotrader.com/scaler/653/490/hn/c/c7a6f38c06d142adb3c6e631fc8a020e.jpg")
session.add(bugatti)
session.commit()

hatchback = Category(user_id=1, name="Hatchback")
session.add(hatchback)
session.commit()


hatch = Vehicle(user_id=1, year=2015, make="Nissan", model="Leaf", trim="S",
mileage=53423, description=sample_description, price=10543, category=hatchback,
image_url="https://images.autotrader.com/scaler/653/490/hn/c/586119d6b54b46fc9d483222c79dc36c.jpg")
session.add(hatch)
session.commit()

hatch = Vehicle(user_id=1, year=2015, make="MINI", model="Cooper", trim="2-Door Hardtop",
mileage=53423, description=sample_description, price=14543, category=hatchback,
image_url="https://images.autotrader.com/scaler/653/490/hn/c/0fafd773c8e7452abd57d3f68f44a157.jpg")
session.add(hatch)
session.commit()


sedan = Category(user_id=1, name="Sedan")
session.add(sedan)
session.commit()


bmw = Vehicle(user_id=1, year=2012, make="BMW", model="328i", trim="Sedan",
  mileage=15000, description=sample_description, price=17000.00 , 
  image_url="https://images.autotrader.com/scaler/653/490/hn/c/91c97d8011254e0d93ff2d482f3479b8.jpg",
  category=sedan)
session.add(bmw)
session.commit()


ford = Vehicle(user_id=1, year=2017, make="Ford", model="Fusion", trim="SE",
mileage=32899, description=sample_description, price=11533, category=sedan,
image_url="https://images.autotrader.com/scaler/653/490/hn/c/26b7ccc468e94879bd7a9ff30f5c9ff6.jpg")
session.add(ford)
session.commit()


suv = Category(user_id=1, name="SUV")
session.add(suv)
session.commit()

jeep = Vehicle(user_id=1, year=2017, make="Jeep", model="Grand Cherokee", trim="Laredo",
mileage=40000, description=sample_description, price=35000.00 , category=suv,
image_url="https://images.autotrader.com/scaler/653/490/images/2017/5/31/457/059/43585821831.457059071.IM1.MAIN.640x480_A.640x480.jpg")
session.add(jeep)
session.commit()


truck = Category(user_id=1, name="Truck")
session.add(truck)
session.commit()

ford = Vehicle(user_id=1, year=2004, make="Ford", model="F350", trim="Lariat",
mileage=180000, description=sample_description, price=16464, category=truck,
image_url="https://images.autotrader.com/scaler/653/490/hn/c/533b228a2e9d469ebae1608f1643aa00.jpg")
session.add(ford)
session.commit()

minivan = Category(user_id=1, name="Minivan")
session.add(minivan)
session.commit()

van = Vehicle(user_id=1, year=2015, make="Nissan", model="Quest", trim="SV", 
mileage=43542, description=sample_description, price=16534, category=minivan,
image_url="https://images.autotrader.com/scaler/653/490/hn/c/4c01c44dd59b41a19781b25084678680.jpg")
session.add(van)
session.commit()

wagon = Category(user_id=1, name="Wagon")
session.add(wagon)
session.commit()

subaru = Vehicle(user_id=1, year=2016, make="Subaru", model="Outback", trim="2.5i Limited",
mileage=45634, description=sample_description, price=21845, category=wagon,
image_url="https://images.autotrader.com/scaler/653/490/hn/c/5b70bb542b28412ab15086310d0976de.jpg")
session.add(subaru)
session.commit()



print "added sample vehicles!"
