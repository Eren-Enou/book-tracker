import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    DB_USERNAME = 'postgres'
    DB_PASSWORD = 'password'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_NAME = 'book-tracker'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
