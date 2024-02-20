# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 12:28:01 2022

@author: hwaln
Test for importing weatherdata from met archive
"""

import netCDF4
import pyproj
import numpy as np
import pandas as pd
import time
from progress.bar import Bar

#Create a format to change the data with a for loop
WEB = u'https://thredds.met.no/thredds/dodsC/metpparchive/{yyyy}/{mm}/{dd}/met_analysis_1_0km_nordic_{yyyy}{mm}{dd}T{hh}Z.nc'
WEBv3 = u'https://thredds.met.no/thredds/dodsC/metpparchivev3/{yyyy}/{mm}/{dd}/met_analysis_1_0km_nordic_{yyyy}{mm}{dd}T{hh}Z.nc'
WEBv2 = u'https://thredds.met.no/thredds/dodsC/metpparchivev2/{yyyy}/{mm}/{dd}/met_analysis_1_0km_nordic_{yyyy}{mm}{dd}T{hh}Z.nc' 
WEBv1 = u'https://thredds.met.no/thredds/dodsC/metpparchivev1/{yyyy}/{mm}/{dd}/met_analysis_1_0km_nordic_{yyyy}{mm}{dd}T{hh}Z.nc' 
WEBfo = u'https://thredds.met.no/thredds/dodsC/metpparchive/{yyyy}/{mm}/{dd}/met_forecast_1_0km_nordic_{yyyy}{mm}{dd}T{hh}Z.nc' 

#Define the start and stop dates and the time step for the hours


def getPostCodeWeatherData(fromTime='2017-01-01 00', toTime='2017-01-01 23', codes_fname='postnummer.csv', codes=[], tz='UTC', store=False, name='', preload=False):
    dcodes=getPostCodeData(codes_fname, codes=codes)
    results, eLst = getLocationsWeatherData(dcodes, fromTime=fromTime, toTime=toTime, tz=tz, store=store, name=name, preload=preload)
    return results, eLst
    
def getLocationsWeatherData(locations, fromTime='2017-01-01 00', toTime='2017-01-01 23', tz='UTC', store=False, name='', preload=False):
    fdict=getFiles(fromTime=fromTime, toTime=toTime, tz=tz)
    results={}
    eLst=[]
    for key in locations.keys():
        results[key]={'TimeStamp':[],
                      'Tout':[],
                      'SolGlob':[],
                      'WindSpd':[],
                      'WindDir':[]}
    bar=Bar('downloading weather data', max=len(fdict['ope']))
    for i in range(0, len(fdict['ope'])):
        data, flag = getData(fdict, i)
        if flag:
            storeData(data, results, locations, preload=preload)
        else:
            eLst+=[fdict['ope'][i]]
        bar.next()
        
    #format results
    for key in results.keys():
        results[key]=pd.DataFrame.from_dict(results[key]) # convert to dataframe
        results[key].set_index('TimeStamp', inplace=True) # set datetime index
        results[key]=results[key].tz_localize('UTC').tz_convert(tz) # convert to correct timezone
        results[key]=results[key].asfreq(freq='1H') # fill in missing files with nan
        results[key].SolGlob=results[key].SolGlob.shift(-1) # shift solar radiation one hour back to represent incomming solar radiation next hour.
    
    #save results files
    if store:
        for key in results.keys():
            results[key].to_csv(name+'_'+key+'.csv', sep=';')
    return results, eLst

def getFiles(fromTime='2017-01-01 00', toTime='2017-01-01 23', tz='UTC'):
    start=pd.to_datetime(fromTime)
    end=pd.to_datetime(toTime)
    td = np.timedelta64(1, 'h')
    dts = pd.DatetimeIndex(np.arange(start, end, td))
    dts=dts.tz_localize(tz).tz_convert('UTC') #set to same timezone as NWT stored data
    fdict = {'rv3' : [],
             'ope' : [],
             'rv2' : [],
             'rv1' : []}

    #Create a list with all the files
    for year, month, day, hour in zip(dts.year, dts.month, dts.day, dts.hour):
        yyyy = str(year)
        mm = '0{}'.format(str(month)) if month<10 else str(month)
        dd = '0{}'.format(str(day)) if day<10 else str(day)
        hh = '0{}'.format(str(hour)) if hour<10 else str(hour)
        fdict['rv3'] += [WEBv3.format(yyyy=yyyy, mm=mm, dd=dd, hh=hh)]
        fdict['ope'] += [WEB.format(yyyy=yyyy, mm=mm, dd=dd, hh=hh)]
        fdict['rv2'] += [WEBv2.format(yyyy=yyyy, mm=mm, dd=dd, hh=hh)]
        fdict['rv1'] += [WEBv1.format(yyyy=yyyy, mm=mm, dd=dd, hh=hh)]
    return fdict
            
def getPostCodeData(fname, codes=[]):
    df=pd.read_csv(fname, sep='\t', dtype={'POSTNR':str},index_col='POSTNR')
    d={}
    if len(codes)==0:
        codes=list(df.index)
    for c in codes:
        d[c]={'lat':df.loc[c]['LAT'],
              'lon':df.loc[c]['LON']}
    return d

def getData(fdict, i):
    flag = False
    data=None
    if not flag:
        try:
            data = netCDF4.Dataset(fdict['rv3'][i], "r")
            flag = checkData(data)
        except:
            print('rv3 not available, trying ope')
    if not flag:
        try:
            data = netCDF4.Dataset(fdict['ope'][i], "r")
            flag = checkData(data)
        except:
            print('ope not available, trying rv2')
    if not flag:
        try:
            data = netCDF4.Dataset(fdict['rv2'][i], "r")
            flag = flag = checkData(data)
        except:
            print('rv2 not available, trying rv1')
    if not flag:
        try:
            data = netCDF4.Dataset(fdict['rv1'][i], "r")
            flag = flag = checkData(data)
        except:
            print('rv1 not available, missing datapoint')
    return data, flag

def checkData(data):
    flag=False
    try:
        getTemperature(data, 0, 0)
        getSolarRad(data, 0, 0)
        flag=True
    except:
        return flag
    
    return flag

def getTime(data):
    return [pd.Timestamp(data.variables["time"][0].data.flatten()[0], unit='s')]
def getTemperature(data,Iy,Ix):
    return [data.variables["air_temperature_2m"][0, Iy, Ix]-273.15]
def getSolarRad(data, Iy, Ix):
    return [data.variables["integral_of_surface_downwelling_shortwave_flux_in_air_wrt_time"][:, Iy, Ix][0]/3600]
def getWindSpeed(data, Iy, Ix):
    return [data.variables["wind_speed_10m"][:, Iy, Ix][0]]
def getWindDir(data, Iy, Ix):
    return [data.variables["wind_direction_10m"][:, Iy, Ix][0]]

def storeData(data, results, dcodes, preload=False):
    if preload:
        try:
            tdata=data.variables["air_temperature_2m"][0, :, :]
        except:
            tdata=None
        try:
            sdata=data.variables["integral_of_surface_downwelling_shortwave_flux_in_air_wrt_time"][0, :, :]
        except:
            sdata=None
        try:
            wsdata=data.variables["wind_speed_10m"][0, :, :]
        except:
            sdata=None
        try:
            wddata=data.variables["wind_direction_10m"][0, :, :]
        except:
            sdata=None
    
    timeStamp=getTime(data)
    for key in results.keys():
        if not 'Iy' in dcodes[key].keys():
            print('Getting projections')
            lat=dcodes[key]['lat']
            lon=dcodes[key]['lon']
    
            #proj = pyproj.Proj(data.variables["projection_lcc"].proj4)
            proj4='+proj=lcc +lat_0=63 +lon_0=15 +lat_1=63 +lat_2=63 +no_defs +R=6.371e+06'
            proj = pyproj.Proj(proj4)
    
            # Compute projected coordinates of lat/lon point
            X, Y = proj(lon, lat)
    
            # Find nearest neighbour
            x = data.variables["x"][:]
            y = data.variables["y"][:]
            dcodes[key]['Ix'] = np.argmin(np.abs(x - X))
            dcodes[key]['Iy'] = np.argmin(np.abs(y - Y))
        Ix=dcodes[key]['Ix']
        Iy=dcodes[key]['Iy']
        results[key]['TimeStamp'] += timeStamp
        try:
            if preload:
                results[key]['Tout'].append(tdata[Iy, Ix]-273.15)
            else:
                results[key]['Tout'] += getTemperature(data, Iy, Ix)
        except:               
           results[key]['Tout'] += [np.nan]
        try:
            if preload:
                results[key]['SolGlob'].append(sdata[Iy, Ix]/3600)
            else:
                results[key]['SolGlob'] += getSolarRad(data, Iy, Ix)
        except:
           results[key]['SolGlob'] += [np.nan] 
        try:
            if preload:
                results[key]['WindSpd'].append(wsdata[Iy, Ix])
            else:
                results[key]['WindSpd'] += getWindSpeed(data, Iy, Ix)
        except:
            results[key]['WindSpd'] += [np.nan]
        try:
            if preload:
                results[key]['WindDir'].append(wddata[Iy, Ix])
            else:
                results[key]['WindDir'] += getWindDir(data, Iy, Ix)
        except:
            results[key]['WindDir'] += [np.nan]
    return

#function with the code from https://github.com/metno/NWPdocs/wiki/Python


