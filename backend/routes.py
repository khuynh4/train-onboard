from flask import *
from __init__ import auth, db, storage
from database_client import Database_Client

"""
This is the script for the server(s). The server should be stateless. If we use Firebase for authentication,
then any request coming from the front end should include the logged in user's unique user ID (uuid) as a string. That uuid
can be used to identify the user in the database and all of the data associated with them. For instance, a trainee
would have a uuid and in the database their training plan would be mapped to their uuid. Any request sent to the
database from the server should include the uuid so that a lookup can be performed to retrieve the relevant info. The 
server should handle the case where no data is returned, meaning that a faulty uuid was given.

https://firebase.google.com/docs/auth/web/start
https://firebase.google.com/docs/reference/js/firebase.User#uid

I would expect the database schema for a training template to have a couple tables. Maybe something like this.
"manager uuid", "template name"
"template name", "training name"
"training name", all the training columns

I would expect the database schema for a training plan to also have a couple tables. One for relating manager to employee,
one for relating employee to training plan. Maybe something like this.
"manager uuid", "employee uuid"
"trainee uuid", "training name"
then, we can leverage the table that relates "training name", all the training columns

Expect a database mapping trainee to meetings
"trainee uuid", all the meeting columns

Also mapping of uuids to names
"manager uuid", "manager name"
"trainee uuid", "trainee name"

The front end will hit the various server endpoints to get data from the databse or update database state.
To make things easier for the demo, it might make sense to have fewer endpoints and just return everything in one shot.
Ie. a manager who wants to get their templates just calls a single endpoint and all templates with all data are returned
in a single json. Same for getting employee plans. Then you control what's displayed using js dropdowns in the front end.
I've put in a bunch of endpoints for now, but it might be better to only have a couple.
"""



app = Flask(__name__)

# communication with the database will be done through the Database_Client
# depending on how we do this, might use a static IP, which would need to be passed to the constructor
db_client = Database_Client("1.1.1.1")


@app.route('/')
def home():
    # For now, just return json result to indicate liveness
    return {"data": "alive"}

###
"""
Authentication Methods
"""
###
#using command line for functionality right now
@app.route('/authentication/login', methods=['POST'])
def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
    except:
        print("Invalid UserID or Password. Try again or sign up.")
        response = input("Would you like to signup? (y/n)")
        if response = 'y':
            return redirect("/authentication/signup") #default redirect to signup route for now
        else:
            return redirect('authentication/login') #redirect to same login route

    #returns the users verification token
    return user['idtoken'], redirect("/") #redirect to home until we have interfaces set up for employees

#function to refresh toekn to avoid stale toekns, tokens are valid for 1 hour per firebase specification
def refreshtoken(user):
    return auth.refresh(user['refreshToken'])['idToken']

@app.route('/authentication/signup', methods=['POST'])
def signup(first_name, last_name, email, age, address, password, confrim_pass): #default using command line until HTML forms are built

    '''
    first_name = input("Enter your first name: \n")
    last_name = input("Enter your last name: \n")
    email = input("Enter your email address: \n")
    address = input("Enter your address: \n")
    age = input("Enter your age: \n")
    password = input("Enter your password: \n")
    confirm_pass = input("Confirm your passowrd: \n")'''

    
    if password == confirm_pass:
        try:
           user = auth.create_username_with_email_and_password(email, password)
        except:
            print("Email already in use. Try using another one")
            return redirect('authentication/signup')
    else:
        print("Passwords do not match. Try again")
        return redirect('/authentication/signup')

    #send verification email
    auth.send_email_verification(user['idToken'])

    #load information to database default to Users node
    data = {
        'name': first_name + last_name,
        'email': email,
        'age': age,
        'address': address
    }

    db.child('Users').push(data)

    return redirect('/') #default redirect to root path

#retrireve account info
@app.route('/authentication/get_account_info', methods=['GET'])
def account_info(user):
    return auth.get_account_info(user['idToken'])


###
"""
Database Methods
"""
###

#add new comapnies to the database
@app.route('/database/add_new_company', methods=['POST'])
def create_new_company(name, num_employees, managers={None: None}, trainee_uuids={None: None}):
    data = {
        'name': name,
        'num_employees': num_employees,
        'managers': managers, #will be a dictionary of "manager_name: manager_uuid" default to none
        'trainees': trainees #will be a dictionary of "trainee_name: trainee_uuid" default to none
    }

    path = 'Companies'

    db.child(path).push(data)

    return redirect('/') #redirect to default page 

#add new managers to the database
@app.route('/database/add_new_manager', methods=['POST'])
def add_new_manager(name, age, company_name, company_uuid, meetings={None: None}, trainees={None: None}, templates={None: None}, files=[None]):
    data = {
        'name': name,
        'age': age,
        'company': company,
        'company_uuid': company_uuid,
        'meetings': meetings, #will be a dictrionary of "Meeting person name: datetime" default to none
        'templates': templates, #will be a dictionary of "template_names: template uid" default to none
        'trainees': trainees #will be a dictrionary of "trainee_name: trainee_uuid" default to none
        'files': files #will be a list containing links to the firebase storage 
    }

    path = 'Managers'

    db.child(path).push(data)

    return redirect('/')

#add new trainees to the database
@app.route('/database/add_new_trainee', methods=['POST'])
def add_new_trainee(name, age, company, company_uuid, meetings={None: None}, managers={None: None}, templates={None: None}, training_plans={None: None})
    data = {
        'name': name,
        'age': age,
        'company': company,
        'company_uuid': company_uuid,
        'meetings': meetings, #will be a dictrionary of "Meeting person name: datetime" default to none
        'managers': managers, #will be a dictionary of "manager_name: manager_uuid" default to none
        'templates': templates, #will be a dictionary of "template_names: template uid" default to none
        'training_plans': training_plans #will be a dictionary of "training plan name: training plan uid"
    }

    path = 'Trainees'

    db.child(path).push(data)

    return redirect('/')

#create new training template
@app.route('database/create_new_template', methods=[POST])
def create_new_template(template_name, trainee_uuid, manager_uuid, company_uuid, data=[None]):
    data = {
        'template_name': template_name,
        'trainee': trainee_uuid,
        'manager': manager_uuid,
        'company': company_uuid,
        'data': data #will be data structure containing links to the firebase storage 
    }

    path = 'Templates'

    db.child(path).push(data)

    return redirect('/')

#create a new training plan
#expect go manager uuid and trainee uuid and respectve templates as a list of template uids as an argument
#will return you to main screen by default while pushing the new training template to the data ase
@app.route('/database/create_new_training_plan', methods=[POST])
def create_new_training_plan(manager_uuid, trainee_uuid, templates=[None]):
    data = {
        'manager': manager_uuid,
        'trainee': trainee_uuid,
        'templates': templates
    }

    path = 'Training Plans'

    db.child(path).push(data)

    return redirect('/')


###
"""
Manager Methods
"""
###

# expect to get uuid, will query database with it to get the names of the training templates associated with that manager
# will return a json of the list of names of the various training templates
@app.route('/manager/get_training_template_names', methods=['GET'])
def get_training_templates_names(manager_uuid):
    return db.child("Templates").order_by_child("manager").equal_to(manager_uuid).get()



# expect to get uuid. Also expect to get template name as url argument. Will query the database with these things to get
# the relevant training template. Will return it as a json dict of a list of dicts of trainings
@app.route('/manager/get_training_template/<string:template_uid>', methods=['GET'])
def get_training_template(template_uid):
    template = db.child("Templates").child(template_uuid).get().val()
    trainings = template['data']

    return data



# expect to get uuid, json of the training as a string to be added. Also expect to get template name as url argument. Will add to database.
@app.route('/manager/add_training_to_training_template/<string:uid>', methods=['POST'])
def add_training_to_training_template(template_uid, data={None: None}):
    #find template
    path = "Templates"
    template = db.child(path).child(template_uid).get().val()

    data = template['data']
    template_name = template['name']

    #find company name
    company = db.child('Companies').child(template['company']).get()
    company_name = company.val()['name']

    #find manager name
    manager = db.child('Managers').child(template['manager']).get()
    manager_name = manager.val()['name']

    #find trainee name
    trainee = db.child("Trainees").child(template['trainee']).get()
    trainee_name = trainee.val()['name']

    #create path in storage
    #data in storage will be ordered by a hierarchy from Company -> Manager -> Trainee -> Template -> training data
    cloud_filepath = '{}/{}/{}}/{}/'.format(company_name, manager_name, trainee_name, template_name)

    #post data into storage with format 'data.key()/data.value()'
    #values should be filenames or else it wont push to storage
    keys = data.keys()
    values = data.values()

    for key in keys:
        filename = values[key]
        cloud_filename = cloud_filename + string(key) + '/' + filename
        storage.child(cloud_filename).put(filename) #add the file to the correct directory in Firebase storage

        #fetch Firebase storage url
        url = storage.child(cloud_filename).get_url(None)

        #add url to template data
        data.append(url)

    #finally, update the training template in the database
    db.child(path).child(template_uid).update({'data': data})

    return redirect('/')





# expect to get manager uuid, trainee name. Also expect to get template name as url argument. Will add relevant trainings
# to employee plan.
@app.route('/manager/add_template_to_training_plan/<string:template_uid>', methods=['GET', 'POST'])
def add_template_to_training_plan(manager_uid, trainee_uid, template_uid, training_plan_uid):
    #find training plan
    path_training = "Training Plan"
    training_plan = db.child(path_training).child(training_plan_uid).get().val()
    training_templates = training_plan['templates']

    #find template
    path_template = "Templates"
    template = db.child(path_template).child(template_uid).get().val()
    template_name = template['template_name']

    #add template to current training plan
    training_templates[template_name] = template_uid

    #update training plan in data base
    db.child(path_training).child(training_plan_uid).update({'templates': training_templates})

    return redirect('/')


    





# expect to get manager uuid. Returns json list of trainee names
@app.route('/manager/get_trainee_names', methods=['GET'])
def get_trainee_names(manager_uuid):
    path = 'Trainees'
    trainees = db.child(path).order_by_child('manager').get()

    trainee_names = {}
    for trainee in trainees:
        name = trainee.val()['name']
        trainee_uuid = trainee.key()
        trainee_names[name] = trainee_uuid

    return trainee_names




# expect to get manager uuid, trainee name.
@app.route('/manager/get_trainee_training_plan', methods=['GET'])
def manager_get_trainee_training_plan(manager_uuid, trainee_name):
    path = "Traingin Plan"
    training_plans = db.child(path).order_by_child("manager").equal_to(manager_uuid).get()

    trainee_plans = {}
    for plan in training_plans:
        if plan.val()['name'] == trainee_name:
            trainee_plans[plan.key()] = plan.val()

    return trainee_plans



###
"""
Trainee Methods
"""
###

# expect to get trainee uuid, return json of list of trainings
@app.route('/trainee/get_trainee_training_plan', methods=['GET'])
def trainee_get_trainee_training_plan(trainee_uuid):
    path = "Training Plans"
    training_plans = db.child(path).order_by_child('trainee').equal_to(trainee_uuid).get()

    return training_plans.val()



# expect to get trainee uuid, return json of list of meetings
@app.route('/trainee/get_trainee_meetings', methods=['GET'])
def get_trainee_meetings(trainee_uuid):
    path = "Trainees"
    trainee = db.child(path).child(trainee_uuid).get()

    meetings = trainee.val()['meetings']

    return meetings



# it seems to me most of the employee functionality could be done in the front end. Else, have some sort of partitioning of trainings and meetings
# when returned by the server (ie. far out, upcoming, overdue). Don't need many(any?) more trainee endpoints on the backend server.



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)