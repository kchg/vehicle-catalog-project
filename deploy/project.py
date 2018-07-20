from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import session as login_session
from flask import make_response, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Vehicle
from functools import wraps
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random
import string
import httplib2
import json
import requests
import os

app = Flask(__name__)
client_secrets_file = '/var/www/vehicle-catalog-project/deploy/client_secrets.json'

CLIENT_ID = json.loads(
    open(client_secrets_file, 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"

engine = create_engine('postgresql://catalog:password@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def get_state():
    state = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return state


@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, login_session=login_session)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    print 'started gconnect'

    # Check state from client is the same as server state
    if request.args.get('state') != login_session['state']:
        print 'invalid'
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain one-time-code from client
    code = request.data
    print 'token validated'

    try:
        # Exchange the one-time-token for the credentials
        oauth_flow = flow_from_clientsecrets(client_secrets_file, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    print "done!"
    flash('Welcome %s!' % login_session['username'], "success")
    return 'done'


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']

    # Revoke access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token={0}'.format(
        login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        login_session.clear()
        flash('Sucessfully disconnected.', "success")
    else:
        login_session.clear()
        flash('Logged out but failed to revoke token for given user.',
              "warning")
    return redirect(url_for('catalog'))


@app.route('/')
@app.route('/catalog')
def catalog():
    categories = session.query(Category).all()
    recents = session.query(Vehicle).order_by(Vehicle.id.desc()).limit(10)
    return render_template('catalog.html', categories=categories,
                           recents=recents, login_session=login_session,
                           state=get_state())


@app.route('/catalog/<category_name>/items')
def categoryItems(category_name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Vehicle).filter_by(category_name=category.name)
    return render_template('category.html', categories=categories, items=items,
                           category=category, login_session=login_session,
                           state=get_state())


@app.route('/catalog/<category_name>/<item_id>/')
def item(category_name, item_id):
    category = session.query(Category).filter_by(name=category_name).one()
    vehicle = session.query(Vehicle).filter_by(category=category).filter_by(
        id=item_id).one()
    return render_template('vehicle.html', vehicle=vehicle,
                           login_session=login_session, state=get_state())


@app.route('/catalog/add', methods=['GET', 'POST'])
@app.route('/catalog/<category_name>/add', methods=['GET', 'POST'])
def addVehicle(category_name=None):
    if 'username' not in login_session:
        flash('Login to add new vehicles', "danger")
        if category_name is not None:
            return redirect(url_for('categoryItems',
                            category_name=category_name))
        return redirect('/')
    if request.method == 'POST':
        category_name = request.form.get('inputCategory', None)
        mileage = request.form.get('inputMileage', None)
        description = request.form.get('inputDescription', None)
        newVehicle = Vehicle(year=request.form.get('inputYear', None),
                             make=request.form.get('inputMake', None),
                             model=request.form.get('inputModel', None),
                             price=request.form.get('inputPrice', None),
                             category_name=category_name,
                             mileage=mileage,
                             description=description,
                             trim=request.form.get('inputTrim', ""),
                             image_url=request.form.get('inputURL', None),
                             user_id=login_session['user_id'])
        session.add(newVehicle)
        session.commit()
        flash('{0} {1} {2} {3} Added'.format(
            newVehicle.year, newVehicle.make, newVehicle.model,
            newVehicle.trim), "success")
        if category_name is not None:
            return redirect(url_for('categoryItems',
                                    category_name=category_name))
        return redirect('/')
    else:
        categories = session.query(Category).all()
        return render_template('addvehicle.html', category_name=category_name,
                               login_session=login_session, state=get_state(),
                               categories=categories)


@app.route('/catalog/<category_name>/<item_id>/edit', methods=['GET', 'POST'])
def editVehicle(item_id, category_name):
    if 'username' not in login_session:
        flash('Login to edit vehicles', 'danger')
        return redirect(url_for('item', category_name=category_name,
                                item_id=item_id))
    if request.method == 'POST':
        # Grab all the data from the editvehicle.html form
        editedVehicle = session.query(Vehicle).filter_by(
            category_name=category_name).filter_by(id=item_id).one()
        editedVehicle.year = request.form.get('inputYear', None)
        editedVehicle.make = request.form.get('inputMake', None)
        editedVehicle.model = request.form.get('inputModel', None)
        editedVehicle.trim = request.form.get('inputTrim', "")
        editedVehicle.price = request.form.get('inputPrice', None)
        editedVehicle.mileage = request.form.get('inputMileage', None)
        editedVehicle.description = request.form.get('inputDescription', None)
        editedVehicle.image_url = request.form.get('inputURL', None)
        editedVehicle.category_name = request.form.get('inputCategory', None)
        session.add(editedVehicle)
        session.commit()
        flash('{0} {1} {2} {3} Edited'.format(
            editedVehicle.year, editedVehicle.make,
            editedVehicle.model, editedVehicle.trim), "success")
        return redirect(url_for('item', category_name=category_name,
                                item_id=item_id))

    else:
        categories = session.query(Category).all()
        vehicle = session.query(Vehicle).filter_by(
            category_name=category_name).filter_by(id=item_id).one()
        if vehicle.user_id != login_session['user_id']:
            flash('You cannot edit this vehicle because you are not the owner',
                  'danger')
            return redirect(url_for('item', category_name=category_name,
                            item_id=item_id))
        return render_template(
            'editvehicle.html', category_name=category_name,
            vehicle=vehicle, categories=categories,
            state=get_state(), login_session=login_session)


@app.route('/catalog/<category_name>/<item_id>/delete',
           methods=['GET', 'POST'])
def deleteVehicle(item_id, category_name):
    if 'username' not in login_session:
        flash('Login to delete vehicles', 'danger')
        return redirect(url_for('item', category_name=category_name,
                                item_id=item_id))
    if request.method == 'POST':
        vehicle = session.query(Vehicle).filter_by(
            category_name=category_name).filter_by(
            id=item_id).one()
        session.delete(vehicle)
        session.commit()
        flash('Successfully deleted {0} {1} {2} {3}'.format(
            vehicle.year, vehicle.make, vehicle.model, vehicle.trim),
            "success")
        return redirect('/')
    else:
        categories = session.query(Category).all()
        vehicle = session.query(Vehicle).filter_by(
            category_name=category_name) .filter_by(id=item_id).one()
        if vehicle.user_id != login_session['user_id']:
            flash(('You cannot delete this vehicle '
                  'because you are not the owner'),
                  'danger')
            return redirect(url_for('item', category_name=category_name,
                                    item_id=item_id))
        return render_template(
            'deletevehicle.html', vehicle=vehicle,
            state=get_state(), login_session=login_session)


@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


@app.route('/catalog/<category_name>/JSON')
def categoryJSON(category_name):
    vehicles = session.query(Vehicle).filter_by(category_name=category_name)
    return jsonify(vehicles=[r.serialize for r in vehicles])


@app.route('/catalog/<category_name>/<item_id>/JSON')
def vehicleJSON(category_name, item_id):
    vehicle = session.query(Vehicle).filter_by(
        category_name=category_name).filter_by(id=item_id).one()
    return jsonify(vehicle=vehicle.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
