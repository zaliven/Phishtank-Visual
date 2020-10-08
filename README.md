# Phishtank Visual
## Overview 
This project implements the Phishtank api to build a simple ETL pipeline to fetch data every 8 hours into an ElasticSearch database. Afterwards, it visualizes Matplotlib plots to display different statistics from the database.


## Files
```
application.py - Backend for the application, built on Flask. Handles GET requests, updates the database and draws plots.

dataprocess.py - Processes and transforms the data received from Phishtank's api.

visualizer.py - Receives a pandas dataframe and utilizes Matplotlib to build plots.
``` 

## Demonstration
Available at https://zaliven.github.io/Phishtank-Visual/


