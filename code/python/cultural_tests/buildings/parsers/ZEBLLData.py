# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 09:12:09 2018

@author: hwaln

Modified on Fri Nov 29 12:26:00 2019

@author: afager
"""

import pandas as pd
import os
import numpy as np
import datetime

def readDataFile(filename):
    df = pd.read_csv(filename, sep=';')  # get input array from excel/csv/txt file via Pandas
    df.index = df.Timestamp
    df.index = pd.to_datetime(df.index - 719529, unit='D')  #spesific for matlab timestamp
    df.index = df.index.round('T')
    df.index.name = 'TimeStamp'
    df.index = df.index.tz_localize('Etc/GMT-1', ambiguous='infer')
    df['HtTot'] = df.Q_heating + df.Q_ventilation
    df = df[['Ta', 'Ws', 'Wd', 'I_sol_G', 'h_rel', 'air_pressure', 'Ti', 'Ti_main', 'Ti_bathroom', 'Ti_bedroom_east',
             'Ti_bedroom_west', 'Ti_PCA', 'To', 'To_main', 'To_bathroom', 'To_bedroom_east', 'To_bedroom_west',
             'Tv_supply',  'HtTot', 'Q_heating', 'Q_ventilation', 'Q_appliances']]  # Headers in the original file, in the order of our choice
    df.columns = ['Tout', 'WindSpd', 'WindDir', 'SolGlob', 'RH', 'PO', 'Ti', 'Ti1', 'Ti2', 'Ti3', 'Ti4', 'Ti5', 'TiOp',
                  'TiOp1', 'TiOp2', 'TiOp3', 'TiOp4', 'TVents', 'HtTot', 'HtRoom', 'HtVent', 'ElTot']  # Change name to ZEN standard
    df['PO'] = df['PO'].divide(10)
    df['HtTot'] = df['HtTot'].divide(1000)
    df['HtRoom'] = df['HtRoom'].divide(1000)
    df['HtVent'] = df['HtVent'].divide(1000)
    df['ElTot'] = df['ElTot'].divide(1000)
    #   df.index=df.index.tz_convert('Europe/Oslo')
    return df


"""ZEN STANDARD HEADERS:"""

"""
Category,Unit,Description,Column name

"","","",TimeStamp

Weather variable,C,Temperature Outdoor,Tout
Weather variable,m/s,Wind Speed,WindSpd
Weather variable,deg,Wind Direction,WindDir
Weather variable,W/m2,Global Solar Horizontal Radiation,SolGlob
Weather variable,W/m2,Direct Normal Radiation,SolDir
Weather variable,W/m2,Diffuse Solar Radiation,SolDiff
Weather variable,%,Relative Humidity,RH
Weather variable,kPa,Atmospheric Pressure,PO

Temperature,C,Temperature indoor average,Ti
Temperature,C,Temperature indoor # or specification,Ti#
Temperature,C,Temperature indoor operative,TiOp
Temperature,C,Temperature indoor operative # or specification,TiOp#
Temperature,C,Temperature Ventilation supply,Tvents

Heating system,kg/h,Mass Flow,HtMass
Heating system,C,Supply Temperature,HtSup
Heating system,C,Return Temperature,HtRet

Ventilation,m3/s,Ventilation Flow rate,VentFlow

Heat use,kWh,Heat Total,HtTot
Heat use,kWh,Domestic Hot Water,HtDHW
Heat use,kWh,Room heating,HtRoom
Heat use,kWh,Snow melting,HtSnow
Heat use,kWh,Space heating,HtSpace
Heat use,kWh,Ventilation heating battery,HtVent

Electricity use,kWh,Electricity Total,ElTot
Electricity use,kWh,Electricity Auxiliaries,ElAux
Electricity use,kWh,Electricity Ventilation fans,ElFan
Electricity use,kWh,Electricity Heating,ElHeat
Electricity use,kWh,Electricity Heat Pump,ElHP
Electricity use,kWh,Electricity Lighting,ElLight
Electricity use,kWh,Electricity Plug loads,ElPlug
Electricity use,kWh,Electricity use common areas only,ElOth

Cool use,kWh,Cool Total,ClTot
Cool use,kWh,Cool Room,ClRoom
Cool use,kWh,Cool Ventilation,ClVent

District Heating,m3,Volume Flow,DHVF
District Heating,C,Return Temperature,DHTr
District Heating,C,Supply Temperature,DHTs
"""

def createMetaDataDict():  # First part of the csv file
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    d = {'Header_line': 20, # Needs to be updated if length of d is longer or shorter
         'File owner': 'Harald Taxt Walnum @sintef byggforsk',
         'Data Source': 'ZEBLL experiment',
         'Last update': now,
         'Location': 'Trondheim',
         'Weather data': 'Local',
         'Name building': 'ZEB Living Lab',
         'Year of construction': '2014',
         'Floor area [m2]': '105',
         'Number of units': '1',
         'Building type': 'Single Family House',
         'Energy efficicency standard': 'Passive House',
         'Timestamp format': '%d.%m.%Y %H:%M',
         'Time zone': 'UTC+1',
         'Daylight_saving_time': 1}
    return d


# Category, Unit, Description of the data set taken from ZEN STANDARD HEADERS, order have to mach the order of df.column in readDataFile

def createMetaDataHeader():  
    d = {'col0': ['', '', ''],
         'col1': ['Weather variable', 'C', 'Temperature Outdoor'],
         'col2': ['Weather variable', 'm/s', 'Wind_speed'],
         'col3': ['Weather variable', 'deg', 'Wind_direction'],
         'col4': ['Weather variable', 'W/m2', 'Global Solar Horizontal Radiation'],
         'col5': ['Weather variable', '%', 'Relative Humidity'],
         'col6': ['Weather variable', 'kPa', 'Atmospheric Pressure'],
         'col7': ['Temperature', 'C', 'Temperature Indoor Building average'],
         'col8': ['Temperature', 'C', 'Temperature Indoor Main zone'],
         'col9': ['Temperature', 'C', 'Temperature Indoor Bathroom'],
         'col10': ['Temperature', 'C', 'Temperature Indoor Bedroom east'],
         'col11': ['Temperature', 'C', 'Temperature Indoor Bedroom west'],
         'col12': ['Temperature', 'C', 'Temperature Indoor PCA'],
         'col13': ['Temperature', 'C', 'Temperature Indoor operative Building average'],
         'col14': ['Temperature', 'C', 'Temperature Indoor operative Main zone'],
         'col15': ['Temperature', 'C', 'Temperature Indoor operative Bathroom'],
         'col16': ['Temperature', 'C', 'Temperature Indoor operative Bedroom east'],
         'col17': ['Temperature', 'C', 'Temperature Indoor operative Bedroom west'],
         'col18': ['Temperature', 'C', 'Temperature Ventilation supply'],
         'col19': ['Heat use', 'kWh', 'Heat Total'],
         'col20': ['Heat use', 'kWh', 'Room heating'],
         'col21': ['Heat use', 'kWh', 'Ventilation heating battery'],
         'col22': ['Electricity use', 'kWh', 'Electricity total']
         }
    df = pd.DataFrame(d)
    return df


def createBuildingZENCSV(df_D):
    df_D.index = df_D.index.tz_localize(None)  # convert to naive time zone handling
    dM = createMetaDataDict()
    df_H = createMetaDataHeader()
    fname = savedir + Bid + '.txt'
    with open(fname, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for key, value in dM.items():  # write header dict
            writer.writerow([key, value])
        csv_file.write('\n')
        df_H.to_csv(csv_file, header=False, index=False, sep=';')
        df_D.to_csv(csv_file, sep=';', date_format='%d.%m.%Y %H:%M')
    return True


savedir = 'C:\\'  # directory for the created files to be stored
bid = []  # list of the file names for the created files
path = 'C:\\Experiment 2\\'
# path = 'C:\\Experiment 3\\'
# path = 'C:\\Experiment 4\\'
files = os.listdir(path)
files = files[4:]  # choosing the files to be converted
for file in files:
    bid.append(f'Experiment_2_{file.split(".")[0]}')  # remember to change the number to match the path
print(files)
print(bid)

for file, Bid in zip(files, bid):
    df = readDataFile(path + file)
    createBuildingZENCSV(df)

