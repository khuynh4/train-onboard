import json
import requests

"""
url = 'http://localhost:5000'
params = {
    'name' : 'Jake',
    'info' : 'pretty cool'
}
r = requests.post(url, data=params)
r = json.loads(r.text)
print(r)
"""
"""
first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    age = request.form["age"]
    address = request.form["address"]
    password = request.form["password"]
    confirm_password = request.form["confirm_pass"]
"""

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

# login and test authentication of verification token
"""
url = 'http://localhost:8080/authentication/login'
params = {
    'email' : 'luoma@colorado.edu',
    'password' : 'password'
}
r = requests.post(url, data=params)
print(r.text)

url = 'http://localhost:8080/authentication/test'
params = {
    'authorization' : r.text
}
r = requests.post(url, data=params)
print(r.text)
"""

# add new company
"""
url = 'http://localhost:8080/database/add_new_company'
params = {
    'identifier' : '123abc',
    'name' : 'ACME Company',
    'num_employees' : '3',
    'managers' : {
        'NYFVp8qdnPhUX3Q4pzJ1LMbwvWh1' : 'Jake Luoma'
    },
    'trainees' : {
        'MhDrj7IGknRLcDiz87btbK8zlwt2' : 'Warren Fulton',
        'arbitrary_uuid' : 'Arbitrary Name'
    }
}
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
"""

# add new manager
"""
url = 'http://localhost:8080/database/add_new_manager'
params = {
    'manager_uuid' : 'NYFVp8qdnPhUX3Q4pzJ1LMbwvWh1',
    'name' : 'Jake Luoma',
    'age' : '30',
    'trainees' : {
        'MhDrj7IGknRLcDiz87btbK8zlwt2' : 'Warren Fulton',
        'arbitrary_uuid' : 'Arbitrary Name'
    }
}
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
"""

# add new trainee
"""
url = 'http://localhost:8080/database/add_new_trainee'
params = {
    'trainee_uuid' : 'MhDrj7IGknRLcDiz87btbK8zlwt2',
    'name' : 'Warren Fulton',
    'age' : '22'
}
data = json.dumps(params)
r = requests.post(url, data=data)
print(r.text)
"""

# login, then test manager getting list of employees
"""
url = 'http://localhost:8080/authentication/login'
params = {
    'email' : 'luoma@colorado.edu',
    'password' : 'password'
}
r = requests.post(url, data=params)
print("verification token = {}".format(r.text))

url = 'http://localhost:8080/manager/get_trainees'
headers = {'authorization' : r.text}
r = requests.get(url, headers=headers)
print(r.text)
"""

# login, then test manager getting an employee training plan
"""
url = 'http://localhost:8080/authentication/login'
params = {
    'email' : 'luoma@colorado.edu',
    'password' : 'password'
}
r = requests.post(url, data=params)
print("verification token = {}".format(r.text))

url = 'http://localhost:5000/manager/get_trainees'
params = {'manager_uuid' : 'NYFVp8qdnPhUX3Q4pzJ1LMbwvWh1'}
data = json.dumps(params)
r = requests.get(url, data=data)
print(r.text)
"""

# test manager getting templates
url = 'http://localhost:5000/manager/get_training_templates'
params = {'manager_uuid' : 'NYFVp8qdnPhUX3Q4pzJ1LMbwvWh1'}
data = json.dumps(params)
r = requests.get(url, data=data)
print(r.text)