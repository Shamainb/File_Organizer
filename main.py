from dotenv import load_dotenv
import os
import pyrebase
import firebase_admin
from firebase_admin import credentials
from flask import Flask, render_template, request

#Load environment variables
load_dotenv()

firebaseConfig = {
  'apiKey': os.getenv('API_KEY'),
  'authDomain': "file-organizer-ae30c.firebaseapp.com",
  'projectId': "file-organizer-ae30c",
  'storageBucket': "file-organizer-ae30c.appspot.com",
  'messagingSenderId': "403035956223",
  'appId': "1:403035956223:web:ea41743539721fafc3fdca",
  'measurementId': "G-QYVSM3WXTZ",
  'databaseURL': "firebase-adminsdk-9i992@file-organizer-ae30c.iam.gserviceaccount.com"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

cred = credentials.Certificate("/home/shamain/Desktop/File_Organizer/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()



app = Flask(__name__)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['user_email']
        password = request.form['user_pwd']

        try:
            # Sign in with email and password
            user_info = auth.sign_in_with_email_and_password(email, password)
            account_info = auth.get_account_info(user_info['idToken'])
            
            # Check if the user's email is verified
            if not account_info['users'][0]['emailVerified']:
                verify_message = 'Please verify your email'
                return render_template('index.html', umessage=verify_message)
            
            return render_template('home.html')
        except Exception as e:
            unsuccessful = 'Please check your credentials'
            return render_template('index.html', umessage=unsuccessful)
    
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        pwd0 = request.form['user_pwd0']
        pwd1 = request.form['user_pwd1']

        if pwd0 == pwd1:
            try:
                email = request.form['user_email']
                password = request.form['user_pwd1']
                
                # Create a new user
                new_user = auth.create_user_with_email_and_password(email, password)
                
                # Send email verification
                auth.send_email_verification(new_user['idToken'])
                
                return render_template('verify_email.html')
            except Exception as e:
                existing_account = 'This email is already used'
                return render_template('create_account.html', exist_message=existing_account)
        else:
            return render_template('create_account.html', message="Passwords do not match")
    
    return render_template('create_account.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['user_email']
        
        # Send password reset email
        auth.send_password_reset_email(email)
        
        return render_template('index.html', umessage="Password reset email sent")
    
    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(debug=True)
