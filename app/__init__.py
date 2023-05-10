# from authlib.oauth2.rfc6750 import BearerTokenValidator
# from authlib.integrations.flask_oauth2 import ResourceProtector
# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask, jsonify, app
# from sqlalchemy import create_engine, text
# import requests
# import logging
# from flask_limiter import Limiter


# uri = 'postgresql://postgres:4Hockeyiscold*@spotify.coacb9cwipmh.us-east-1.rds.amazonaws.com:5432/postgres'
# engine = create_engine(uri)
# app = Flask(__name__)
# app.config.from_object('config')
# db = SQLAlchemy(app)
# app.logger.setLevel(logging.INFO)


# #####################################################

# # $headers = @{ 'Authorization' = 'Bearer 123456789' }
# # Invoke-WebRequest -Uri 'http://localhost:5000/' -Headers $headers


# from flask import Flask, redirect, request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import Flow
# from googleapiclient.discovery import build

# client_secrets_file = r'app\auth.json'
# flow = Flow.from_client_secrets_file(
#     client_secrets_file,
#     scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'],
#     redirect_uri='http://localhost:5000/google/callback')


# #####################################################


# @app.route('/')
# def index():
#     print("Hello World")
#     return "hello world"


# @app.route('/playlists', methods=['GET'])
# def get_tab1():
#     connection = engine.connect()
#     result = connection.execute(text("SELECT * FROM playlists"))
#     dict_rows = [dict(zip(['id', 'title', 'artist', 'album',
#                       'uri'], row)) for row in result.fetchall()]
#     connection.close()
#     return jsonify(dict_rows)


# @app.route('/library', methods=['GET'])
# def get_library():
#     connection = engine.connect()
#     result = connection.execute(text("SELECT * FROM library"))
#     dict_rows = [dict(zip(['id', 'date', 'artist', 'album',
#                       'uri'], row)) for row in result.fetchall()]
#     connection.close()
#     return jsonify(result)


# @app.route('/streaming_history')
# def get_streaming_history():
#     connection = engine.connect()
#     result = connection.execute(text("SELECT * FROM streaming_history"))
#     dict_rows = [dict(zip(['id', 'title', 'artist', 'song',
#                       'uri'], row)) for row in result.fetchall()]
#     connection.close()
#     return jsonify(dict_rows)


# @app.route('/top_artists')
# def get_top_artists():
#     connection = engine.connect()
#     result = connection.execute(text("SELECT * FROM top_artists"))
#     dict_rows = [dict(zip(['id', 'artist', 'num', 'song',
#                       'info'], row)) for row in result.fetchall()]
#     connection.close()
#     return jsonify(dict_rows)


# @app.route('/top_tracks')
# def get_top_tracks():
#     connection = engine.connect()
#     result = connection.execute(text("SELECT * FROM top_tracks"))
#     r = result.fetchall()
#     dict_rows = [dict(zip(['index', 'song', 'artist', 'album',
#                       'uri', 'playlist'], row)) for row in result.fetchall()]

#     connection.close()
#     return jsonify(dict_rows)


from flask import Flask, redirect, request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

app = Flask(__name__)

access_token = '123456789'


@app.route('/')
def index():
    credentials = Credentials.from_authorized_user_info(
        info=request.authorization)
    if not credentials:
        credentials = Credentials.from_authorized_user_info(
            info={'access_token': access_token})

    # Use the credentials to call the Google APIs
    service = build('calendar', 'v3', credentials=credentials)
    events = service.events().list(calendarId='primary').execute()

    # Return a response to the user
    return f'Hello, {events["summary"]}!'


if __name__ == '__main__':
    app.run()
