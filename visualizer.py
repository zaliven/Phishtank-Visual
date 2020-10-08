import matplotlib
matplotlib.use('Agg') # Set backend for matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import base64
from io import BytesIO

# Generates base64 for png images of plots
def visualize(df):
    hours = get_hours(df)
    targets = get_top_targets(df)
    domains = get_top_domains(df)
    countries = get_countries_pie(df)
    months = get_months(df)
    days = get_top_days(df)
    return {
        'hours' : hours,
        'targets' : targets,
        'domains' : domains,
        'pie' : countries,
        'months' : months,
        'days' : days
    }


def get_encoded_image():
    tmpfile = BytesIO()
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(6.5, 4)
    fig.savefig(tmpfile, format='png', bbox_inches='tight')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    plt.clf()
    return encoded


def get_hours(df):
    new_df = df.groupby('hour').count()
    hours = [hour for hour, df in new_df.groupby('hour')]
    plt.plot(hours, new_df['target'])
    plt.title('Hourly activity (UTC)')
    plt.xlabel('Hour')
    plt.ylabel('Count of records')
    return get_encoded_image()


def get_top_targets(df):
    exclude_other = df['target'].isin(['Other'])
    top_ten = df[~exclude_other]['target'].value_counts()[:10]
    targets = top_ten.index.tolist()
    values = top_ten.values
    plt.bar(targets, values)
    plt.title('Top 10 targeted companies')
    plt.xticks(targets, rotation='vertical')
    plt.xlabel('Target (Excluding \'Other\' targets)')
    plt.ylabel('Count of records')
    return get_encoded_image()


def get_top_domains(df):
    top_ten = df['domain'].value_counts()[:10]
    domains = top_ten.index.tolist()
    values = top_ten.values
    plt.bar(domains, values)
    plt.title('Top 10 site domains')
    plt.xticks(domains, rotation='vertical')
    plt.xlabel('Domain')
    plt.ylabel('Count of records')
    return get_encoded_image()


def get_countries_pie(df):
    top_ten = df['country'].value_counts()[:10]
    countries = top_ten.index.tolist()
    values = top_ten.values
    plt.pie(values, labels=countries)
    plt.title('Top 10 countries records distribution')
    return get_encoded_image()


def get_months(df):
    df.month.unique()
    top_ten = df.month.value_counts().sort_index(ascending=False)[:20][::-1]
    months = top_ten.index.tolist()
    values = top_ten.values
    plt.plot(months, values)
    plt.xticks(months, rotation='vertical')
    plt.title('Activity over the last 20 months')
    plt.ylabel('Count of records')
    return get_encoded_image()


def get_top_days(df):
    top_ten = df['date'].value_counts()[:10]
    dates = top_ten.index.tolist()
    values = top_ten.values
    plt.bar(dates, values)
    plt.title('Top 10 most active days')
    plt.xticks(dates, rotation='vertical')
    plt.xlabel('Day')
    plt.ylabel('Count of records')
    return get_encoded_image()