#from ast import Param
from ocp.param_est import ParameterEstimation
import numpy as np
import json
import casadi as ca
import ocp.dae as dae
import ocp.integrators as integrators
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint
from matplotlib import rc
from ocp.tests.utils import get_opt_config_path, get_data_path
import os
# text:
rc('mathtext', default='regular')
# datetime:
#plt.rcParams["date.autoformatter.minute"] = "%Y-%m-%d %H:%M"
import matplotlib.dates as mdates
import stats
import analyse
import requests
from pprint import pprint

if __name__ == "__main__":
    
    #df = analyse.concat_log()
    df = pd.read_csv("parsed/20230227_20230305.csv", sep=";")
    df.index = pd.to_datetime(df["2"])
    #analyse.plot_apt(df, apt='H0101', freq='5T', acc=True)
    analyse.plot_agg_apt(df, analyse.second_floor, freq='5T', acc=False)
    plt.show()
    #print("yes")
    
    # get weather data
    client_id = '481d59ad-3a8d-433e-9553-50f1ae36a064' 
    client_secret = '37c1a755-f2be-42f8-b858-2fa7f433ca0e'
    endpoint = 'https://frost.met.no/observations/availableTimeSeries/v0.jsonld'
    #endpoint = 'https://frost.met.no/observations/v0.jsonld'
    #endpoint = 'https://frost.met.no/sources/v0.jsonld'
    #parameters = {
    #    'sources': 'SN18700,SN90450',
    #    'elements': 'mean(air_temperature P1h)',
    #    'referencetime': '2023-02-01/2023-02-02',
    #}
    parameters = {
        'sources': 'SN19428',
        #'elements': 'mean(air_temperature P1H)',
        'referencetime': '2023-02-01/2023-02-02',
    }
    # Issue an HTTP GET request
    r = requests.get(endpoint, parameters, auth=(client_id,''))
    # Extract JSON data
    json = r.json()
    if r.status_code == 200:
        data = json['data']
        print('Data retrieved from frost.met.no!')
    else:
        print('Error! Returned status code %s' % r.status_code)
        print('Message: %s' % json['error']['message'])
        print('Reason: %s' % json['error']['reason'])
        
    df = pd.DataFrame()
    #sources = dict()
    avail = dict()
    for i in range(len(data)):
        #sources[i] = data[i]
        avail[i] = {
                    "name": data[i]["elementId"],
                    "time_res": data[i]["timeResolution"]
                    }
        #row = pd.DataFrame(data[i]['observations'])
        #row['referenceTime'] = data[i]['referenceTime']
        #row['sourceId'] = data[i]['sourceId']
        #df = df.append(row)
    pprint(avail)
    df = df.reset_index()
    # These additional columns will be kept
    columns = ['sourceId','referenceTime','elementId','value','unit','timeOffset']
    df2 = df[columns].copy()
    # Convert the time value to something Python understands
    df2['referenceTime'] = pd.to_datetime(df2['referenceTime'])
    df2.head()