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

    try:
        db.child('Managers').order_by_key().equal_to(user_uuid).get().val()[user_uuid]
        designation = "manager"
    except:
        try:
            db.child('Trainees').order_by_key().equal_to(user_uuid).get().val()[user_uuid]
            designation = "trainee"
        except:
            designation = "unassigned"

    session['uuid'] = user_uuid
    session['name'] = name
    session['refresh_token'] = user['refreshToken']

    payload = {
        'headers': header,
        'access_token': user['idToken'],
        'uuid': user_uuid,
        'name': name,
        'email': email,
        'designation' : designation,
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
        'url': url_for('.index'),
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
# this method uses the manager_uuid and queries the database to get a dictionary of trainee_name : trainee_uuid pairs of the manager's trainees
# and returns a json of the dictionary of {trainee_name : trainee_uuid} pairs
@app.route('/manager/get_trainees', methods=['GET'])
def manager_get_trainees():
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
# this method uses the trainee_uuid and queries the Trainees database to get a string of the trainee's plan_id and return it
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
# the plan and trainings added directly to the plan). It returns a json of the dictionary of training_id : training_name pairs.
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
        trainings = db.child('Plans').order_by_key().equal_to(plan_id).get().val()[plan_id]['Trainings']
    except:
        trainings = {}

    # now get trainings from the templates (templates will be a dict of template_id : template_name)
    try:
        template_ids = db.child('Plans').order_by_key().equal_to(plan_id).get().val()[plan_id]['Templates']
        for template_id in template_ids.keys():
            # index into the templates table using the template_id and get the trainings (template_trainings will be a dict of training_id : training_name)
            template_trainings = db.child('Templates').order_by_key().equal_to(template_id).get().val()[template_id]['Trainings']
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
        templates = db.child('Managers').order_by_key().equal_to(manager_uuid).get().val()[manager_uuid]['Templates']
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
# returns a json of the dictionary of template's manager, the template name, and the template's training_id : training_name pairs.
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
        template = db.child('Templates').order_by_key().equal_to(template_id).get().val()[template_id]
    except:
        template = {}

    payload = {
        'headers' : header,
        'template' : template
    }

    return jsonify(payload)

# expect the request to have the following fields: manager_uuid, training_id
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the training_id field should contain the training_id for which you want to get the training's contents. 
# This value can be gotten from the /manager/get_training_template or /manager/get_trainee_training_plan_contents endpoints.
# this method uses the training_id to query the Trainings database to get the training contents. It returns the training
# contents as a json.
@app.route('/manager/get_training', methods=['GET'])
def manager_get_training():
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
        'training' : training
    }

    return jsonify(payload)

# expect the request to have the following fields: manager_uuid, template_name
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the template_name is supplied by the client
# this method adds a new empty template to the manager and returns a dictionary of the newly created template_id : template_name
# NOTE: when a new template is made, it has no trainings associated with it and no Trainings field
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
    description = req.get('description')

    if not manager_uuid:
        return jsonify({'headers': header, 'msg': 'Missing manager uuid'}), 400
    if not template_name:
        return jsonify({'headers': header, 'msg': 'Missing template name'}), 400
    if not description:
        return jsonify({'headers': header, 'msg': 'Missing description'}), 400

    template_id = db.generate_key()

    data = {
        "manager" : manager_uuid,
        "template_name" : template_name,
        'description' : description
    }

    # make new empty template in Templates database
    db.child('Templates').child(template_id).set(data)

    # add template reference to manager
    # since we can't append to database, get the template info from the manager (will be a dict of template_id : template_name)
    try:
        templates = db.child('Managers').order_by_key().equal_to(manager_uuid).get().val()['Templates']
    except:
        templates = {}

    templates.update({template_id : template_name})

    # set plan's template data by combining the templates dict with a dict of the new template_id : template_name to be added
    try:
        db.child('Managers').child(manager_uuid).child('Templates').update(templates)
    except: # the Manager doesn't currently have any templates so it needs to bet set for the first time
        db.child('Managers').child(manager_uuid).child('Templates').set(templates)

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
# this method makes a new training and adds that training to the given template. It returns a dictionary of the newly created training_id : training_name
# or it returns a dictionary of {"failure" : "failure"}
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
    if not note:
        return jsonify({'headers': header, 'msg': 'Missing note'}), 400
    if not due_date:
        return jsonify({'headers': header, 'msg': 'Missing due date'}), 400
    if not duration:
        return jsonify({'headers': header, 'msg': 'Missing duration'}), 400

    # make a new training
    try:
        training_key = db.generate_key()
        data = {
            'name' : training_name,
            'note' : note,
            'due_date' : due_date,
            'duration' : duration,
            'complete' : 'false'
        }
        db.child('Trainings').child(training_key).set(data)
        if documentation_links:
            db.child('Trainings').child(training_key).child('Documentation_Links').set(documentation_links)
        if other_links:
            db.child('Trainings').child(training_key).child('Other_Links').set(other_links)

        # since we can't append to database, get the trainings currently in the template (will be a dict of training_id : training_name)
        # try except to handle case where template has no trainings in it to start
        try:
            trainings = db.child('Templates').order_by_key().equal_to(template_id).get().val()[template_id]["Trainings"]
        except:
            trainings = {}

        # set template data by combining the templates dict with a dict of the new training_id : training name to be added
        trainings.update({training_key : training_name})

        try:
            db.child('Templates').child(template_id).child("Trainings").update(trainings)
        except:
            db.child('Templates').child(template_id).child("Trainings").set(trainings)

        training = {training_key : training_name}
    except:
        training = {"failure" : "failure"}

    payload = {
        'headers' : header,
        'training' : training
    }

    return jsonify(payload)

# expect the request to have the following fields: manager_uuid, template_id, template_name, plan_id
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the template_id can be gotten from the endpoint /manager/new_empty_template or /manager/get_training_templates
# the template name is a string supplied by the user
# the plan id can be gotten from the endpoint /manager/get_trainee_training_plan_id
# this method adds the template_id to the templates field of the given plan and returns "success" or "failure"
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

    try:
        # since we can't append to database, get the template info currently in the plan (will be a dict of template_id : template_name)
        # try except to handle the case where the plan doesn't have any Templates field yet
        try:
            templates = db.child('Plans').order_by_key().equal_to(plan_id).get().val()['Templates']
        except:
            templates = {}

        # set plan's template data by combining the templates dict with a dict of the new template_id : template_name to be added
        templates.update({template_id : template_name})

        try:
            db.child('Plans').child(plan_id).child('Templates').update(templates)
        except:
            db.child('Plans').child(plan_id).child('Templates').set(templates)

        response = "success"
    except:
        response = "failure"

    payload = {
        'headers' : header,
        'response' : response
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
# this method makes a new training and adds that training to the given plan. It returns a dictionary of the {training_id : training_name}
# or it returns a dictionary of {"failure" : "failure"}
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
    if not note:
        return jsonify({'headers': header, 'msg': 'Missing note'}), 400
    if not due_date:
        return jsonify({'headers': header, 'msg': 'Missing due date'}), 400
    if not duration:
        return jsonify({'headers': header, 'msg': 'Missing duration'}), 400

    # make a new training
    try:
        training_key = db.generate_key()
        data = {
            'name' : training_name,
            'note' : note,
            'due_date' : due_date,
            'duration' : duration,
            'complete' : 'false'
        }
        db.child('Trainings').child(training_key).set(data)
        if documentation_links:
            db.child('Trainings').child(training_key).child('Documentation_Links').set(documentation_links)
        if other_links:
            db.child('Trainings').child(training_key).child('Other_Links').set(other_links)

        # since we can't append to database, get the trainings currently in the plan (will be a dict of training_id : training_name)
        # try except in case plan has no trainings in it yet
        try:
            trainings = db.child('Plans').order_by_key().equal_to(plan_id).get().val()[plan_id]['Trainings']
        except:
            trainings = {}

        # set plan's training data by combining the trainings dict with a dict of the new training_id : training_name to be added
        trainings.update({training_key : training_name})

        try:
            db.child('Plans').child(plan_id).child('Trainings').update(trainings)
        except:
            db.child('Plans').child(plan_id).child('Trainings').set(trainings)

        training = {training_key : training_name}
    except:
        training = {"failure" : "failure"}

    payload = {
        'headers' : header,
        'training' : training
    }

    return jsonify(payload)

# expect the request to have the following fields: manager_uuid, training_id, documentation_links, other_links
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the training_id can be gotten from the endpoint /manager/add_training_to_training_plan, /manager/add_training_to_training_template, or /manager/get_trainee_training_plan_contents
# the documentation links are a dictionary of link : name supplied by the user
# the other links are a dictionary of link : name supplied by the user
# manager_uuid and training_id are required. For the other fields, if there is nothing to be added, do not include them in the request.
# NOTE: this method APPENDS info to the relevant fields and returns either "success" or "failure"
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

    try:
    # since we can't append to database, need to get current list of things, then add to it
        training = db.child('Trainings').order_by_key().equal_to(training_id).get().val()[training_id]

        if documentation_links:
            try:
                original_documentation_links = training['Documentation_Links'] # will be a dict of {link : name}
            except:
                original_documentation_links = {}
            original_documentation_links.update(documentation_links) # combine the original dict with the new dict
            db.child('Trainings').child(training_id).child('Documentation_Links').update(original_documentation_links)

        if other_links:
            try:
                original_other_links = training['Other_Links'] # will be a dict of {link : name}
            except:
                original_other_links = {}
            original_other_links.update(other_links) # combine the original dict with the new dict
            db.child('Trainings').child(training_id).child('Other_Links').update(original_other_links)

        response = "success"
    except:
        response = "failure"

    payload = {
        'headers' : header,
        'response' : response
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
# NOTE: this method OVERWRITES info in the relevant fields and returns "success" or "failure"
# TODO: existing bug - if you change the training name, it'll be changed in the Trainings table but not the Plans table. Would require plan_id to also train in Plans table.
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

    try:
        if training_name:
            db.child('Trainings').child(training_id).update({'name' : training_name})
        
        if note:
            db.child('Trainings').child(training_id).update({'note' : note})

        if due_date:
            db.child('Trainings').child(training_id).update({'due_date' : due_date})

        if duration:
            db.child('Trainings').child(training_id).update({'duration' : duration})

        response = "success"
    except:
        response = "failure"

    payload = {
        'headers' : header,
        'response' : response
    }

    return jsonify(payload)

# expect the request to have the following fields: manager_uuid, template_id, training_id
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the template_id can be gotten from the endpoint /manager/new_empty_template or /manager/get_training_templates
# the training_id can be gotten from the endpoint /manager/add_training_to_training_plan, /manager/add_training_to_training_template, or /manager/get_trainee_training_plan_contents
# this method uses the template_id and training_id to remove the training
# from the template and delete it from the database (safe, since it can only be pointed to from the template)
# Returns "success" or "failure"
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

    try:
        # remove the training entry from the Templates table
        db.child('Templates').child(template_id).child('Trainings').child(training_id).remove()

        # remove the training entry in the Trainings table that corresponds to the training_id
        db.child('Trainings').child(training_id).remove()

        response = "success"
    except:
        response = "failure"

    payload = {
        'headers' : header,
        'response' : response
    }

    return jsonify(payload)

# expect the request to have the following fields: manager_uuid, plan_id, training_id
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the plan id can be gotten from the endpoint /manager/get_trainee_training_plan_id
# the training_id can be gotten from the endpoint /manager/add_training_to_training_plan, /manager/add_training_to_training_template, or /manager/get_trainee_training_plan_contents
# this method uses the plan_id and training_id to remove the training
# from the plan and delete it from the database (safe, since it can only be pointed to from the plan)
# returns "success" or "failure"
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

    try:
        # remove the training entry from the Plans table
        db.child('Plans').child(plan_id).child('Trainings').child(training_id).remove()

        # remove the training entry in the Trainings table that corresponds to the training_id
        db.child('Trainings').child(training_id).remove()

        response = "success"
    except:
        response = "failure"

    payload = {
        'headers' : header,
        'response' : response
    }

    return jsonify(payload)

# expect the request to have the following fields: manager_uuid
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# this method uses manager uuid to query the managers database to get the list of events then returns the list of events
@app.route('/manager/get_manager_events', methods=['GET'])
def get_manager_events():
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
        events = db.child('Managers').order_by_key().equal_to(manager_uuid).get().val()[manager_uuid]['Events']
    except:
        events = {}

    payload = {
        'headers' : header,
        'events' : events
    }

    return jsonify(payload)



###
"""
Trainee Methods
query methods - get plan_id (done), get task ids in plan (done), view specific task in plan or template (done), view events (done)
update methods - mark task complete (done)
"""
###

# expect request to have the following fields: trainee_uuid
# the trainee_uuid field should contain the trainee's unique id which was provided to the client upon the trainee logging in
# this method uses the trainee_uuid and queries the database to get a dictionary of trainee_name : trainee_uuid pairs of the trainee's peers
# and returns a json of the dictionary of {trainee_name : trainee_uuid} pairs
@app.route('/trainee/get_peers', methods=['GET'])
def trainee_get_trainees():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400
    
    trainee_uuid = req.get('trainee_uuid')

    if not trainee_uuid:
        return jsonify({'headers': header, 'msg': 'Missing trainee uuid'}), 400

    try:
        peers = db.child('Trainees').order_by_key().equal_to(trainee_uuid).get().val()[trainee_uuid]["Team"]
    except:
        peers = {}

    payload = {
        'headers': header,
        'peers' : peers
    }

    return jsonify(payload), 200

# expect request to have the following fields: trainee_uuid
# the trainee_uuid field should contain the trainee's unique id which was provided to the client upon the trainee logging in
# this method uses the trainee_uuid and queries the database to get a dictionary of trainee_uuid/name pairs of the trainee's trainees
# and returns a json of the dictionary of {manager_name : manager_uuid} pairs
@app.route('/trainee/get_managers', methods=['GET'])
def trainee_get_managers():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400
    
    trainee_uuid = req.get('trainee_uuid')

    if not trainee_uuid:
        return jsonify({'headers': header, 'msg': 'Missing trainee uuid'}), 400

    try:
        managers = db.child('Trainees').order_by_key().equal_to(trainee_uuid).get().val()[trainee_uuid]["Managers"]
    except:
        managers = {}

    payload = {
        'headers': header,
        'managers' : managers
    }

    return jsonify(payload), 200


# expect the request to have the following fields: trainee_uuid
# the authorization header should contain the user's verification token received from logging in
# this method uses the trainee uuid to get and return the string of the trainee's plan_id
@app.route('/trainee/get_trainee_plan_id', methods=['GET'])
def trainee_get_plan_id():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400

    trainee_uuid = req.get('trainee_uuid')

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

# expect request to have the following fields: trainee_uuid, plan_id
# the trainee_uuid field should contain the trainee's unique id which was provided to the client upon the trainee logging in
# the plan_id field should contain the plan_id of the plan which should be retrieved. This value can be gotten from the /trainee/get_trainee_training_plan_id endpoint
# this method uses the plan_id and queries the Plans database to get the dictionary of training_id : training_name from the plan (both from the templates associated with
# the plan and trainings added directly to the plan). It returns a json of the dictionary of training_id : training_name.
@app.route('/trainee/get_trainee_training_plan_contents', methods=['GET'])
def trainee_get_trainee_training_plan_contents():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400
    
    trainee_uuid = req.get('trainee_uuid')
    plan_id = req.get('plan_id')

    if not trainee_uuid:
        return jsonify({'headers': header, 'msg': 'Missing trainee uuid'}), 400
    if not plan_id:
        return jsonify({'headers': header, 'msg': 'Missing plan id'}), 400

    # get trainings added directly to the plan first (trainings will be a dict of training_id : training_name)
    try:
        trainings = db.child('Plans').order_by_key().equal_to(plan_id).get().val()[plan_id]['Trainings']
    except:
        trainings = {}

    # now get trainings from the templates (templates will be a dict of template_id : template_name)
    try:
        template_ids = db.child('Plans').order_by_key().equal_to(plan_id).get().val()[plan_id]['Templates']
        for template_id in template_ids.keys():
            # index into the templates table using the template_id and get the trainings (template_trainings will be a dict of training_id : training_name)
            template_trainings = db.child('Templates').order_by_key().equal_to(template_id).get().val()[template_id]['Trainings']
            # merge the trainings from this template into the trainings dict
            trainings.update(template_trainings)
    except:
        pass

    payload = {
        'headers' : header,
        'trainings' : trainings
    }
    
    return jsonify(payload)

# expect the request to have the following fields: trainee_uuid, training_id
# the trainee_uuid field should contain the trainee's unique id which was provided to the client upon the trainee logging in
# the training_id field should contain the training_id for which you want to get the training's contents. 
# This value can be gotten from the /trainee/get_trainee_training_plan_contents endpoint.
# this method uses the training_id to query the Trainings database to get the training contents. It returns the training
# contents as a json.
@app.route('/trainee/get_training', methods=['GET'])
def trainee_get_training():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400
    
    trainee_uuid = req.get('trainee_uuid')
    training_id = req.get('training_id')

    if not trainee_uuid:
        return jsonify({'headers': header, 'msg': 'Missing trainee uuid'}), 400
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

# expect the request to have the following fields: trainee_uuid
# the trainee_uuid field should contain the trainee's unique id which was provided to the client upon the trainee logging in
# this method uses trainee uuid to query the Trainees database to get the list of events then returns the list of events
@app.route('/trainee/get_trainee_events', methods=['GET'])
def get_trainee_events():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400

    trainee_uuid = req.get('trainee_uuid')

    if not trainee_uuid:
        return jsonify({'headers': header, 'msg': 'Missing trainee uuid'}), 400

    try:
        events = db.child('Trainees').order_by_key().equal_to(trainee_uuid).get().val()['Events']
    except:
        events = {}

    payload = {
        'headers' : header,
        'events' : events
    }

    return jsonify(payload)

# expect request to have the following header: authorization
# expect the request to have the following fields: trainee_uuid, training_id
# the trainee_uuid field should contain the trainee's unique id which was provided to the client upon the trainee logging in
# the training_id field should contain the training_id that you want to mark complete. It can be gotten from the /trainee/get_trainee_training_plan_contents endpoint
# this method uses the training_id to mark the given training as complete
# returns "success" or "failure"
@app.route('/trainee/mark_task_complete', methods=['POST'])
def mark_task_complete():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400
    
    trainee_uuid = req.get('trainee_uuid')
    training_id = req.get('training_id')

    if not trainee_uuid:
        return jsonify({'headers': header, 'msg': 'Missing trainee uuid'}), 400
    if not training_id:
        return jsonify({'headers': header, 'msg': 'Missing training id'}), 400

    try:
        db.child('Trainings').child(training_id).update({'complete' : 'true'})
        response = "success"
    except:
        response = "failure"

    payload = {
        'headers' : header,
        'response' : response
    }

    return jsonify(payload)



###
"""
Shared Methods
add methods - add new event (done)
"""
###


# expect the request to have the following fields: manager_uuid, trainee_uuid
# the manager_uuid field should contain the manager's unique id which was provided to the client upon the manager logging in
# the trainee_uuid field should contain the trainee's unique id which was provided to the client upon the trainee logging in
# the start, end, and text fields are strings provided by the user
# The manager can get their trainees' uuids and names through the endpoint /manager/get_trainees
# The trainee can get their managers' uuids and names through the endpoint /trainee/get_managers
# this method uses trainee uuid and manager uuid to add an event to both the trainee and manager's lists of events.
# It returns "success" or "failure"
@app.route('/shared/add_event_between_manager_and_trainee', methods=['POST'])
def add_event_between_manager_and_trainee():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400

    trainee_uuid = req.get('trainee_uuid')
    trainee_name = req.get('trainee_name')
    manager_uuid = req.get('manager_uuid')
    manager_name = req.get('manager_name')
    start = req.get('start')
    end = req.get('end')
    text = req.get('text')

    if not trainee_uuid:
        return jsonify({'headers': header, 'msg': 'Missing trainee uuid'}), 400
    if not trainee_name:
        return jsonify({'headers': header, 'msg': 'Missing trainee name'}), 400
    if not manager_uuid:
        return jsonify({'headers': header, 'msg': 'Missing manager uuid'}), 400
    if not manager_name:
        return jsonify({'headers': header, 'msg': 'Missing manager name'}), 400
    if not start:
        return jsonify({'headers': header, 'msg': 'Missing start timestamp'}), 400
    if not end:
        return jsonify({'headers': header, 'msg': 'Missing end timestamp'}), 400
    if not text:
        return jsonify({'headers': header, 'msg': 'Missing event text'}), 400
    
    try:
        event_key = db.generate_key()

        # make a new manager event
        manager_event_data = {
            'start' : start,
            'end' : end,
            'text' : text,
            'with' : trainee_name,
        }
        db.child('Managers').child(manager_uuid).child("Events").child(event_key).set(manager_event_data)

        # make a new trainee event
        trainee_event_data = {
            'start' : start,
            'end' : end,
            'text' : text,
            'with' : manager_name,
        }
        db.child('Trainees').child(trainee_uuid).child("Events").child(event_key).set(trainee_event_data)

        result = "success"
    except:
        result = "failure"

    payload = {
        'headers' : header,
        'result' : result
    }

    return jsonify(payload)

# expect the request to have the following fields: trainee_uuid1, trainee_uuid2
# the trainee_uuid1 field should contain the trainee's unique id which was provided to the client upon the trainee logging in
# The trainee can get their peers' uuids through the endpoint /trainee/get_team
# this method uses trainee_uuid1 and trainee_uuid2 to add an event to both the trainee and their peer's lists of events.
# It returns "success" or "failure"
@app.route('/shared/add_event_between_trainee_and_trainee', methods=['POST'])
def add_event_between_trainee_and_trainee():
    header = {'Access-Control-Allow-Origin': '*'}
    
    #receive data from front end
    try:
        req = request.get_json(force=True)
    except:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400

    trainee_uuid1 = req.get('trainee_uuid1')
    trainee_name1 = req.get('trainee_name1')
    trainee_uuid2 = req.get('trainee_uuid2')
    trainee_name2 = req.get('trainee_name2')
    start = req.get('start')
    end = req.get('end')
    text = req.get('text')

    if not trainee_uuid1:
        return jsonify({'headers': header, 'msg': 'Missing trainee uuid 1'}), 400
    if not trainee_name1:
        return jsonify({'headers': header, 'msg': 'Missing trainee name 1'}), 400
    if not trainee_uuid2:
        return jsonify({'headers': header, 'msg': 'Missing trainee uuid 2'}), 400
    if not trainee_name2:
        return jsonify({'headers': header, 'msg': 'Missing trainee name 2'}), 400
    if not start:
        return jsonify({'headers': header, 'msg': 'Missing start timestamp'}), 400
    if not end:
        return jsonify({'headers': header, 'msg': 'Missing end timestamp'}), 400
    if not text:
        return jsonify({'headers': header, 'msg': 'Missing event text'}), 400
    
    try:
        event_key = db.generate_key()

        # make a new event for trainee 1
        trainee_event_data1 = {
            'start' : start,
            'end' : end,
            'text' : text,
            'with' : trainee_name2,
        }
        db.child('Trainees').child(trainee_uuid1).child("Events").child(event_key).set(trainee_event_data1)

        # make a new event for trainee 1
        trainee_event_data2 = {
            'start' : start,
            'end' : end,
            'text' : text,
            'with' : trainee_name1,
        }
        db.child('Trainees').child(trainee_uuid2).child("Events").child(event_key).set(trainee_event_data2)

        result = "success"
    except:
        result = "failure"

    payload = {
        'headers' : header,
        'result' : result
    }

    return jsonify(payload)



if __name__ == '__main__':
    app.run(port=5000, debug=True)