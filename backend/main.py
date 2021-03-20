from flask import Flask, request

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
Manager Methods
"""
###

# expect to get uuid, will query database with it to get the names of the training templates associated with that manager
# will return a json of the list of names of the various training templates
@app.route('/manager/get_training_template_names', methods=['GET'])
def get_training_templates_names():
    pass



# expect to get uuid. Also expect to get template name as url argument. Will query the database with these things to get
# the relevant training template. Will return it as a json dict of a list of dicts of trainings
@app.route('/manager/get_training_template/<string:template_name>', methods=['GET'])
def get_training_template(template_name):
    pass



# expect to get uuid, json of the training to be added. Also expect to get template name as url argument. Will add to database.
@app.route('/manager/add_training_to_training_template/<string:template_name>', methods=['POST'])
def add_training_to_training_template(template_name):
    pass



# expect to get manager uuid, trainee name. Also expect to get template name as url argument. Will add relevant trainings
# to employee plan.
@app.route('/manager/add_template_to_training_plan/<string:template_name>', methods=['POST'])
def add_template_to_training_plan(template_name):
    pass



# expect to get manager uuid. Returns json list of trainee names
@app.route('/manager/get_trainee_names', methods=['GET'])
def get_trainee_names():
    pass



# expect to get manager uuid, trainee name.
@app.route('/manager/get_trainee_training_plan', methods=['GET'])
def manager_get_trainee_training_plan():
    pass



# expect to get manager uuid, trainee name, json of the training to be added.
@app.route('/manager/add_training_to_training_plan', methods=['POST'])
def add_training_to_training_plan():
    pass



###
"""
Trainee Methods
"""
###

# expect to get trainee uuid, return json of list of trainings
@app.route('/trainee/get_trainee_training_plan', methods=['GET'])
def trainee_get_trainee_training_plan():
    pass



# expect to get trainee uuid, return json of list of meetings
@app.route('/trainee/get_trainee_meetings', methods=['GET'])
def get_trainee_meetings():
    pass



# it seems to me most of the employee functionality could be done in the front end. Else, have some sort of partitioning of trainings and meetings
# when returned by the server (ie. far out, upcoming, overdue). Don't need many(any?) more trainee endpoints on the backend server.



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)