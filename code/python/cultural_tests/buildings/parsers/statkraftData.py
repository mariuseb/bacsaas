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
    df=pd.read_excel(filename, sheet_name='Rådata', usecols=([0,3,4,5,6,7]), header=(0), skiprows=([1]), index_col=0) #get input array from excel file via Pandas
    df.index=pd.to_datetime(df.index, format='%d.%m.%Y %H')
    df.index.name='TimeStamp'
    df.index=df.index.tz_localize('Etc/GMT-1', ambiguous='infer')
    df.columns=['FV_Ts', 'FV_Tr', 'FV_dT', 'HtTot', 'FV_V']
#    df['Qv']= f.d_water(df.Tr)*df.V*(f.h_water(df.Ts)-f.h_water(df.Tr))/1000/3600
    df.index=df.index.tz_convert('Europe/Oslo')    
    return df

#get wether data
def getMetData(stationId):
    df_met = met.getMetDataTimeSeries(stationId, 'mean(air_temperature PT1H)', '2017-01-01', '2018-01-01')
    if not isinstance(df_met, pd.DataFrame):
        df_met = met.getMetDataTimeSeries(stationId, 'air_temperature', '2017-01-01', '2018-01-01')
    if isinstance(df_met, pd.DataFrame):
#        df_met.index=df_met.index.tz_localize('Etc/GMT', ambiguous='infer')
        df_met.index=df_met.index.tz_convert('Europe/Oslo')
    else: 
        print('\WARNING: No outdoor temperature found\n')
    return df_met

def getStationId(street, zipcode):
    stationId=None
    long, lat = getCoordnates(street, zipcode)
    if not long==None:
        stationId = met.getNearestStation(long, lat)
        if stationId=='SN68173': #quickfix
            stationId='SN68860'
        if stationId=='SN17851': #quickfix
            stationId='SN17850'
        if stationId=='SN68863': #quickfix
            stationId='SN68860'
        if stationId=='SN17251': #quickfix
            stationId='SN17280'
        if stationId=='SN27590': #quickfix
            stationId='SN27780'
        if stationId=='SN27600': #quickfix
            stationId='SN27780'
        if stationId=='SN27540': #quickfix
            stationId='SN27780'
        if stationId=='SN27630': #quickfix
            stationId='SN27780'
        if stationId=='SN4781': #quickfix
            stationId='SN4780'
    return stationId

def getClimaData(df, street, zipcode, btype):
    cFileLst = os.listdir('../../Data/Statkraft/WeatherFiles/')
    if any (zipcode.strip(' ').split(' ')[0] in s for s in cFileLst):
        cFile=[s for s in cFileLst if zipcode.strip(' ').split(' ')[0] in s][0]
        df_clima=pd.read_csv('../../Data/Statkraft/WeatherFiles/'+cFile, sep='\t', 
                             na_values=['', ' ', 'x'], index_col=0)
        df_clima.dropna(how='all',inplace=True)
        df_clima.index=pd.to_datetime(df_clima.index, format='%d.%m.%Y-%H:%M')
        #stationId='SN' + str(df_clima['St.no'].iloc[0])
        stationId='Unknown'
        #df_clima.drop('St.no', axis=1, inplace=True)
        df_clima.rename(columns={'FF':'WindSpd', 'QSI':'SolGlob','TA':'Tout'}, inplace=True)
        df_clima=df_clima.tz_localize('Etc/GMT-1', ambiguous='infer')
        df_clima=df_clima.tz_convert('Europe/Oslo')
        df=pd.concat([df_clima, df], axis=1, join='inner')
        df.index.name='TimeStamp'
    else:
        print('\WARNING: ' + zipcode + ' eKlima file not found\n')
        eklimaerrlist.append(zipcode)
        if not skipFrostData:
            stationId = getStationId(street, zipcode)
            if not stationId == None:
                df_T= getMetData(stationId)
                if not isinstance(df_T, pd.DataFrame):
                   #temperr= temperr+1
                   temperrlist.append(btype + ' ' + street + ',' + zipcode + ' ' + stationId) 
                df['Tout']= df_T
            else:
                print('\WARNING: Location not found\n')
                stationId='Unknown'
                #locerr+=1
                locerrlist.append(btype + ' ' + street + ',' + zipcode)
                df['Tout']= np.nan
        else:
            stationId='Unknown'
            df['Tout']= np.nan
        df['SolGlob'] = np.nan
        df['WindSpd'] = np.nan
    df=df[['Tout','SolGlob','WindSpd','HtTot','FV_V','FV_Ts','FV_Tr']]
    return df, stationId

def getEfficiencyLevel(df, df_Meta):
    es='R'
#    year=float(df_Meta['Year'].iloc[0])
#    if not np.isnan(year):
#        if year>2013:es='E'
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

def getBid(df, df_Meta, btype):
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
    bid=bid+'_' + getEfficiencyLevel(df, df_Meta)
    return bid

def getSummaryDict(df, df_Meta, Bid):
    d={}
    d['bTypeId']=Bid.split('_')[0]
    d['bEnum']='_'.join(Bid.split('_')[1:4])
    d['fname']=df_Meta['FileName'].values[0]
    d['Year']=(df_Meta['Year'].values[0])
    d['Area']=df_Meta['Area'].values[0]
    d['sumHeat']=df['HtTot'].mean()*365*24 #assuming representative period
    d['peakHeat']=df['HtTot'].max()
    d['countHeatNaN']=df['HtTot'].isnull().sum()
    d['countHeatNotZero']=df.HtTot[df.HtTot>0].count()
    return d
    

def genCsvFromAllFilesInFolder(directory, btype, btypeShort, skip=0):
    i=1
    df_allMeta=pd.read_csv(directory+'../../Metadata/'+btypeShort+'Metadata.csv', sep=';')
    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):
            if i>skip:
                df=readDataFile(directory+filename)
                fnamelist = filename.split(',')
                street = fnamelist[0]
                zipcode = fnamelist[1]
                df, stationId = getClimaData(df, street, zipcode, btype)
                df_Meta=df_allMeta.loc[df_allMeta['FileName']==filename]
                Bid=getBid(df, df_Meta, btype)
                bol=createBuildingZENCSV(df, Bid, btype, stationId, df_Meta)
                if bol : sumlist.append(getSummaryDict(df, df_Meta, Bid))
            i+=1
    return temperrlist, locerrlist

def getCoordnates(street, zipcode):
    geolocator=Nominatim(user_agent="user")
    address = address = street + ',' + zipcode
    location=geolocator.geocode(address)
    if location==None:
        location=geolocator.geocode(zipcode)
    if location==None:
        return None, None
    long = location.longitude
    lat = location.latitude
    return long, lat
    
def createMetaDataDict(stationId, btype, df_Meta):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    d={'Header_line' : 20,
       'File owner': 'Harald Taxt Walnum @sintef byggforsk',
       'Data Source' : 'Statkraft varme 2018',
       'Last update' : now,
       'Location' : df_Meta['ZipCode'].values[0],
       'Weather data' : stationId,
       'Name building' : 'Unknown',
       'Year of construction' : df_Meta['Year'].values[0],
       'Floor area [m2]' : df_Meta['Area'].values[0],
       'Number of units' : df_Meta['Units'].values[0],
       'Building type': btype,
       'Energy efficicency standard' : df_Meta['EffStandard'].values[0],
       'Timestamp format' : '%d.%m.%Y %H:%M',
       'Time zone' : 'Europe/Oslo',
       'Daylight_saving_time':1}
    return d

def createMetaDataHeader():
    d={'col0': ['','',''],
       'col1': ['Weather variable', 'C', 'Temperature Outdoor'],
       'col2': ['Weather variable', 'W/m2', 'Global Solar Horizontal Radiation'],
       'col3': ['Weather variable', 'm/s', 'Wind_speed'],
       'col4': ['Heat use', 'kWh', 'Heat Total'],
       'col5': ['District Heating', 'm3', 'Volume flow'],
       'col6': ['District Heating', 'C', 'Supply Temperature'], 
       'col7': ['District Heating', 'C', 'Return Temperature'],
       }
    df=pd.DataFrame(d)
    return df

def createBuildingZENCSV(df_D, Bid, btype, stationId,  df_Meta):
    df_D.index=df_D.index.tz_localize(None) #convert to naive time zone handling
    dM=createMetaDataDict(stationId, btype, df_Meta)
    if not float(dM['Floor area [m2]'])>0:
        return False
    df_H=createMetaDataHeader()
    fname=savedir+Bid+'.txt'
    ensure_dir(fname)
    with open(fname, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for key, value in dM.items(): #write header dict
            writer.writerow([key, value])
        csv_file.write('\n') 
        df_H.to_csv(csv_file, header=False, index=False, sep=';')
        df_D.to_csv(csv_file, sep=';', date_format='%d.%m.%Y %H:%M')
    return True

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def genAllCsvFiles(skip=[]):
    basedir = '../../Data/Statkraft/Forbruksdata/'
    dirlist=['Boligblokk', 'Barnehage', 'Butikk', 'Hotel', 'Idrettsbygning', 'Kjøpesenter', 'Kontor', 'Kulturbygning', 'Skole', 'Småhus','Leiligheter', 'Sykehjem', 'Sykehus', 'Universitet og høyskole']
    btypelist=['Apartment Block', 'Kindergarten', 'Comercial Building', 'Hotel', 'Sports Facility', 'Shopping Mal', 'Office', 'Cultural Building', 'School', 'Single Family House', 'Apartment', 'Nursing Home', 'Hospital', 'University, Collage' ]
    btypeShortlist=['AB', 'KG', 'CB', 'HO', 'SF', 'SM', 'OF', 'CL', 'SC', 'SFH', 'AP', 'NH', 'HS', 'UC']
    for i in range(0,len(btypelist)):
        if not btypeShortlist[i] in skip:
            genCsvFromAllFilesInFolder(basedir+dirlist[i]+ '/', btypelist[i], btypeShortlist[i], skip=0)
    return


savedir='../../Data/ZENcsv/'
#btype='Apartment Block'
#btypeShort='AB'
#locerr=0
#temperr=0
eklimaerrlist=[]
locerrlist=[] 
temperrlist=[]
sumlist=[]
#genCsvFromAllFilesInFolder(directory, btype, btypeShort, skip=0)
skip=['SFH', 'AP','UC']
skipFrostData = True
genAllCsvFiles(skip)

def genInitialMetaDataFileInFolder(directory, btype, btypeShort):
    df=pd.DataFrame(columns=['FileName', 'ZipCode', 'Year', 'Area', 'Units', 'EffStandard'])
    i=0
    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):
            fnamelist = filename.split(',')
            zipcode = fnamelist[1]
            units=pd.np.nan
            if btypeShort == 'AB':
                if fnamelist[len(fnamelist)-1].endswith('enheter.xlsx'):
                    end=fnamelist[len(fnamelist)-1].split(' ')
                    units=end[len(end)-2]            
            df.loc[i]=[filename,zipcode,pd.np.nan,pd.np.nan,units,pd.np.nan]
            i=i+1
    df.to_csv(directory+btypeShort+'Metadata.csv', sep=';')
    return

def createAllInitialMetaDataFiles(skip=[]):
    basedir = '../../Data/Statkraft/Forbruksdata/'
    dirlist=['Boligblokk', 'Barnehage', 'Butikk', 'Hotel', 'Idrettsbygning', 'Kjøpesenter', 'Kontor', 'Kulturbygning', 'Skole', 'Småhus','Leiligheter', 'Sykehjem', 'Sykehus', 'Universitet og høyskole']
    btypelist=['Apartment Block', 'Kindergarten', 'Comercial Building', 'Hotel', 'Sports Facility', 'Shopping Mal', 'Office', 'Cultural Building', 'School', 'Single Family House', 'Apartment', 'Nursing Home', 'Hospital', 'University, Collage' ]
    btypeShortlist=['AB', 'KG', 'CB', 'HO', 'SF', 'SM', 'OF', 'CL', 'SC', 'SFH', 'AP', 'NH', 'HS', 'UC']
    for i in range(0,len(btypelist)):
        if not btypeShortlist[i] in skip:
            genInitialMetaDataFileInFolder(basedir+dirlist[i]+ '/', btypelist[i], btypeShortlist[i])
    return

#### handle summary ####
dfsummary=pd.DataFrame(sumlist)
dfsummary.to_csv(savedir+'StatkraftSummary.dat', sep=';')

def getbTIdSummary(bid): ## e.g. '1-Apt-xxx'
    return dfsummary.loc[dfsummary['bTypeId']==bid]

def plotbTIdSpesHeatvsYear(bid, name=False):
    df=getbTIdSummary(bid)
    fig,ax = plt.subplots(1,1)
    ax.scatter(x=df['Year'], y=df['sumHeat']/df['Area'])
    if name: #names each point with identifier
        for i, txt in enumerate(df['bEnum'].values):
            ax.annotate(txt, (df['Year'].values[i],(df['sumHeat']/df['Area']).values[i]))
    ax.set_ylabel('Spesific Heat [kWh/m2]')
    ax.set_xlabel('Year of construction/rehab')
    return
    
def plotbidPeakLoadHoursvsSpesHeat(bid, name=False):
    df=getbTIdSummary(bid)
    fig,ax = plt.subplots(1,1)
    ax.scatter(x=df['sumHeat']/df['Area'], y=df['sumHeat']/df['peakHeat'])
    if name: #names each point with identifier
        for i, txt in enumerate(df['bEnum'].values):
            ax.annotate(txt, ((df['sumHeat']/df['Area']).values[i],(df['sumHeat']/df['peakHeat']).values[i]))
    ax.set_ylabel('Peak Load Hours [h]')
    ax.set_xlabel('Spesific Heat [kWh/m2]')
    return
