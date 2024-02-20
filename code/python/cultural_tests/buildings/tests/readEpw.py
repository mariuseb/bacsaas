# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 14:04:10 2019

@author: hwaln
"""

import pvlib.iotools.epw as epw

filename='NOR_TD_Trondheim-Voll.012570_TMYx.2003-2017.epw'
refYear=2019

data, meta= epw.read_epw(filename, coerce_year=refYear)

def createSimienFile(data, filename='NOR_TD_Trondheim-Voll.012570_TMYx.2003-2017.dat'):
    cols=['temp_air', 'relative_humidity', 'wind_speed', 'wind_direction', 
          'global_hor_illum', 'diffuse_horizontal_illum', 'dni','dhi' 
          ]
    df=data[cols]
    df.to_csv()