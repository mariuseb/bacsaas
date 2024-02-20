# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 08:32:29 2018

@author: hwaln
"""

"""

This program shows how to retrieve a time series of observations from the following
combination of source, element and time range:

source:     SN18700
element:    mean(wind_speed P1D) see: https://frost.met.no/elementtable
startDate: 2010-04-01 
endDate:   2010-05-31

a personal client_id must be generated at: https://frost.met.no/auth/requestCredentials.html

"""


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
        df=pd.DataFrame(lst, columns=cols)
        df.set_index('Time', inplace=True)
        df.index=pd.to_datetime(df.index)
        return df
        
    else:
        print('error in: {} {} \n'.format(station, element))
        print('\tstatus code: {}\n'.format(r.status_code))
        if 'error' in r.json():
            assert(r.json()['error']['code'] == r.status_code)
            print('\tmessage: {}\n'.format(r.json()['error']['message']))
            print('\treason: {}\n'.format(r.json()['error']['reason']))
        else:
            print('\tother error\n')
        return -1
    
def getNearestStation(long, lat, client_id=CLIENTID):
    location = 'nearest(POINT('+str(long)+ ' ' + str(lat)+'))'
    r = requests.get(
        'https://frost.met.no/sources/v0.jsonld',
        {'types': 'SensorSystem', 'geometry': location, 'stationholder':'*'},
        auth=(client_id, '')
    )
    if r.status_code == 200:
        sid=r.json()['data'][0]['id']
    else:
        print('error in: {} {} \n'.format(long, lat))
        print('\tstatus code: {}\n'.format(r.status_code))
        if 'error' in r.json():
            assert(r.json()['error']['code'] == r.status_code)
            print('\tmessage: {}\n'.format(r.json()['error']['message']))
            print('\treason: {}\n'.format(r.json()['error']['reason']))
        else:
            print('\tother error\n')
        return -1
    
    return sid

def getStationInfoFromId (station, client_id=CLIENTID):
    r = requests.get(
        'https://frost.met.no/sources/v0.jsonld',
        {'types': 'SensorSystem', 'ids': station},
        auth=(client_id, '')
        )
    return r

def getStationInfoFromName (name, client_id=CLIENTID):
    r = requests.get(
        'https://frost.met.no/sources/v0.jsonld',
        {'types': 'SensorSystem', 'name': name},
        auth=(client_id, '')
        )
    return r

def getAvailableTimeSeriesFromId (station, client_id=CLIENTID):
    r = requests.get(
        'https://frost.met.no/observations/availableTimeSeries/v0.jsonld',
        {'referencetime' : '2017-01-01', 'sources': station},
        auth=(client_id, '')
        )
    return r
