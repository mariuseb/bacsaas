# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 13:11:56 2018

@author: hwaln
"""

import csv
import pandas as pd
import os


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def getZENcsvMetaData(fname):
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

def getZENcsvTimeSeries(fname, hrow):
    df = pd.read_csv(fname, index_col=0, skiprows=hrow-1, sep=';')
    try:
        df.index=pd.to_datetime(df.index, format='%d.%m.%Y %H:%M')
    except ValueError:
        print('Warning: timestamp format not standard. Trying day first')
        df.index=pd.to_datetime(df.index, format='%Y.%m.%d %H:%M')
    return df

def getZENcsv(fname):
    d = getZENcsvMetaData(fname)
    hrow = int(d[list(d)[0]])
    df = getZENcsvTimeSeries(fname,hrow)
    return d, df

def readAllcsvsFromFolder(directory):
    Mdict = {}
    Bdict = {}
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            print('reading file: '+ filename)
            key=filename.split('.')[0]
            path=directory if not directory=='.' else ''
            Mdict[key], Bdict[key]=getZENcsv(path+filename)
    return Mdict, Bdict

def writeZENcsv(savedir, bid, metaData, tsData, tsHeader):
    fname=savedir+bid+'.txt'
    ensure_dir(fname)
    with open(fname, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for key, value in metaData.items(): #write header dict
            writer.writerow([key, value])
        csv_file.write('\n') 
        tsHeader.to_csv(csv_file, header=False, index=False, sep=';')
        tsData.to_csv(csv_file, sep=';',date_format='%Y-%m-%dT%H:%M%z')
    return

def writeAllZENcsv(savedir, metaData, tsData, tsHeader):
    for bid in metaData.keys():
        writeZENcsv(savedir, bid, metaData[bid], tsData[bid], tsHeader[bid])
    return