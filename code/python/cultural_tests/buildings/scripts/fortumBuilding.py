# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 09:39:59 2018

@author: hwaln
"""

import pandas as pd
import matplotlib.pyplot as plt
import metdata as met
import csv as csv
import datetime
import buildingdata.lib.zenCSV as zen
import numpy as np

#get data
fname = '../../Data/Fortum/ZENcsv/b50.csv'
df=zen.getZENcsvTimeSeries(fname,17)

#add date information
def addDateInfo (df):
    df['tday']=df.index.hour
    #add weekend (=0) and not weekend (=1) info
    df['WorkingDay']=(df.index.dayofweek<5).astype(int)
    df['Season']=df.index.map(get_season)
    return df

def get_season(date):
    Y = 2017
    seasons = {'Summer':(pd.datetime(Y,6,1), pd.datetime(Y,9,1)),
               'Autumn':(pd.datetime(Y,9,1), pd.datetime(Y,12,1)),
               'Spring':(pd.datetime(Y,3,1), pd.datetime(Y,6,1))}
    date=date.replace(year=Y)
    for season,(season_start, season_end) in seasons.items():
        if date>=season_start and date<= season_end:
            return season
    else:
        return 'Winter'    
    

def get_seasonID(date):
    Y = 2017
    seasons = {3:(pd.datetime(Y,6,1), pd.datetime(Y,9,1)),
               4:(pd.datetime(Y,9,1), pd.datetime(Y,12,1)),
               2:(pd.datetime(Y,3,1), pd.datetime(Y,6,1))}
    date=date.replace(year=Y)
    for season,(season_start, season_end) in seasons.items():
        if date>=season_start and date<= season_end:
            return season
    else:
        return 1

def splitSeasons(df):
    df_W = df.loc[df.Season == 'Winter']
    df_S = df.loc[df.Season == 'Summer']
    df_M = df.loc[(df.Season != 'Winter') & (df.Season != 'Summer')]
    return df_W, df_S, df_M

def plotSepWeekdayLines (v1, name, unit, err=False):
    linew=0.5
    #fname = v1.name.split('[')[0]+'SepWeekdayLines'
    cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df=v1.to_frame(v1.name)
    df['Weekday'] = df.index.weekday_name
    df['Weekday']=pd.Categorical(df['Weekday'],categories = cats)
    if err:
        mean = df.groupby([df.index.time, 'Weekday'])[v1.name].mean().unstack()
        err = df.groupby([df.index.time, 'Weekday'])[v1.name].std().unstack()
        ax=mean.plot(lw=linew,subplots=True, sharex=True, sharey=True, yerr=err, capsize=4)
    else:
        df = df.groupby([df.index.time, 'Weekday'])[v1.name].mean().unstack()
        ax=df.plot(lw=linew,subplots=True, sharex=True, sharey=True)
    plt.xticks(np.arange(0,86400,7200))
    #plt.figure().autofmt_xdate()
    for sp in ax.flat:
        sp.set_ylabel(unit)    #ax.layout(3,3)
    return;

def plotSepWorkingDayLines (v1, name, unit, err=False):
    linew=0.5
    df=v1.to_frame(v1.name)
    df['WorkingDay'] = (df.index.dayofweek<5).astype(int)
    if err:
        mean = df.groupby([df.index.time, 'WorkingDay'])[v1.name].mean().unstack()
        err = df.groupby([df.index.time, 'WorkingDay'])[v1.name].std().unstack()
        ax=mean.plot(lw=linew,subplots=True, sharex=True, sharey=True, yerr=err, capsize=4)
    else:
        df = df.groupby([df.index.time, 'WorkingDay'])[v1.name].mean().unstack()
        ax=df.plot(lw=linew,subplots=True, sharex=True, sharey=True)
    plt.xticks(np.arange(0,86400,7200))
    #plt.figure().autofmt_xdate()
    for sp in ax.flat:
        sp.set_ylabel(unit)    #ax.layout(3,3)
    return;

df=addDateInfo(df)
df_W, df_S, df_M = splitSeasons(df)
