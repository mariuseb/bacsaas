# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 09:39:59 2018

@author: hwaln
"""

import pandas as pd
import matplotlib.pyplot as plt
import metdata as met
import csv as csv
import datetime
import buildingdata.lib.zenCSV as zen
import numpy as np
import buildingdata.lib.buildings as bd
import pickle
import pathlib
import math
from geopy.geocoders import Nominatim
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.dates as mdates
from matplotlib.lines import Line2D

#set path data
fname = '../../Data/Fortum/ZENcsv/Tot.csv'
directory = '../../Data/Statkraft/ZENcsv/Kindergarten/'
#df=zen.getZENcsvTimeSeries(fname,17)
"""
Read and write data from ZEN csv to prediction models.

"""
plt.rcParams["font.family"] = "Times New Roman"

#def readAllcsvsFromFolder(directory):
#    Mdict, Bdict=zen.readAllcsvsFromFolder(directory)
#    return Mdict, Bdict

## save and load pickle files
def saveDict(d, name):
    #pickle
    file = open('pickle/' + name + '.dat','wb')
    pickle.dump(d,file,protocol=pickle.HIGHEST_PROTOCOL)
    return

def loadDict(name):
    #read data
    file = open(name,'rb')
    d = []
    d = pickle.load(file)
    file.close()
    return d

def loadAllFiles(directory):
    d={}
    d['AB']=loadDict(directory+'AB.dat')
    d['CB']=loadDict(directory+'CB.dat')
    d['CL']=loadDict(directory+'CL.dat')
    d['HO']=loadDict(directory+'HO.dat')
    d['HS']=loadDict(directory+'HS.dat')
    d['KG']=loadDict(directory+'KG.dat')
    d['NH']=loadDict(directory+'NH.dat')
    d['OF']=loadDict(directory+'OF.dat')
    d['SC']=loadDict(directory+'SC.dat')
    d['SF']=loadDict(directory+'SF.dat')
    d['SM']=loadDict(directory+'SM.dat')
    d['UC']=loadDict(directory+'UC.dat')
    return d

def loadSelectedFiles(directory, blist):
    d={}
    for b in blist:
        d[b]=loadDict(directory+b+'.dat')
    return d

#create a set of csv.
def createRegFilesFromZenBdict(d, endpath, season=None, day=None, normalize=False):
    for key in d:
        df=d[key].copy()
        if normalize:
            df.HtTot=df.HtTot.groupby([df.index.month, df.index.day, df.data_reg.index.hour]).mean().mean()*365*24
        createRegFileFromDf(df, endpath, key, season=season, day=day)
    return

#create a set of csv.
def createRegFilesFromBuildingDict(d, endpath, season=None, day=None, normalize=False):
    for key in d:
        createRegFilesFromBuilding(d[key], endpath, season=season, day=day, normalize=normalize)
    return

def createRegFilesFromBuilding(b, endpath, season=None, day=None, normalize=False):
    df=b.data_reg.copy()
    if normalize:
        df.HtTot=df.HtTot/b.yearlyHeatConsumption
    createRegFileFromDf(df, endpath, b.name, season=season, day=day)
    return


def createRegFileFromDf(df, endpath, name, season=None, day=None):
    df=bd.addDateInfo(df)
    wdStr='_Tot'
    seStr='_Tot'
    if day:
        if day=='wd':
            df=df[df.WorkingDay==1]
            wdStr='_wd'
        elif day=='we':
            df=df[df.WorkingDay==0]
            wdStr='_we'
        else:
            print('ERROR: Undefined WorkingDay opt., must be one of: wd or we')
            return
    if season:
        df_W, df_S, df_M = bd.splitSeasons(df)
        if season == 'Winter':
            seStr='_w'
            df_W.to_csv(endpath+name+seStr+wdStr+'.csv')
        elif season == 'Summer':
            seStr='_s'
            df_S.to_csv(endpath+name+seStr+wdStr+'.csv')
        elif season == 'Middle':
            seStr='_m'
            df_M.to_csv(endpath+name+seStr+wdStr+'.csv')
        else:
            print('ERROR: Undefined Season, must be one of: Winter, Summer or Middle')
            return
    else:
        df.to_csv(endpath+name+seStr+wdStr+'.csv')
    return

def createBuildingFromZENcsvData(fname):
    name=fname.split('.')[0]
    building=bd.building(name=name)
    m,d=zen.getZENcsv(fname)
    building.zenMetaData=m
    building.yearlyHeatConsumption=d.HtTot.groupby([d.index.month, d.index.day, d.index.hour]).mean().mean()*365*24
    building.setRegData(d)
    return building

def createBuildingsFromZENcsvFolder(directory):
    Mdict, Bdict=zen.readAllcsvsFromFolder(directory)
    buildDict={}
    for key in Mdict:
        building=bd.building(name=key)
        building.zenMetaData=Mdict[key]
        building.yearlyHeatConsumption=Bdict[key].HtTot.groupby([Bdict[key].index.month, Bdict[key].index.day, Bdict[key].index.hour]).mean().mean()*365*24
        building.setRegData(Bdict[key])
        buildDict[key]=building
    return buildDict

def plotSepWeekdayLines (v1, name, unit, err=False):
    linew=0.5
    #fname = v1.name.split('[')[0]+'SepWeekdayLines'
    cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df=v1.to_frame(v1.name)
    df['Weekday'] = df.index.weekday_name
    df['Weekday']=pd.Categorical(df['Weekday'],categories = cats)
    if err:
        mean = df.groupby([df.index.time, 'Weekday'])[v1.name].mean().unstack()
        err = df.groupby([df.index.time, 'Weekday'])[v1.name].std().unstack()
        ax=mean.plot(lw=linew,subplots=True, sharex=True, sharey=True, yerr=err, capsize=4)
    else:
        df = df.groupby([df.index.time, 'Weekday'])[v1.name].mean().unstack()
        ax=df.plot(lw=linew,subplots=True, sharex=True, sharey=True)
    plt.xticks(np.arange(0,86400,7200))
    #plt.figure().autofmt_xdate()
    for sp in ax.flat:
        sp.set_ylabel(unit)    #ax.layout(3,3)
    return;

def plotSepWorkingDayLines (v1, name, unit, err=False):
    linew=0.5
    df=v1.to_frame(v1.name)
    df['WorkingDay'] = (df.index.dayofweek<5).astype(int)
    if err:
        mean = df.groupby([df.index.time, 'WorkingDay'])[v1.name].mean().unstack()
        err = df.groupby([df.index.time, 'WorkingDay'])[v1.name].std().unstack()
        ax=mean.plot(lw=linew,subplots=True, sharex=True, sharey=True, yerr=err, capsize=4)
    else:
        df = df.groupby([df.index.time, 'WorkingDay'])[v1.name].mean().unstack()
        ax=df.plot(lw=linew,subplots=True, sharex=True, sharey=True)
    plt.xticks(np.arange(0,86400,7200))
    #plt.figure().autofmt_xdate()
    for sp in ax.flat:
        sp.set_ylabel(unit)    #ax.layout(3,3)
    return;

def plotAllBuildingsHTotalvsPeak(bDict, col='black', linfit=False):
    HTotal = np.zeros(len(bDict))
    Peak = np.zeros_like(HTotal)
    i=0
    for key in bDict:
        HTotal[i]=bDict[key].yearlyHeatConsumption
        Peak[i]=bDict[key].data_reg.HtTot.max()
        i+=1
    plt.plot(HTotal/1000,Peak , 'o', color=col)
    plt.ylabel('Peak load [kW]')
    plt.xlabel('Annual Energy Consumption [MWh]')
    
    if linfit:
        reg = linear_model.LinearRegression()
        reg.fit(HTotal[:,None]/1000, Peak)
        Peak_pred=reg.predict(HTotal[:,None]/1000)
        plt.plot(HTotal/1000,Peak_pred, label=f'y={reg.intercept_:g}+x*{reg.coef_[0]:g}', color=col)
        plt.legend()
        plt.title(f'R^2={r2_score(Peak,Peak_pred):g}')
    return HTotal, Peak
    
def createScatterMatrices(d, directory):
    for key in d:
        pd.plotting.scatter_matrix(d[key].data_reg)
        plt.savefig(directory+str(key)+'.png', dpi=400)
        plt.clf()
        plt.close()
    return 

def plotAllHtvsTout(d, directory):
    for key in d:
        d[key].data_reg.plot.scatter(x='Tout', y='HtTot')
        plt.savefig(directory+str(key)+'.png', dpi=400)
        plt.clf()
        plt.close()
    return

def plotAllLoadProfiles(d, directory, norm=False):
    for key in d:
        if not (norm):
            d[key].data_reg.HtTot.sort_values(ascending=False).reset_index().HtTot.plot()
            plt.ylabel('Load [kW]')
            plt.xlabel('Hours')
            plt.savefig(directory+str(key)+'_LP.png', dpi=400)
        else:
            (d[key].data_reg.HtTot.sort_values(ascending=False).reset_index().HtTot/d[key].data_reg.HtTot.max()*100).plot()
            plt.ylabel('Load [%]')
            plt.xlabel('Hours')
            plt.savefig(directory+str(key)+'_LPrel.png', dpi=400)
        plt.clf()
        plt.close()
    return

def plotCommonLoadProfiles(d,norm=False, store=False):
    for key in d:
        if not (norm):
            d[key].data_reg.HtTot.sort_values(ascending=False).reset_index().HtTot.plot()

        else:
            (d[key].data_reg.HtTot.sort_values(ascending=False).reset_index().HtTot/d[key].data_reg.HtTot.max()*100).plot()

    if not (norm):
        plt.ylabel('Load [kW]')
    else:
        plt.ylabel('Load [%]')
    plt.xlabel('Hours')
    return


def createHtPlot(d, period, normalize=False):
    ax=plt.plot()
    lw1=0.5
    lw2=2
    norm=1
    for key in d:
        if normalize:
            norm=d[key].HtTot.sum()
        if key=='Tot':
            ax=(d[key].HtTot[period]/norm).plot(lw=lw2)
        else:
            ax=(d[key].HtTot[period]/norm).plot(lw=lw1)
    return ax

def rollingMaxDf(d, normalize=False, pred=False):
    dfmax = pd.DataFrame(columns=['Time [H]'])
    for i in range(0,24):
        dfmax.loc[i]=i+1   
    for key in d:
        try:
            if pred=='Season':
                peak=d[key].data_reg.HtTot_predS.max()
            elif pred=='Year':
                peak=d[key].data_reg.HtTot_predY.max()
            else:
                peak=d[key].data_reg.HtTot.max()
        except:
            print('Warning')
        s = pd.Series()
        for i in range(0,24):
            freq = str(i+1)+'H'
            if normalize:
                try:
                    if pred=='Season':
                        s.loc[i]=(d[key].data_reg.HtTot_predS.rolling(freq).mean().max())/peak
                    elif pred =='Year':
                        s.loc[i]=(d[key].data_reg.HtTot_predY.rolling(freq).mean().max())/peak
                    else:
                        s.loc[i]=(d[key].data_reg.HtTot.rolling(freq).mean().max())/peak
                except:
                    print('Warning')
            else:
                try:
                    if pred=='Season':
                        s.loc[i]=(d[key].data_reg.HtTot_predS.rolling(freq).mean().max())
                    elif pred=='Year':
                        s.loc[i]=(d[key].data_reg.HtTot_predY.rolling(freq).mean().max())    
                    else:
                        s.loc[i]=(d[key].data_reg.HtTot.rolling(freq).mean().max())
                except:
                    print('Warning')
                        
        dfmax[key]=s
    dfmax.set_index('Time [H]', inplace=True)
    return dfmax

def createRollingHist(d, pltLst, catName):
    dfmax=rollingMaxDf(d, normalize=True)
    bins=np.linspace(0,1,21)
    for i in pltLst:
        dfmax.loc[i].plot.hist(bins=bins)
        #plt.xlim(0,1)
        plt.xlabel('Peak relative to maximum 1 hour peak')
        plt.ylabel('Number of buildings')
        plt.savefig('../plot/Statkraft/'+catName+'/'+str(i)+'H_hist.png', dpi=400, bbox_inches='tight')
        plt.close()
        
def createCommonRollingHist(d, pltLst, catName):
    fig,ax =  plt.subplots(1,len(pltLst), figsize=(5*len(pltLst),5), sharey=True)
    dfmax=rollingMaxDf(d, normalize=True)
    bins=np.linspace(0,1,21)
    k=0
    for i in pltLst:
        dfmax.loc[i].plot.hist(bins=bins, ax=ax[k])
        #plt.xlim(0,1)
        ax[k].set_xlabel('Peak relative to maximum 1 hour peak')
        ax[k].set_title(str(i)+' hour average')
        k+=1
    
    ax[0].set_ylabel('Number of buildings')
    plt.savefig('../plot/Statkraft/'+catName+'/Common_hist.png', dpi=400, bbox_inches='tight')
    plt.close()
    
def createCommonMaHistMat(d, pltLst, nmLst, norm=False, pred=False):
    columns = pd.MultiIndex.from_product([pltLst, ['mean', 'std', 'min (20%)', 'max (20%)']], names=['Hours', 'Results'])
    df=pd.DataFrame(columns=columns, index=nmLst)
    fig,ax =  plt.subplots(len(d),len(pltLst), figsize=(2.5*len(pltLst),1.3*len(nmLst)), sharex='col', sharey='row')
    bins=np.linspace(0,1,21)
    j=0
    for key in d:
        dfmax=rollingMaxDf(d[key], normalize=True, pred=pred)
        k=0
        for i in pltLst:
            if norm:
                weights=pd.Series(1./dfmax.loc[i].dropna().size, index = dfmax.loc[i].dropna().index)
                (1-dfmax.loc[i].dropna()).plot.hist(bins=bins, ax=ax[j,k], weights=weights)
            else:
                (1-dfmax.loc[i]).plot.hist(bins=bins, ax=ax[j,k])
            df.loc[nmLst[j]][i]['mean']=1-dfmax.loc[i].mean()
            df.loc[nmLst[j]][i]['std']=dfmax.loc[i].std()
            df.loc[nmLst[j]][i]['min (20%)']=1-dfmax.loc[i].quantile(0.8)
            df.loc[nmLst[j]][i]['max (20%)']=1-dfmax.loc[i].quantile(0.2)
            #plt.xlim(0,1)
            k+=1
        
        ax[j,0].set_ylabel(nmLst[j])
        if norm:
            ax[j,0].set_ylim(0, 0.8)
            ax[j,0].set_yticks(np.linspace(0, 0.8, 5))
        j+=1
    k=0
    for i in pltLst:
        ax[0,k].set_title(str(i)+' hour average')
        ax[len(d)-1,k].set_xlabel(r'$P_{flex}$')
        ax[len(d)-1,k].set_xticks(np.linspace(0, 1, 6))
        k+=1
    fig.align_ylabels(ax[:, 0])
    
    fig.text(0.04, 0.5, '% of number of buildings', va='center', rotation='vertical')
    
    return df
    

def plotAllBuildingtdaySpline(bDict, season='Winter', workday=True):
    ax=plt.plot()
    lw=0.5
    for key in bDict:
        if workday:
            if bDict[key].Winter_wd.set:
                ax=bd.plotDaySpline(bDict[key].Winter_wd.spl, lw=lw)
        else:
            if bDict[key].Winter_we.set:
                ax=bd.plotDaySpline(bDict[key].Winter_we.spl, lw=lw)
                
    return ax

def plotBuildingtdaySplineComparison(b, season='Winter', workday=True, weekend=True):
    fig, ax = plt.subplots(1,1, figsize=(7.5,7.5))
    lw=1
    lab=[]
    x=np.linspace(0, 23, 24)
    if workday:
        if b.Year_wd.set:
            ax.plot(x, b.Year_wd.spl(x), lw=lw)
            lab.append('Full year workday')
    if weekend:
        if b.Year_we.set:
            ax.plot(x, b.Year_we.spl(x), lw=lw)
            lab.append('Full year weekend')
    
    if (season=='Winter'):
        if workday:
            if b.Winter_wd.set:
                ax.plot(x, b.Winter_wd.spl(x), lw=lw)
                lab.append('Season workday')
        if weekend:
            if b.Winter_we.set:
                ax.plot(x, b.Winter_we.spl(x), lw=lw)
                lab.append('Season weekend')
    if (season=='Summer'):
        if workday:
            if b.Summer_wd.set:
                ax.plot(x, b.Summer_wd.spl(x), lw=lw)
                lab.append('Season workday')
        if weekend:
            if b.Summer_we.set:
                ax.plot(x, b.Summer_we.spl(x), lw=lw)
                lab.append('Season weekend')
    if (season=='Middle'):
        if workday:
            if b.Middle_wd.set:
                ax.plot(x, b.Middle_wd.spl(x), lw=lw)
                lab.append('Season workday')
        if weekend:
            if b.Middle_we.set:
                ax.plot(x, b.Middle_we.spl(x), lw=lw)
                lab.append('Season weekend')
    
    ax.set_ylabel('Heating power [kW]')
    ax.set_xlabel('Hour of day')
    ax.legend(ax.lines, lab, loc=0)
    
    return
    
#df=addDateInfo(df)
#df_W, df_S, df_M = splitSeasons(df)


#building.predictData()

"""
Work with prediction models
"""
def setAllBuildingPredModelsFromDir(bDict, predDir, r2Tresh):
    for key in bDict:
        bDict[key].setBildingPredModelsFromDir(predDir, r2Tresh=r2Tresh)
    return bDict

def setNewDataToAllBuildingPredModels(bDict, data):
    for key in bDict:
        bDict[key].setNewData(data)
    return bDict

def removeAllBuildingsWithoutPredModel(bDict, Winter=False, Summer=False, Middle=False):
    remList=[]
    for key in bDict:
        delete=False
        if Winter:
            if not bDict[key].Winter_wd.set or not bDict[key].Winter_we.set : delete=True
        if Summer:
            if not bDict[key].Summer_wd.set or not bDict[key].Summer_we.set : delete=True
        if Middle:
            if not bDict[key].Middle_wd.set or not bDict[key].Middle_we.set : delete=True
        if delete:
            remList.append(key)
        
    for b in remList:
        bDict.pop(b, 'empty')
        print(b + ' removed from building dictionary')
    return bDict

def selectAllBuildingsWithGoodModels(bDict, r2Tresh=0.8, Winter=False, Summer=False, Middle=False, Year=False):
    d={}
    for key in bDict:
        keep=True
        if Winter:
            if not (bDict[key].Winter_wd.r2 > r2Tresh) or not (bDict[key].Winter_we.r2 > r2Tresh) : keep=False
        if Summer:
            if not (bDict[key].Summer_wd.r2 > r2Tresh) or not (bDict[key].Summer_we.r2 > r2Tresh) : keep=False
        if Middle:
            if not (bDict[key].Middle_wd.r2 > r2Tresh) or not (bDict[key].Middle_we.r2 > r2Tresh) : keep=False
        if Year:
            if not (bDict[key].Year_wd.r2 > r2Tresh) or not (bDict[key].Year_we.r2 > r2Tresh) : keep=False
        if keep:
            d[key]=bDict[key]
    return d

def selectAllCatBuildingsWithGoodModels(abDict, r2Tresh=0.8, Winter=False, Summer=False, Middle=False, Year=False):
    d={}
    for key in abDict:
        d[key]=selectAllBuildingsWithGoodModels(abDict[key], r2Tresh=r2Tresh, Winter=Winter, Summer=Summer, Middle=Middle, Year=Year)
    return d

def predictAllbDictBuildingsWithRegDataSeason(bDict):
    for key in bDict:
        print(f'Predicting {bDict[key].name}')
        bDict[key].predictRegData()
    return

def predictAllbDictBuildingsWithRegDataYear(bDict):
    for key in bDict:
        print(f'Predicting {bDict[key].name}')
        bDict[key].predictRegData(year=True)
    return

def predictAllbDictBuildingsWithNewData(bDict):
    for key in bDict:
        print(f'Predicting {bDict[key].name}')
        bDict[key].predictNewData()
    return


#get outdoor temperature time seris from met
def getMetData(stationId, start, end): #timeformat: YYYY-MM-DD
    Tout = met.getMetDataTimeSeries(stationId, 'mean(air_temperature PT1H)', start, end)
    if not isinstance(Tout, pd.DataFrame):
        Tout = met.getMetDataTimeSeries(stationId, 'air_temperature', start, end)
    Tout.index=Tout.index.tz_localize('Etc/GMT', ambiguous='infer')
    Tout.index=Tout.index.tz_convert('Europe/Oslo')
    Tout.index=Tout.index.tz_localize(None)
    Tout.columns=['Tout']
    return Tout

def plotAllBuildingsPredHTotalvsPeak(bDict, reg=False, linfit=False):
    HTotal = np.zeros(len(bDict))
    Peak = np.zeros_like(HTotal)
    i=0
    if not reg:
        for key in bDict:
            HTotal[i]=bDict[key].yearlyHeatConsumption
            Peak[i]=bDict[key].data_new.HtTot_pred.max()
            i+=1
        plt.plot(HTotal/1000,Peak , 'o', color='red')
    else:
        for key in bDict:
            HTotal[i]=bDict[key].yearlyHeatConsumption
            Peak[i]=bDict[key].data_reg.HtTot_pred.max()
            i+=1
            plt.plot(HTotal/1000,Peak , 'o', color='blue')
    plt.ylabel('Peak load [kW]')
    plt.xlabel('Annual Energy Consumption [MWh]')
    
    if linfit:
        reg = linear_model.LinearRegression()
        reg.fit(HTotal[:,None]/1000, Peak)
        Peak_pred=reg.predict(HTotal[:,None]/1000)
        if not reg:
            plt.plot(HTotal/1000,Peak_pred, label=f'y={reg.intercept_:g}+x*{reg.coef_[0]:g}', color='red')
        else:
            plt.plot(HTotal/1000,Peak_pred, label=f'y={reg.intercept_:g}+x*{reg.coef_[0]:g}', color='blue')
        plt.legend()
        plt.title(f'R^2={r2_score(Peak,Peak_pred):g}')
    return HTotal, Peak

def plotCategoryPredictorR2vsHtotal(bDict):
    fig, axes = plt.subplots(2,1, figsize=(10,10))
    for key in bDict:
        axes[0].plot(bDict[key].yearlyHeatConsumption/1000, bDict[key].Winter_wd.r2, 'o', color='blue')
        axes[1].plot(bDict[key].yearlyHeatConsumption/1000, bDict[key].Winter_we.r2, 'o', color='blue')
        axes[0].plot(bDict[key].yearlyHeatConsumption/1000, bDict[key].Middle_wd.r2, 'o', color='green')
        axes[1].plot(bDict[key].yearlyHeatConsumption/1000, bDict[key].Middle_we.r2, 'o', color='green')
        axes[0].plot(bDict[key].yearlyHeatConsumption/1000, bDict[key].Summer_wd.r2, 'o', color='red')
        axes[1].plot(bDict[key].yearlyHeatConsumption/1000, bDict[key].Summer_we.r2, 'o', color='red')
        axes[0].plot(bDict[key].yearlyHeatConsumption/1000, bDict[key].Year_wd.r2, 'o', color='brown')
        axes[1].plot(bDict[key].yearlyHeatConsumption/1000, bDict[key].Year_we.r2, 'o', color='brown')
        
    axes[0].set_ylim([0,1])
    axes[1].set_ylim([0,1])
    axes[0].set_xlim(left=10)
    axes[1].set_xlim(left=10)
    
    axes[0].set_ylabel('R^2')
    axes[1].set_ylabel('R^2')
    axes[1].set_xlabel('Yearly heat consumption [MWh]')
    axes[1].set_xlabel('Yearly heat consumption [MWh]')
    axes[1].set_xscale('log')
    axes[0].set_xscale('log')
    
    axes[0].set_title('Weekdays')
    axes[1].set_title('Weekends')
    
    fig.legend([axes[0].lines[0], axes[0].lines[1], axes[0].lines[2], axes[0].lines[3]], 
               ['Winter', 'Middle', 'Summer', 'Full year'], loc = 'lower center', ncol=4)
    return

def plotAllPredictorR2vsHtotal(abDict, season='All', year=True, linfit=False, horizontal=False):
    if horizontal:
        fig, axes = plt.subplots(1,2, figsize=(7.5,4), sharey=True)
        mks=3
    else:
        fig, axes = plt.subplots(2,1, figsize=(7.5,7.5))
        mks=5
    Htot=[] 
    r2_wd=[] 
    r2_we=[]
    for key in abDict:
        bDict=abDict[key]
        for key in bDict:
            if season:
                if (season=='Winter' or season=='All'):
                    axes[0].plot(bDict[key].yearlyHeatConsumption/1000, bDict[key].Winter_wd.r2, 'o', color='blue', markersize=mks)
                    if not math.isnan(bDict[key].Winter_wd.r2):
                        Htot.append(bDict[key].yearlyHeatConsumption/1000)
                        r2_wd.append(bDict[key].Winter_wd.r2)    
                    axes[1].plot(bDict[key].yearlyHeatConsumption/1000, bDict[key].Winter_we.r2, 'o', color='blue', markersize=mks)
                    if not math.isnan(bDict[key].Winter_we.r2):
                        r2_we.append(bDict[key].Winter_we.r2)
                if (season=='Middle' or season=='All'):        
                    axes[0].plot(bDict[key].yearlyHeatConsumption/1000, bDict[key].Middle_wd.r2, 'o', color='green', markersize=mks)
                    if not math.isnan(bDict[key].Middle_wd.r2):
                        Htot.append(bDict[key].yearlyHeatConsumption/1000)
                        r2_wd.append(bDict[key].Middle_wd.r2)
                    axes[1].plot(bDict[key].yearlyHeatConsumption/1000, bDict[key].Middle_we.r2, 'o', color='green', markersize=mks)
                    if not math.isnan(bDict[key].Middle_we.r2):
                        r2_we.append(bDict[key].Middle_we.r2)
                if (season=='Summer' or season=='All'):
                    axes[0].plot(bDict[key].yearlyHeatConsumption/1000, bDict[key].Summer_wd.r2, 'o', color='red', markersize=mks)
                    if not math.isnan(bDict[key].Summer_wd.r2):
                        Htot.append(bDict[key].yearlyHeatConsumption/1000)
                        r2_wd.append(bDict[key].Summer_wd.r2)
                    axes[1].plot(bDict[key].yearlyHeatConsumption/1000, bDict[key].Summer_we.r2, 'o', color='red', markersize=mks)
                    if not math.isnan(bDict[key].Summer_we.r2):
                        r2_we.append(bDict[key].Summer_we.r2)
            if year:
                axes[0].plot(bDict[key].yearlyHeatConsumption/1000, bDict[key].Year_wd.r2, 'o', color='brown', markersize=mks)
                if not math.isnan(bDict[key].Year_wd.r2):
                    Htot.append(bDict[key].yearlyHeatConsumption/1000)
                    r2_wd.append(bDict[key].Year_wd.r2)
                axes[1].plot(bDict[key].yearlyHeatConsumption/1000, bDict[key].Year_we.r2, 'o', color='brown', markersize=mks)
                if not math.isnan(bDict[key].Year_we.r2):
                    r2_we.append(bDict[key].Year_we.r2)
        
    axes[0].set_ylim([0,1])
    axes[1].set_ylim([0,1])
    axes[0].set_xlim(left=10)
    axes[1].set_xlim(left=10)
    
    axes[0].set_ylabel('R$^2$')
    if not horizontal: axes[1].set_ylabel('R$^2$')
    if horizontal: axes[0].set_xlabel('Yearly heat consumption [MWh]')
    axes[1].set_xlabel('Yearly heat consumption [MWh]')
    axes[1].set_xscale('log')
    axes[0].set_xscale('log')
    
    axes[0].set_title('Weekdays')
    axes[1].set_title('Weekends')
    
    if horizontal: plt.subplots_adjust(wspace=0.05)
    
    if season:
        if year:
            fig.legend([axes[0].lines[0], axes[0].lines[1], axes[0].lines[2], axes[0].lines[3]], 
                       ['Winter', 'Shoulder', 'Summer', 'Full year'], loc = 'lower center', ncol=4)
        else:
            fig.legend([axes[0].lines[0], axes[0].lines[1], axes[0].lines[2]], 
                       ['Winter', 'Shoulder', 'Summer'], loc = 'lower center', ncol=4)
    if linfit:
        Htot=np.array(Htot)
        r2_wd=np.array(r2_wd)
        r2_we=np.array(r2_we)
        lm = linear_model.LinearRegression()
        lm.fit(Htot[:,None], r2_wd)
        pred=lm.predict(np.logspace(1,4,50)[:,None])
        axes[0].plot(np.logspace(1,4,50),pred, color='black')
        lm = linear_model.LinearRegression()
        lm.fit(Htot[:,None], r2_we)
        pred=lm.predict(np.logspace(1,4,50)[:,None])
        axes[1].plot(np.logspace(1,4,50),pred, color='black')
    return

def R2summary(d):
    index = pd.MultiIndex.from_product([['Winter', 'Middle', 'Summer', 'Year'], ['wd', 'we']], names=['Season', 'Day'])
    df=pd.DataFrame(index=index, columns=d.keys())
    for key in d:
        df.loc['Winter', 'wd'][key]=d[key].Winter_wd.r2
        df.loc['Winter', 'we'][key]=d[key].Winter_we.r2
        df.loc['Middle', 'wd'][key]=d[key].Middle_wd.r2
        df.loc['Middle', 'we'][key]=d[key].Middle_we.r2
        df.loc['Summer', 'wd'][key]=d[key].Summer_wd.r2
        df.loc['Summer', 'we'][key]=d[key].Summer_we.r2
        df.loc['Year', 'wd'][key]=d[key].Year_wd.r2
        df.loc['Year', 'we'][key]=d[key].Year_we.r2
    return df


def createCommonPredHistMat(d, nmLst, pltLst=[['Winter', 'wd'],['Winter','we']]):
    fig,ax =  plt.subplots(len(d),len(pltLst), figsize=(3*len(pltLst),3*len(d)), sharex='col', sharey='row')
    bins=np.linspace(0,1,11)
    j=0
    for key in d:
        dfR2=R2summary(d[key])
        k=0
        for i in pltLst:
            dfR2.loc[i[0],i[1]].plot.hist(bins=bins, ax=ax[j,k])
            k+=1
        
        ax[j,0].set_ylabel(nmLst[j])
        j+=1
    k=0
    for i in pltLst:
        ax[0,k].set_title(i[0] +' '+i[1])
        ax[len(d)-1,k].set_xlabel('R^2')
        k+=1
    fig.align_ylabels(ax[:, 0])
    return

def createLpHistMat(d, model='Season'):
    s=pd.Series(index=d.keys())
    for key in d:
        if model=='Season':
            s.loc[key]=d[key].lp_alphaS
        elif model=='Year':
            s.loc[key]=d[key].lp_alphaS
        else:
            print('Warning: create LpHistMat: undefined model')
            return
    s.plot.hist()
    return
    

def plotMeasuredDataAndPredictions(b, start, end, measured = True, season=True, year=True, Tamb=False, Tlp=False):
    fig, ax = plt.subplots(1,1, figsize=(7.5,7.5))
    ax_sec=ax.twinx()
    lab=[]
    lines=[]
    
    if (measured) : 
        b.data_reg.HtTot[start:end].plot(label='Measured', lw=1.5, ax=ax)
        lab.append('Measured')
    if (season) : 
        b.data_reg.HtTot_predS[start:end].plot(label='Season prediction', lw=1, ax=ax)
        lab.append('Season prediction')
    if (year) : 
        b.data_reg.HtTot_predY[start:end].plot(label='Full year prediction', lw=1, ax=ax)
        lab.append('Full year prediction')
    if (Tamb) : 
        b.data_reg.Tout[start:end].plot(label='Outdoor temperature', color='black', lw=1, ax=ax_sec)
        lab.append('Outdoor temperature')
    if (Tlp): 
        if(season) : b.data_reg.ToutlpS[start:end].plot(label='Outdoor temperature', lw=1, ax=ax_sec)
        if (year) : b.data_reg.ToutlpY[start:end].plot(label='Outdoor temperature', lw=1, ax=ax_sec)
    
    ax.set_ylabel('Heating power [kW]')
    ax.set_xlabel('')
    ax_sec.set_ylabel('Outdorr Temperature [$^\circ$C]')
    
    ax.legend(ax.lines + ax_sec.lines, lab, loc='upper left') 
    
    return

def createSingleDayPred (b, toutlp, season='Winter', WorkingDay=1):
    df=pd.DataFrame(index=np.linspace(0,23,24), columns=['tday', 'ToutlpS','ToutlpY', 'Season', 'Ht_pred' ])
    df['tday']=np.linspace(0,23,24)
    df['ToutlpS']=toutlp
    df['ToutlpS']=toutlp
    df['Season']=season
    df['WorkingDay']=WorkingDay
    Year=False if not season=='Year' else True
    df['Ht_pred']=df.apply(b.predictRow, axis=1)   
    return df

def createCommonSingleDayPlot(d, toutlp, season='Winter', WorkingDay=1, norm=True, plot=True):
    df=pd.DataFrame(index=np.linspace(0,23,24))
    for key in d:
        df[key]=createSingleDayPred(d[key], toutlp, season=season, WorkingDay=WorkingDay).Ht_pred
    
    if plot:
        (df/df.sum()).plot()
        plt.ylim(0)
        plt.legend(ncol=3)
        plt.ylabel('Normalized Heat demand [kW/kWh]')
        plt.xlabel('Time of day')
    return df

def createIaqvecDayPlot(d):
    nmLst=['Apartment blocks', 'Hotels', 'Nursing homes', 'Offices', 'Schools']
    sd = {}
    sd[nmLst[0]]=d['AB']['AB46']
    sd[nmLst[1]]=d['HO']['HO8']
    sd[nmLst[2]]=d['NH']['NH1']
    sd[nmLst[3]]=d['OF']['OF28']
    sd[nmLst[4]]=d['SC']['SC4']
    
    df_1=createCommonSingleDayPlot(sd, -15, plot=False)
    df_2=createCommonSingleDayPlot(sd, 0, plot=False)
    
    fig, ax = plt.subplots(1,2, sharey=True, figsize=(7.5,5))
    (df_1/df_1.sum()).plot(ax=ax[0], legend='')
    (df_2/df_2.sum()).plot(ax=ax[1], legend='')
    
    ax[0].set_ylabel('Normalized Heat demand [kW/kWh]')
    ax[0].set_xlabel('Time of day')
    ax[1].set_xlabel('Time of day') 
    
    plt.legend(ax[0].lines, nmLst, ncol=5, bbox_to_anchor=(1.15, -0.1))
    
    ax[1].tick_params(axis='y', labelleft=True)
    ax[0].set_title('(a)')
    ax[1].set_title('(b)')
    
    return fig,ax

def createIaqvecDayPlot2(d):
    nmLst=['Apartment blocks', 'Hotels', 'Nursing homes', 'Offices', 'Schools']
    sd = {}
    sd[nmLst[0]]=d['AB']['AB46']
    sd[nmLst[1]]=d['HO']['HO8']
    sd[nmLst[2]]=d['NH']['NH1']
    sd[nmLst[3]]=d['OF']['OF28']
    sd[nmLst[4]]=d['SC']['SC4']
    

    
    fig, ax = plt.subplots(1,2, sharey=True, figsize=(7.5,5))
    
    s=createSingleDayPred(sd[nmLst[0]], -15).Ht_pred
    (s/s.sum()).plot(ax=ax[0], color='blue', linestyle='-')
    s=createSingleDayPred(sd[nmLst[0]], 0).Ht_pred
    (s/s.sum()).plot(ax=ax[0], color='blue', linestyle='--')
    
    s=createSingleDayPred(sd[nmLst[1]], -15).Ht_pred
    (s/s.sum()).plot(ax=ax[0], color='orange', linestyle='-')
    s=createSingleDayPred(sd[nmLst[1]], 0).Ht_pred
    (s/s.sum()).plot(ax=ax[0], color='orange', linestyle='--')
    
    s=createSingleDayPred(sd[nmLst[2]], -15).Ht_pred
    (s/s.sum()).plot(ax=ax[0], color='green', linestyle='-')
    s=createSingleDayPred(sd[nmLst[2]], 0).Ht_pred
    (s/s.sum()).plot(ax=ax[0], color='green', linestyle='--')
    
    s=createSingleDayPred(sd[nmLst[3]], -15).Ht_pred
    (s/s.sum()).plot(ax=ax[1], color='red', linestyle='-')
    s=createSingleDayPred(sd[nmLst[3]], 0).Ht_pred
    (s/s.sum()).plot(ax=ax[1], color='red', linestyle='--')
    
    s=createSingleDayPred(sd[nmLst[4]], -15).Ht_pred
    (s/s.sum()).plot(ax=ax[1], color='purple', linestyle='-')
    s=createSingleDayPred(sd[nmLst[4]], 0).Ht_pred
    (s/s.sum()).plot(ax=ax[1], color='purple', linestyle='--')
    
    ax[0].set_ylabel('Normalized Heat demand [kW/kWh]')
    ax[0].set_xlabel('Time of day')
    ax[1].set_xlabel('Time of day') 
    
    plt.legend(list(ax[0].lines[i] for i in [0,2,4])+list(ax[1].lines[i] for i in [0,2]), nmLst, ncol=5, bbox_to_anchor=(1.15, -0.1))
    
    ax[1].tick_params(axis='y', labelleft=True)
    ax[0].set_title('(a)')
    ax[1].set_title('(b)')
    
    return fig,ax
    

def createIaqvecDayPlot3(d):
    nmLst=['Apartment blocks', 'Hotels', 'Nursing homes', 'Offices', 'Schools']
    sd = {}
    sd[nmLst[0]]=d['AB']['AB46']
    sd[nmLst[1]]=d['HO']['HO8']
    sd[nmLst[2]]=d['NH']['NH1']
    sd[nmLst[3]]=d['OF']['OF9']
    sd[nmLst[4]]=d['SC']['SC4']
    

    
    fig, ax = plt.subplots(2,2, sharey=True, sharex=True, figsize=(7.5,5))
    
    s=createSingleDayPred(sd[nmLst[0]], -15).Ht_pred
    (s/s.sum()).plot(ax=ax[0,0], color='blue', linestyle='-')
    s=createSingleDayPred(sd[nmLst[0]], 0).Ht_pred
    (s/s.sum()).plot(ax=ax[0,1], color='blue', linestyle='-')
    
    s=createSingleDayPred(sd[nmLst[1]], -15).Ht_pred
    (s/s.sum()).plot(ax=ax[0,0], color='orange', linestyle='-')
    s=createSingleDayPred(sd[nmLst[1]], 0).Ht_pred
    (s/s.sum()).plot(ax=ax[0,1], color='orange', linestyle='-')
    
    s=createSingleDayPred(sd[nmLst[2]], -15).Ht_pred
    (s/s.sum()).plot(ax=ax[0,0], color='green', linestyle='-')
    s=createSingleDayPred(sd[nmLst[2]], 0).Ht_pred
    (s/s.sum()).plot(ax=ax[0,1], color='green', linestyle='-')
    
    s=createSingleDayPred(sd[nmLst[3]], -15).Ht_pred
    (s/s.sum()).plot(ax=ax[1,0], color='red', linestyle='-')
    s=createSingleDayPred(sd[nmLst[3]], 0).Ht_pred
    (s/s.sum()).plot(ax=ax[1,1], color='red', linestyle='-')
    
    s=createSingleDayPred(sd[nmLst[4]], -15).Ht_pred
    (s/s.sum()).plot(ax=ax[1,0], color='purple', linestyle='-')
    s=createSingleDayPred(sd[nmLst[4]], 0).Ht_pred
    (s/s.sum()).plot(ax=ax[1,1], color='purple', linestyle='-')
    
    ax[0,0].set_ylabel('Normalized Heat demand \n [kW/kWh]')
    ax[1,0].set_ylabel('Normalized Heat demand \n [kW/kWh]')
    ax[1,0].set_xlabel('Time of day')
    ax[1,1].set_xlabel('Time of day') 
    
    plt.legend(ax[0,0].lines+ ax[1,0].lines , nmLst, ncol=5, bbox_to_anchor=(1.15, -0.25))
    
    ax[0,1].tick_params(axis='y', labelleft=True)
    ax[1,1].tick_params(axis='y', labelleft=True)
    ax[0,0].set_title('(a)  -15$^\circ$C')
    ax[0,1].set_title('(a)  0$^\circ$C')
    ax[1,0].set_title('(b)  -15$^\circ$C')
    ax[1,1].set_title('(b)  0$^\circ$C')
    
    return fig,ax

def createIaqvecPredVSMeasuredPlot(d, r2=False):
    nmLst=['Apartment block', 'Hotel', 'Nursing home', 'Office', 'School']
    sd = {}
    sd[nmLst[0]]=d['AB']['AB46']
    sd[nmLst[1]]=d['HO']['HO8']
    sd[nmLst[2]]=d['NH']['NH1']
    sd[nmLst[3]]=d['OF']['OF28']
    sd[nmLst[4]]=d['SC']['SC4']
    

    
    fig = plt.figure(figsize=(7.5,5))
    ax1 = fig.add_subplot(2,3,1)
    ax2 = fig.add_subplot(2,3,2)
    ax3 = fig.add_subplot(2,3,3)
    ax4 = fig.add_subplot(2,3,4)
    ax5 = fig.add_subplot(2,3,5)
    
    
    sd[nmLst[0]].data_reg.HtTot['2017-02-08':'2017-02-09'].plot(ax=ax1, color='blue', linestyle='-')
    sd[nmLst[0]].data_reg.HtTot_predS['2017-02-08':'2017-02-09'].plot(ax=ax1, color='blue', linestyle='--')
    sd[nmLst[1]].data_reg.HtTot['2017-02-08':'2017-02-09'].plot(ax=ax2, color='blue', linestyle='-')
    sd[nmLst[1]].data_reg.HtTot_predS['2017-02-08':'2017-02-09'].plot(ax=ax2, color='blue', linestyle='--')
    sd[nmLst[2]].data_reg.HtTot['2017-02-08':'2017-02-09'].plot(ax=ax3, color='blue', linestyle='-')
    sd[nmLst[2]].data_reg.HtTot_predS['2017-02-08':'2017-02-09'].plot(ax=ax3, color='blue', linestyle='--')
    sd[nmLst[3]].data_reg.HtTot['2017-01-04':'2017-01-05'].plot(ax=ax4, color='blue', linestyle='-')
    sd[nmLst[3]].data_reg.HtTot_predS['2017-01-04':'2017-01-05'].plot(ax=ax4, color='blue', linestyle='--')
    sd[nmLst[4]].data_reg.HtTot['2017-02-08':'2017-02-09'].plot(ax=ax5, color='blue', linestyle='-')
    sd[nmLst[4]].data_reg.HtTot_predS['2017-02-08': '2017-02-09'].plot(ax=ax5, color='blue', linestyle='--')

    ax1.set_ylabel('Heat load kWh/h')
    ax4.set_ylabel('Heat load kWh/h')
    
    ax1.set_xlabel('')
    ax2.set_xlabel('')
    ax3.set_xlabel('')
    ax4.set_xlabel('')
    ax5.set_xlabel('')
    
    if r2:
        ax1.set_title(f'{nmLst[0]} (R^2={sd[nmLst[0]].Winter_wd.r2:.2g})')
        ax2.set_title(f'{nmLst[1]} (R^2={sd[nmLst[1]].Winter_wd.r2:.2g})')
        ax3.set_title(f'{nmLst[2]} (R^2={sd[nmLst[2]].Winter_wd.r2:.2g})')
        ax4.set_title(f'{nmLst[3]} (R^2={sd[nmLst[3]].Winter_wd.r2:.2g})')
        ax5.set_title(f'{nmLst[4]} (R^2={sd[nmLst[4]].Winter_wd.r2:.2g})')
    else:
        ax1.set_title(nmLst[0])
        ax2.set_title(nmLst[1])
        ax3.set_title(nmLst[2])
        ax4.set_title(nmLst[3])
        ax5.set_title(nmLst[4])
        
    ax1.xaxis.set_major_formatter(mdates.DateFormatter(''))
    ax1.xaxis.set_minor_formatter(mdates.DateFormatter(''))
    ax1.set_xticklabels([0,6,12,18,0,6,12,18,0], minor=True)
    ax1.set_xlabel('Hour of day')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter(''))
    ax2.xaxis.set_minor_formatter(mdates.DateFormatter(''))
    ax2.set_xticklabels([0,6,12,18,0,6,12,18,0], minor=True)
    ax2.set_xlabel('Hour of day')
    ax3.xaxis.set_major_formatter(mdates.DateFormatter(''))
    ax3.xaxis.set_minor_formatter(mdates.DateFormatter(''))
    ax3.set_xticklabels([0,6,12,18,0,6,12,18,0], minor=True)
    ax3.set_xlabel('Hour of day')
    ax4.xaxis.set_major_formatter(mdates.DateFormatter(''))
    ax4.xaxis.set_minor_formatter(mdates.DateFormatter(''))
    ax4.set_xticklabels([0,6,12,18,0,6,12,18,0], minor=True)
    ax4.set_xlabel('Hour of day')
    ax5.xaxis.set_major_formatter(mdates.DateFormatter(''))
    ax5.xaxis.set_minor_formatter(mdates.DateFormatter(''))
    ax5.set_xticklabels([0,6,12,18,0,6,12,18,0], minor=True)
    ax5.set_xlabel('Hour of day')
    
    plt.subplots_adjust(hspace=0.5)

    costum_lines = [Line2D([0],[0], color='blue', linestyle='-'),
        Line2D([0],[0], color='blue', linestyle='--')]
    plt.legend(costum_lines, ['Measured', 'Predicted'], bbox_to_anchor=(1.2,1))
    
    return fig
#bDict=createBuildingsFromZENcsvFolder(directory)
#bDict=setAllBuildingPredModelsFromDir(bDict, '../R/StatkraftAB/Winter/', r2Tresh=0.5)
#bDict = removeAllBuildingsWithoutPredModel(bDict, Winter=True)

def createAllDataPlots(skip=[]):
    basedir = '../../Data/Statkraft/ZENcsv/'
    dirlist=['Apartment Block', 'Kindergarten', 'Comercial Building', 'Hotel', 'Sports Facility', 'Shopping Mal', 'Office', 'Cultural Building', 'School', 'Single Family House', 'Apartment', 'Nursing Home', 'Hospital', 'University, Collage' ]
    btypeShortlist=['AB', 'KG', 'CB', 'HO', 'SF', 'SM', 'OF', 'CL', 'SC', 'SFH', 'AP', 'NH', 'HS', 'UC']
    for i in range(0,len(dirlist)):
        if not btypeShortlist[i] in skip:
            pathlib.Path('../plot/Statkraft/'+btypeShortlist[i]).mkdir(parents=True, exist_ok=True)
            bDict=createBuildingsFromZENcsvFolder(basedir+dirlist[i]+ '/')
            plotAllLoadProfiles(bDict, '../plot/Statkraft/'+btypeShortlist[i]+'/', norm=True)
            plotAllLoadProfiles(bDict, '../plot/Statkraft/'+btypeShortlist[i]+'/', norm=False)
            plotAllHtvsTout(bDict, '../plot/Statkraft/'+btypeShortlist[i]+'/')
    return

def createAllRegFiles(season = None, day= None, normalize=False, skip=[]):
    basedir = '../../Data/Statkraft/ZENcsv/'
    dirlist=['Apartment Block', 'Kindergarten', 'Comercial Building', 'Hotel', 'Sports Facility', 'Shopping Mal', 'Office', 'Cultural Building', 'School', 'Single Family House', 'Apartment', 'Nursing Home', 'Hospital', 'University, Collage' ]
    btypeShortlist=['AB', 'KG', 'CB', 'HO', 'SF', 'SM', 'OF', 'CL', 'SC', 'SFH', 'AP', 'NH', 'HS', 'UC']
    seasonDir= season if season else 'Year'
    norm = 'norm' if normalize else ''
    for i in range(0,len(dirlist)):
        if not btypeShortlist[i] in skip:
            endpath='../R/Statkraft/'+btypeShortlist[i]+'/'+seasonDir+norm+'/'
            pathlib.Path(endpath).mkdir(parents=True, exist_ok=True)
            bDict=createBuildingsFromZENcsvFolder(basedir+dirlist[i]+ '/')
            createRegFilesFromBuildingDict(bDict, endpath, season=season, day=day, normalize=normalize)
    return


def createbDictAndLoadWinterProfiles(skip=['SFH', 'AP']):
    basedir = '../../Data/Statkraft/ZENcsv/'
    dirlist=['Apartment Block', 'Kindergarten', 'Comercial Building', 'Hotel', 'Sports Facility', 'Shopping Mal', 'Office', 'Cultural Building', 'School', 'Single Family House', 'Apartment', 'Nursing Home', 'Hospital', 'University, Collage' ]
    btypeShortlist=['AB', 'KG', 'CB', 'HO', 'SF', 'SM', 'OF', 'CL', 'SC', 'SFH', 'AP', 'NH', 'HS', 'UC']
    for i in range(0,len(dirlist)):
        if not btypeShortlist[i] in skip:
            bDict=createBuildingsFromZENcsvFolder(basedir+dirlist[i]+ '/')
            bDict=setAllBuildingPredModelsFromDir(bDict, '../R/Statkraft/'+btypeShortlist[i]+'/Winter/', r2Tresh=0.5)
            bDict = removeAllBuildingsWithoutPredModel(bDict, Winter=True)
            predictAllbDictBuildingsWithRegDataSeason(bDict)
            saveDict(bDict, btypeShortlist[i])
            
    return

def createbDictAndLoadAllProfiles(skip=['SFH', 'AP']):
    abDict={}
    basedir = '../../Data/Statkraft/ZENcsv/'
    dirlist=['Apartment Block', 'Kindergarten', 'Comercial Building', 'Hotel', 'Sports Facility', 'Shopping Mal', 'Office', 'Cultural Building', 'School', 'Single Family House', 'Apartment', 'Nursing Home', 'Hospital', 'University, Collage' ]
    btypeShortlist=['AB', 'KG', 'CB', 'HO', 'SF', 'SM', 'OF', 'CL', 'SC', 'SFH', 'AP', 'NH', 'HS', 'UC']
    for i in range(0,len(dirlist)):
        if not btypeShortlist[i] in skip:
            bDict=createBuildingsFromZENcsvFolder(basedir+dirlist[i]+ '/')
            bDict=setAllBuildingPredModelsFromDir(bDict, '../R/Statkraft/'+btypeShortlist[i]+'/All/', r2Tresh=0.2)
            bDict=setAllBuildingPredModelsFromDir(bDict, '../R/Statkraft/'+btypeShortlist[i]+'/Year/', r2Tresh=0.5)
            #bDict = removeAllBuildingsWithoutPredModel(bDict, Winter=True)
            predictAllbDictBuildingsWithRegDataSeason(bDict)
            predictAllbDictBuildingsWithRegDataYear(bDict)
            abDict[btypeShortlist[i]]=bDict
            saveDict(bDict, btypeShortlist[i])    
    saveDict(abDict, 'All')
    return abDict












