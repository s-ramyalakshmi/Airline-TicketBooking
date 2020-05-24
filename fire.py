import pyrebase


config = {

    'apiKey': "AIzaSyA520VBeHVrhEF1hpJ13S2D1ZD94TlyNOE",
    "authDomain": "software-engineering-6e9a7.firebaseapp.com",
    'databaseURL': "https://software-engineering-6e9a7.firebaseio.com",
    'projectId': "software-engineering-6e9a7",
    'storageBucket': "software-engineering-6e9a7.appspot.com",
    'messagingSenderId': "329135496498"
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

for i in db.child('users').child('padigelavivekreddy').child('journey').get().each():
    print(i.key())
