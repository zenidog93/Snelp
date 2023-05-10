from flask_app import app   
from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.user_model import User
from flask_app.models import ride_model
from flask_app.models import destination_model

#displays
@app.route('/')
def home():
    return render_template('index.html')

# displays
@app.route('/display/ikon/mountains')
def ikon_home_page():
    return render_template('display_ikon_home.html')

@app.route('/<mountain_name>/display/mountain')
def display_mountain_reviews(mountain_name):
    data = {
        'mountain_name' : mountain_name
    }
    print('\n\n???', data)

    this_mountain = destination_model.Destination.get_one_destination_by_name(data)
    
    print('\n\n\n???',this_mountain)
    
    all_rides = ride_model.Ride.get_all_rides_by_mountain(data)
    return render_template('display_one_mountain.html', all_rides = all_rides, this_mountain = this_mountain)

@app.route('/display/mountain/by_search', methods= ['post'])
def display_mountain_reviews_by_search():
    if not User.validate_search(request.form):
        
        return redirect('/')
    
    data = {
        'mountain_name' : request.form['mountain_name']
    }
    this_mountain = destination_model.Destination.get_one_destination_by_name(data)
    
    if this_mountain == False:
        flash("Mountain not found. Try again")
        return redirect('/')
    
    print('\n\n\n???',this_mountain)
    
    all_rides = ride_model.Ride.get_all_rides_by_mountain(data)
    return render_template('display_one_mountain.html', all_rides = all_rides, this_mountain = this_mountain)


#######################

# DISPLAYS - user login page
@app.route('/display/user/login')
def display_user_login():
    return render_template('display_user_login.html')

#ACTION - logs in the user if they have an account
@app.route ("/user/login", methods=['POST'])
def user_login():
    data = {
        'email' : request.form['email']
    }
    
    user_in_db = User.get_one_by_email(data) ## returns false or a user
    
    # if email not found
    if not user_in_db:
        flash("Email or password are invalid")
        return redirect('/display/user/login')
    
    #check to make sure the password matches with its email
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/display/user/login')
    
    session['user_id'] = user_in_db.id
    
    return redirect('/user_dashboard')


#displays
@app.route('/display/create/account/form')
def display_create_account_form():
    
    return render_template('display_create_account_form.html')

#creates user, hashes their password, and directs them to their dashboard
@app.route('/user/create', methods =['POST'])
def register_user():
    if not User.validate_registration(request.form):
        return redirect('/display/create/account/form')
    
    #1 has the passwords
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # get the data dictionary ready with the new hashed password to create a User
    data = {
        **request.form,
        'password' :pw_hash
    }
    #3 pass it to the user model
    user_id = User.create_user(data)
    
    #4 we store the user_id in session to keep track of the which user is currently logged in. 
    session['user_id'] = user_id
    return redirect ('/user_dashboard')

    
    #check to make sure the password matches with its email
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    
    session['user_id'] = user_in_db.id
    
    return redirect('/user_dashboard')

#ACTION- takes user to their dashboard with their rides only
@app.route('/user_dashboard')
def display_dash():
    if 'user_id'  not in session:
        return redirect ('/display/user/login')
    
    data = {
        'id': session['user_id']
    }
    
    logged_user = User.get_one(data)
    this_user= User.get_users_rides(data)
    
    #####eventually bring in this users dashboard
    print(this_user)
    return render_template("display_user_dashboard.html", logged_user = logged_user, this_user= this_user)

#ACTION-logs current user pit
@app.route('/logout')
def logout():
    if 'user_id'  not in session:
        return redirect ('/display/user/login')
    session.clear()
    return redirect('/')