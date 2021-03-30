from flask import *
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



app = Flask(__name__)


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

#using command line for functionality right now
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



#function to refresh toekn to avoid stale tokens, tokens are valid for 1 hour per firebase specification
def refreshtoken(user):
    return auth.refresh(user['refreshToken'])['idToken']



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


#TODO not going to send full user in request. Need to get user info using some other request trigger.
#retrieve account info
@app.route('/authentication/get_account_info', methods=['GET'])
def account_info():
    user = request.form["user"]
    return auth.get_account_info(user['idToken'])


###
"""
Database Methods
create methods - create new company, create new manager, create new employee
add methods - add manager to company, add employee to company, add employee to manager
query methods - view companies, view managers, view employes
removal methods
"""
###

#add new companies to the database
@app.route('/database/add_new_company', methods=['POST'])
def create_new_company():
    name = request.form["name"]
    num_employees = request.form["num_employees"]

    try:
        managers = request.form["managers"]
    except:
        managers = {None : None}
    
    try:
        trainees = request.form["trainees"]
    except:
        trainees = {None : None}

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
def add_new_manager():
    name = request.form["name"]
    age = request.form["age"]
    company_name = request.form["company_name"]
    company_uuid = request.form["company_uuid"]
    
    try:
        meetings = request.form["meetings"]
    except:
        meetings = {None : None}

    try:
        trainees = request.form["trainees"]
    except:
        trainees = {None : None}

    try:
        templates = request.form["templates"]
    except:
        templates = {None : None}

    try:
        files = request.form["files"]
    except:
        files = {None : None}

    data = {
        'name': name,
        'age': age,
        'company': company_name,
        'company_uuid': company_uuid,
        'meetings': meetings, #will be a dictionary of "Meeting person name: datetime" default to none
        'templates': templates, #will be a dictionary of "template_names: template uid" default to none
        'trainees': trainees, #will be a dictionary of "trainee_name: trainee_uuid" default to none
        'files': files #will be a list containing links to the firebase storage 
    }

    path = 'Managers'

    db.child(path).push(data)

    return redirect('/')

#add new trainees to the database
@app.route('/database/add_new_trainee', methods=['POST'])
def add_new_trainee():
    name = request.form["name"]
    age = request.form["age"]
    company_name = request.form["company_name"]
    company_uuid = request.form["company_uuid"]
    
    try:
        meetings = request.form["meetings"]
    except:
        meetings = {None : None}

    try:
        managers = request.form["trainees"]
    except:
        managers = {None : None}

    try:
        templates = request.form["templates"]
    except:
        templates = {None : None}

    try:
        training_plans = request.form["files"]
    except:
        training_plans = {None : None}

    data = {
        'name': name,
        'age': age,
        'company': company_name,
        'company_uuid': company_uuid,
        'meetings': meetings, #will be a dictionary of "Meeting person name: datetime" default to none
        'managers': managers, #will be a dictionary of "manager_name: manager_uuid" default to none
        'templates': templates, #will be a dictionary of "template_names: template uid" default to none
        'training_plans': training_plans #will be a dictionary of "training plan name: training plan uid"
    }

    path = 'Trainees'

    db.child(path).push(data)

    return redirect('/')

#create new training template
# not sure that you need trainee_uuid here - you're just creating a new template, not tying it to an employee
@app.route('/database/create_new_template', methods=["POST"])
def create_new_template():
    template_name = request.form["template_name"]
    trainee_uuid = request.form["trainee_uuid"]
    manager_uuid = request.form["manager_uuid"]
    company_uuid = request.form["company_uuid"]

    try:
        data = request.form["data"]
    except:
        data = [None]

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
@app.route('/database/create_new_training_plan', methods=["POST"])
def create_new_training_plan():
    manager_uuid = request.form["manager_uuid"]
    trainee_uuid = request.form["trainee_uuid"]
    
    try:
        templates = request.form["templates"]
    except:
        templates = [None]

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
query methods - view manager's employees, view specific employee plan, view templates available, view specific template, view specific task in plan or template, 
add methods - add task to specific employee plan or specific template, add documentation/link/notes/due date to specific task
remove methods - remove task from specific employee plan or specific template, remove documentation/link/notes/due date from specific task
"""
###

# expect to get verification token, manager uuid, will query database to get the name/ID pairs of the manager's employees
# and return a json of the list of name/ID pairs
@app.route('/manager/get_trainee_names', methods=['GET'])
def get_trainee_names():
    # use manager uuid and token to get employee name/uuid pairs and return them

    manager_uuid = request.form["manager_uuid"]

    path = 'Trainees'
    trainees = db.child(path).order_by_child('manager').equal_to(manager_uuid).get()

    trainee_names = {}
    for trainee in trainees:
        name = trainee.val()['name']
        trainee_uuid = trainee.key()
        trainee_names[name] = trainee_uuid

    return trainee_names

# expect to get verification token, manager uuid, employee uuid, will query database to get 
@app.route('/manager/get_trainee_training_plan', methods=['GET'])
def manager_get_trainee_training_plan():
    manager_uuid = request.form["manager_uuid"]
    trainee_name = request.form["trainee_name"]

    path = "Training Plan"
    training_plans = db.child(path).order_by_child("manager").equal_to(manager_uuid).get()

    trainee_plans = {}
    for plan in training_plans:
        if plan.val()['name'] == trainee_name:
            trainee_plans[plan.key()] = plan.val()

    return trainee_plans


# expect to get verification token, will query database to get the name/ID pairs of the training templates associated with that manager
# will return a json of the list of name/ID pairs of the various training templates
@app.route('/manager/get_training_template_names', methods=['GET'])
def get_training_templates_names():
    # use manager uuid and token to get templates name/ID pairs and return them

    manager_uuid = request.form["manager_uuid"]
    return db.child("Templates").order_by_child("manager").equal_to(manager_uuid).get()



# expect to get uuid. Also expect to get template name as url argument. Will query the database with these things to get
# the relevant training template. Will return it as a json dict of a list of dicts of trainings
@app.route('/manager/get_training_template', methods=['GET'])
def get_training_template():
    template_uuid = request.form["template_uuid"]
    template = db.child("Templates").child(template_uuid).get().val()
    trainings = template['data']

    return trainings



# expect to get uuid, json of the training as a string to be added. Also expect to get template name as url argument. Will add to database.
@app.route('/manager/add_training_to_training_template', methods=['POST'])
def add_training_to_training_template():
    template_uuid = request.form["template_uuid"]

    try:
        data = request.form["data"]
    except:
        data = {None : None}

    #find template
    path = "Templates"
    template = db.child(path).child(template_uuid).get().val()

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
        cloud_filename = cloud_filename + str(key) + '/' + filename
        storage.child(cloud_filename).put(filename) #add the file to the correct directory in Firebase storage

        #fetch Firebase storage url
        url = storage.child(cloud_filename).get_url(None)

        #add url to template data
        data.append(url)

    #finally, update the training template in the database
    db.child(path).child(template_uuid).update({'data': data})

    return redirect('/')




"""
As written, don't use manager_uuid or trainee_uuid - just checking: is that correct?
Also, should this be both GET and POST?
"""
# expect to get manager uuid, trainee name. Also expect to get template name as url argument. Will add relevant trainings
# to employee plan.
@app.route('/manager/add_template_to_training_plan', methods=['GET', 'POST'])
def add_template_to_training_plan():
    manager_uuid = request.form["manager_uuid"]
    trainee_uuid = request.form["trainee_uuid"]
    template_uuid = request.form["template_uuid"]
    training_plan_uuid = request.form["training_plan_uuid"]
    
    #find training plan
    path_training = "Training Plan"
    training_plan = db.child(path_training).child(training_plan_uuid).get().val()
    training_templates = training_plan['templates']

    #find template
    path_template = "Templates"
    template = db.child(path_template).child(template_uuid).get().val()
    template_name = template['template_name']

    #add template to current training plan
    training_templates[template_name] = template_uuid

    #update training plan in data base
    db.child(path_training).child(training_plan_uuid).update({'templates': training_templates})

    return redirect('/')


    



###
"""
Trainee Methods
query methods - view plan, view specific task in plan, view calendar
update methods - mark task complete
"""
###

# expect to get trainee uuid, return json of list of trainings
@app.route('/trainee/get_trainee_training_plan', methods=['GET'])
def trainee_get_trainee_training_plan():
    trainee_uuid = request.form["trainee_uuid"]

    path = "Training Plans"
    training_plans = db.child(path).order_by_child('trainee').equal_to(trainee_uuid).get()

    return training_plans.val()



# expect to get trainee uuid, return json of list of meetings
@app.route('/trainee/get_trainee_meetings', methods=['GET'])
def get_trainee_meetings():
    trainee_uuid = request.form["trainee_uuid"]

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
    app.run(host='0.0.0.0', port=8080, debug=True)