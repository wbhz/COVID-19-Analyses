import json
import requests
from os import makedirs
from os.path import join, exists
from datetime import date, timedelta
from pprint import pprint
import pandas as pd
import numpy as np
from time import sleep


def guardian_download():  # Adapted from https://gist.github.com/dannguyen/c9cb220093ee4c12b840

    MY_API_KEY = 'be75bbfd-b802-48bc-b2c6-3dcd9b1b80e5'
    API_ENDPOINT = 'http://content.guardianapis.com/search?q=coronavirus%20OR%20covid'
    my_params = {
        'from-date': "2020-01-01",
        'to-date': "2020-04-01",
        'order-by': "newest",
        'show-fields': 'webTitle',
        'page-size': 200,  # Max page size
        'api-key': MY_API_KEY
    }

    start_date = date(2020, 1, 1)
    end_date = date(2020, 4, 30)
    dayrange = range((end_date - start_date).days + 1)

    df = pd.DataFrame()

    for day in dayrange:
        dt = start_date + timedelta(days=day)
        datestr = dt.strftime('%Y-%m-%d')

        print("Downloading", datestr)
        all_results = []
        my_params['from-date'] = datestr
        my_params['to-date'] = datestr
        current_page = 1
        total_pages = 1
        while current_page <= total_pages:
            print("...page", current_page)
            my_params['page'] = current_page
            response = requests.get(API_ENDPOINT, my_params)
            data = response.json()
            temp = pd.json_normalize(data['response']['results'])
            df = df.append(temp, ignore_index=True)

            # if there is more than one page
            current_page += 1
            total_pages = data['response']['pages']

        sleep(0.5)  # Reduce load

    return df


guardian_df = guardian_download()

len(guardian_df)
guardian_df.to_csv('guardian_covid.csv')
