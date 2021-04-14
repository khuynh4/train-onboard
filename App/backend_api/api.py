#!python3
from flask import Flask, request, jsonify, redirect, url_for, session
from flask_cors import cross_origin, CORS
from datetime import timedelta

from pyrebase import pyrebase

firebaseConfig = {
	'apiKey': "AIzaSyDe6g46cEfOWkyJpXXPtpnihper_Z60n0Q",
	'authDomain': "traindatabase-c33ac.firebaseapp.com",
	'projectId': "traindatabase-c33ac",
	'storageBucket': "traindatabase-c33ac.appspot.com",
	'messagingSenderId': "978921770047",
	'appId': "1:978921770047:web:bdd7ce0d3b1e987231fc8a",
	'measurementId': "G-RBYQ8DX7TF",
	'databaseURL': "https://traindatabase-c33ac-default-rtdb.firebaseio.com/"
	}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

#temporarily replace quote function
#there is an error in the pyrebase library that encodes quotes and special characters incorrectly to the url
#which has not been patched yet
#the below function and assignment temporarily fixes the problem until the library is patched
def noquote(s):
    return s
pyrebase.quote = noquote

app = Flask(__name__)
app.secret_key = 'ejIk28Ik3hhUUEik620ssnYYe78bbneYQ092'
app.permanent_session_lifetime = timedelta(days=5)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/index', methods=['GET'])
def index():
    
    #check if user session is still alive
    if 'uuid' in session:
        #refresh id token in case it has expired
        access_token = auth.refresh(session['refreshToken'])['idToken']

        #update session id token
        session['access_token'] = access_token

        payload = {
            'headers': {'Access-Control-Allow-Origin': '*'},
            'access_token': access_token,
            'uuid': session['uuid'],
            'name': session['name'],
            'email': session['email'],
            'redirect_url': url_for('/api/user'),
            'isLoggedIn': True
        }

        return jsonify(payload), 200

    else:

        payload = {
            'headers': {'Access-Control-Allow-Origin': '*'},
            'access_token': '',
            'uuid': '',
            'name': '',
            'email': '',
            'redirect_url': '',
            'isLoggedIn': False
        }

        return jsonify(payload), 200


        


@app.route('/api/login', methods=['POST'])
@cross_origin()
def login():
    #header required to send information between servers cross origin
    header = {'Access-Control-Allow-Origin': '*'}

    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400

    email = req.get('email')
    password = req.get('password')

    if not email:
        return jsonify({'headers': header, 'msg': 'email is missing'}), 400
    
    if not password:
        return jsonify({'headers': header, 'msg': 'Password is missing'}), 400
    
    try:
        user = auth.sign_in_with_email_and_password(email, password)
    except:
        return jsonify({'headers': header, 'route': url_for('api/signup')})
    
    #deal with session variables to keep track of user information to pass around backend and frontend easily
    session.permamnent = True
    session['email'] = email

    user_data = db.child('Users').order_by_child("email").equal_to(email).get().val()
    user_uuid = list(user_data.keys())[0]
    name = user_data[user_uuid]['name']

    session['uuid'] = user_uuid
    session['name'] = name
    session['refresh_token'] = user['refreshToken']

    payload = {
        'headers': header,
        'access_token': user['idToken'],
        'uuid': user_uuid,
        'name': name,
        'email': email,
        'isLoggedIn': True
    }

    return jsonify(payload), 200

@app.route('/api/signup', methods=['POST'])
@cross_origin() #needed to allow the backend server to receive data from frontend server cross origin
def signup():
    header = {'Access-Control-Allow-Origin': '*'}
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400
    
    first_name = req.get('first_name')
    last_name = req.get('last_name')
    email = req.get('email')
    age = req.get('age')
    address = req.get('address')
    password = req.get('password')
    confirm_pass = req.get('confirm_pass')

    if not first_name:
        return jsonify({'headers': header, 'msg': 'First Name is missing'}), 400
    
    if not last_name:
        return jsonify({'headers': header, 'msg': 'Last Name is missing'}), 400
    
    if not email:
        return jsonify({'headers': header, 'msg': 'Email is missing'}), 400
    
    if not age:
        return jsonify({'headers': header, 'msg': 'Age is missing'}), 400
    
    if not address:
        return jsonify({'headers': header, 'msg': 'Address is missing'}), 400
    
    if not password:
        return jsonify({'headers': header, 'msg': 'Password is missing'}), 400

    if not confirm_pass:
        return jsonify({'headers': header, 'msg': 'Confirm Password is missing'}), 400

    
    if not password == confirm_pass:
        return jsonify({'headers': header, 'msg': 'Password and confirm password do not match.'}), 400

    try:
        user = auth.create_user_with_email_and_password(email, password)
    except Exception as e:
        attrs = vars(e)
        print(attrs)
        return jsonify({'headers': header, 'msg': 'User already exists.', 'url': url_for('/api/login')}), 400

    #deal with session variables
    session['user'] = f'{first_name} {last_name}'
    session['email'] = f'{email}'
    session['idToken'] = user['idToken']
    session['refreshToken'] = user['refreshToken']

    #send verification email
    auth.send_email_verification(user['idToken'])

    #put data into database
    data = {
        'name': f'{first_name} {last_name}',
        'email': email,
        'age': age,
        'address': address
    }

    db.child('Users').push(data)

    #retrieve user uuid
    user_uuid = list(db.child('Users').order_by_child('email').equal_to(email).get().val().keys())[0]

    session['uuid'] = user_uuid
    session.permanent = True

    payload = {
        'headers': header,
        'access_token': user['idToken'],
        'uuid': user_uuid,
        'name': f'{first_name} {last_name}',
        'email': email,
        'isLoggedIn': True
    }

    return jsonify(payload), 200
    
@app.route('/api/logout', methods=['GET'])
def logout():
    #pop all session variables
    for session_var in session.keys():
        session.pop(session_var, None)

    #return route for index and make logged in false
    payload = {
        'header': {'Access-Control-Allow-Origin': '*'},
        'url': url_for('/index'),
        'isLoggedIn': False
    }

    return jsonify(payload), 200


###
"""
Manager Methods
query methods - get manager's employees (done), get specific employee plan_id (done), get specific employee plan contents (done),
get template_ids (done), get specific template contents (done), get specific task in plan or template (done), 

add methods - add task to specific employee plan (done), add task to specific template (done), add template to plan (done), add documentation/links to specific task (done),
update specific task's name/note/due date/duration (done)

remove methods - remove task from specific employee plan or specific template (written, but implementation depends on schema we choose), remove documentation/link/notes/due date from specific task
"""
###

# expect request to have the following fields: manager_uuid
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# this method uses the manager_uuid and queries the database to get a dictionary of trainee_uuid/name pairs of the manager's trainees
# and returns a json of the dictionary of trainee_uuid/name pairs
@app.route('/manager/get_trainees', methods=['GET'])
def get_trainees():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400
    
    manager_uuid = req.get('manager_uuid')

    if not manager_uuid:
        return jsonify({'headers': header, 'msg': 'Missing manager uuid'}), 400

    # TODO rename "Trainees" to trainees OR make all keys capitalized in databases
    try:
        trainees = db.child('Managers').order_by_key().equal_to(manager_uuid).get().val()[manager_uuid]["Trainees"]
    except:
        trainees = {}

    payload = {
        'headers': header,
        'trainees' : trainees
    }

    return jsonify(payload), 200

# expect request to have the following fields: manager_uuid, trainee_uuid
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the trainee_uuid field should contain the uuid of the trainee whose plan should be retrieved. This value can be gotten from the /manager/get_trainees endpoint
# this method uses the trainee_uuid and queries the Trainees database to get a string of the trainee's plan_id and returns a json of the plan_id
@app.route('/manager/get_trainee_training_plan_id', methods=['GET'])
def manager_get_trainee_training_plan_id():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400
    
    manager_uuid = req.get('manager_uuid')
    trainee_uuid = req.get('trainee_uuid')

    if not manager_uuid:
        return jsonify({'headers': header, 'msg': 'Missing manager uuid'}), 400
    if not trainee_uuid:
        return jsonify({'headers': header, 'msg': 'Missing trainee uuid'}), 400

    try:
        plan_id = db.child('Trainees').order_by_key().equal_to(trainee_uuid).get().val()[trainee_uuid]['plan']
    except:
        plan_id = ""

    payload = {
        'headers': header,
        'plan_id' : plan_id
    }

    return jsonify(payload)

# expect request to have the following fields: manager_uuid, plan_id
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the plan_id field should contain the plan_id of the plan which should be retrieved. This value can be gotten from the /manager/get_trainee_training_plan_id endpoint
# this method uses the plan_id and queries the Plans database to get the dictionary of training_id : training_name from the plan (both from the templates associated with
# the plan and trainings added directly to the plan). It returns a json of the dictionary of training_id : training_name.
@app.route('/manager/get_trainee_training_plan_contents', methods=['GET'])
def manager_get_trainee_training_plan_contents():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400
    
    manager_uuid = req.get('manager_uuid')
    plan_id = req.get('plan_id')

    if not manager_uuid:
        return jsonify({'headers': header, 'msg': 'Missing manager uuid'}), 400
    if not plan_id:
        return jsonify({'headers': header, 'msg': 'Missing plan id'}), 400

    # get trainings added directly to the plan first (trainings will be a dict of training_id : training_name)
    try:
        trainings = db.child('Plans').order_by_key().equal_to(plan_id).get().val()[plan_id]['trainings']
    except:
        trainings = {}

    # now get trainings from the templates (templates will be a dict of template_id : template_name)
    try:
        template_ids = db.child('Plans').order_by_key().equal_to(plan_id).get().val()[plan_id]['templates']
        for template_id in template_ids.keys():
            # index into the templates table using the template_id and get the trainings (template_trainings will be a dict of training_id : training_name)
            template_trainings = db.child('Templates').order_by_key().equal_to(template_id).get().val()[template_id]['trainings']
            # merge the trainings from this template into the trainings dict
            trainings.update(template_trainings)
    except:
        pass

    payload = {
        'headers' : header,
        'trainings' : trainings
    }
    
    return jsonify(payload)

# expect request to have the following fields: manager_uuid
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# this method uses to manager_uuid to query the Managers database to get
# the a dictionary of the manager's training template_id : template_name pairs. It returns a json of the dictionary of template_id : template_name pairs
@app.route('/manager/get_training_templates', methods=['GET'])
def get_training_templates():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400
    
    manager_uuid = req.get('manager_uuid')

    if not manager_uuid:
        return jsonify({'headers': header, 'msg': 'Missing manager uuid'}), 400

    try:
        templates = db.child('Managers').order_by_key().equal_to(manager_uuid).get().val()[manager_uuid]['templates']
    except:
        templates = {}

    payload = {
        'headers' : header,
        'templates' : templates
    }

    return jsonify(payload)

# expect the request to have the following fields: manager_uuid, template_id
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the template_id should contain the template_id for the template the manager wants to retrieve. This value can be gotten from the /manager/get_training_templates endpoint
# this method uses the template_id to query the Templates database to get a dictionary of training_id : training_name. The method
# returns a json of the dictionary of training_id : training_name pairs.
@app.route('/manager/get_training_template', methods=['GET'])
def get_training_template():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400
    
    manager_uuid = req.get('manager_uuid')
    template_id = req.get('template_id')

    if not manager_uuid:
        return jsonify({'headers': header, 'msg': 'Missing manager uuid'}), 400
    if not template_id:
        return jsonify({'headers': header, 'msg': 'Missing template id'}), 400

    try:
        trainings = db.child('Templates').order_by_key().equal_to(template_id).get().val()[template_id]
    except:
        trainings = {}

    payload = {
        'headers' : header,
        'trainings' : trainings
    }

    return jsonify(payload)

# expect the request to have the following fields: manager_uuid, training_id
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the training_id field should contain the training_id for which you want to get the training's contents. 
# This value can be gotten from the /manager/get_training_template or /manager/get_trainee_training_plan_contents endpoints.
# this method uses the training_id to query the Trainings database to get the training contents. It returns the training
# contents as a json.
@app.route('/manager/get_training', methods=['GET'])
def get_training():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400
    
    manager_uuid = req.get('manager_uuid')
    training_id = req.get('training_id')

    if not manager_uuid:
        return jsonify({'headers': header, 'msg': 'Missing manager uuid'}), 400
    if not training_id:
        return jsonify({'headers': header, 'msg': 'Missing training id'}), 400

    try:
        training = db.child('Trainings').order_by_key().equal_to(training_id).get().val()[training_id]
    except:
        training = {}

    payload = {
        'headers' : header,
        'trainings' : training
    }

    return jsonify(payload)

# expect the request to have the following fields: manager_uuid, template_name
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the template_name is supplied by the client
# this method adds a new empty template to the manager and returns a json dictionary of template_id : template_name
# TODO possibly rewrite how the empty template is added to the Templates database so it doesn't have an entry at all.
# Would require rewriting the methods that modify templates to check for that and make a new entry if it doesn't exist. Probably
# better than how it is now, where there's just a dummy training ID for each template.
@app.route('/manager/new_empty_template', methods=['POST'])
def new_empty_template():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400
    
    manager_uuid = req.get('manager_uuid')
    template_name = req.get('template_name')

    if not manager_uuid:
        return jsonify({'headers': header, 'msg': 'Missing manager uuid'}), 400
    if not template_name:
        return jsonify({'headers': header, 'msg': 'Missing template name'}), 400

    template_id = db.generate_key()

    data = {"no_training_id" : "no_training_name"}

    # make new empty template in Templates database
    db.child('Templates').child(template_id).set(data)

    # add template reference to manager
    # since we can't append to database, get the template info from the manager (will be a dict of template_id : template_name)
    try:
        templates = db.child('Managers').order_by_key().equal_to(manager_uuid).get().val()['templates']
    except:
        templates = {}

    templates.update({template_id : template_name})

    # set plan's template data by combining the templates dict with a dict of the new template_id : template_name to be added
    try:
        db.child('Managers').child(manager_uuid).child('templates').update(templates)
    except: # the Manager doesn't currently have any templates so it needs to bet set for the first time
        db.child('Managers').child(manager_uuid).child('templates').set(templates)

    payload = {
        'headers' : header,
        'template' : {template_id : template_name}
    }

    return jsonify(payload)

# expect the request to have the following fields: manager_uuid, template_id, training_name, documentation_links, other_links, note, due_date, duration
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the template_id can be gotten from the endpoint /manager/new_empty_template or /manager/get_training_templates
# the training_name is a string supplied by the user
# the documentation links are a dictionary of link : name supplied by the user
# the other links are a dictionary of link : name supplied by the user
# the note is a string supplied by the user
# the due_date is a string supplied by the user
# the duration is a string supplied by the user
# this method makes a new training and adds that training to the given template. It returns the training_id : training_name
@app.route('/manager/add_training_to_training_template', methods=['POST'])
def add_training_to_training_template():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400

    manager_uuid = req.get('manager_uuid')
    template_id = req.get('template_id')
    training_name = req.get('training_name')
    documentation_links = req.get('documentation_links')
    other_links = req.get('other_links')
    note = req.get('note')
    due_date = req.get('due_date')
    duration = req.get('duration')

    if not manager_uuid:
        return jsonify({'headers': header, 'msg': 'Missing manager uuid'}), 400
    if not template_id:
        return jsonify({'headers': header, 'msg': 'Missing template id'}), 400
    if not training_name:
        return jsonify({'headers': header, 'msg': 'Missing training name'}), 400
    if not documentation_links:
        return jsonify({'headers': header, 'msg': 'Missing documentation links'}), 400
    if not other_links:
        return jsonify({'headers': header, 'msg': 'Missing other links'}), 400
    if not note:
        return jsonify({'headers': header, 'msg': 'Missing note'}), 400
    if not due_date:
        return jsonify({'headers': header, 'msg': 'Missing due date'}), 400
    if not duration:
        return jsonify({'headers': header, 'msg': 'Missing duration'}), 400

    # make a new training
    training_key = db.generate_key()
    data = {
        'name' : training_name,
        'note' : note,
        'due_date' : due_date,
        'duration' : duration,
        'complete' : 'false'
    }
    db.child('Trainings').child(training_key).set(data)
    db.child('Trainings').child(training_key).child('documentation_links').set(documentation_links)
    db.child('Trainings').child(training_key).child('other_links').set(other_links)

    # TODO might want to rewrite this to handle templates with no trainings in them
    # TODO make robust once decide that
    # since we can't append to database, get the trainings currently in the template (will be a dict of training_id : training_name)
    trainings = db.child('Templates').order_by_key().equal_to(template_id).get().val()[template_id]

    # set template data by combining the templates dict with a dict of the new training_id : training name to be added
    trainings.update({training_key : training_name})
    db.child('Templates').child(template_id).update(trainings)

    payload = {
        'headers' : header,
        'training' : {training_key : training_name}
    }

    return jsonify(payload)

# expect the request to have the following fields: manager_uuid, template_id, template_name, plan_id
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the template_id can be gotten from the endpoint /manager/new_empty_template or /manager/get_training_templates
# the template name is a string supplied by the user
# the plan id can be gotten from the endpoint /manager/get_trainee_training_plan_id
# this method adds the template_id to the templates field of the given plan and returns success or failure
@app.route('/manager/add_template_to_training_plan', methods=['POST'])
def add_template_to_training_plan():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400

    manager_uuid = req.get('manager_uuid')
    template_id = req.get('template_id')
    template_name = req.get('template_name')
    plan_id = req.get('plan_id')

    if not manager_uuid:
        return jsonify({'headers': header, 'msg': 'Missing manager uuid'}), 400
    if not template_id:
        return jsonify({'headers': header, 'msg': 'Missing template id'}), 400
    if not template_name:
        return jsonify({'headers': header, 'msg': 'Missing template name'}), 400
    if not plan_id:
        return jsonify({'headers': header, 'msg': 'Missing plan id'}), 400

    # TODO make robust
    # since we can't append to database, get the template info currently in the plan (will be a dict of template_id : template_name)
    templates = db.child('Plans').order_by_key().equal_to(plan_id).get().val()['templates']

    # set plan's template data by combining the templates dict with a dict of the new template_id : template_name to be added
    templates.update({template_id : template_name})
    db.child('Plans').child(plan_id).child('templates').update(templates)

    payload = {
        'headers' : header,
        'response' : "success"
    }

    return jsonify(payload)

# expect the request to have the following fields: manager_uuid, plan_id, training_name, documentation_links, other_links, note, due_date, duration
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the plan id can be gotten from the endpoint /manager/get_trainee_training_plan_id
# the training_name is a string supplied by the user
# the documentation links are a dictionary of link : name supplied by the user
# the other links are a dictionary of link : name supplied by the user
# the note is a string supplied by the user
# the due_date is a string supplied by the user
# the duration is a string supplied by the user
# this method makes a new training and adds that training to the given plan. It returns the training_id : training_name
@app.route('/manager/add_training_to_training_plan', methods=['POST'])
def add_training_to_training_plan():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400

    manager_uuid = req.get('manager_uuid')
    plan_id = req.get('plan_id')
    training_name = req.get('training_name')
    documentation_links = req.get('documentation_links')
    other_links = req.get('other_links')
    note = req.get('note')
    due_date = req.get('due_date')
    duration = req.get('duration')

    if not manager_uuid:
        return jsonify({'headers': header, 'msg': 'Missing manager uuid'}), 400
    if not plan_id:
        return jsonify({'headers': header, 'msg': 'Missing plan id'}), 400
    if not training_name:
        return jsonify({'headers': header, 'msg': 'Missing training name'}), 400
    if not documentation_links:
        return jsonify({'headers': header, 'msg': 'Missing documentation links'}), 400
    if not other_links:
        return jsonify({'headers': header, 'msg': 'Missing other links'}), 400
    if not note:
        return jsonify({'headers': header, 'msg': 'Missing note'}), 400
    if not due_date:
        return jsonify({'headers': header, 'msg': 'Missing due date'}), 400
    if not duration:
        return jsonify({'headers': header, 'msg': 'Missing duration'}), 400

    # make a new training
    training_key = db.generate_key()
    data = {
        'name' : training_name,
        'note' : note,
        'due_date' : due_date,
        'duration' : duration,
        'complete' : 'false'
    }
    db.child('Trainings').child(training_key).set(data)
    db.child('Trainings').child(training_key).child('documentation_links').set(documentation_links)
    db.child('Trainings').child(training_key).child('other_links').set(other_links)

    # TODO might want to rewrite this to handle plans with no trainings in them
    # TODO make robust once decide that
    # since we can't append to database, get the trainings currently in the plan (will be a dict of training_id : training_name)
    trainings = db.child('Plans').order_by_key().equal_to(plan_id).get().val()[plan_id]['trainings']

    # set plan's training data by combining the trainings dict with a dict of the new training_id : training_name to be added
    trainings.update({training_key : training_name})
    db.child('Plans').child(plan_id).child('trainings').update(trainings)

    payload = {
        'headers' : header,
        'training' : {training_key : training_name}
    }

    return jsonify(payload)

# expect the request to have the following fields: manager_uuid, training_id, documentation_links, other_links
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the training_id can be gotten from the endpoint /manager/add_training_to_training_plan, /manager/add_training_to_training_template, or /manager/get_trainee_training_plan_contents
# the documentation links are a dictionary of link : name supplied by the user
# the other links are a dictionary of link : name supplied by the user
# manager_uuid and training_id are required. For the other fields, if there is nothing to be added, do not include them in the request.
# this method APPENDS info to the relevant fields
@app.route('/manager/add_info_to_training', methods=['POST'])
def add_info_to_training():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400

    manager_uuid = req.get('manager_uuid')
    training_id = req.get('training_id')
    documentation_links = req.get('documentation_links')
    other_links = req.get('other_links')

    if not manager_uuid:
        return jsonify({'headers': header, 'msg': 'Missing manager uuid'}), 400
    if not training_id:
        return jsonify({'headers': header, 'msg': 'Missing training id'}), 400

    # TODO make robust
    # since we can't append to database, need to get current list of things, then add to it
    training = db.child('Trainings').order_by_key().equal_to(training_id).get().val()[training_id]

    if documentation_links:
        original_documentation_links = training['documentation_links'] # will be a dict of {link : name}
        original_documentation_links.update(documentation_links) # combine the original dict with the new dict
        db.child('Trainings').child(training_id).child('documentation_links').update(original_documentation_links)

    if other_links:
        original_other_links = training['other_links'] # will be a dict of {link : name}
        original_other_links.update(other_links) # combine the original dict with the new dict
        db.child('Trainings').child(training_id).child('other_links').update(original_other_links)

    payload = {
        'headers' : header,
        'response' : "success"
    }

    return jsonify(payload)

# expect the request to have the following fields: manager_uuid, training_id, training_name, note, due_date, duration
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the training_id can be gotten from the endpoint /manager/add_training_to_training_plan, /manager/add_training_to_training_template, or /manager/get_trainee_training_plan_contents
# training_name is a string supplied by the user
# note is a string supplied by the user
# due_date is a string supplied by the user
# duration is a string supplied by the user
# manager_uuid and training_id are required. For the other fields, put an empty string in the fields that you don't want to overwrite
# the authorization header should contain the user's verification token received from logging in
# this method verifies the verification token to get the manager uuid, and OVERWRITES info in the relevant fields
@app.route('/manager/update_training_info', methods=['POST'])
def update_training_info():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400

    manager_uuid = req.get('manager_uuid')
    training_id = req.get('training_id')
    training_name = req.get('training_name')
    note = req.get('note')
    due_date = req.get('due_date')
    duration = req.get('duration')

    if not manager_uuid:
        return jsonify({'headers': header, 'msg': 'Missing manager uuid'}), 400
    if not training_id:
        return jsonify({'headers': header, 'msg': 'Missing training id'}), 400

    # TODO make robust
    if training_name:
        db.child('Trainings').child(training_id).child('name').update(training_name)
    
    if note:
        db.child('Trainings').child(training_id).child('note').update(note)

    if due_date:
        db.child('Trainings').child(training_id).child('due_date').update(due_date)

    if duration:
        db.child('Trainings').child(training_id).child('duration').update(duration)

    payload = {
        'headers' : header,
        'response' : "success"
    }

    return jsonify(payload)

# expect the request to have the following fields: manager_uuid, template_id, training_id
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the template_id can be gotten from the endpoint /manager/new_empty_template or /manager/get_training_templates
# the training_id can be gotten from the endpoint /manager/add_training_to_training_plan, /manager/add_training_to_training_template, or /manager/get_trainee_training_plan_contents
# this method uses the template_id and training_id to remove the training
# from the template and delete it from the database (safe, since it can only be pointed to from the template)
@app.route('/manager/remove_training_from_template', methods=['POST'])
def remove_training_from_template():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400

    manager_uuid = req.get('manager_uuid')
    template_id = req.get('template_id')
    training_id = req.get('training_id')

    if not manager_uuid:
        return jsonify({'headers': header, 'msg': 'Missing manager uuid'}), 400
    if not template_id:
        return jsonify({'headers': header, 'msg': 'Missing template id'}), 400
    if not training_id:
        return jsonify({'headers': header, 'msg': 'Missing training id'}), 400

    #TODO make robust
    # get the trainings currently in the template (will be a dict of training_id : training_name)
    trainings = db.child('Templates').order_by_key().equal_to(template_id).get().val()[template_id]
    # remove the training entry from the dict - using pop() so it won't crash if the key isn't present
    trainings.pop(training_id, None)
    # update the templates entry
    db.child('Templates').child(template_id).update(trainings)

    # remove the training entry in the Trainings table that corresponds to the training_id
    db.child('Trainings').child(training_id).remove()

    payload = {
        'headers' : header,
        'response' : "success"
    }

    return jsonify(payload)

# expect the request to have the following fields: plan_id, training_id
# this method verifies the verification token and uses the plan_id and training_id to remove the training
# from the plan and delete it from the database (safe, since it can only be pointed to from the plan)
@app.route('/manager/remove_training_from_plan', methods=['POST'])
def remove_training_from_plan():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400

    manager_uuid = req.get('manager_uuid')
    plan_id = req.get('plan_id')
    training_id = req.get('training_id')

    if not manager_uuid:
        return jsonify({'headers': header, 'msg': 'Missing manager uuid'}), 400
    if not plan_id:
        return jsonify({'headers': header, 'msg': 'Missing plan id'}), 400
    if not training_id:
        return jsonify({'headers': header, 'msg': 'Missing training id'}), 400

    # TODO make robust
    # get the trainings currently in the plan (will be a dict of training_id : training_name)
    trainings = db.child('Plans').order_by_key().equal_to(plan_id).get().val()[training_id]
    # remove the training entry from the dict - using pop() so it won't crash if the key isn't present
    trainings.pop(training_id, None)
    # update the plan entry
    db.child('Plans').child(training_id).update(trainings)

    # remove the training entry in the Trainings table that corresponds to the training_id
    db.child('Trainings').child(training_id).remove()

    payload = {
        'headers' : header,
        'response' : "success"
    }

    return jsonify(payload)




if __name__ == '__main__':
    app.run(port=5000, debug=True)