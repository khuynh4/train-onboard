import logging
import os

from flask import Flask, jsonify, request
import flask_cors
import google.auth.transport.requests
import google.oauth2.id_token
import requests_toolbelt.adapters.appengine

from __init__ import auth, db, storage

"""
Admin Methods - not in our product backlog; propose we just set these things up manually and make accounts for Josh/Scott/George to do their testing - call it "doing things that don't scale"
create methods - create new company, create new manager, create new employee
add methods - add manager to company, add employee to company, add employee to manager
query methods - view companies, view managers, view employes
removal methods

Authentication
signup - I propose that we get rid of signup and say that we manually make accounts for now
log in

Manager Methods
query methods - view manager's employees, view specific employee plan, view templates available, view specific template, view specific task in plan or template, 
add methods - add task to specific employee plan or specific template, add documentation/link/notes/due date to specific task
remove methods - remove task from specific employee plan or specific template, remove documentation/link/notes/due date from specific task

Employee Methods
query methods - view plan, view specific task in plan, view calendar
update methods - mark task complete
I propose that the google calendar integration be done in the front end

I feel like the databases should not point bidirectionally for this project. For simplicity's sake, it's easier if they go one way.
Ie. company -> managers and employees
manager -> employees and templates
employee -> plan
template -> trainings
plan -> templates, trainings
training -> training things like name, documentation links, other links, notes, due date
no user db. No signup. We make their account as either a manager or a employee and give them the credentials to log in.
"""


# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
#requests_toolbelt.adapters.appengine.monkeypatch()
HTTP_REQUEST = google.auth.transport.requests.Request()

app = Flask(__name__)
flask_cors.CORS(app)


@app.route('/')
def home():
    # For now, just return json result to indicate liveness
    return {"data": "alive"}



###
"""
Authentication Methods
log in
sign up
"""
###

# for server testing purposes. typically, login will be handled on the client.
@app.route('/authentication/login', methods=['POST'])
def login():
    email = request.form["email"]
    password = request.form["password"]

    try:
        user = auth.sign_in_with_email_and_password(email, password)
    except:
        print("Invalid UserID or Password. Try again or sign up.")
        return 0

    #returns the users verification token
    return user['idToken']

# for server testing purposes to verify that the token verification functions are working
@app.route('/authentication/test', methods=['POST'])
def test():
    uuid = verify(request)
    if uuid == None:
        return 'Unauthorized', 401
    else:
        return {"data" : uuid}



# for server testing purposes. Typically, token refresh will be handled on the client.
# function to refresh toekn to avoid stale tokens, tokens are valid for 1 hour per firebase specification
def refreshtoken(user):
    return auth.refresh(user['refreshToken'])['idToken']


# for server testing purposes. Typically, signup/login will be handled on the client.
@app.route('/authentication/signup', methods=['POST'])
def signup(): #default using command line until HTML forms are built
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    age = request.form["age"]
    address = request.form["address"]
    password = request.form["password"]
    confirm_password = request.form["confirm_pass"]

    
    if password == confirm_password:
        try:
            user = auth.create_user_with_email_and_password(email, password)
        except:
            print("Email already in use. Try using another one")
            return 
    else:
        print("Passwords do not match. Try again")
        return 0

    #send verification email
    auth.send_email_verification(user['idToken'])

    #load information to database default to Users node
    data = {
        'name': "{} {}".format(first_name, last_name),
        'email': email,
        'age': age,
        'address': address
    }

    db.child('Users').push(data)

    return user['idToken']



###
"""
ADMIN Methods - hidden API for use by founders to manually add new companies, managers, employees
create methods - create new company, create new manager, create new employee
add methods (not implemented) - add manager to company, add employee to company, add employee to manager
query methods (not implemented) - view companies, view managers, view employes
removal methods
"""
###

# add new companies to the database
@app.route('/database/add_new_company', methods=['POST'])
def create_new_company():
    req = request.get_json(force=True)
    identifier = req["identifier"]
    name = req["name"]
    num_employees = req["num_employees"]

    try:
        managers = req["managers"] # will be of the form: 'managers' : {"uuid 1" : "name 1", "uuid 2" : "name 2"}
    except:
        managers = {None : None}
    
    try:
        trainees = req["trainees"] # will be of the form: 'trainees' : {"uuid 1" : "name 1", "uuid 2" : "name 2"}
    except:
        trainees = {None : None}

    # set company data
    path = 'Companies'
    data = {
        'name': name,
        'num_employees': num_employees,
    }
    db.child(path).child(identifier).set(data)

    db.child(path).child(identifier).child("Managers").set(managers)
    db.child(path).child(identifier).child("Trainees").set(trainees)

    return {"response" : "success"}

# add new managers to the database
@app.route('/database/add_new_manager', methods=['POST'])
def add_new_manager():
    req = request.get_json(force=True)
    manager_uuid = req["manager_uuid"]
    name = req["name"]
    age = req["age"]

    try:
        trainees = req["trainees"] # will be of the form: 'trainees' : {"uuid 1" : "name 1", "uuid 2" : "name 2"}
    except:
        trainees = {None : None}

    try:
        templates = req["templates"] # will be of the form: 'templates' : {"template id 1" : "template name 1", "template id 2" : "template name 2"}
    except:
        templates = {None : None}

    try:
        meetings = req["meetings"] # will be of the form: 'meetings' : {"uuid 1" : "datetime 1", "uuid 2" : "datetime 2"}
    except:
        meetings = {None : None}

    # set manager data
    path = 'Managers'
    data = {
        'name': name,
        'age': age,
    }
    db.child(path).child(manager_uuid).set(data)

    db.child(path).child(manager_uuid).child("Trainees").set(trainees)
    db.child(path).child(manager_uuid).child("Templates").set(templates)
    db.child(path).child(manager_uuid).child("Meetings").set(meetings)

    return {"response" : "success"}

# add new trainees to the database
@app.route('/database/add_new_trainee', methods=['POST'])
def add_new_trainee():
    req = request.get_json(force=True)
    trainee_uuid = req["trainee_uuid"]
    name = req["name"]
    age = req["age"]
    
    try:
        meetings = req["meetings"] # will be of the form: 'meetings' : {"uuid 1" : "datetime 1", "uuid 2" : "datetime 2"}
    except:
        meetings = {None : None}

    # make a new plan for the trainee
    plan_key = db.generate_key()
    data = {
        'templates' : 'none',
        'trainings' : 'none'
    }
    db.child('Plans').child(plan_key).set(data)

    # set trainee data
    path = 'Trainees'
    data = {
        'name': name,
        'age': age,
        'plan': plan_key
    }
    db.child('Trainees').child(trainee_uuid).set(data)

    db.child(path).child(trainee_uuid).child("Meetings").set(meetings)

    return {"response" : "success"}


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

# https://cloud.google.com/appengine/docs/standard/python/authenticating-users-firebase-appengine
# takes a request, extracts the verification token, checks if it's valid, and returns None if invalid or the uuid if valid.
def verify(request):
    id_token = request.headers['authorization']
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, HTTP_REQUEST, audience=os.environ.get('GOOGLE_CLOUD_PROJECT'))
    if not claims:
        return None

    # Each identity provider sends a different set of claims, but each has at least a sub claim with a unique user ID and a claim that 
    # provides some profile information, such as name or email, that you can use to personalize the user experience on your app.
    return claims['sub']

# expect request to have the following headers: authorization
# expect request to have the following fields: none
# the authorization header should contain the user's verification token received from logging in
# this method verifies the verification token to get the manager uuid and queries the database to get uuid/name pairs of the manager's employees
# and returns a json of the list of uuid/name pairs
@app.route('/manager/get_trainees', methods=['GET'])
def get_trainees():
    manager_uuid = verify(request)
    if manager_uuid == None:
        return 'Unauthorized', 401

    trainees = db.child('Managers').order_by_key().equal_to(manager_uuid).get().val()[manager_uuid]["Trainees"]

    return trainees

# expect request to have the following header: authorization
# expect request to have the following fields: trainee_uuid
# the authorization header should contain the user's verification token received from logging in
# this method verifies the verification token to get the manager uuid and queries the database to get
# the trainee's plan_id.
@app.route('/manager/get_trainee_training_plan_id', methods=['GET'])
def manager_get_trainee_training_plan_id():
    manager_uuid = verify(request)
    if manager_uuid == None:
        return 'Unauthorized', 401

    req = request.get_json(force=True)

    trainee_uuid = req['trainee_uuid']

    plan_id = db.child('Trainees').order_by_key().equal_to(trainee_uuid).get().val()[trainee_uuid]['plan']

    # here is where we could use the plan_id to query the plan table to get template_ids and individual trainings
    # then query the templates table with the template_ids to get all trainings for this user
    # if we don't do that here, we'll need another method to do that

    return plan_id

# expect request to have the following header: authorization
# expect request to have the following fields: plan_id
# the authorization header should contain the user's verification token received from logging in
# this method verifies the verification token and queries the database to get
# the list of training_ids from the plan (both from templates associated with the plan and trainings added directly to the plan).
@app.route('/manager/get_trainee_training_plan_contents', methods=['GET'])
def manager_get_trainee_training_plan_contents():
    manager_uuid = verify(request)
    if manager_uuid == None:
        return 'Unauthorized', 401

    req = request.get_json(force=True)

    plan_id = req['plan_id']

    # get trainings added directly to the plan first
    trainings = db.child('Plans').order_by_key().equal_to(plan_id).get().val()[plan_id]['trainings']

    # now get trainings from the templates
    template_ids = db.child('Plans').order_by_key().equal_to(plan_id).get().val()[plan_id]['templates']
    for template_id in template_ids:
        trainings.append(db.child('Templates').order_by_key().equal_to(template_id).get().val()[template_id]['trainings'])
    
    return trainings

# expect request to have the following header: authorization
# the authorization header should contain the user's verification token received from logging in
# this method verifies the verification token to get the manager uuid and queries the database to get
# the manager's training template_id/template_name pairs.
@app.route('/manager/get_training_templates', methods=['GET'])
def get_training_templates():
    manager_uuid = verify(request)
    if manager_uuid == None:
        return 'Unauthorized', 401

    return db.child('Managers').order_by_key().equal_to(manager_uuid).get().val()[manager_uuid]['templates']

# expect request to have the following header: authorization
# expect the request to have the following fields: template_id
# the authorization header should contain the user's verification token received from logging in
# this method verifies the verification token to get the manager uuid and queries the database to get
# the training template's contents (training_id/training_name pairs)
@app.route('/manager/get_training_template', methods=['GET'])
def get_training_template():
    manager_uuid = verify(request)
    if manager_uuid == None:
        return 'Unauthorized', 401

    req = request.get_json(force=True)

    template_id = req['template_id']

    return db.child('Templates').order_by_key().equal_to(template_id).get().val()[template_id]

# expect request to have the following header: authorization
# expect the request to have the following fields: training_id
# the authorization header should contain the user's verification token received from logging in
# this method verifies the verification token to get the manager uuid and queries the database to get
# the training's contents
@app.route('/manager/get_training', methods=['GET'])
def get_training():
    manager_uuid = verify(request)
    if manager_uuid == None:
        return 'Unauthorized', 401

    req = request.get_json(force=True)

    training_id = req['training_id']

    return db.child('Trainings').order_by_key().equal_to(training_id).get().val()[training_id]

# expect request to have the following header: authorization
# expect the request to have the following fields: template_id, training_name, documentation_links, other_links, note, due_date, duration
# the authorization header should contain the user's verification token received from logging in
# this method verifies the verification token to get the manager uuid, makes a new training, and adds that training to the given template
@app.route('/manager/add_training_to_training_template', methods=['POST'])
def add_training_to_training_template():
    manager_uuid = verify(request)
    if manager_uuid == None:
        return 'Unauthorized', 401

    req = request.get_json(force=True)

    template_id = req['template_id']
    training_name = req['training_name']
    documentation_links = req['documentation_links']
    other_links = req['other_links']
    note = req['note']
    due_date = req['due_date']
    duration = req['duration']

    # make a new training
    training_key = db.generate_key()
    data = {
        'name' : training_name,
        'documentation_links' : documentation_links,
        'other_links' : other_links,
        'note' : note,
        'due_date' : due_date,
        'duration' : duration
    }
    db.child('Trainings').child(training_key).set(data)

    # since we can't append to database, get the trainings currently in the template
    trainings = db.child('Templates').order_by_key().equal_to(template_id).get().val()[template_id]

    # set template data - note that this might not be right depending on how trainings are listed in there
    trainings.append({training_key : training_name})
    db.child('Templates').child(template_id).update(trainings)

    return {"response" : "success"}

# expect request to have the following header: authorization
# expect the request to have the following fields: template_id, plan_id
# the authorization header should contain the user's verification token received from logging in
# this method verifies the verification token to get the manager uuid, then adds the template_id to the
# templates field of the given plan
@app.route('/manager/add_template_to_training_plan', methods=['POST'])
def add_template_to_training_plan():
    manager_uuid = verify(request)
    if manager_uuid == None:
        return 'Unauthorized', 401

    req = request.get_json(force=True)

    template_id = req['template_id']
    plan_id = req['plan_id']

    # since we can't append to database, get the template_ids currently in the plan
    templates = db.child('Plans').order_by_key().equal_to(plan_id).get().val()['templates']

    # set template data - this may not be right. Need to nail down the schema for plans and how template_ids are stored
    templates.append(template_id)
    db.child('Plans').child(plan_id).update(templates)

    return {"response" : "success"}

# expect request to have the following header: authorization
# expect the request to have the following fields: plan_id, training_name, documentation_links, other_links, note, due_date, duration
# the authorization header should contain the user's verification token received from logging in
# this method verifies the verification token to get the manager uuid, makes a new training, and adds that training to the given plan
@app.route('/manager/add_task_to_training_plan', methods=['POST'])
def add_task_to_training_plan():
    manager_uuid = verify(request)
    if manager_uuid == None:
        return 'Unauthorized', 401

    req = request.get_json(force=True)

    plan_id = req['plan_id']
    training_name = req['training_name']
    documentation_links = req['documentation_links']
    other_links = req['other_links']
    note = req['note']
    due_date = req['due_date']
    duration = req['duration']

    # make a new training
    training_key = db.generate_key()
    data = {
        'name' : training_name,
        'documentation_links' : documentation_links,
        'other_links' : other_links,
        'note' : note,
        'due_date' : due_date,
        'duration' : duration
    }
    db.child('Trainings').child(training_key).set(data)

    # since we can't append to database, get the trainings currently in the plan
    trainings = db.child('Plans').order_by_key().equal_to(plan_id).get().val()[plan_id]['trainings']

    # set plan's training data - note that this might not be right depending on how trainings are listed in there
    trainings.append({training_key : training_name})
    db.child('Plans').child(plan_id).child('trainings').update(trainings)

    return {"response" : "success"}

# expect request to have the following header: authorization
# expect the request to have the following fields: training_id, documentation_links, other_links
# training_id is required. For the other fields, put an empty string in the fields that you don't want to add to
# the authorization header should contain the user's verification token received from logging in
# this method verifies the verification token to get the manager uuid, and APPENDS info to the relevant fields
@app.route('/manager/add_info_to_task', methods=['POST'])
def add_info_to_task():
    manager_uuid = verify(request)
    if manager_uuid == None:
        return 'Unauthorized', 401

    req = request.get_json(force=True)

    training_id = req['training_id']
    documentation_links = req['documentation_links']
    other_links = req['other_links']

    # since we can't append to database, need to get current list of things, then add to it
    training = db.child('Trainings').order_by_key().equal_to(training_id).get().val()[training_id]

    if documentation_links != "":
        original_documentation_links = training['documentation_links']
        new_documentation_links = original_documentation_links + documentation_links
        db.child('Trainings').child(training_id).child('documentation_links').update(new_documentation_links)

    if other_links != "":
        original_other_links = training['other_links']
        new_other_links = original_other_links + other_links
        db.child('Trainings').child(training_id).child('other_links').update(new_other_links)

    
# expect request to have the following header: authorization
# expect the request to have the following fields: training_id, training_name, note, due_date, duration
# training_id is required. For the other fields, put an empty string in the fields that you don't want to overwrite
# the authorization header should contain the user's verification token received from logging in
# this method verifies the verification token to get the manager uuid, and OVERWRITES info in the relevant fields
@app.route('/manager/update_task_info', methods=['POST'])
def update_task_info():
    manager_uuid = verify(request)
    if manager_uuid == None:
        return 'Unauthorized', 401

    req = request.get_json(force=True)

    training_id = req['training_id']
    training_name = req['training_name']
    note = req['note']
    due_date = req['due_date']
    duration = req['duration']

    if training_name != "":
        db.child('Trainings').child(training_id).child('name').update(training_name)
    
    if note != "":
        db.child('Trainings').child(training_id).child('note').update(note)

    if due_date != "":
        db.child('Trainings').child(training_id).child('due_date').update(due_date)

    if duration != "":
        db.child('Trainings').child(training_id).child('duration').update(duration)

# expect request to have the following header: authorization
# expect the request to have the following fields: template_id, training_id
# the authorization header should contain the user's verification token received from logging in
# this method verifies the verification token and uses the template_id and training_id to remove the training
# from the template and delete it from the database (safe, since it can only be pointed to from the template)
@app.route('/manager/remove_task_from_template', methods=['POST'])
def remove_task_from_template():
    manager_uuid = verify(request)
    if manager_uuid == None:
        return 'Unauthorized', 401

    req = request.get_json(force=True)

    template_id = req['template_id']
    training_id = req['training_id']

    # possibly not correct yet - depends on schema - this code gives a hint of how the schema should look to make it easy to manage
    db.child('Templates').child(template_id).child(training_id).remove()
    db.child('Trainings').child(training_id).remove()

# expect request to have the following header: authorization
# expect the request to have the following fields: plan_id, training_id
# the authorization header should contain the user's verification token received from logging in
# this method verifies the verification token and uses the plan_id and training_id to remove the training
# from the plan and delete it from the database (safe, since it can only be pointed to from the plan)
@app.route('/manager/remove_task_from_plan', methods=['POST'])
def remove_task_from_plan():
    manager_uuid = verify(request)
    if manager_uuid == None:
        return 'Unauthorized', 401

    req = request.get_json(force=True)

    plan_id = req['plan_id']
    training_id = req['training_id']

    # possibly not correct yet - depends on schema - this code gives a hint of how the schema should look to make it easy to manage
    db.child('Plans').child(plan_id).child('trainings').child(training_id).remove()
    db.child('Trainings').child(training_id).remove()


###
"""
Trainee Methods
query methods - view plan (partially done), view specific task in plan, view calendar, view meetings (done)
update methods - mark task complete
"""
###

# expect request to have the following header: authorization
# expect the request to have the following fields: None
# the authorization header should contain the user's verification token received from logging in
# this method verifies the verification token to get the trainee uuid, then returns the plan_id
# it could be extended to return the ids of the trainings in the plan
@app.route('/trainee/get_trainee_training_plan', methods=['GET'])
def trainee_get_trainee_training_plan():
    trainee_uuid = verify(request)
    if trainee_uuid == None:
        return 'Unauthorized', 401

    plan_id = db.child('Plans').order_by_key().equal_to(trainee_uuid).get().val()['plan']

    return plan_id



# expect request to have the following header: authorization
# expect the request to have the following fields: None
# the authorization header should contain the user's verification token received from logging in
# this method verifies the verification token to get the trainee uuid, then returns the list of meetings
@app.route('/trainee/get_trainee_meetings', methods=['GET'])
def get_trainee_meetings():
    trainee_uuid = verify(request)
    if trainee_uuid == None:
        return 'Unauthorized', 401

    meetings = db.child('Trainees').order_by_key().equal_to(trainee_uuid).get().val()['meetings']

    return meetings



@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='0.0.0.0', port=8080, debug=False)