
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration settings for Flask app
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:4Hockeyiscold*@spotify.coacb9cwipmh.us-east-1.rds.amazonaws.com:5432/postgres'
SQLALCHEMY_TRACK_MODIFICATIONS = False
