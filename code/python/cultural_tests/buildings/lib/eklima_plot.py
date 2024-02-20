# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 09:40:31 2019

@author: kariso
"""

import matplotlib.pyplot as plt
import pandas as pd

def plot_eklima_temp(filename):    
    df_eklima=pd.read_csv(filename, skiprows=18, skipfooter=12, engine='python', sep=';', index_col=1, na_values=['x','',' '])
    df_eklima.index=pd.to_datetime(df_eklima.index, format='%d.%m.%Y-%H:%M')
    df_eklima['TA'].plot()
    return 

def plot_eklima_wind(filename):    
    df_eklima=pd.read_csv(filename, skiprows=18, skipfooter=12, engine='python', sep=';', index_col=1, na_values=['x','',' '])
    df_eklima.index=pd.to_datetime(df_eklima.index, format='%d.%m.%Y-%H:%M')
    df_eklima['FF'].plot()
    return 

def plot_eklima_solar(filename):    
    df_eklima=pd.read_csv(filename, skiprows=18, skipfooter=12, engine='python', sep=';', index_col=1, na_values=['x','',' '])
    df_eklima.index=pd.to_datetime(df_eklima.index, format='%d.%m.%Y-%H:%M')
    df_eklima['QSI'].plot()
    return 

def plot_eklima_all(filename):
    df_eklima=pd.read_csv(filename, skiprows=40, skipfooter=5, engine='python', sep=';', index_col=1, na_values=['x','',' '])
    df_eklima.index=pd.to_datetime(df_eklima.index, format='%d.%m.%Y-%H:%M')
    fig, ax=plt.subplots(3,1, sharex=True)
    df_eklima['TA'].plot(ax=ax[0])
    df_eklima['FF'].plot(ax=ax[1])
    df_eklima['QSI'].plot(ax=ax[2])
    ax[0].set_ylabel('Outdoor temperature [C]')
    return



"""
import matplotlib.pyplot as plt
plt.clf()
df_eklima.describe()
"""