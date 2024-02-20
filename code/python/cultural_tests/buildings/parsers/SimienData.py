# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 09:12:09 2018

@author: hwaln
"""

import pandas as pd
import matplotlib.pyplot as plt
#import metdata as met
import csv as csv
import datetime
import os
from geopy.geocoders import Nominatim
import numpy as np


def readDataFile(filename):
    print(filename)

    df=pd.read_csv(filename, skiprows=9, sep='\t', decimal=',', encoding = "ISO-8859-1", index_col=False)
    #df['TimeStamp']=pd.to_datetime(df.dato, format='d%.m%.Y%')+pd.to_timedelta(df.hr-1, unit='h')
    firstDate=pd.to_datetime('01012007', format='%d%m%Y')
    df['TimeStamp']=pd.date_range(firstDate, periods=len(df.index), freq='H')
    df.index=df.TimeStamp
    df.index=df.index.tz_localize('Etc/GMT-1', ambiguous='infer') 
    df.index=df.index.tz_convert('Europe/Oslo')
    df.index = df.index.tz_localize(None)
    return df


def genCsvFromAllFilesInFolder(directory, skip=0):
    i=1
    for filename in os.listdir(directory):
        df=readDataFile(directory+filename)
        createBuildingZENCSV(df, filename)
        i+=1
    return temperrlist, locerrlist


def createMetaDataDict(btype, location, df):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    d={'Header line' : 20,
       'File owner': 'Igor Satori @sintef byggforsk',
       'Data Source' : 'Simien Standard Buildings',
       'Last update' : now,
       'Location' : location,
       'Weather data' : 'NS3031',
       'Name building' : 'SimienStandard',
       'Year of construction' : 'NA',
       'Floor area [m2]' : areaDict[btype],
       'Number of_units' : 'Unknown',
       'Building type': btype,
       'Efficicency standard' : 'Unknown',
       'Timestamp format' : '%d.%m.%Y %H:%M',
       'Time zone' : 'Europe/Oslo',
       'Daylight saving time':1}

    return d

def createMetaDataHeader():
    d={'col0': ['','',''],
       'col1': ['Weather variable', 'C', 'Temperature Outdoor'],
       'col2': ['Temperature', 'C', 'Temperature indoor (average)'],
       'col3': ['Temperature', 'C', 'Temperature indoor (operational)'],
       'col4': ['Temperature', 'C', 'Temperature ventilation supply'],
       'col5': ['Air flowrate', 'm3/s', 'Ventilation flow rate'],
       'col6': ['Electricity use', 'kWh', 'Electricity Total'],
       'col7': ['Electricity use', 'kWh', 'Electricity Lighting'],
       'col8': ['Electricity use', 'kWh', 'Electricity Auxiliaries'],
       'col9': ['Electricity use', 'kWh', 'Electricity Ventilation fans'],
       'col10': ['Heat use', 'kWh', 'Heat Total'],
       'col11': ['Heat use', 'kWh', 'Heat Room'],
       'col12': ['Heat use', 'kWh', 'Heat Ventilation'],
       'col13': ['Cool use', 'kWh', 'Cool Total'],
       'col14': ['Cool use', 'kWh', 'Cool Room'],
       'col15': ['Cool use', 'kWh', 'Cool Ventilation']
       }
    df=pd.DataFrame(d)
    return df

def creatBuildingDataDf(df):
    df[['Effekt belysning [W]', 'Effekt utstyr [W]','Effekt vifter [W]',
        'Romoppv.[W]', 'Vent.varme.[W]',
        'Romkjøling [W]', 'Vent.kjøling [W]'
        ]]=df[['Effekt belysning [W]', 'Effekt utstyr [W]','Effekt vifter [W]',
                 'Romoppv.[W]', 'Vent.varme.[W]',
                 'Romkjøling [W]', 'Vent.kjøling [W]']]/1000
    df_D=df[['Utetemp. [°C]', 
             'Lufttemp.[°C]','Op. temp.[°C]',
             'Tilluftstemp.[°C]', 'Luftmengde [m³/h]',
             'Effekt belysning [W]', 'Effekt utstyr [W]','Effekt vifter [W]',
             'Romoppv.[W]', 'Vent.varme.[W]',
             'Romkjøling [W]', 'Vent.kjøling [W]']]
    df_D.columns=['Tout',
                  'Ti', 'Ti_1',
                  'Tvent', 'VentFlow',
                  'ElLight', 'ElAux', 'ElFan',
                  'HtRoom', 'HtVent',
                  'ClRoom', 'ClVent']
    df_D['ElTot']=df_D['ElLight']+df_D['ElAux']+df_D['ElFan']
    df_D['HtTot']=df_D['HtRoom']+df_D['HtVent']
    df_D['ClTot']=df_D['ClRoom']+df_D['ClVent']
    
    df_D=df_D[['Tout',
                  'Ti', 'Ti_1',
                  'Tvent', 'VentFlow',
                  'ElTot','ElLight', 'ElAux', 'ElFan',
                  'HtTot','HtRoom', 'HtVent',
                  'ClTot','ClRoom', 'ClVent']]
    return df_D

def getEfficiencyLevel(std):
    es='N'
    try:
        if std=='PH':
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

def getBid(df, dMeta, btype, std):
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
    bid = bid+'_' + getEfficiencyLevel(std)
    return bid

def getSummaryDict(df, dM, bid, filename):
    d={}
    d['bTypeId']=bid.split('_')[0]
    d['bEnum']='_'.join(bid.split('_')[1:4])
    d['fname']=filename
    d['Year']=dM['Year_of_construction']
    d['Area']=dM['Floor_area_heat']
    d['sumHeat']=df['HtTot'].mean()*365*24 #assuming representative period
    d['peakHeat']=df['HtTot'].max()
    d['countHeatNaN']=df['HtTot'].isnull().sum()
    d['countHeatNotZero']=df.HtTot[df.HtTot>0].count()
    d['sumEl']=df['ElTot'].mean()*365*24 #assuming representative period
    d['peakEl']=df['ElTot'].max()
    d['countHeatNaN']=df['ElTot'].isnull().sum()
    d['countHeatNotZero']=df.ElTot[df.ElTot>0].count()
    return d

def createBuildingZENCSV(df, filename):
    df_D=creatBuildingDataDf(df)
    btype=btypeDict[filename.split(' ')[0]]
    std=filename.split(' ')[1].strip('.txt.')
    dM=createMetaDataDict(btype, 'Oslo', std)
    df_H=createMetaDataHeader()
    bid=getBid(df_D, dM, btype, std)
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


btypeDict={'boligblokk' : 'Apartment Block', 
            'kontorbygg' : 'Office', 
            'småhus' : 'Single Family House', 
            }
areaDict={'Apartment Block':900, 
            'Office' : 8748, 
            'Single Family House':175,
            }
directory='../../Data/Simuleringer/SimienStandardBygg/Filer/'
#btype='Apartment Block'
#btypeShort='AB'
#locerr=0
#temperr=0
locerrlist=[] 
temperrlist=[]
sumlist=[]
savedir='../../Data/ZENcsv'
#genCsvFromAllFilesInFolder(directory, btype, btypeShort, skip=0)
skip=['AB', 'CB', 'SF', 'CL', 'SFH', 'AP', 'UC']
genCsvFromAllFilesInFolder(directory, skip=0)

dfsummary=pd.DataFrame(sumlist)
dfsummary.to_csv(savedir+'summary.dat', sep=';')