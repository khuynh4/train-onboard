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
#the bellow function and assignment temporarily fixes the problem until the library is patched
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
    login_json = request.get_json()

    #header required to send information between servers cross origin
    header = {'Access-Control-Allow-Origin': '*'}

    if not login_json:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400

    email = login_json['email']
    password = login_json['password']

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
    response = request.get_json()

    if not response:
        return jsonify({'headers': header, 'msg': 'Missing JSON'}), 400
    
    first_name = response['first_name']
    last_name = response['last_name']
    email = response['email']
    age = response['age']
    address = response['address']
    password = response['password']
    confirm_pass = response['confirm_pass']

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
    


if __name__ == '__main__':
    app.run(port=5000, debug=True)