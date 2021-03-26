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

# authentication
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

# login
"""
url = 'http://localhost:8080/authentication/login'
params = {
    'email' : 'luoma@colorado.edu',
    'password' : 'password',
    }
r = requests.post(url, data=params)
print(r.text)
"""

# add new company
"""
url = 'http://localhost:8080/database/add_new_company'
params = {
    'name' : 'ACME Company',
    'num_employees' : '2'
    }
r = requests.post(url, data=params)
print(r.text)
"""

# add new manager
"""
url = 'http://localhost:8080/database/add_new_manager'
params = {
    'name' : 'Fenton the Dog', # https://www.youtube.com/watch?v=3GRSbr0EYYU
    'age' : '6',
    'company_name' : 'ABC Corp',
    'company_uuid' : 'iwlupo84UENk',
    }
r = requests.post(url, data=params)
print(r.text)
"""

# add new trainee
"""
url = 'http://localhost:8080/database/add_new_trainee'
params = {
    'name' : 'Felix the Cat',
    'age' : '6',
    'company_name' : 'ABC Corp',
    'company_uuid' : 'iwlupo84UENk',
    }
r = requests.post(url, data=params)
print(r.text)
"""

# create new template
url = 'http://34.68.166.146:8080/database/create_new_template'
params = {
    'template_name' : 'Test Template',
    'trainee_uuid' : 'Njwwol98JJwny65',
    'manager_uuid' : 'jjfiUUe662Ruuwm',
    'company_uuid' : 'iwlupo84UENk',
    }
r = requests.post(url, data=params)
print(r.text)
