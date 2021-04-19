import json
import requests

# server-side signup
"""
url = 'http://localhost:8080/authentication/signup'
params = {
    'first_name' : 'Jake',
    'last_name' : 'Luoma',
    'email' : 'luoma@colorado.edu',
    'age' : '30',
    'address' : '123 ABC Street',
    'password' : 'password',
    'confirm_pass' : 'password'
}
r = requests.post(url, data=params)
r = json.loads(r.text)
print(r)
"""

# manager login and logout
"""
url = 'http://localhost:5000/api/login'
params = {
    'email' : 'luoma.jake@gmail.com',
    'password' : 'password'
}
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
url = "http://localhost:5000/index"
r = requests.get(url)
print(r.text)
url = 'http://localhost:5000/api/logout'
r = requests.get(url)
print(r.text)
url = "http://localhost:5000/index"
r = requests.get(url)
print(r.text)
"""

# trainee login and logout
"""
url = 'http://localhost:5000/api/login'
params = {
    'email' : 'wafu4975@colorado.edu',
    'password' : 'Warrenfulton98'
}
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
url = "http://localhost:5000/index"
r = requests.get(url)
print(r.text)
url = 'http://localhost:5000/api/logout'
r = requests.get(url)
print(r.text)
url = "http://localhost:5000/index"
r = requests.get(url)
print(r.text)
"""

# test manager getting trainees
"""
url = 'http://localhost:5000/manager/get_trainees'
params = {'manager_uuid' : '-MXmPqXDWN0PGufepgZC'}
data = json.dumps(params)
r = requests.get(url, data=data)
print(r.text)
"""

# test manager getting a trainee's plan_id
"""
url = 'http://localhost:5000/manager/get_trainee_training_plan_id'
params = {
    'manager_uuid' : '-MXmPqXDWN0PGufepgZC',
    'trainee_uuid' : '-MXSr7gxFkFupIMfnkXs'
    }
data = json.dumps(params)
r = requests.get(url, data=data)
print(r.text)
"""

# test manager getting a plan's contents
"""
url = 'http://localhost:5000/manager/get_trainee_training_plan_contents'
params = {
    'manager_uuid' : '-MXmPqXDWN0PGufepgZC',
    'plan_id' : '-MX9H6qe2jf9NPyh-SWV'
    }
data = json.dumps(params)
r = requests.get(url, data=data)
print(r.text)
"""

# test manager getting their template ids
"""
url = 'http://localhost:5000/manager/get_training_templates'
params = {
    'manager_uuid' : '-MXmPqXDWN0PGufepgZC'
    }
data = json.dumps(params)
r = requests.get(url, data=data)
print(r.text)
"""

# test manager getting a template's contents
"""
url = 'http://localhost:5000/manager/get_training_template'
params = {
    'manager_uuid' : '-MXmPqXDWN0PGufepgZC',
    'template_id' : '-MWjXs9F-oMekBr8Au5r'
    }
data = json.dumps(params)
r = requests.get(url, data=data)
print(r.text)
"""

# test manager getting a specific training
"""
url = 'http://localhost:5000/manager/get_training'
params = {
    'manager_uuid' : '-MXmPqXDWN0PGufepgZC',
    'training_id' : 'training_id2'
    }
data = json.dumps(params)
r = requests.get(url, data=data)
print(r.text)
"""

###
"""
[START]
These tests are meant to be run in succession
"""
###
# test manager making a new template
"""
url = 'http://localhost:5000/manager/new_empty_template'
params = {
    'manager_uuid' : '-MXmPqXDWN0PGufepgZC',
    'template_name' : 'Test Template',
    'description' : 'Test template description'
    }
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
"""

# test manager adding a training to a template with no trainings in it
"""
url = 'http://localhost:5000/manager/add_training_to_training_template'
params = {
    'manager_uuid' : '-MXmPqXDWN0PGufepgZC',
    'template_id' : '-MY_yURxvwrilaDJb6Va', # need to plug in the template id for the template that was created
    'training_name' : 'Test Training1',
    'documentation_links' : {},
    'other_links' : {},
    'note' : 'Test note',
    'due_date' : '2021-04-16T11:30:30',
    'duration' : 8
    }
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
"""

# test manager adding a training to a template with one training in it
"""
url = 'http://localhost:5000/manager/add_training_to_training_template'
params = {
    'manager_uuid' : '-MXmPqXDWN0PGufepgZC',
    'template_id' : '-MY_yURxvwrilaDJb6Va',
    'training_name' : 'Test Training2',
    'documentation_links' : {'link' : 'link description'},
    'other_links' : {},
    'note' : 'Test note',
    'due_date' : '2021-04-16T11:30:30',
    'duration' : 8
    }
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
"""

# test manager adding a template to a training plan
"""
url = 'http://localhost:5000/manager/add_template_to_training_plan'
params = {
    'manager_uuid' : '-MXmPqXDWN0PGufepgZC',
    'template_id' : '-MY_yURxvwrilaDJb6Va',
    'template_name' : 'Test Template',
    'plan_id' : '-MX9H6qe2jf9NPyh-SWV'
    }
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
"""

# test manager adding a training to a training plan
"""
url = 'http://localhost:5000/manager/add_training_to_training_plan'
params = {
    'manager_uuid' : '-MXmPqXDWN0PGufepgZC',
    'plan_id' : '-MX9H6qe2jf9NPyh-SWV',
    'training_name' : 'Test Training3',
    'documentation_links' : {'link' : 'link description'},
    'other_links' : {},
    'note' : 'Test note',
    'due_date' : '2021-04-16T11:30:30',
    'duration' : 8
    }
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
"""

# test manager adding info to a training
"""
url = 'http://localhost:5000/manager/add_info_to_training'
params = {
    'manager_uuid' : '-MXmPqXDWN0PGufepgZC',
    'training_id' : '-MYa2nougG5B23VJ3etB',
    'documentation_links' : {'link2' : 'link description2'},
    'other_links' : {'link' : 'link_description'},
    }
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
"""

# test manager updating info in a training
"""
url = 'http://localhost:5000/manager/update_training_info'
params = {
    'manager_uuid' : '-MXmPqXDWN0PGufepgZC',
    'training_id' : '-MYa2nougG5B23VJ3etB',
    'note' : 'updated note',
    }
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
"""

# test manager removing training from a template
"""
url = 'http://localhost:5000/manager/remove_training_from_template'
params = {
    'manager_uuid' : '-MXmPqXDWN0PGufepgZC',
    'template_id' : '-MY_yURxvwrilaDJb6Va',
    'training_id' : '-MYa-wdM5cjU1-BjyCYC',
    }
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
"""

# test manager removing training from a plan
"""
url = 'http://localhost:5000/manager/remove_training_from_plan'
params = {
    'manager_uuid' : '-MXmPqXDWN0PGufepgZC',
    'plan_id' : '-MX9H6qe2jf9NPyh-SWV',
    'training_id' : '-MYa2nougG5B23VJ3etB',
    }
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
"""

# test manager removing training from a plan
"""
url = 'http://localhost:5000/manager/get_manager_events'
params = {
    'manager_uuid' : '-MXmPqXDWN0PGufepgZC'
    }
data = json.dumps(params)
r = requests.get(url, data=data)
print(r.text)
"""

###
"""
Trainee Tests
"""
###

# test trainee getting the uuids of their peers
"""
url = 'http://localhost:5000/trainee/get_peers'
params = {
    'trainee_uuid' : '-MXSr7gxFkFupIMfnkXs'
    }
data = json.dumps(params)
r = requests.get(url, data=data)
print(r.text)
"""

# test trainee getting the uuids of their managers
"""
url = 'http://localhost:5000/trainee/get_managers'
params = {
    'trainee_uuid' : '-MXSr7gxFkFupIMfnkXs'
    }
data = json.dumps(params)
r = requests.get(url, data=data)
print(r.text)
"""

# test trainee getting their plan id
"""
url = 'http://localhost:5000/trainee/get_trainee_plan_id'
params = {
    'trainee_uuid' : '-MXSr7gxFkFupIMfnkXs'
    }
data = json.dumps(params)
r = requests.get(url, data=data)
print(r.text)
"""

# test trainee getting their plan contents (pairs of training_id : training_name)
"""
url = 'http://localhost:5000/trainee/get_trainee_training_plan_contents'
params = {
    'trainee_uuid' : '-MXSr7gxFkFupIMfnkXs',
    'plan_id' : '-MX9H6qe2jf9NPyh-SWV'
    }
data = json.dumps(params)
r = requests.get(url, data=data)
print(r.text)
"""

# test trainee getting the contents of a specific training
"""
url = 'http://localhost:5000/trainee/get_training'
params = {
    'trainee_uuid' : '-MXSr7gxFkFupIMfnkXs',
    'training_id' : 'training_id'
    }
data = json.dumps(params)
r = requests.get(url, data=data)
print(r.text)
"""

# test trainee getting their events
"""
url = 'http://localhost:5000/trainee/get_trainee_events'
params = {
    'trainee_uuid' : '-MXSr7gxFkFupIMfnkXs'
    }
data = json.dumps(params)
r = requests.get(url, data=data)
print(r.text)
"""

# test trainee marking one of their trainings complete
"""
url = 'http://localhost:5000/trainee/mark_task_complete'
params = {
    'trainee_uuid' : '-MXSr7gxFkFupIMfnkXs',
    'training_id' : 'training_id'
    }
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
"""

###
"""
Shared Method Tests
"""
###

# test adding an event between a manager and a trainee
"""
url = 'http://localhost:5000/shared/add_event_between_manager_and_trainee'
params = {
    'manager_uuid' : '-MXmPqXDWN0PGufepgZC',
    'manager_name' : 'Jake Luoma',
    'trainee_uuid' : '-MXSr7gxFkFupIMfnkXs',
    'trainee_name' : 'Warren Fulton',
    'start' : 'start datetime',
    'end' : 'end datetime',
    'text' : 'text note'
    }
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
"""

# test adding an event between two trainees
"""
url = 'http://localhost:5000/shared/add_event_between_trainee_and_trainee'
params = {
    'trainee_uuid1' : '-MYG8kHNEhUsI0JoXhnN',
    'trainee_name1' : 'Andrea Chomorro',
    'trainee_uuid2' : '-MXSr7gxFkFupIMfnkXs',
    'trainee_name2' : 'Warren Fulton',
    'start' : 'start datetime',
    'end' : 'end datetime',
    'text' : 'text note'
    }
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
"""