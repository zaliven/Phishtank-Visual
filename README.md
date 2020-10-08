# Phishtank Visual
## Overview 
This project implements the Phishtank API to build a simple ETL pipeline to fetch data every 8 hours into an ElasticSearch database. Afterwards, it visualizes Matplotlib plots to display different statistics from the database.


## Files
```
application.py - Backend for the application, built on Flask. Handles GET requests, updates the database and draws plots.

dataprocess.py - Processes and transforms the data received from Phishtank's api.

visualizer.py - Receives a pandas dataframe and utilizes Matplotlib to build plots. Converts plot images to base64 and sends them back to the main application.

plot.ipynb - A jupyter notebook to analyse the dataset before loading
``` 

## ETL Pipeline
    
1.  Read data from Phishtank
  
    The script reads data from Phishtank's API. It processes only new data, of logs with '_phish_id'
    greater than the maximum '_phish_id'
    in the database.
    
2.  Process data using Pandas
    
    Transforms them to create five fields listed below :
    -   _phish_id, date, month, hour, url, domain, target, ip_address, country
    
3.  Load it back to ElasticSearch

## External python libraries used
- Pandas
- Matplotlib
- APScheduler
- es_pandas

![Imgur](https://i.imgur.com/vLyITl2.png)

## Demonstration
Available at https://zaliven.github.io/Phishtank-Visual/


