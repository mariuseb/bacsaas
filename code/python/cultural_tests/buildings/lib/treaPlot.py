# -*- coding: utf-8 -*-
"""
Standard Plotting functions for treaData files

Created on Wed Aug 24 08:52:48 2022

@author: hwaln
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import math
import buildings.lib.treaPlot as treaPlot

reaDir=os.path.join(os.path.dirname(__file__), '../resources/')
meaTypes=pd.read_csv(reaDir+'measurement_types.csv', sep=';', index_col='description_short')
meaElHeatProd=['ElBoil', 'ElHP', 'ElHWH', 'ELDHW', 'ElSpace', 'ElSnow']
meaElCoolProd=['ElClTech', 'ElClComf', 'ElClTot']
meaHtIn=[col for col in meaTypes.index if (meaTypes.loc[col]['measurement_category']=='Heat production' or meaTypes.loc[col]['measurement_category']=='Heat import')]+['ElBoil']
meaHtUse=[col for col in meaTypes.index if meaTypes.loc[col]['measurement_category']=='Heat use']

def plotDictAllMeaSep(dTS, d_meta, directory, overwrite=True):
    '''
    Creates plot with a subplot for each measurement for all buildings
    in dictionary

    Parameters
    ----------
    dTS : dictionary
        Dictionary holding timeseries for each building.
    d_meta : dictionary 
        Dictionary holding metadata for each building.
    directory : String
        String with folder for storing plots
    overwrite : Boolean (default=True)
        Boolean for overwriting existing plots

    Returns
    -------
    None.

    '''
    
    existingPlots=os.listdir(directory)
    
    for bui in dTS.keys():
        if (overwrite) or ((bui+'.png') not in existingPlots):   
            if d_meta[bui]['building_category']!='nan':
                plotAllMeaSep(dTS[bui], bui, directory)
                # n_col = len(dTS[bui].columns)
                # width = len(dTS[bui].index) / 180
                # n = 0
                # fig, ax = plt.subplots(n_col,1, figsize=(width, 10 * n_col), num=1,clear=True)
                # for col in dTS[bui].columns:
                #     dTS[bui][col].plot(ax=ax[n], fontsize = 20)
                #     ax[n].set_title(col, fontsize = 30)
                #     ax[n].set_ylabel(col, fontsize = 30)
                #     ax[n].set(xlabel = None)
                #     plt.tight_layout()
                #     n += 1
                # plt.savefig(directory + bui + '.png', format="png")
                # fig.clear()
                # plt.close(fig)
        else:
            print(f'{bui} plot already exists')
    

def plotAllMeaSep(df, bui, directory):
    """
    

    Parameters
    ----------
    dTS : Dataframe
        Pandas Dataframe holding timeseries for the building.
    bui : string
        Building ID used for naming plot.
    directory : string
        directory for where to store plot.

    Returns
    -------
    None.

    """
    plt.ioff() #turns off interactive plotting
    n_col = len(df.columns)
    width = len(df.index) / 180
    n = 0
    fig, ax = plt.subplots(n_col,1, figsize=(width, 10 * n_col), num=1,clear=True, sharex=True)
    for col in df.columns:
        df[col].plot(ax=ax[n], fontsize = 20)
        ax[n].set_title(col, fontsize = 30)
        ax[n].set_ylabel(col, fontsize = 30)
        ax[n].set(xlabel = None)
        plt.tight_layout()
        n += 1
    plt.savefig(directory + bui + '.png', format="png")
    
    plt.ion() #turns on interactive plotting

def splitSubMea(cols):
    cols_sub=[]
    cols_super=[]
    for col in cols:
        if (meaTypes.loc[col].subtypes == meaTypes.loc[col].subtypes): #check if column has subcolumns
           subCols=[c.strip() for c in meaTypes.loc[col].subtypes.split(',')] #get list of subcolumns
           if any(c in subCols for c in cols): #check if any of columns in subcolumns
               if col not in cols_super: cols_super.append(col)
           else:
               for scol in subCols:
                   if (meaTypes.loc[scol].subtypes == meaTypes.loc[scol].subtypes):#check if subcolumns has subcolumns
                       subsubCols=[c.strip() for c in meaTypes.loc[scol].subtypes.split(',')] #get list of subsubcolumns
                       if any(c in subsubCols for c in cols): #check if any of columns in subsubcolumns
                           if col not in cols_super: cols_super.append(col)
                       else:
                           if col not in cols_sub: cols_sub.append(col)
                   else:
                       if col not in cols_sub: cols_sub.append(col)
                           
        else: #no subcolumns
            if col not in cols_sub: cols_sub.append(col)
            
    return cols_sub, cols_super

    
def plotElectricProfile(df, bui, fromDate=None, toDate=None, directory=None):
    fig, ax = plt.subplots(3,1, sharex=True)
    if not fromDate: fromDate=df.index[0].strftime('%Y-%m-%d')
    if not toDate: toDate=df.index[-1].strftime('%Y-%m-%d')
    cols=[col for col in df.columns if col.startswith('El')]
    data=df.loc[fromDate:toDate][cols].copy()
    
    #create common import export data series
    data['ElImp_net']=data['ElImp'].sub(data['ElExp']) if 'ElExp' in cols else data['ElImp']
    if 'ElPV' in cols: #create separate plot with net import
        data['ElPV_neg']=data['ElPV'].mul(-1)
        data['ElImp+PV']=data['ElImp_net'].add(data['ElPV'])
    
    sumColsEl=[col for col in cols if (meaTypes.loc[col].subtypes == meaTypes.loc[col].subtypes)]
    colsElHeat=[col for col in cols if col in meaElHeatProd]
    colsElCool=[col for col in cols if col in meaElCoolProd]
    colsElUse=[col for col in cols if col not in (meaElHeatProd+meaElCoolProd+sumColsEl+['ElImp', 'ElPV', 'ElExp'])]
    
    #create total El plot
    areaLst=colsElUse+colsElCool+colsElHeat
    lineLst=['ElImp_net', 'ElPV', 'ElImp+PV'] if 'ElPV' in cols else ['ElImp']
    plotProfile(data, ax=ax[0], areaLst=areaLst, lineLst=lineLst)
    
    #create El heat plot
    areaLst=colsElHeat
    lineLst=[]
    plotProfile(data, ax=ax[1], areaLst=areaLst, lineLst=lineLst)
    
    #create El specific plot
    areaLst=colsElUse
    lineLst=['ElTot'] if 'ElTot' in cols else []
    plotProfile(data, ax=ax[2], areaLst=areaLst, lineLst=lineLst)
    
    plt.draw()
    
    return fig, ax

def plotHeatProfile(df, bui, fromDate=None, toDate=None, directory=None):
    fig, ax = plt.subplots(2,1, sharex=True)
    if not fromDate: fromDate=df.index[0].strftime('%Y-%m-%d')
    if not toDate: toDate=df.index[-1].strftime('%Y-%m-%d')
    colsIn=[col for col in df.columns if col in (meaHtIn)]
    colsUse=[col for col in df.columns if col in (meaHtUse)]
    colsUseSub, colsUseSuper = splitSubMea(colsUse)
    data=df.loc[fromDate:toDate][colsIn+colsUse].copy()
    
    #create common import export data series
    data['HtIn']=data[colsIn].sum(axis=1, skipna=False)
    
    #create total Ht plot
    areaLst=colsUseSub
    lineLst=['HtIn']
    plotProfile(data, ax=ax[0], areaLst=areaLst, lineLst=lineLst)
       
    #create Ht In
    areaLst=colsIn
    lineLst=['HtTot'] if 'HtTot' in df.columns else []
    plotProfile(data, ax=ax[1], areaLst=areaLst, lineLst=lineLst)
    
    plt.draw()
    
    return fig, ax

def plotProfile(df, ax=None, fromDate=None, toDate=None, areaLst=[], lineLst=[]):
    if not ax: fig, ax = plt.subplots(1,1)
    if not fromDate: fromDate=df.index[0].strftime('%Y-%m-%d')
    if not toDate: toDate=df.index[-1].strftime('%Y-%m-%d')

    if areaLst: df.loc[fromDate: toDate][areaLst].plot.area(ax=ax, linewidth=0)
    if lineLst: df.loc[fromDate: toDate][lineLst].plot(ax=ax)
    ax.relim()
    ax.autoscale()
    return ax
    
