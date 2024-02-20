# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 07:50:02 2023

@author: hwaln
"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

parsed_data_dir = "./parsed/"

apt_rooms = {
    'H0101': ['1060', '1062', '1063', '1064'],
    'H0102': ['1070', '1072', '1073', '1074'],
    'H0103': ['1010', '1012', '1013', '1014'],
    'H0104': ['1020', '1022', '1023', '1024'],
    'H0105': ['1030', '1032', '1033', '1034'],
    'H0106': ['1050', '1052', '1053', '1054'],
    'H0201': ['1060', '1062', '1063', '1064'],
    'H0202': ['2070', '2072', '2073', '2074'],
    'H0203': ['2010', '2012', '2013', '2014'],
    'H0204': ['2020', '2022', '2023', '2024'],
    'H0205': ['2030', '2032', '2033', '2034'],
    'H0206': ['2050', '2052', '2053', '2054'],
}

# appartment agg lists
all_apts = [x for x in apt_rooms.keys()]
first_floor = [x for x in apt_rooms.keys() if 'H01' in x]
second_floor = [x for x in apt_rooms.keys() if 'H02' in x]

south_facade = ['H0102', 'H0103', 'H0104', 'H0202', 'H0203', 'H0204']
north_facade = ['H0101', 'H0105', 'H0106', 'H0201', 'H0205', 'H0206']


def concat_log(directory=parsed_data_dir):
    dfs=[]
    for f in os.listdir(directory):
        dfs.append(pd.read_csv(directory+f, sep=';', index_col=0, parse_dates=True))
    
    df=pd.concat(dfs)
    return df


def search_tags(search_list, system=None, subsystem=None, component=None):

    # search system
    if system is None:
        res_tags = search_list
    else:
        res_tags = [x for x in search_list if f'_{system}_' in x]

    # search subsystem
    if subsystem is None:
        res_tags = res_tags
    else:
        res_tags = [x for x in res_tags if f'_{subsystem}_' in x]

    # search component id
    if component is None:
        res_tags = res_tags
    else:
        res_tags = [x for x in res_tags if f'{component}' in x]

    return res_tags


def create_tag(system, subsystem, component):
    return '_'.join(['1273', system, subsystem, component])


def plot_apt(df, apt='H0101', freq='5T', acc=False):
    fig, ax = plt.subplots(4, 1, sharex=True)
    
    # temperatures
    ax_=ax[0]
    tag_list=[]
    # room temperature
    for room in apt_rooms[apt]:
        tag_list.append(create_tag('563', room, 'RT601'))
    # ventilation extract
    tag_list.append(create_tag('360', apt[2:], 'RT501'))
    # plot
    df[tag_list].resample(freq).nearest().plot(ax=ax_, lw=0.5)
    
    #mean room temp
    df[tag_list[:-2]].mean(axis=1).resample(freq).nearest().plot(ax=ax_)
    
    ax_.legend(apt_rooms[apt]+['Vent_ext']+['mean'])

    # actuators
    ax_= ax[1]
    tag_list = []
    for room in apt_rooms[apt]:
        tag_list+=search_tags(df.columns, system='563', subsystem=room, component='SC')
        tag_list+=search_tags(df.columns, system='563', subsystem=room, component='LZ')
    # plot
    df[tag_list].resample(freq).mean().plot(ax=ax_, drawstyle='steps-post')
    ax_.legend(['_'.join(x.split('_')[2:]) for x in tag_list])
    
    # heating
    ax_= ax[2]
    tag_list = []
    tag_list += search_tags(df.columns, system='320', subsystem='002', component=f'OE{apt[2:]}')
    
    if acc:
        df[tag_list].resample(freq).nearest().plot(ax=ax_, drawstyle='steps-post')
    else:
        df[tag_list].diff().resample(freq).sum().plot(ax=ax_, drawstyle='steps-post')
    ax_.legend(['Space Heating'])
    
    # hot water
    ax_= ax[3]
    tag_list = []
    tag_list += search_tags(df.columns, system='310', subsystem='001', component=f'RF{apt[2:]}')
    if acc:
        df[tag_list].resample(freq).nearest().plot(ax=ax_, drawstyle='steps-post')
    else:
        df[tag_list].diff().resample(freq).sum().plot(ax=ax_, drawstyle='steps-post')
    ax_.legend(['DHW'])


def plot_agg_apt(df, apts, freq='5T', acc=False):
    fig, ax = plt.subplots(3, 1, sharex=True)
    
    # temperatures
    ax_=ax[0]
    tag_list=[]
    # room temperature
    for apt in apts:
        tag_list_apt=[]
        for room in apt_rooms[apt]:
            tag_list_apt.append(create_tag('563', room, 'RT601'))
        tag_list_apt=tag_list_apt[:-1]  # Remove bathroom
        # plot
        df[tag_list_apt].mean(axis=1).resample(freq).nearest().plot(ax=ax_, lw=0.5)
        tag_list += tag_list_apt
    #mean room temp
    df[tag_list].mean(axis=1).resample(freq).nearest().plot(ax=ax_)
    ax_.legend(apts+['mean'])


    
    # heating
    ax_= ax[1]
    tag_list = []
    for apt in apts:
        tag_list += search_tags(df.columns, system='320', subsystem='002', component=f'OE{apt[2:]}')
    
    if acc:
        df[tag_list].sub(df[tag_list].iloc[0]).sum(axis=1).resample(freq).nearest().plot(ax=ax_, drawstyle='steps-post')
    else:
        df[tag_list].diff().sum(axis=1).resample(freq).sum().plot(ax=ax_, drawstyle='steps-post')
    ax_.legend(['Space Heating'])
    
    # hot water
    ax_= ax[2]
    tag_list = []
    for apt in apts:
        tag_list += search_tags(df.columns, system='310', subsystem='001', component=f'RF{apt[2:]}')
        
    if acc:
        df[tag_list].sub(df[tag_list].iloc[0]).sum(axis=1).resample(freq).nearest().plot(ax=ax_, drawstyle='steps-post')
    else:
        df[tag_list].diff().sum(axis=1).resample(freq).sum().plot(ax=ax_, drawstyle='steps-post')
    ax_.legend(['DHW'])