import pyrebase


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
db = firebase.database()
storage = firebase.storage()

'''
db = firebase.database()
storage = firebase.storage()
auth = firebase.auth()

#Authentication
#Login
email = input("Enter your email")
password = input("Enter your password")


try:
	auth.sign_in_with_email_and_password(email, password)
except:
	print("Invalid user or password. Try again.")


#Sign up
email = input("Enter your email")
password = input("Enter your password")
confirm_pass = input("Confirm Password")

if password == confirm_pass:

	try:
		auth.create_user_with_email_and_password(email, password)
	except:
		print("Username already exists")


#Storage
filename = input("Enter the name of the file")
cloud_filename = input("Enter the name of the file on the cloud")
storage.child(cloud_filename).put(filename)
print(storage.child(cloud_filename).get_url(None))

#download
cloud_filename = input("Enter the name of the file you want to download")
storage.child("google.txt").download("", "downloaded.txt")

#reading file
cloud_filename = input("Enter the name of the file you want to download")
url = storage.child(cloud_filename).get_url(None)
f = urllive.request.urlopen(url).read()
print(f)

#Database
data = {
	'name': "John Smith",
	'age': 40,
	'position': "manager"
}

#db.child("Users").child("Employees").child("Managers").child("12345").set(data)
#db.child("Users").child("Employees").child("Trainee").child("12346").set(data)

#Update
#db.child("Users/Employees/Managers/12345").update({'name': "John"})

people = db.child("Users/Employees/Managers").get()
for person in people.each():
	if person.val()['name'] == 'John':
		db.child("Users/Employees/Managers").child(person.key()).update({'name': "Jane"})

#Delete
people = db.child("Users/Employees/Managers").get()
for person in people.each():
	if person.val()['name'] == 'Jane':
		db.child("Users/Employees/Managers").child(person.key()).child('age').remove()

#Read
people = db.child("Users/Employees/Trainee").child('12346').get()
print(people.val())'''

#Connect DB with storage
name = input("Enter Name")
age = input("Enter  age")
position = input("Enter position")
filename = input("Enter file")
cloud_filename = input("Enter cloud name")

storage.child(cloud_filename).put(filename)
url = storage.child(cloud_filename).get_url(None)

data = {
	'name': name,
	'age': age,
	'position': position,
	'url': url
}

db.child('Users/Employees/Managers').push(data)










