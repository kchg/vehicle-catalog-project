# Used Vehicle Catalog Application

This project is for Udacity's [Full Stack Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004). This project exposes a database containing vehicles and their categories, allowing you to add, edit, and delete them through the Google OAuth authentication system. 


# How to run this project

- Install [VirtualBox](https://www.virtualbox.org/).
- Install [Vagrant](https://www.vagrantup.com/).
- Pull this code into your local environment.
- Navigate to the **vagrant** folder.
- Launch the vagrant configuration in your command line using `vagrant up`.
- Connect to your vagrant instance using `vagrant ssh`.
- Once launched, navigate to `/vagrant`.
- To set up the database, run `python database_setup.py`.
- To add sample vehicles, run `python addvehicles.py`.
- To launch the application, run `python project.py`.
- Finally, visit `http://localhost:5000` in your browser to interact with the application.

# Technologies Used
1. Python
2. SQL
3. Flask
4. SQLAlchemy
5. HTML/CSS
6. Bootstrap
7. OAuth

