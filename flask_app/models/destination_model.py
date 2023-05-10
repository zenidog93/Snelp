from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Destination:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.lat = data['lat']
        self.lng = data['lng']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_one_destination_by_name(cls, data):
        query = """
                SELECT *
                FROM destinations
                WHERE name = %(mountain_name)s;
                """
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        if results:
            this_mountain = cls(results[0])
            return this_mountain
        return False
    
    @classmethod
    def get_all_mountains(cls):
        query = """
                SELECT *
                FROM destinations
                """
        results = connectToMySQL(DATABASE).query_db(query)
        all_mountains  = []
        if results:
            for row in results:
                this_mountain = cls(row)
                all_mountains.append(this_mountain)
        return all_mountains
        