# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 14:43:26 2019

@author: hwaln
"""

import pandas as pd
import matplotlib.pyplot as plt

dfsummary=pd.read_csv('summary.txt', sep=';', index_col=0)

print(dfsummary.bTypeId.unique()) #prints list of available building Type ids (bid)
bid=dfsummary.bTypeId.unique()[0] #sets bid to the first object in the list. Change this to select a different building type

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
    ax.set_title(bid)
    return
    
def plotbTIdPeakLoadHoursvsSpesHeat(bid, name=False):
    df=getbTIdSummary(bid)
    fig,ax = plt.subplots(1,1)
    ax.scatter(x=df['sumHeat']/df['Area'], y=df['sumHeat']/df['peakHeat'])
    if name: #names each point with identifier
        for i, txt in enumerate(df['bEnum'].values):
            ax.annotate(txt, ((df['sumHeat']/df['Area']).values[i],(df['sumHeat']/df['peakHeat']).values[i]))
    ax.set_ylabel('Peak Load Hours [h]')
    ax.set_xlabel('Spesific Heat [kWh/m2]')
    ax.set_title(bid)
    return

