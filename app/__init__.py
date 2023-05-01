from authlib.oauth2.rfc6750 import BearerTokenValidator
from authlib.integrations.flask_oauth2 import ResourceProtector, current_token
from flask import Flask, jsonify, request, redirect, url_for, session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, app, url_for
from sqlalchemy import create_engine, text
from flask_oauthlib.client import OAuth, OAuthException, redirect
import requests
import logging


uri = 'postgresql://postgres:4Hockeyiscold*@spotify.coacb9cwipmh.us-east-1.rds.amazonaws.com:5432/postgres'
engine = create_engine(uri)

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

app.logger.setLevel(logging.INFO)


#####################################################

# require_oauth = ResourceProtector()

# app.secret_key = 'stuff'  # Replace with your own secret key

# # At the beginning of your Flask app
# ALLOWED_USERS = ['user1@example.com', 'user2@example.com']

# # In the CustomBearerTokenValidator class


# class CustomBearerTokenValidator(BearerTokenValidator):

#     def authenticate_token(self, token_string):
#         # Query Spotify API to get user information
#         headers = {'Authorization': f'Bearer {token_string}'}
#         response = requests.get('http://127.0.0.1:5000', headers=headers)
#         app.logger.info(f'{response}', request.method, request.url)
#         if response.status_code == 200:
#             # If the response is 200 OK, the token is valid
#             user_data = response.json()

#             # Check if the user's email is in the list of allowed users
#             if user_data['email'] in ALLOWED_USERS and token_string == "123456789":
#                 return {'user_id': user_data['id'], 'access_token': token_string}
#             else:
#                 return None
#         else:
#             return None

#     def request_invalid(self, request):
#         return False

#     def token_revoked(self, token):
#         return False

#####################################################


@app.route('/', methods=['GET'])
def hello_world():
    print("You have gotten access!!!")


@app.route('/playlists', methods=['GET'])
def get_tab1():
    connection = engine.connect()
    result = connection.execute(text("SELECT * FROM playlists"))
    dict_rows = [dict(zip(['id', 'title', 'artist', 'album',
                      'uri', 'playlist'], row)) for row in result.fetchall()]
    connection.close()
    return jsonify(dict_rows)


@app.route('/library', methods=['GET'])
def get_library():
    connection = engine.connect()
    result = connection.execute(text("SELECT * FROM library"))
    connection.close()
    return jsonify(result)


@app.route('/streaming_history')
def get_streaming_history():
    connection = engine.connect()
    result = connection.execute(text("SELECT * FROM streaming_history"))
    connection.close()
    return jsonify(result)


@app.route('/top_artists')
def get_top_artists():
    connection = engine.connect()
    result = connection.execute(text("SELECT * FROM top_artists"))
    connection.close()
    return jsonify(result)


@app.route('/top_tracks')
def get_top_tracks():
    connection = engine.connect()
    result = connection.execute(text("SELECT * FROM top_tracks"))
    connection.close()
    return jsonify(result)
