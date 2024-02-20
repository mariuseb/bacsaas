# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 10:19:10 2018

@author: hwaln
"""

import pandas as pd
import matplotlib.pyplot as plt
import buildingdata.lib.metdata as met
import csv as csv
import datetime

def readAllRawData():
    #import heat consumption
    df_Q=pd.read_excel('FortumData.xlsx', sheet_name="Q", header=(0), skiprows=([1]), index_col=0) #get input array from excel file via Pandas
    df_Q.index=pd.to_datetime(df_Q.index, format='%d.%m.%Y %H')
    df_Q.index.name='Time'
    df_Q.index=df_Q.index.tz_localize('Europe/Oslo', ambiguous='infer')
    #df_Q.index=df_Q.index.tz_convert('Etc/GMT-1')
    
    #import m3
    df_V=pd.read_excel('FortumData.xlsx', sheet_name="V", header=(0), skiprows=([1]), index_col=0) #get input array from excel file via Pandas
    df_V.index=pd.to_datetime(df_V.index, format='%d.%m.%Y %H')
    df_V.index.name='Time'
    df_V.index=df_V.index.tz_localize('Europe/Oslo', ambiguous='infer')
    #df_V.index=df_V.index.tz_convert('Etc/GMT-1')
    
    #import Ts
    df_Ts=pd.read_excel('FortumData.xlsx', sheet_name="Ts", header=(0), skiprows=([1]), index_col=0) #get input array from excel file via Pandas
    df_Ts.index=pd.to_datetime(df_Ts.index, format='%d.%m.%Y %H')
    df_Ts.index.name='Time'
    df_Ts.index=df_Ts.index.tz_localize('Europe/Oslo', ambiguous='infer')
    #df_Ts.index=df_Ts.index.tz_convert('Etc/GMT-1')
    
    #import Ti
    df_Tr=pd.read_excel('FortumData.xlsx', sheet_name="Tr", header=(0), skiprows=([1]), index_col=0) #get input array from excel file via Pandas
    df_Tr.index=pd.to_datetime(df_Tr.index, format='%d.%m.%Y %H')
    df_Tr.index.name='Time'
    df_Tr.index=df_Tr.index.tz_localize('Europe/Oslo', ambiguous='infer')
    #df_Tr.index=df_Tr.index.tz_convert('Etc/GMT-1')
    
    #import dT
    df_dT=pd.read_excel('FortumData.xlsx', sheet_name="dT", header=(0), skiprows=([1]), index_col=0) #get input array from excel file via Pandas
    df_dT.index=pd.to_datetime(df_dT.index, format='%d.%m.%Y %H')
    df_dT.index.name='Time'
    df_dT.index=df_dT.index.tz_localize('Europe/Oslo', ambiguous='infer')
    #df_dT.index=df_dT.index.tz_convert('Etc/GMT-1')
    
    return df_Q, df_V, df_Ts, df_Tr, df_dT

def readAllCSVData():
    bdir='../../Data/Fortum/Splitcsv/'
    df_Q=pd.read_csv(bdir+'Q.csv', index_col='Time',)
    df_Q.index=pd.to_datetime(df_Q.index)
    
    df_V=pd.read_csv(bdir+'V.csv', index_col='Time',)
    df_V.index=pd.to_datetime(df_V.index)
    
    df_Ts=pd.read_csv(bdir+'Ts.csv', index_col='Time',)
    df_Ts.index=pd.to_datetime(df_Ts.index)
    
    df_Tr=pd.read_csv(bdir+'Tr.csv', index_col='Time',)
    df_Tr.index=pd.to_datetime(df_Tr.index)
    
    df_dT=pd.read_csv(bdir+'dT.csv', index_col='Time',)
    df_dT.index=pd.to_datetime(df_dT.index)
    
    df_met=pd.read_csv(bdir+'met.csv', index_col='Time',)
    df_met.index=pd.to_datetime(df_met.index)    
    
    return df_Q, df_V, df_Ts, df_Tr, df_dT, df_met

def norm_df(df):
    df_norm=df/df.sum()
    return df_norm

#get wether data
def getMetData():
    df_met = (met.getMetDataTimeSeries('SN18701', 'mean(air_temperature PT1H)', '2016-12-31T23', '2017-12-31T23')).resample('1H').mean()
    df_met['globSol']=(met.getMetDataTimeSeries('SN18700', 'mean(surface_downwelling_shortwave_flux_in_air PT1H)', '2016-12-31T23', '2017-12-31T23')).resample('1H').mean()
    df_met['WindSpeed']=(met.getMetDataTimeSeries('SN18700', 'wind_speed', '2016-12-31T23', '2017-12-31T23')).resample('1H').mean()
    df_met.index=df_met.index.tz_localize('Etc/GMT', ambiguous='infer')
    df_met.index=df_met.index.tz_convert('Europe/Oslo')
    return df_met

#sort to one data frame for each building
def sortBuildingData (df_Q, df_V, df_Ts, df_Tr, df_met):
    buildingList = [str(c) for c in df_Q.columns]
    buildingDict= {}
    i=0
    for b in buildingList:
        df = pd.DataFrame()
        df = df.assign(Tout=df_met.iloc[:,0])
        df = df.assign(SolGlob=df_met.iloc[:,1])
        df = df.assign(WindSpd=df_met.iloc[:,2])

        df = df.assign(HtTot=df_Q.iloc[:,i])
        df = df.assign(FV_V=df_V.iloc[:,i])
        df = df.assign(FV_Ts=df_Ts.iloc[:,i])
        df = df.assign(FV_Tr=df_Tr.iloc[:,i])
        df.index.rename('TimeStamp', inplace=True)
        buildingDict[b]=df
        i=i+1
    
    return buildingDict

def createAggregatedProfile(bDict):
    df=pd.DataFrame(0,index=bDict[list(bDict)[0]].index, columns=bDict[list(bDict)[0]].columns)
    df.Tout=bDict[list(bDict)[0]].Tout
    df.SolGlob=bDict[list(bDict)[0]].SolGlob
    df.WindSpd=bDict[list(bDict)[0]].WindSpd
    for key in bDict:
        df.HtTot=df.HtTot.add(bDict[key].HtTot)
        df.FV_V=df.FV_V.add(bDict[key].FV_V)
        df.FV_Ts=df.FV_Ts.add(bDict[key].FV_Ts*bDict[key].HtTot)
        df.FV_Tr=df.FV_Tr.add(bDict[key].FV_Tr*bDict[key].HtTot)
    df.FV_Ts=df.FV_Ts/df.HtTot
    df.FV_Tr=df.FV_Tr/df.HtTot
    bDict['Tot']=df
    return bDict


def createScatterMatrices(d):
    for key in d:
        pd.plotting.scatter_matrix(d[key])
        plt.savefig('plot/'+str(key)+'.png', dpi=400)
        plt.clf()
        plt.close()
    return

def createHtPlot(d, period, normalize=False):
    ax=plt.plot()
    lw1=0.5
    lw2=2
    norm=1
    for key in d:
        if normalize:
            norm=d[key].HtTot.sum()
        if key == 'Tot':
            ax=(d[key].HtTot[period]/norm).plot(lw=lw2)
        else:
            ax=(d[key].HtTot[period]/norm).plot(lw=lw1)
    return ax

def removeBuildingsFromDict(bDict):
    bList = ['B1','B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10',
             'B11', 'B12','B13','B14','B15', 'B53']
    for b in bList:
        df=bDict.pop(b, 'empty')
    return bDict

def createMetaDataDict():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    d={'Header_line' : 17,
       'File_owner': 'Harald Taxt Walnum @sintef byggforsk',
       'Last_update' : now,
       'Location' : 'Oslo',
       'Weather_data' : 'Blindern',
       'Name_bulding' : 'Unknown',
       'Floor_area_total' : '',
       'Building_type': 'Appartment Block',
       'Efficicency_standard' : 'Unknown',
       'Timestamp_format' : '%d.%m.%Y %H:%M',
       'Time_zone' : 'Europe/Oslo',
       'Daylight_saving_time':1}
    return d

def createMetaDataHeader():
    d={'col0': ['','',''],
       'col1': ['Weather variable', 'C', 'Temperature Outdoor'],
       'col2': ['Weather variable', 'W/m2', 'Global Solar Radiation'],
       'col3': ['Weather variable', 'm/s', 'Wind Speed'],
       'col4': ['Heat use', 'kWh', 'Heat Total'],
       'col5': ['District Heating', 'm3', 'Volume flow'],
       'col6': ['District Heating', 'C', 'Supply Temperature'], 
       'col7': ['District Heating', 'C', 'Return Temperature'],
       }
    df=pd.DataFrame(d)
    return df

def createBuildingSimpleCSVs(d):
    for key in d:
        d[key].to_csv('Data/SingleBuilding/'+str(key)+'.csv')
    return

def createBuildingZENCSVs(bDict):
    for key in bDict:
        df_D=bDict[key]
        df_D.index=df_D.index.tz_localize(None) #convert to naive time zone handling
        dM=createMetaDataDict()
        df_H=createMetaDataHeader()
        with open('../../Data/Fortum/ZENcsv/'+str(key)+'.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            for key, value in dM.items(): #write header dict
                writer.writerow([key, value])
            csv_file.write('\n') 
            df_H.to_csv(csv_file, header=False, index=False, sep=';')
            df_D.to_csv(csv_file, sep=';', date_format='%d.%m.%Y %H:%M')
    return

def genZENCSVFromAllDataCSV():
    df_Q, df_V, df_Ts, df_Tr, df_dT, df_met = readAllCSVData()
    df_met.index=df_met.index.tz_localize('Europe/Oslo', ambiguous='infer')
    df_Q.index=df_Q.index.tz_localize('Europe/Oslo', ambiguous='infer')
    df_V.index=df_V.index.tz_localize('Europe/Oslo', ambiguous='infer')
    df_Ts.index=df_Ts.index.tz_localize('Europe/Oslo', ambiguous='infer')
    df_Tr.index=df_Tr.index.tz_localize('Europe/Oslo', ambiguous='infer')
    df_dT.index=df_dT.index.tz_localize('Europe/Oslo', ambiguous='infer')
    bDict=sortBuildingData (df_Q, df_V, df_Ts, df_Tr, df_met)
    bDict=removeBuildingsFromDict(bDict)
    bDict=createAggregatedProfile(bDict)
    createBuildingZENCSVs(bDict)
    return