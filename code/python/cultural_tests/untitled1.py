# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 07:33:53 2023

@author: hwaln
"""

import pandas as pd
import os
import numpy as np

new_data_dir = "./recieved/"
parsed_data_dir = "./parsed/"


def concatCustomers(df, comMap={}):
    customers = set(df.CUSTOMER)

    dfs = []
    dfcom = pd.DataFrame()
    i = 1
    for c in customers:
        d = df[df.CUSTOMER == c].copy()
        d.index = pd.to_datetime(d.READING_TIME, format="%d.%m.%y %H:%M")
        d.loc[d.first_valid_index()] = np.nan
        # d = fixDST(d)
        d.index = d.index.tz_localize("Etc/Gmt-1")
        if str(c) in comMap.keys():
            if comMap[str(c)] in dfcom.columns:
                dfcom[comMap[str(c)]].add(d.READING_VALUE * 1000)
            else:
                dfcom[comMap[str(c)]] = d.READING_VALUE * 1000
        else:
            dfs.append((d.READING_VALUE * 1000).rename(f"ElImp_{i}"))
            i += 1
    dfs.append(dfcom)
    df1 = pd.concat(dfs, axis=1)
    return df1


def parse_new_files():
    files = os.listdir(new_data_dir)
    dfs = []
    for f in files:
        dfs.append(pd.read_csv(f, sep=";"))
    df = pd.concat(dfs, ignore_index=True)
