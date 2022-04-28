from cmath import log
from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy import true
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user


# Creating "views" Blueprint
auth = Blueprint('auth', __name__)

#Defining Login route 
@auth.route('/login', methods=['GET','POST'])
def login():
    # Accessing and Strong Data from Login From
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Return User from DB
        user = User.query.filter_by(email=email).first()

        if user:
            # Password Check
            if check_password_hash(user.password, password) :
                flash('Logged in Succesfully!.', category='success')

                # Loggging User in Dashboard after login
                login_user(user, remember=True)
                # Redirecting to dashboard after signup
                return redirect(url_for('views.dashboard'))

            else:
                flash('Incorrect Password. Please try again!', category='error')
        else :
            flash('User does not exists. Please SignUp!', category='error')
            return redirect(url_for('auth.sign_up'))


    return render_template("login.html", user=current_user)

# Defining Logout route 
@auth.route('/logout')
@login_required
def logout():
    # Logging out the user
    logout_user()
    flash('Logged out of your account!.', category='success')
    return redirect(url_for('auth.login'))

# Defining SignUP route 
@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():

    #Accessing and Strong Data from SignUp From
    #Differenciation b/n GET and POST method
    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # Check for multiple emails
        user = User.query.filter_by(email=email).first()

        #Checking form data is valid or not
        if user:
            flash('User Already Exists. Please Login!.', category="error")
            return redirect(url_for('auth.login'))
        elif len(fname) < 2 or len(lname) < 1:
            flash('First Name must be longer than 2 characters.', category="error")
        elif len (email) < 6 :
            flash('Email must be longer than 4 characters.', category="error")
        elif password1 != password2:
            flash('Entered passwords don\'t match!', category="error")
        elif len(password1) < 5 : 
            flash('Password must be at leat 7 characters.', category="error")
        else : 
            new_user = User(email=email,fname=fname,lname=lname,password=generate_password_hash(password1, method='sha256'))

            # Adding new user to database
            db.session.add(new_user)
            # print('NEW USER ADDED')
            db.session.commit()
            
            flash('Account created Succesfully!.', category="success")
            # Loggging User in Dashboard after signup
            login_user(new_user, remember=True)
            # Redirecting to dashboard after signup
            return redirect(url_for('views.dashboard'))

    return render_template("sign-up.html",user=current_user)
