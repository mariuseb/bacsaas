# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 09:06:31 2022

@author: hwaln

Scripts for cleaning data series
"""
import numpy as np
import pandas as pd

def cleanEOSDataframe(df, tresh=3, col=None):
    
    if isinstance(col, str): #clean all collumns based on one column
        counter=0
        for day in list(set(df.index.date)):
            s=df.loc[day.strftime('%Y-%m-%d')].copy()
            s['subgroup'] = (s[col] != s[col].shift(1)).cumsum()
            maxCon=s.groupby(list(s.columns)).size().reset_index(name='count')['count'].max()
            if maxCon>=tresh: 
                #print('removing:'+day.strftime('%Y-%m-%d'))
                df.loc[day.strftime('%Y-%m-%d')]=np.nan
                counter+=1
        return df, counter
    else: # clean each column individually
        counter=[]
        if not col:
            col=df.columns
        for i,column in enumerate(col):
            df[column], c = cleanEOSDataSeries(df[column],tresh=tresh)
            counter.append(c)
        return df, counter
        

def cleanEOSDataSeries(ser, tresh=3):
    """
    Method for cleaning EOS data (Energinet/Optima). 
    Based on EOS systems that filles inn missing data with average within the period.
    The script removes the full day if missing data is found

    Parameters
    ----------
    ser : Pandas Series
        Data series for cleaning.
    tresh : Integer, optional
        Number of equal datapoints within one day for removal of day. The default is 3.

    Returns
    -------
    df['col'] : Pandas Series
        Series with cleaned data.
    counter : Integer
        Number of removed days.

    """
    counter=0
    df=ser.to_frame(name='col')
    for day in list(set(df.index.date)):
        s=df.loc[day.strftime('%Y-%m-%d')].copy()
        s['subgroup'] = (s['col'] != s['col'].shift(1)).cumsum()
        maxCon=s.groupby('subgroup').size().reset_index(name='count')['count'].max()
        val=s.iloc[s.groupby('subgroup').size().reset_index(name='count')['count'].idxmax()]['col']
        # if (maxCon>=tresh and val != 0.0) or (maxCon>=23): #remove if number of consecutive equal data points higher than threshold, but not if 0 
        if (maxCon>=tresh and val != 0.0): #remove if number of consecutive equal data points higher than threshold, but not if 0 
            #print('removing:'+day.strftime('%Y-%m-%d'))
            df.loc[day.strftime('%Y-%m-%d')]=np.nan
            counter+=1
    return df['col'], counter     

def removeOutliersDataframe(df, nSTD_tresh=15, preceedingZero='Only'):
    """
    Remove outliers that are outside set number of standard deviations.
    Must be used with care for energy time series which can have large daily and seasonal variations.

    Parameters
    ----------
    df : Pandas Dataframe
        Dataframe for outlier removal.
    nSTD_tresh : INTEGER, optional
        Number of standard deviations to remove outlier. The default is 15.
    preceedingZero : String, optional ['False','Only', 'All'], default is 'Only'
        Check for preceeding zeros. Tyipal for energy measurements
        If ['False']: only remove outlier
        If 'Only': only remove outlier and preceeding zeros if preceeding zero(s)
        If 'All' : remove outlier also without preceeding zero

    Returns
    -------
    None.

    """
    for col in df.columns:
        removeOutliersSeries(df[col], name=col, nSTD_tresh=nSTD_tresh, preceedingZero=preceedingZero)
    return

def removeOutliersSeries(s, name='', nSTD_tresh=15, preceedingZero='Only'):
    """
    Remove outliers that are outside set number of standard deviations.
    Must be used with care for energy time series which can have large daily and seasonal variations.

    Parameters
    ----------
    s : Pandas Series
        Data series for outlier removal.
    name : STRING, optional
        Name of dataseries, used for printing only
    nSTD_tresh : INTEGER, optional
        Number of standard deviations to remove outlier. The default is 15.
    preceedingZero : String, optional ['False','Only', 'All'], default is 'Only'
        Check for preceeding zeros. Tyipal for energy measurements
        If ['False']: only remove outlier
        If 'Only': only remove outlier and preceeding zeros if preceeding zero(s)
        If 'All' : remove outlier also without preceeding zero

    Returns
    -------
    None.

    """
    
    upper=s.mean()+s.std()*nSTD_tresh
    lower=s.mean()-s.std()*nSTD_tresh
    keep=(s>lower) & (s<upper) | (s.isna())
    if preceedingZero in ['Only', 'All']:
        nout=0
        nzero=0
        outliers=s[~keep].index.tolist()
        for o in outliers:
            i=s.index.tolist().index(o)-1
            rem=[i+1]
            val=s.iloc[i]
            while val == 0:
                rem.append(i)
                val=s.iloc[i]
                i = i-1
            if preceedingZero=='All' or len(rem)>1:
                nout+=1
                nzero+=len(rem)-1
                s.iloc[rem]=np.nan
        print(f'{name} removed outliers, zeros: {nout}, {nzero}')
    else:
        nout=s[~keep].count()
        s[~keep]=np.nan
        print(f'{name} removed outliers: {nout}')
    return

def removeDataPointsFromDataframe(df, data_points):
    """
    Remove specific datapoints from dataframe.

    Parameters
    ----------
    df : Pandas Dataframe
        Dataframe for outlier removal.
    data_points : dictionary 
        Dictionary with data points. Timestamp is used as key. 
        Columns should be given as single columns name or list of colum names. 
        If key value is 'All', all columns will be set to nan

    Returns
    -------
    None.

    """
    for key in data_points.keys():
        if 'All' in data_points[key]:
            df.loc[key]=np.nan #set all columns to nan
        else:
            df.loc[key,data_points[key]]=np.nan #set selected columns to nan
    
    return