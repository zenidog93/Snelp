from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

from flask_app.models import user_model

class Ride:
    def __init__(self, data):
        self.id = data['id']
        self.destination = data['destination']
        self.trail_name = data['trail_name']
        self.difficulty = data['difficulty']
        self.equipment = data['equipment']
        self.ride_exp = data['ride_exp']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
        
    @classmethod
    def create_ride(cls, data):
        query = """
                INSERT INTO rides (destination, trail_name, difficulty, equipment, ride_exp, created_at, updated_at, user_id)
                VAlUES ( %(destination)s, %(trail_name)s, %(difficulty)s, %(equipment)s, %(ride_exp)s, NOW(), NOW(), %(user_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def delete_ride(cls, data):
        query = """
                DELETE
                FROM rides
                WHERE id = %(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_one_ride_for_edit(cls, data):
        query = """
                SELECT *
                FROM rides
                JOIN users
                ON users.id = rides.user_id
                WHERE rides.id = %(id)s
                """
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        if results: 
            this_ride = cls(results[0])
            row = results[0]
            user_data = {
                **row, 
                'id' : row['user_id'],
                'created_at': row['created_at'],
                'updated_at' : row['updated_at']
            }
            this_user = user_model.User(user_data)
            this_ride.creator = this_user
            return this_ride
        return False
    
    @classmethod
    def update_ride(cls, data):
        query = """
                UPDATE rides
                SET 
                    destination = %(destination)s, 
                    trail_name = %(trail_name)s,
                    difficulty = %(difficulty)s, 
                    equipment = %(equipment)s, 
                    ride_exp = %(ride_exp)s 
                WHERE id = %(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_all_rides_by_mountain(cls, data):
        query = """
                SELECT *
                FROM rides
                JOIN users
                ON users.id= rides.user_id
                WHERE destination = %(mountain_name)s
                ORDER BY rides.created_at DESC;
                """
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        all_rides = []
        if results:
            for row in results:
                this_ride = cls(row)
                
                user_data = {
                    **row, 
                    'id' : row['users.id'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_ride.creator = this_user
                all_rides.append(this_ride)
        return all_rides
    
    @staticmethod
    def validate_ride(recipe_submission):
        is_valid = True
        
        if len(recipe_submission['trail_name']) < 1:
            is_valid = False
            flash("Name your trail :) ") 
        
        if len(recipe_submission['ride_exp']) < 1:
            is_valid = False
            flash("You must enter your review")
            
        return is_valid