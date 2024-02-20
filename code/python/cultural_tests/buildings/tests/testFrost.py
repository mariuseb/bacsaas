# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 08:32:29 2018

@author: hwaln
"""

"""

This program shows how to retrieve a time series of observations from the following
combination of source, element and time range:

source:     SN18700
element:    mean(wind_speed P1D)
time range: 2010-04-01 .. 2010-05-31

"""

import sys, os
import requests # See http://docs.python-requests.org/
import pandas as pd

CLIENTID = '359b5239-acab-4d83-b55f-ce3688b9ab4e'

def getMetDataTimeSeries(station, element, startDate, endDate, client_id=CLIENTID):
    
    # issue an HTTP GET request
    r = requests.get(
        'https://frost.met.no/observations/v0.jsonld',
        {'sources': station, 'elements': element, 'referencetime': startDate +'/' + endDate},
        auth=(client_id, '')
    )
    
    # extract the time series from the response
    if r.status_code == 200:
        cols=['Time', element ]
        lst=[]
        for item in r.json()['data']:
            iso8601 = item['referenceTime']
            value = item['observations'][0]['value']
            #print('{} {}\n'.format(iso8601, item['observations'][0]['value']))
            lst.append([iso8601, value])
        df=pd.DataFrame(lst, Columns=cols)
        df.set_index('Time', inplace=True)
        df.index=pd.to_datetime(df.index, format='%d.%m.%Y %H')
        return df
        
    else:
        print('error:\n')
        print('\tstatus code: {}\n'.format(r.status_code))
        if 'error' in r.json():
            assert(r.json()['error']['code'] == r.status_code)
            print('\tmessage: {}\n'.format(r.json()['error']['message']))
            print('\treason: {}\n'.format(r.json()['error']['reason']))
        else:
            print('\tother error\n')
        return -1