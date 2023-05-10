from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

from flask_app.models import ride_model
from flask_app.models import destination_model

from flask import flash

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        query = """
                INSERT INTO users (first_name, last_name,email, password, created_at, updated_at)
                VAlUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());
                """
        return connectToMySQL(DATABASE).query_db(query, data) 
    
    
    #get one by id
    @classmethod
    def get_one(cls, data):
        query = """
                SELECT *
                FROM users
                WHERE id = %(id)s;
                """
        results=  connectToMySQL(DATABASE).query_db(query, data) 
        
        if len(results) <1:
            return False
        
        return cls(results[0])
        #get one by email
    @classmethod
    def get_one_by_email(cls, data):
        query = """
                SELECT *
                FROM users
                WHERE users.email = %(email)s;
                """
        results=  connectToMySQL(DATABASE).query_db(query, data) 
        
        if len(results) < 1:
            return False
        
        return cls(results[0])
    
    @classmethod
    def get_users_rides(cls, data):
        query = """
                SELECT *
                FROM users
                JOIN rides
                ON users.id = rides.user_id
                WHERE users.id = %(id)s
                ORDER BY rides.created_at DESC;
                """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            this_user= cls(results[0])
            these_rides = []
            these_destinations = []
            
            for row in results:
                ride_dict = {
                    **row, 
                    'id' : row['rides.id'],
                    'created_at' : row['rides.created_at'],
                    'updated_at' : row['rides.updated_at']
                }
                this_ride = ride_model.Ride(ride_dict)
                these_rides.append(this_ride)
                this_user.rides = these_rides
                
                
            return this_user
        else: 
            False
    
    @staticmethod
    def validate_search(form_submitted):
        is_valid = True
        if len(form_submitted['mountain_name']) < 0:
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_registration(register):
        is_valid = True # we always assume this is true unless the following happens. If any happen, the we can't register/do the create_user query
        if len(register['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        
        #checks to make sure the last name input has characters in it
        if len(register['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
            
        if len(register['email']) < 1:
            
            is_valid = False
            flash("Invalid email address")
        
        #here , we are checking to make sure the email is valid and also to make sure it doesn't already exist
        elif not EMAIL_REGEX.match(register['email']): 
            flash("Invalid email address!")
            is_valid = False
        else:
            data_from_email = {
                'email' : register['email']
            }
            email_exists = User.get_one_by_email(data_from_email)
        
            if email_exists:
                is_valid = False
                flash ("Looks like you already registered with us!")
        
        #assigned the password we got from the requested form to a variable we can use here since it is returned to us as a string
        password = register['password']
        
        if len(password) < 3:
            is_valid = False
            flash("Password must be at least 3 characters long")
        
        #makes sure that the password you typed second matches with what you first typed
        elif not password == register['confirm_password']:
            is_valid = False
            flash("Passwords don't match")
        

        return is_valid  