# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 13:11:56 2018

@author: hwaln
"""

import csv
import pandas as pd
import os

reaDir=os.path.join(os.path.dirname(__file__), '../resources/')
meaTypes=pd.read_csv(reaDir+'measurement_types.csv', sep=';', index_col='description_short')
metaData=pd.read_csv(reaDir+'metadata.csv', sep=';', index_col='description_short', encoding="ISO-8859-1")
metaDataNaNs=['nan', '', 'Unknown', 'Ukn']

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def getTreaCsvMetaData(fname):
    """
    Read metadata from Treasure standard file

    Parameters
    ----------
    fname : string
        filename for datafile to read

    Returns
    -------
    d : dict
        Dictionary with metadata

    """
    d={}
    with open(fname, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        row = next(reader)
        d[row[0]]=row[1]
        nrow = int(row[1])
        for i, row in enumerate(reader):
            if i>(nrow-1):
                break
            if not row:
                break
            #k, v = row
            #d[k] = v
            d[row[0]]=row[1]
        return d

def getTreaCsvTimeSeries(fname, meta):
    """
    Get time sereies data from Treasure standard file

    Parameters
    ----------
    fname : string
        filename for datafile to read
    meta : dict
        Dictionary with metadata

    Returns
    -------
    df : Pandas dataframe
        Dataframe with time series

    """
    hrow = int(meta[list(meta)[0]])
    try:
        df = pd.read_csv(fname, index_col=0, skiprows=hrow-1, sep=';')
    except:
        df = pd.read_csv(fname, index_col=0, skiprows=hrow-1, sep=';', encoding = 'ISO-8859-1')
    if 'timestamp_format' in meta.keys():
        df.index=pd.to_datetime(df.index, format=meta['timestamp_format'])
    else:
        try:
            df.index=pd.to_datetime(df.index, format='%d.%m.%Y %H:%M')
        except ValueError:
            print('Warning: timestamp format not standard. Trying day first')
            df.index=pd.to_datetime(df.index, format='%Y.%m.%d %H:%M')
    if 'time_zone' in meta.keys():
        df.index=df.index.tz_convert(meta['time_zone'])
        if not meta['time_zone']=='Etc/Gmt-1':
            print(f'Warning: {fname} time_zone not standard. Check')
    else:
        print(f'Warning: {fname} time_zone not defined. Check')
    return df

def getTreaCsv(fname):
    """
    get metadata and timeseries from Treasure datafile

    Parameters
    ----------
    fname : string
        filename for datafile to read

    Returns
    -------
    d : dict
        Dictionary with metadata
    df : Pandas dataframe
        Dataframe with time series
    """
    d = getTreaCsvMetaData(fname)
    df = getTreaCsvTimeSeries(fname,d)
    return d, df

def readAllcsvsFromFolder(directory, ext='txt'):
    """
    Read all Treasure datafiles from a specified directory

    Parameters
    ----------
    directory : string
        path to directory
    ext : string, optional
        file extension for datafiles. The default is 'txt'.

    Returns
    -------
    Mdict : dict
        dictionary with metadata dictionaries for each file.
    Bdict : dict
        dictionary with timesereis for each file.

    """
    Mdict = {}
    Bdict = {}
    for filename in os.listdir(directory):
        if filename.endswith('.'+ext):
            print('reading file: '+ filename)
            key=filename.split('.')[0]
            path=directory if not directory=='.' else ''
            Mdict[key], Bdict[key]=getTreaCsv(path+filename)
    return Mdict, Bdict

def createHeader(df, bid=None):
    """
    Creates a header dataframe for the standard treasure file format

    Parameters
    ----------
    df : Pandas Dataframe
        Dataframe containing timeseries data. column names must be in line with description_short in Treasure.

    Returns
    -------
    header : Pandas Dataframe
        Dataframe with header.

    """
    d={'col0': ['','','']}
    for i,col in enumerate(df.columns):
        if col in meaTypes.index:
            d['col'+str(i+1)]=list(meaTypes.loc[col][['measurement_category', 'unit', 'description']].values)
        else:
            if col.split('_')[0] in meaTypes.index: 
                d['col'+str(i+1)]=list(meaTypes.loc[col.split('_')[0]][['measurement_category', 'unit', 'description']].values)
                print(f'Warning: column {col} is enumerated. Assuming submeter')
            else:
                raise KeyError(f'column {col},{bid} not in allowed measurement types')
    header=pd.DataFrame(d)
    #make sure index has correct name
    df.index.name="TimeStamp"
    return header

def createHeaderDict(d_ts):
    """
    Creates a header dataframe for each dataframe in d_ts

    Parameters
    ----------
    d_ts : dict
        dictionary with timesereis for each file.

    Returns
    -------
    d_head : dict
        dictionary with header for each timeseries.

    """
    d_head={}
    for bid in d_ts.keys():
        d_head[bid]=createHeader(d_ts[bid], bid=bid)
    return d_head

def addHeaderLine(mData):
    hl=len(mData.keys())+6
    mData_new={'Header_line':hl}
    mData_new.update(mData)
    return mData_new

def checkMetaData(bid, mData):
    metaDataLst=list(metaData.index)
    check=True
    for m in mData.keys():
        if not m in metaDataLst:
            print (f'{bid}: {m} is not in metadata list, file not created')
            check = False
    # check header line
    hl=len(mData.keys())+5
    if 'Header_line' in mData.keys():
        if not int(mData['Header_line'])==hl:
            print (f'{bid}: Header line is not correct. Automatically updated')
            mData['Header_line']=hl
    else:
        print (f'{bid}: Header_line not in metadata. Automatically added')
        mData=addHeaderLine(mData)
    return mData, check

def writeTreaCsv(savedir, bid, mData, tsData, tsHeader=None):
    """
    Write treasure datafil

    Parameters
    ----------
    savedir : string
        Path to directory where files should be saved
    bid : string
        Building ID or name of file.
    mData : dict
        Dictionary with metadata
    tsData : Pandas dataframe
        Dataframe with time series
    tsHeader : Pandas dataframe
        Dataframe with header for timeseries. If None, it is automatically generated. Default is None

    Returns
    -------
    None.

    """
    
    #check metadata
    mData, flag = checkMetaData(bid, mData)
    if not flag:
        return
    
    if tsHeader is None:
        tsHeader=createHeader(tsData)
    fname=savedir+bid+'.txt'
    ensure_dir(fname)
    with open(fname, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for key, value in mData.items(): #write header dict
            writer.writerow([key, value])
        csv_file.write('\n') 
        tsHeader.to_csv(csv_file, header=False, index=False, sep=';')
        tsData.to_csv(csv_file, sep=';',date_format='%Y-%m-%dT%H:%M:%S%z')
    return

def writeAllTreaCsv(savedir, mData, tsData, tsHeader=None):
    """
    Write a set of Treasure data files to a folder

    Parameters
    ----------
    savedir : string
        Path to directory where files should be saved
    mData : dict
        dictionary with metadata dictionaries for each file.
    tsData : dict
        dictionary with timeseries for each file.
    tsHeader : dict
        dictionary with header for each timeseries. If None, it is automatically generated. Default is None

    Returns
    -------
    None.

    """
    if tsHeader is None:
        tsHeader=createHeaderDict(tsData)
    for bid in mData.keys():
        writeTreaCsv(savedir, bid, mData[bid], tsData[bid], tsHeader[bid])
    return

def getMeaBuiStatistics(d_meta, d_ts, fields=['All'], skip=[], sortby='building_category'):
    d={}
    for bui in d_meta.keys():
        sort=d_meta[bui][sortby]
        if not sort in d.keys():
            d[sort]={}
        if fields[0]=='All':
            for col in d_ts[bui].columns:
                if not col in skip:
                    col = 'ElImp' if 'ElImp_' in col else col
                    if not col in d[sort].keys():
                        d[sort][col]=0
                    d[sort][col]+=1
        else:
            if len(skip)>0 : print('Warning: skip not applicable for selected columns')
            for col in fields:
                if col in d_ts[bui].columns:
                    if not col in d[sort].keys():
                        d[sort][col]=0
                    d[sort][col]+=1
    return d

def getMeaAreaStatistics(d_meta, d_ts, fields=['All'], skip=[], sortby='building_category'):
    d={}
    for bui in d_meta.keys():
        sort=d_meta[bui][sortby]
        if not sort in d.keys():
            d[sort]={}
        if fields[0]=='All':
            for col in d_ts[bui].columns:
                if not (col in skip or 'ElImp_' in col):
                    if not col in d[sort].keys():
                        d[sort][col]=0
                    try:
                        d[sort][col]+=round(float(d_meta[bui]['floor_area']))
                    except:
                        pass                        
        else:
            for col in fields:
                if len(skip)>0 : print('Warning: skip not applicable for selected columns')
                if col in d_ts[bui].columns:
                    if not col in d[sort].keys():
                        d[sort][col]=0
                    try:
                        d[sort][col]+=round(float(d_meta[bui]['floor_area']))
                    except:
                        pass 
    return d  

def getMeaPointStatistics(d_meta, d_ts, fields=['All'], skip=[], sortby='building_category'):
    d={}
    for bui in d_meta.keys():
        sort=d_meta[bui][sortby]
        if not sort in d.keys():
            d[sort]={}
        if fields[0]=='All':
            for col in d_ts[bui].columns:
                if not col in skip:
                    col_ = 'ElImp' if 'ElImp_' in col else col
                    if not col_ in d[sort].keys():
                        d[sort][col_]=0
                    d[sort][col_]+=d_ts[bui][col].count()
        else:
            for col in fields:
                if len(skip)>0 : print('Warning: skip not applicable for selected columns')
                if col in d_ts[bui].columns:
                    if not col in d[sort].keys():
                        d[sort][col]=0
                    d[sort][col]+=d_ts[bui][col].count()
    return d        

def getAvailableMetaDataStatistics(d_meta, fields=['All'], skip=[], sortby='building_category'):
    d={}
    for bui in d_meta.keys():
        sort=d_meta[bui][sortby]
        if not sort in d.keys():
            d[sort]={}
        if fields[0]=='All':
            for f in d_meta[bui]:
                if not f in skip and d_meta[bui][f] not in metaDataNaNs:
                    if not f in d[sort].keys():
                        d[sort][f]=0
                    d[sort][f]+=1
        else:
            for f in fields:
                if len(skip)>0 : print('Warning: skip not applicable for selected columns')
                if f in d_meta[bui].keys() and d_meta[bui][f] not in metaDataNaNs:
                    if not f in d[sort].keys():
                        d[sort][f]=0
                    d[sort][f]+=1
    return d

def getMetaDataValueStatistics(d_meta, fields, sortby='building_category'):
    fields=[fields]
    d={}
    for bui in d_meta.keys():
        sort=d_meta[bui][sortby]
        if not sort in d.keys():
            d[sort]={f:{} for f in fields}
        for f in fields:
            if f in d_meta[bui].keys() and d_meta[bui][f] not in metaDataNaNs:
                val=d_meta[bui][f]
                if val in d[sort][f].keys():
                    d[sort][f][val]+=1
                else:
                    d[sort][f][val]=1
            else:
                if 'ukn' in d[sort][f].keys():
                    d[sort][f]['ukn']+=1
                else:
                    d[sort][f]['ukn']=1
    return d
        
        