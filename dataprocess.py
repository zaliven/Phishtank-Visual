from datetime import datetime
import re
import pandas as pd
from es_pandas import es_pandas
import gc
import traceback


# Phishtank json and csv outputs are different. json format contains more data (column 'details').
class Dataprocessor:
    def __init__(self, host):
        self.ep = es_pandas(host)
        print("Connected to elasticsearch")

    def process_data(self, url, read_fmt, index):
        # If index exists, import only new results to avoid duplicates
        max_id = self.get_max_id(index)
        df = self.filter_ids(self.read_data(url, read_fmt), max_id)  
        # Extract time related info
        df = df.rename(columns={'verification_time' : 'date'})
        df['date'] = pd.to_datetime(df['date'])
        df['hour'] = df['date'].apply(lambda x: x.strftime("%H"))
        df['date'] = df['date'].apply(lambda x: x.strftime("%Y-%m-%d"))
        df['month'] = df['date'].apply(lambda x: x[:7])

        # Extract domain from url
        df['domain'] = df['url'].apply(lambda x: re.findall("http[s]?://(.*?)(?:$|/)", x)[0])

        columns = ['phish_id', 'url', 'domain', 'target', 'date', 'month', 'hour']
        extra_columns = []
        # Phishtank json format contains extra 'details' column
        if read_fmt == "json":
            df['ip_address'] = df['details'].apply(lambda x: x[0]['ip_address'] if len(x) > 0 else 'Unknown')
            df['country'] = df['details'].apply(lambda x: x[0]['country'] if len(x) > 0 else 'Unknown')
            extra_columns = ['country', 'ip_address']
        return df[columns + extra_columns]


    def read_data(self, url, read_fmt):
        df = pd.DataFrame()
        if read_fmt == "csv":
            df = pd.read_csv(url)
        elif read_fmt == "json":
            df = pd.read_json(url)
        return df


    def get_max_id(self, index):
        max_id = 0
        try:
            df = self.ep.to_pandas(index)
            max_id = df['phish_id'].max()
            print("Importing results with id greater than %s" % max_id)
        except:
            print("Index not found. Creating new index for %s" % index)
            self.ep.es.indices.create(index=index)
        return max_id


    # Function will return a dataframe with phish_id larger than max_id. For new indexes, dataframe will remain unchanged.
    def filter_ids(self, df, max_id):
        return df[df['phish_id'] > max_id]
