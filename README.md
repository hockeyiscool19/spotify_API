# spotify_API

This Spotify API is pretty simple: 1) This repository takes data from the Spotipy API provided from Spotify, 2) utilizes data requested from Spotify via an email request, 3) transports these tables into an AWS RDS database, and 4) exposes database endpoints using flask. Thus, it provides a template for how you in you project could use Spotify data to analyze your own music tastes! 


How to make a request:


```
$headers = @{
    'Authorization' = 'Bearer 123456789'
}
curl -Uri "http://localhost:5000/" -Headers $headers


```
