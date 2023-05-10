from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, app
from sqlalchemy import create_engine, text
import logging
import os

# Get the PostgreSQL URI from environment variables
uri = os.environ.get('POSTGRES_URI')
# Create a connection to the database
engine = create_engine(uri)
# Initialize Flask application
app = Flask(__name__)
# Initialize SQLAlchemy with the Flask application
db = SQLAlchemy(app)
# Set the logging level to INFO
app.logger.setLevel(logging.INFO)

# Route for the homepage


@app.route('/')
def index():
    print("Hello World")
    return "hello world"

# Route for getting playlist data from the database


@app.route('/playlists', methods=['GET'])
def get_tab1():
    connection = engine.connect()
    result = connection.execute(text("SELECT * FROM playlists"))
    dict_rows = [dict(zip(['id', 'title', 'artist', 'album',
                      'uri'], row)) for row in result.fetchall()]
    connection.close()
    return jsonify(dict_rows)

# Route for getting library data from the database


@app.route('/library', methods=['GET'])
def get_library():
    connection = engine.connect()
    result = connection.execute(text("SELECT * FROM library"))
    dict_rows = [dict(zip(['id', 'date', 'artist', 'album',
                      'uri'], row)) for row in result.fetchall()]
    connection.close()
    return jsonify(result)

# Route for getting streaming history data from the database


@app.route('/streaming_history')
def get_streaming_history():
    connection = engine.connect()
    result = connection.execute(text("SELECT * FROM streaming_history"))
    dict_rows = [dict(zip(['id', 'title', 'artist', 'song',
                      'uri'], row)) for row in result.fetchall()]
    connection.close()
    return jsonify(dict_rows)

# Route for getting top artists data from the database


@app.route('/top_artists')
def get_top_artists():
    connection = engine.connect()
    result = connection.execute(text("SELECT * FROM top_artists"))
    dict_rows = [dict(zip(['id', 'artist', 'num', 'song',
                      'info'], row)) for row in result.fetchall()]
    connection.close()
    return jsonify(dict_rows)

# Route for getting top tracks data from the database


@app.route('/top_tracks')
def get_top_tracks():
    connection = engine.connect()
    result = connection.execute(text("SELECT * FROM top_tracks"))
    r = result.fetchall()
    dict_rows = [dict(zip(['index', 'song', 'artist', 'album',
                      'uri', 'playlist'], row)) for row in result.fetchall()]
    connection.close()
    return jsonify(dict_rows)
