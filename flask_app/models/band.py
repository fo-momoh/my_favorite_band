from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class Band:
    def __init__(self, data):
        self.id = data["id"]
        self.band_name = data["band_name"]
        self.music_genre = data["music_genre"]
        self.home_city = data["home_city"]
        self.user_id = data["user_id"] #======= We add user_id session in order to display edit page
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

# Function made in order to display all bands in welcome page, specifically in line 22 of user controller.
    @classmethod
    def get_all_bands(cls):
        query = "SELECT * FROM bands JOIN users ON bands.user_id = users.id;"
        results = connectToMySQL('belt_schema').query_db(query)
        bands = []
        if results:
            for row in results:
                temp_var = (cls(row))
                data = {
                    "id": row["users.id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "password": row["password"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"]
                }
                temp_var.creator = user.User(data)
                bands.append(temp_var)
        return bands

# Creates a band and assignes it to the creator with USER_ID.
    @classmethod
    def create_band(cls, data):
        query = "INSERT INTO bands (user_id, band_name, music_genre, home_city, created_at, updated_at) VALUES ( %(user_id)s, %(band_name)s, %(music_genre)s,%(home_city)s, NOW(), NOW());"
        result = connectToMySQL('belt_schema').query_db(query, data)
        return result

# I am using it but don't know if it really works. 
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM bands JOIN users ON bands.user_id = users.id WHERE bands.id = %(id)s;"
        results = connectToMySQL("belt_schema").query_db(query, data)
        if results:
            bands = cls(results[0])
            bands.creator = user.User(results[0])
            return bands

# Updates a band.
    @classmethod
    def update_band(cls, data):
        query = "UPDATE bands SET band_name = %(band_name)s, music_genre = %(music_genre)s, home_city = %(home_city)s, updated_at = NOW() WHERE id = %(id)s;"
        connectToMySQL("belt_schema").query_db(query, data)
        # return data["id"]

# Deletes a band.
    @classmethod
    def delete_band(cls, data):
        query = "DELETE FROM bands WHERE id = %(id)s;"
        connectToMySQL("belt_schema").query_db(query, data)


# Validates data from the band section.
    @staticmethod
    def band_validator(data):
        is_valid = True
        if len(data["band_name"]) <= 3:
            flash("Name must be at least 3 characters")
            is_valid = False
        if len(data["music_genre"]) <= 3:
            flash("Music Genre must be at least 3 characters")
            is_valid = False
        if len(data["home_city"]) <= 3:
            flash("Home City must be at least 3 characters")
            is_valid = False
        return is_valid