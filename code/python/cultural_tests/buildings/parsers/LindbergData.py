# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 09:12:09 2018

@author: hwaln
"""

import pandas as pd
import matplotlib.pyplot as plt
import buildingdata.lib.metdata as met
import csv as csv
import datetime
import os
from geopy.geocoders import Nominatim
import numpy as np


def readDataFile(filename):
    print(filename)
    if filename.endswith('.xlsx'):
        df=pd.read_excel(filename, sheet_name=0, header=(0)) #get input array from excel file via Pandas
        df['T']=pd.to_numeric(df['T'], errors='coerce')
        df['W']=pd.to_numeric(df['W'], errors='coerce')
        df['eloriginal']=pd.to_numeric(df['eloriginal'], errors='coerce')
        df['horiginal']=pd.to_numeric(df['horiginal'], errors='coerce')
    else:
        dtype={'dato' : str,
               'T' : np.float64, 
               'W' : np.float64,
               'eloriginal' : np.float64,
               'horiginal' : np.float64}
        df=pd.read_csv(filename, header=([0]), sep='\t', decimal=',', na_values=[' ', 'x', 'verdi mangler'], thousands='.', dtype=dtype)
    #df['TimeStamp']=pd.to_datetime(df.dato, format='d%.m%.Y%')+pd.to_timedelta(df.hr-1, unit='h')
    df.dropna(how='all',  inplace=True)
    df.rename(columns=lambda x: x.strip(), inplace=True)
    if isinstance(df.dato.iloc[0], datetime.date):
        firstDate=df.dato.iloc[0]
    elif isinstance (df.dato.iloc[0],str):
        firstDate=pd.to_datetime(df.dato.iloc[0], format='%d.%m.%Y')
    else:
        firstDate=pd.to_datetime(str(int(df.dato.iloc[0])).zfill(8), format='%d%m%Y')
    df['TimeStamp']=pd.date_range(firstDate, periods=len(df.index), freq='H')
    df.index=df.TimeStamp
    df.index=df.index.tz_localize('Etc/GMT-1', ambiguous='infer') 
    df.index=df.index.tz_convert('Europe/Oslo')
    df.index = df.index.tz_localize(None)
    return df


def genCsvFromAllFilesInFolder(directory, btype, btypeShort, skip=0):
    i=1
    for filename in os.listdir(directory):
        df=readDataFile(directory+filename)
        location = filename.split('_')[1]
        location = location.split('.')[0]
        createBuildingZENCSV(df, btype, location, filename)
        i+=1
    return temperrlist, locerrlist


def createMetaDataDict(btype, location, df):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    d={'Header_line' : 20,
       'File owner': 'Karen Lindbeg @sintef byggforsk',
       'Data Source' : 'Karen Lindberg Phd',
       'Last update' : now,
       'Location' : location,
       'Weather data' : 'Local',
       'Name building' : 'Unknown',
       'Year of construction' : 'Unknown' if not 'constrYr' in df.columns else 'Unknown' if pd.isnull(df['constrYr'].values[0]) else int(df['constrYr'].values[0]),
       'Floor area [m2]' : 'Unknown' if not 'sqmHeat' in df.columns else 'Unknown' if pd.isnull(df['sqmHeat'].values[0]) else df['sqmHeat'].values[0],
       'Number of units' : 'Unknown' if not nUnitsDict[btype] else 'Unknown' if not nUnitsDict[btype] in df.columns else df[nUnitsDict[btype]].values[0],
       'Building type': btype,
       'Energy efficicency standard' : 'Unknown' if not 'eLabel' in df.columns else 'Unknown' if pd.isnull(df['eLabel'].values[0]) else df['eLabel'].values[0],
       'Timestamp format' : '%d.%m.%Y %H:%M',
       'Time zone' : 'Europe/Oslo',
       'Daylight saving time':1}
    if d['Floor area [m2]']=='Unknown': 
        d['Floor area [m2]']='Unknown' if not 'sqm' in df.columns else 'Unknown' if pd.isnull(df['sqm'].values[0]) else df['sqm'].values[0]
    return d

def createMetaDataHeader():
    d={'col0': ['','',''],
       'col1': ['Weather variable', 'C', 'Temperature Outdoor'],
       'col2': ['Weather variable', 'm/s', 'Wind_speed'],
       'col3': ['Electricity use', 'kWh', 'Electricity Total'],
       'col4': ['Heat use', 'kWh', 'Heat Total'],
       }
    df=pd.DataFrame(d)
    return df

def creatBuildingDataDf(df):
    df_D=df[['T', 'W', 'eloriginal', 'horiginal']]
    df_D.columns=['Tout', 'WindSpd', 'ElTot', 'HtTot']
    #df_D['Tout']=[x.replace(',','.') for x in df_D['Tout']]
    #df_D['Tout']=df_D['Tout'].astype(float) 
    #df_D[['Tout', 'WindSpd', 'ElTot', 'HtTot']]=[x.replace(',','.') for x in df_D[['Tout', 'WindSpd', 'ElTot', 'HtTot']]]
    #df_D[['Tout', 'WindSpd', 'ElTot', 'HtTot']]=df_D[['Tout', 'WindSpd', 'ElTot', 'HtTot']].astype(float)  
    return df_D

def getEfficiencyLevel(filename):
    es='R'
    try:
        bnr=int(filename.split('_')[0][-2:])
        if bnr>59:
            es='E'
    except:
        print('not able to reed filenumber for efficiency category')
    return es

def getProgNr(bid):
    fileLst=os.listdir(savedir)
    nmLst=[]
    for fname in fileLst:
        if fname.startswith(bid): nmLst.append(fname.split('_')[1])
    if not nmLst:
        nextNumber=1
    else:
        nmLst.sort()
        nextNumber=int(nmLst[-1])+1
    progNr=str(nextNumber).zfill(4)
    return progNr

def getBid(df, dMeta, btype, filename):
    btypedict={'Apartment Block':'1-Apt-xxx', 
                'Kindergarten':'6-Kdg-xxx', 
                'Comercial Building':'3-Shp-xxx', 
                'Hotel':'5-Htl-xxx', 
                'Sports Facility':'6-Cus-xxx', 
                'Shopping Mal':'3-Shp-Mal', 
                'Office':'3-Off-xxx', 
                'Cultural Building':'6-Cus-xxx', 
                'School':'6-Sch-xxx', 
                'Single Family House':'1-Hou-xxx', 
                'Apartment':'1-Apt-Sng', 
                'Nursing Home':'7-Nsh-xxx', 
                'Hospital':'7-Hsp-xxx', 
                'University, Collage':'6-Uni-xxx'}
    bid=btypedict[btype]
    bid = bid + '_' + getProgNr(bid)
    bid = bid+'_' + getEfficiencyLevel(filename)
    return bid

def getSummaryDict(df, dM, bid, filename):
    d={}
    d['bTypeId']=bid.split('_')[0]
    d['bEnum']='_'.join(bid.split('_')[1:4])
    d['fname']=filename
    d['Year']=dM['Year of construction']
    d['Area']=dM['Floor area [m2]']
    d['sumHeat']=df['HtTot'].mean()*365*24 #assuming representative period
    d['peakHeat']=df['HtTot'].max()
    d['countHeatNaN']=df['HtTot'].isnull().sum()
    d['countHeatNotZero']=df.HtTot[df.HtTot>0].count()
    d['sumEl']=df['ElTot'].mean()*365*24 #assuming representative period
    d['peakHeat']=df['ElTot'].max()
    d['countHeatNaN']=df['ElTot'].isnull().sum()
    d['countHeatNotZero']=df.ElTot[df.ElTot>0].count()
    return d

def createBuildingZENCSV(df, btype, location, filename):
    df_D=creatBuildingDataDf(df)
    dM=createMetaDataDict(btype, location, df)
    df_H=createMetaDataHeader()
    bid=getBid(df_D, dM, btype, filename)
    sumlist.append(getSummaryDict(df_D, dM, bid, filename))
    fname=savedir+bid+'.txt'
    ensure_dir(fname)
    with open(fname, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for key, value in dM.items(): #write header dict
            writer.writerow([key, value])
        csv_file.write('\n') 
        df_H.to_csv(csv_file, header=False, index=False, sep=';')
        df_D.to_csv(csv_file, sep=';', date_format='%d.%m.%Y %H:%M')
    return

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def genAllCsvFiles(skip=[]):
    basedir = '../../Data/Phd Lindberg/OriginalData/'
    dirlist=['Boligblokk', 'Barnehage', 'Butikk', 'Hotel', 'Idrettsbygning', 'Kjopesenter', 'Kontor', 'Kulturbygning', 'Skole', 'Småhus','Leiligheter', 'Sykehjem', 'Sykehus', 'Universitet og høyskole']
    btypelist=['Apartment Block', 'Kindergarten', 'Comercial Building', 'Hotel', 'Sports Facility', 'Shopping Mal', 'Office', 'Cultural Building', 'School', 'Single Family House', 'Apartment', 'Nursing Home', 'Hospital', 'University, Collage' ]
    btypeShortlist=['AB', 'KG', 'CB', 'HO', 'SF', 'SM', 'OF', 'CL', 'SC', 'SFH', 'AP', 'NH', 'HS', 'UC']
    for i in range(0,len(btypelist)):
        if not btypeShortlist[i] in skip:
            genCsvFromAllFilesInFolder(basedir+dirlist[i]+ '/', btypelist[i], btypeShortlist[i], skip=0)
    return

nUnitsDict={'Apartment Block' : None, 
            'Kindergarten' : None, 
            'Comercial Building' : None, 
            'Hotel' : 'room', 
            'Sports Facility' : None, 
            'Shopping Mal' : None, 
            'Office' : None, 
            'Cultural Building' : None, 
            'School' : None, 
            'Single Family House' : None, 
            'Apartment' : None, 
            'Nursing Home' : 'nBeds', 
            'Hospital' : None, 
            'University, Collage' : None}

#directory='../../Data/Statkraft/Forbruksdata/Boligblokk/'
#btype='Apartment Block'
#btypeShort='AB'
#locerr=0
#temperr=0
locerrlist=[] 
temperrlist=[]
sumlist=[]
savedir='../../Data/ZENcsv/'
#genCsvFromAllFilesInFolder(directory, btype, btypeShort, skip=0)
skip=['AB', 'CB', 'SF', 'CL', 'SFH', 'AP', 'UC']
genAllCsvFiles(skip)

dfsummary=pd.DataFrame(sumlist)
dfsummary.to_csv(savedir+'Lindbergsummary.dat', sep=';')