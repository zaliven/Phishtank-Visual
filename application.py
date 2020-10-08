from flask import Flask, render_template
import os
import time
from datetime import datetime
from es_pandas import es_pandas
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from dataprocess import Dataprocessor
from visualizer import visualize
import traceback

project_root = os.path.dirname(__file__)
application = app = Flask(__name__, template_folder=project_root)
app.config['TEMPLATES_AUTO_RELOAD'] = True

elastic_host = "<ELASTICSEARCH_HOST>"
url = "http://data.phishtank.com/data/<API_KEY>/online-valid.json" # Phishtank API
es_index = "phishtank" # ElasticSearch index
dp = Dataprocessor(elastic_host) # ElasticSearch client and data processing functions

plotlib_images = ""
last_update = datetime.now().strftime("%H:%M - %b %d, %Y")

@app.route('/')
def index():
    return render_template("templates/index.html", mtplb=plotlib_images, time=last_update)


def post_to_elastic(df):
    dp.ep.to_es(df, es_index)


def update_database():
    print("Importing database")
    new_df = dp.process_data(url, read_fmt=url.split(".")[3], index=es_index) # Get new data to push to database
    post_to_elastic(new_df)


def update_index_page():
    global plotlib_images
    df = dp.ep.to_pandas(es_index)
    plotlib_images = visualize(df)

def job():
    global last_update
    try:
         update_database()
    except Exception as e:
        print("Error while updating database: ", e)
        print(traceback.format_exc())
    else:
        print("Updating plots")
        update_index_page()
        last_update = datetime.now().strftime("%H:%M - %b %d, %Y")
    finally:
        print("Finished running job - ", time.strftime("%d. %B %Y %I:%M:%S %p"))

job()
scheduler = BackgroundScheduler()
scheduler.add_job(func=job, trigger="interval", hours=8)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
