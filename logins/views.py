from django.shortcuts import render, HttpResponse, redirect, reverse
import pyrebase
from django.contrib import auth as authe
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.conf.urls.static import static
user = {}
# Create your views here.
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
storage = firebase.storage()

def base(request):
    mesg = []
    if 'emailVerificationMesg' in request.session:
        mesg += request.session.get('emailVerificationMesg')
        request.session.pop('emailVerificationMesg', None)
    if 'notsignedin' in request.session:
        mesg += request.session.get('notsignedin')
        request.session.pop('notsignedin')
    return render(request, 'base.html', {'mesg': mesg})

def signin(request):
    error = ''
    if 'mesg' in request.session:
        error = request.session.get('mesg')
        request.session.pop('mesg', None)
    mesg = []
    if 'emailVerificationMesg' in request.session:
        mesg.append(request.session.get('emailVerificationMesg'))
        request.session.pop('emailVerificationMesg', None)
    if 'notsignedin' in request.session:
        mesg.append(request.session.get('notsignedin'))
        request.session.pop('notsignedin')
    print(mesg)
    return render(request,'signin/signin.html', {'error': error, 'mesg': mesg})

def signup(request):
    return render(request, 'signup/signup.html', {})

def postsignin(request):
    email = request.POST.get('email')
    passw = request.POST.get('password')
    try:
        user = auth.sign_in_with_email_and_password(email,passw)
        print(user)
    except:
        message="invalid info"
        request.session['mesg'] = 'Invalid Username or Password'
        request.session['mesgcount'] = int(2)
        return redirect(reverse(signin))
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    request.session['key'] = email.split('@')[0]
    #return redirect(v.book)
    mesg = []
    mesg.append("Successfully Signed In")
    return redirect(base)
    #return redirect(v.book)

def postsignup(request):
    name  = request.POST.get("uname")
    email = request.POST.get("cemail")
    number = request.POST.get("unumber")
    passw = request.POST.get("password")
    gender = request.POST.get("cgender")
    agree = request.POST.get("cagree")
    print("name = " + str(name) )
    print("email = " + str(email) )
    print("passw = " + str(passw) )
    print("gender = " + str(gender) )
    print("agree = " + str(agree) )
    try:
        user = auth.create_user_with_email_and_password(email, passw)
        auth.send_email_verification(user['idToken'])
        data = { 'name': name,
                 'number': number,
                 'email': email,
                 'gender': gender,
                 'profilepic': "NO",
                 'document': "NO",
               }
        db = firebase.database()
        db.child("users").child(email.split('@')[0]).set(data)
        request.session['emailVerificationMesg'] = 'Verification email has been sent'

    except:
            message="invalid info"
            return render(request,'signup/signup.html',{"messg":message})
    session_id = user['idToken']
    request.session['b_no']=0
    request.session['booking_no']=0

    request.session['uid'] = str(session_id)
    mesg = []
    request.session['key'] = email.split('@')[0]
    mesg.append("Successfully Signed Up")
    return render(request, 'base.html', {'mesg': mesg})

def logout(request):
    if 'uid' in request.session:
        request.session.pop('uid')
    if 'key' in request.session:
        request.session.pop('key')
    request.session['notsignedin'] = 'Successfully Logged Out'
    return redirect(reverse(signin))

def profile(request):
    if 'uid' not in request.session:
        request.session['notsignedin'] = "Please SignIn to avail the services"
        return redirect(reverse(signin))
    email = auth.get_account_info(request.session['uid'])["users"][0]["email"]
    url = "https://cdn0.iconfinder.com/data/icons/male-user-action-icon-set-4-ibrandify/512/25-512.png"
    docu = "Not uploaded Yet"
    if db.child("users").child(email.split("@")[0]).child("profilepic").get().val() == "YES":
        url = storage.child('images/' + email + '/profilepic').get_url(None)
    if db.child("users").child(email.split("@")[0]).child("document").get().val() == "YES":
        docu = "Uploaded"
    data = db.child("users").child(email.split("@")[0]).get().val()
    print(data['name'])
    uploaded_file_url = "already uploaded"
    uploaded_file_urli = "already uploaded"
    if 'uploaded_file_url' in request.session:
        uploaded_file_url = request.session['uploaded_file_url']
    if 'uploaded_file_urli' in request.session:
        uploaded_file_urli = request.session['uploaded_file_urli']
    return render(request, 'profile/profile.html', {
            'uploaded_file_url': uploaded_file_url,
            'uploaded_file_urli': uploaded_file_urli,
            'url': url,
            'name': data['name'],
            'gender': data['gender'],
            'email': data['email'],
            'number': data['number'],
            'document': docu
        })

def resetpassword(request):
    print("coming")
    try:
        user = auth.send_password_reset_email(email)
    except:
        message="invalid info"
        return render(request, 'base.html', {"messg":message})
    return redirect(reverse(profile))

def simple_upload(request):
    email = auth.get_account_info(request.session['uid'])["users"][0]["email"]
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        storage.child("images/" + email + "/profilepic").put("." + uploaded_file_url)
        db = firebase.database()
        db.child("users").child(email.split("@")[0]).update({"profilepic": "YES"})
        request.session['uploaded_file_url'] = uploaded_file_url
        return redirect(reverse(profile))
    request.FILES['myfile'] = None
    return render(request, 'base.html')

def document_upload(request):
    print("yanaicoming")
    email = auth.get_account_info(request.session['uid'])["users"][0]["email"]
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        storage.child("document/" + email + "/doc").put("." + uploaded_file_url)
        db = firebase.database()
        db.child("users").child(email.split("@")[0]).update({"document": "YES"})
        request.session['uploaded_file_urli'] = filename
        return redirect(reverse(profile))
    request.FILES['myfile'] = None
    return render(request, 'base.html')

def updateprofile(request):
    db = firebase.database()
    email = auth.get_account_info(request.session['uid'])["users"][0]["email"]
    print(email)
    print("updateprofile")
    name = request.POST.get("FullName")
    print("vivek name name \n\n\n\n\n\n")
    print(name)
    if name != None:
        db.child("users").child(email.split("@")[0]).update({"name": name})
    gender = request.POST.get("Gender")
    if gender != None:
        db.child("users").child(email.split("@")[0]).update({"gender": gender})
    number = request.POST.get("PhoneNumber")
    if number != None:
        db.child("users").child(email.split("@")[0]).update({"number": number})
    return redirect(reverse(profile))
