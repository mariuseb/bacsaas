# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 13:29:17 2022

@author: hwaln
"""

import pandas as pd

fname='RDRF.txt'
df=pd.read_csv(fname, sep=';', index_col=0)
df.index=pd.to_datetime(df.index)
