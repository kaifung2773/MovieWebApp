from pymongo import MongoClient
import os

# Database configuration
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = "sample_mflix"

class Database:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DATABASE_NAME]
        
    # Collections as properties
    @property
    def movies(self):
        return self.db.movies
    
    @property 
    def users(self):
        return self.db.users
        
    def close_connection(self):
        self.client.close()

# Create single instance
database = Database()

# For easy importing
movies_collection = database.movies
users_collection = database.users