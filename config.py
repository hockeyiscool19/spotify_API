
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration settings for Flask app
DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRES_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False
