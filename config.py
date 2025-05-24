import os

class Config:
    SECRET_KEY = '-#123!G@m3Pl4n3R!-'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gameplanner.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Folder where uploaded images will be saved
    UPLOAD_FOLDER = 'static/images/games'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # Limit: 2MB
