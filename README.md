# spotify_API

This Spotify API is pretty simple: 1) This repository takes data from the Spotipy API provided from Spotify, 2) utilizes data requested from Spotify via an email request, 3) transports these tables into an AWS RDS database, and 4) exposes database endpoints using flask. Thus, it provides a template for how you in you project could use Spotify data to analyze your own music tastes! 

A tour through this repository:

A) The Folder RDSPipeline includes a pre-mde API which connects Python to AWS RDS from existing CSVs found in data and from API calls using Spotipy
B) The folder called "data" includes CSVs provided by Spotify via email.
C) The App folder includes an __init__.py file which includes database connections and defines routes for the API, exposing endpoints from AWS. The schema of the database is very simple, since it only includes 5 tables. The API works via localhost, using a simple webrequest:

```
curl -Uri "http://localhost:5000/"
```

