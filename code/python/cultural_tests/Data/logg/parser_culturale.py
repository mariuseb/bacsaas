# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 07:33:53 2023

@author: hwaln
"""

import pandas as pd
import os
import numpy as np
import buildings.lib.metNWP as met

new_data_dir = "./recieved/"
parsed_data_dir = "./parsed/"

digital_tags = ['LZ', 'SC']

Location={'lan':10,
          'lon':59}

def convert_to_datetime(index):
    index = pd.to_datetime(index, format="%Y-%m-%dT%H:%M", utc=True)
    return index

def concatTags(df):
    tags = sorted(set(df[1]))
    dfs = []
    d_tags = []
    for t in tags:
        if any(x in t.split('_')[4] for x in digital_tags):
            # Store at take digital tags after analog
            d_tags.append(t)
        else:
            d = df[df[1] == t].copy()
            d.index = convert_to_datetime(d[2])
            name = '_'.join(t.split('_')[1:])
            try:
                dfs.append(d[3].rename(f"{name}").resample('5T').nearest(limit=1))
            except Exception as e:
                print(f'Failed to resample {t}, {e}')
    for t in d_tags:
        d = df[df[1] == t].copy()
        d.index = convert_to_datetime(d[2])
        name = '_'.join(t.split('_')[1:])
        # add top and bottom row
        # get start and end of measurement period
        start = int(not bool(d[3].iloc[0]))  # time series start with oposite of first measured value
        end = d[3].iloc[-1]  # time series ends with same as last measured value
        boarders = pd.Series(index=dfs[0].index[[0, -1]], name=t, data=[start, end])
        d = pd.concat([boarders, d[3]], ignore_index=False).sort_index()
        try:
            dfs.append(d.rename(f"{name}").resample('1S').ffill().resample('5T').mean())
        except Exception as e:
            print(f'Failed to resample {t}, {e}')

    dfTot = pd.concat(dfs, axis=1)
    dfTot.index = dfTot.index.tz_convert("Etc/Gmt-1")
    return dfTot

def get_weather_data:
    
     df, e=met.getLocationsWeatherData(location, 
                                       fromTime=fromTimes[i], toTime=toTimes[i],
                                       tz=tz, store=True, name=year)

def parse_new_files(save=True, move=True):
    files = os.listdir(new_data_dir)
    dfs = []
    for f in files:
        if '.csv' in f:
            dfs.append(pd.read_csv(new_data_dir+f, sep=";", header=None))
    df = pd.concat(dfs, ignore_index=True)
    dfTot = concatTags(df)
    if save:
        name=f'{dfTot.index[0].strftime("%Y%m%d")}_{dfTot.index[-1].strftime("%Y%m%d")}'
        dfTot.to_csv(f'{parsed_data_dir}{name}.csv', sep=';')
    if move:
        # move imported file to imported folder
        for f in files:
            os.rename(new_data_dir+f, f"{new_data_dir}treated/{f}")
