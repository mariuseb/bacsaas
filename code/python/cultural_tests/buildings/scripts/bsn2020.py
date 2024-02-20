# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 07:37:55 2019

@author: hwaln
"""

import buildingdata.scripts.buildingScripts as bs
import buildingdata.lib.buildings as bd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.transforms as mtransforms
import matplotlib.path as mpltPath
import pickle as pk

predMods={'dailySS_HtTot_Win':'SS/HtTot/',
          'dailySS_HtSpace_Win':'SS/HtSpace/',
          'dailySS_HtSpace_All':'SS/HtSpace/allYear/',
          'dailyOS_HtTot_Win':'OS/HtTot/',
          'dailyOS_HtSpace_Win':'OS/HtSpace/',
          'dailyOS_HtSpace_All':'OS/HtSpace/allYear/',
          'dailySS_HtTot_SWin':'Sol/SS/HtTot/',
          'dailySS_HtSpace_SWin':'Sol/SS/HtSpace/',
          'dailySS_HtSpace_SAll':'Sol/SS/HtSpace/allYear/',
          'dailyOS_HtTot_SWin':'Sol/OS/HtTot/',
          'dailyOS_HtSpace_SWin':'Sol/OS/HtSpace/',
          'dailyOS_HtSpace_SAll':'Sol/OS/HtSpace/allYear/',
          }

def readZenCsvData(directory='../../Data/ZENcsv/all_data/'):
    bDict=bs.createBuildingsFromZENcsvFolder(directory)
    return bDict

def addSolarToSimienFiles(bDict):
    solGlob=pd.read_excel('NS_3031_2007_Klima.xlsx').globSol.values
    for key in bDict:
        if int(key.split('_')[1])>9000:
            bDict[key].data_reg['SolGlob']=solGlob
    return

def createRegFiles(bDict, directory='../R/allZenFiles/'):
    bs.createRegFilesFromBuildingDict(bDict, directory+'daily/', resample='1D')
    bs.createRegFilesFromBuildingDict(bDict, directory+'hourly/')

def setAllBuildingPredModelsFromDir(bDict, predDir='../R/allZenFiles/daily/steadyState/', name='dailySS', modType='Season', r2Tresh=0):
    for key in bDict:
        bDict[key].setBildingPredModelsFromDir(predDir, name=name, modType=modType, r2Tresh=r2Tresh)
    return bDict

def setAllPredModels(bDict, predDir, r2Tresh=0):
    for key in predMods:
        setAllBuildingPredModelsFromDir(bDict, predDir=predDir+predMods[key], name=key)
    return

def picklebDict(bDict, fname):
    with open(fname, 'wb') as fout:
        # default protocol is zero
        # -1 gives highest prototcol and smallest data file size
        pk.dump(bDict, fout, protocol=-1)

def loadPickledbDict(fname):
    with open(fname, 'rb') as fin:
        return pk.load(fin)

def addYearlyHtSpaceAndHtDHW(bDict):
    for key in bDict:
        if 'HtSpace' in bDict[key].data_reg.columns:
            bDict[key].yearlyHtSpace=bDict[key].data_reg.HtSpace.groupby([bDict[key].data_reg.index.month, bDict[key].data_reg.index.day, bDict[key].data_reg.index.hour]).mean().mean()*365*24
        else:
            print('Warning:'+key+' HtSpace not available')
        if 'HtDHW' in bDict[key].data_reg.columns:
            bDict[key].yearlyHtDHW=bDict[key].data_reg.HtDHW.groupby([bDict[key].data_reg.index.month, bDict[key].data_reg.index.day, bDict[key].data_reg.index.hour]).mean().mean()*365*24
        else:
            print('Warning:'+key+' HtDHW not available')
            
def createResSum(bDict, r2Tresh=0.2):
    d={}
    bTypeLst=['Apt', 'Off']
    index=[]
    for key in bDict.keys():
        if any(bType in key for bType in bTypeLst):
            index.append(key)
    d['beta_wd']=pd.DataFrame(index=index)
    d['beta_we']=pd.DataFrame(index=index)
    d['R2_wd']=pd.DataFrame(index=index)
    d['R2_we']=pd.DataFrame(index=index)
    d['lpAlpha']=pd.DataFrame(index=index)
#    d['G']=pd.DataFrame(index=bDict.keys())
    for predMod in predMods:
        d['beta_wd'][predMod] = [(bDict[key].predModels[predMod].Winter_wd.ToutLP_beta+bDict[key].predModels[predMod].Winter_wd.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]']) for key in index]
        d['beta_we'][predMod] = [(bDict[key].predModels[predMod].Winter_we.ToutLP_beta+bDict[key].predModels[predMod].Winter_we.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]']) for key in index]
        d['lpAlpha'][predMod] = [(bDict[key].predModels[predMod].Winter_wd.lpAlpha) for key in index]
        d['R2_wd'][predMod] = [bDict[key].predModels[predMod].Winter_wd.r2 for key in index]
        d['R2_we'][predMod] = [bDict[key].predModels[predMod].Winter_we.r2 for key in index]

dhwShiftDict={'Apt':30, 'Off':10, 'Sch':10, 'Nsh':15}
def dailyScatterPlotBeta_wdvsHtTot(bDict, predMod='dailySS', r2Tresh=0.5, shiftDHW=False, ann=False):
    fig,ax = plt.subplots(2,2)
    bTypeAxDict={'Apt':ax[0][0], 'Off':ax[1][0], 'Sch':ax[0][1], 'Nsh':ax[1][1]}
    effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
    for key in bDict:
        bType=key.split('_')[0].split('-')[1]
        if bType in bTypeAxDict.keys():
            if bDict[key].predModels[predMod].Winter_wd.r2 >= r2Tresh:
                effCat=key.split('_')[2]
                mea=True if int(key.split('_')[1])<8000 else False
                try:
                    HtTot=bDict[key].yearlyHeatConsumption/float(bDict[key].zenMetaData['Floor area [m2]'])
                except:
                    print(key)
                    continue
                beta=(bDict[key].predModels[predMod].Winter_wd.ToutLP_beta+bDict[key].predModels[predMod].Winter_wd.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]'])
                if shiftDHW and mea:
                    HtTot-=dhwShiftDict[bType]
                bTypeAxDict[bType].plot(HtTot, beta, 'o' if mea else 'x', color=effCatColDict[effCat])
                if ann: bTypeAxDict[bType].annotate(key.split('_')[1], (HtTot, beta))

    for key in bTypeAxDict:
        bTypeAxDict[key].set_title(key)
        bTypeAxDict[key].set_xlabel('HtTot [kWh/m2/year]')
        bTypeAxDict[key].set_ylabel('beta_Ta [kWh/m2/day]')
        bTypeAxDict[key].set_ylim(top=0)
        bTypeAxDict[key].set_xlim(left=0)

def dailyScatterPlotBeta_wdvsYearOfConstr(bDict, predMod='dailySS', r2Tresh=0.5, shiftDHW=False, ann=False):
    fig,ax = plt.subplots(2,2,sharey=True,  gridspec_kw={'width_ratios': [6, 1]})
    plt.subplots_adjust(wspace=0)
    bTypeAxDict={'Apt':ax[0][0], 'Off':ax[1][0]}
    bTypeAxDict2={'Apt':ax[0][1], 'Off':ax[1][1]}
    effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
    for key in bTypeAxDict2:
        bTypeAxDict2[key].plot('Unkown', 0, 'o', visible=False)
    for key in bDict:
        bType=key.split('_')[0].split('-')[1]
        if bType in bTypeAxDict.keys():
            if bDict[key].predModels[predMod].Winter_wd.r2 >= r2Tresh:
                effCat=key.split('_')[2]
                mea=True if int(key.split('_')[1])<8000 else False
                simien=True if int(key.split('_')[1])>9000 else False
                try:
                    year=int(float(bDict[key].zenMetaData['Year of construction']))
                except:
                    print(key)
                    year='Unkown'
                beta=(bDict[key].predModels[predMod].Winter_wd.ToutLP_beta+bDict[key].predModels[predMod].Winter_wd.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]'])
                if not simien:
                    if isinstance(year,int):
                        bTypeAxDict[bType].plot(year, beta, 'o' if mea else 'x', color=effCatColDict[effCat])
                        if ann: bTypeAxDict[bType].annotate(key.split('_')[1], (year, beta))
                    else:
                        bTypeAxDict2[bType].plot(year, beta, 'o' if mea else 'x', color=effCatColDict[effCat])
                        if ann: bTypeAxDict2[bType].annotate(key.split('_')[1], (year, beta))
                elif simien:
                    #line = mlines.Line2D([0, 2020], [beta, beta], color=effCatColDict[effCat])
                    bTypeAxDict[bType].axhline(y=beta, color=effCatColDict[effCat])
                    bTypeAxDict2[bType].axhline(y=beta, color=effCatColDict[effCat])

                    
    ax[1][0].set_xlabel('Year of construction')

    for key in bTypeAxDict:
        bTypeAxDict[key].set_title(key)
        bTypeAxDict[key].set_ylabel('beta_Ta [kWh/degC/m2/day]')
        bTypeAxDict[key].set_ylim(top=0)
        bTypeAxDict[key].set_xlim(1900,2020)       

def dailyScatterPlotIntercept_wdvsYearOfConstr(bDict, predMod='dailySS', r2Tresh=0.5, shiftDHW=False, ann=False):
    fig,ax = plt.subplots(2,2,sharey=True,  gridspec_kw={'width_ratios': [6, 1]})
    plt.subplots_adjust(wspace=0)
    bTypeAxDict={'Apt':ax[0][0], 'Off':ax[1][0]}
    bTypeAxDict2={'Apt':ax[0][1], 'Off':ax[1][1]}
    effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
    for key in bTypeAxDict2:
        bTypeAxDict2[key].plot('Unkown', 0, 'o', visible=False)
    for key in bDict:
        bType=key.split('_')[0].split('-')[1]
        if bType in bTypeAxDict.keys():
            if bDict[key].predModels[predMod].Winter_wd.r2 >= r2Tresh:
                effCat=key.split('_')[2]
                mea=True if int(key.split('_')[1])<8000 else False
                simien=True if int(key.split('_')[1])>9000 else False
                try:
                    year=int(float(bDict[key].zenMetaData['Year of construction']))
                except:
                    #print(key)
                    year='Unkown'
                intercept=(bDict[key].predModels[predMod].Winter_wd.intercept)/float(bDict[key].zenMetaData['Floor area [m2]'])
                if not simien:
                    if isinstance(year,int):
                        bTypeAxDict[bType].plot(year, intercept, 'o' if mea else 'x', color=effCatColDict[effCat])
                        if ann: bTypeAxDict[bType].annotate(key.split('_')[1], (year, intercept))
                    else:
                        bTypeAxDict2[bType].plot(year, intercept, 'o' if mea else 'x', color=effCatColDict[effCat])
                        if ann: bTypeAxDict2[bType].annotate(key.split('_')[1], (year, intercept))
                elif simien:
                    #line = mlines.Line2D([0, 2020], [beta, beta], color=effCatColDict[effCat])
                    bTypeAxDict[bType].axhline(y=intercept, color=effCatColDict[effCat])
                    bTypeAxDict2[bType].axhline(y=intercept, color=effCatColDict[effCat])

                    
    ax[1][0].set_xlabel('Year of construction')

    for key in bTypeAxDict:
        bTypeAxDict[key].set_title(key)
        bTypeAxDict[key].set_ylabel('intercept [kWh/m2/day]')
        bTypeAxDict[key].set_ylim(bottom=0)
        bTypeAxDict[key].set_xlim(1900,2020)    
        
def dailyScatterPlotBeta(bDict, predMod='dailySS', r2Tresh=0.5, shiftDHW=False, ann=False):
    fig,ax = plt.subplots(1,2,sharey=True)
    bTypeAxDict={'Apt':ax[0], 'Off':ax[1]}
    effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
    for key in bDict:
        bType=key.split('_')[0].split('-')[1]
        if bType in bTypeAxDict.keys():
            if bDict[key].predModels[predMod].Winter_wd.r2 >= r2Tresh:
                effCat=key.split('_')[2]
                mea=True if int(key.split('_')[1])<8000 else False
                simien=True if int(key.split('_')[1])>9000 else False                
                beta=(bDict[key].predModels[predMod].Winter_wd.ToutLP_beta+bDict[key].predModels[predMod].Winter_wd.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]'])
                if mea:
                    bTypeAxDict[bType].plot(1, beta, 'o' if mea else 'x', color=effCatColDict[effCat])
                    if ann: bTypeAxDict[bType].annotate(key.split('_')[1], (1, beta))
                elif simien:
                    line = mlines.Line2D([0, 2], [beta, beta], color=effCatColDict[effCat])
                    bTypeAxDict[bType].add_line(line)
        
    ax[0].set_ylabel('beta_Ta [kWh/degC/m2/day]')
    for key in bTypeAxDict:
        bTypeAxDict[key].set_title(key)
        bTypeAxDict[key].set_ylim(top=0)
        bTypeAxDict[key].get_xaxis().set_visible(False)
    return fig, ax

def dailyScatterPlotBeta_wdvsHtSpace(bDict, predMod='dailySS', r2Tresh=0.5, ann=False):
    fig,ax = plt.subplots(2,2)
    bTypeAxDict={'Apt':ax[0][0], 'Off':ax[1][0], 'Sch':ax[0][1], 'Nsh':ax[1][1]}
    effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
    for key in bDict:
        bType=key.split('_')[0].split('-')[1]
        if bType in bTypeAxDict.keys():
            if bDict[key].predModels[predMod].Winter_wd.r2 >= r2Tresh:
                effCat=key.split('_')[2]
                mea=True if int(key.split('_')[1])<8000 else False
                try:
                    HtSpace=bDict[key].yearlyHtSpace/float(bDict[key].zenMetaData['Floor area [m2]'])
                except:
                    print(key)
                    continue
                beta=(bDict[key].predModels[predMod].Winter_wd.ToutLP_beta+bDict[key].predModels[predMod].Winter_wd.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]'])
                bTypeAxDict[bType].plot(HtSpace, beta, 'o' if mea else 'x', color=effCatColDict[effCat])
                if ann: bTypeAxDict[bType].annotate(key.split('_')[1], (HtSpace, beta))

    for key in bTypeAxDict:
        bTypeAxDict[key].set_title(key)
        bTypeAxDict[key].set_xlabel('Yearly heat demand [kWh/m2/year]')
        bTypeAxDict[key].set_ylabel('beta_Ta [kWh/m2/day]')
        bTypeAxDict[key].set_ylim(top=0)
        bTypeAxDict[key].set_xlim(left=0)

def dailyScatterPlotIntercept_wdvsHtSpace(bDict, predMod='dailySS', r2Tresh=0.5, ann=False):
    fig,ax = plt.subplots(2,2)
    bTypeAxDict={'Apt':ax[0][0], 'Off':ax[1][0], 'Sch':ax[0][1], 'Nsh':ax[1][1]}
    effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
    for key in bDict:
        bType=key.split('_')[0].split('-')[1]
        if bType in bTypeAxDict.keys():
            if bDict[key].predModels[predMod].Winter_wd.r2 >= r2Tresh:
                effCat=key.split('_')[2]
                mea=True if int(key.split('_')[1])<8000 else False
                try:
                    HtSpace=bDict[key].yearlyHtSpace/float(bDict[key].zenMetaData['Floor area [m2]'])
                except:
                    print(key)
                    continue
                intercept=(bDict[key].predModels[predMod].Winter_wd.intercept)/float(bDict[key].zenMetaData['Floor area [m2]'])
                bTypeAxDict[bType].plot(HtSpace, intercept, 'o' if mea else 'x', color=effCatColDict[effCat])
                if ann: bTypeAxDict[bType].annotate(key.split('_')[1], (HtSpace, intercept))

    for key in bTypeAxDict:
        bTypeAxDict[key].set_title(key)
        bTypeAxDict[key].set_xlabel('Yearly heat demand [kWh/m2/year]')
        bTypeAxDict[key].set_ylabel('beta_Ta [kWh/m2/day]')
#        bTypeAxDict[key].set_ylim(bottom=0)
#        bTypeAxDict[key].set_xlim(right=0)


def dailyScatterPlotBeta_wdvsIntercept(bDict, predMod='dailySS', r2Tresh=0.5, ann=False, cat=False):
    fig,ax = plt.subplots(2,1)
    bTypeAxDict={'Apt':ax[0], 'Off':ax[1]}
    effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
    simDf=pd.DataFrame(columns=['bType','effCat', 'intercept', 'beta'])
    meaDf=pd.DataFrame(columns=['bType','effCat_old', 'intercept', 'beta'])
    for key in bDict:
        bType=key.split('_')[0].split('-')[1]
        if bType in bTypeAxDict.keys():
            if bDict[key].predModels[predMod].Winter_wd.r2 >= r2Tresh:
                effCat=key.split('_')[2]
                mea=True if int(key.split('_')[1])<8000 else False
                if mea and effCat=='R':
                    try:
                        year=int(float(bDict[key].zenMetaData['Year of construction']))
                        effCat='T' if year>2012 else 'R'
                    except:  
                        pass
                simien=True if int(key.split('_')[1])>9000 else False
                try:
                    intercept=(bDict[key].predModels[predMod].Winter_wd.intercept)/float(bDict[key].zenMetaData['Floor area [m2]'])
                except:
                    print(key)
                    continue
                beta=(bDict[key].predModels[predMod].Winter_wd.ToutLP_beta+bDict[key].predModels[predMod].Winter_wd.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]'])
                bTypeAxDict[bType].plot(intercept, beta, 'o' if mea else 'x', color=effCatColDict[effCat])
                if ann: bTypeAxDict[bType].annotate(key.split('_')[1], (intercept, beta))
                if mea:
                    meaDf.loc[key]=[bType, effCat, intercept, beta]
                else:
                    simDf.loc[key]=[bType, effCat, intercept, beta]

    for key in bTypeAxDict:
        bTypeAxDict[key].set_title(key)
        bTypeAxDict[key].set_xlabel('intercept [kWh/m2/day]')
        bTypeAxDict[key].set_ylabel('beta_Ta [kWh/degC/m2/day]')
        bTypeAxDict[key].set_ylim(top=0)
        bTypeAxDict[key].set_xlim(left=0)
    if cat:
        catFac_beta=0.2
        catFac_int=0.2
        prolongIntEff=1.5
        prolongIntTek=1.5
        for bType in bTypeAxDict.keys():
            # Efficient
            beta_max=0
            beta_min=(catFac_beta*simDf[simDf['bType']==bType][simDf['effCat']=='E']['beta'].mean()+(1-catFac_beta)*simDf[simDf['bType']==bType][simDf['effCat']=='T']['beta'].mean())
            int_max=(catFac_int*simDf[simDf['bType']==bType][simDf['effCat']=='E']['intercept'].mean()+(1-catFac_int)*simDf[simDf['bType']==bType][simDf['effCat']=='T']['intercept'].mean())
            int_min=0
            rectE = plt.Rectangle((int_min, beta_min), (int_max-int_min)*prolongIntEff, beta_max-beta_min,
                         facecolor="green", alpha=0.1)
            bTypeAxDict[bType].add_patch(rectE)
            
            #Tek
            rectT = plt.Rectangle((int_max-(int_max-int_min)*(prolongIntTek-1), beta_min-(beta_max-beta_min)/2), (int_max-int_min)*prolongIntTek, (beta_max-beta_min)/2,
                         facecolor="blue", alpha=0.1)
            bTypeAxDict[bType].add_patch(rectT)
            
        #Categorize       
        meaDf['effCat_new']=False
        meaDf.loc[rectE.get_path().contains_points(meaDf[['intercept','beta']]),'effCat_new']='E'
        meaDf.loc[rectT.get_path().contains_points(meaDf[['intercept','beta']]),'effCat_new']='T'
            
    return meaDf

def calcPolygons(simDf, catFac_beta=0.3, catFac_int=0.3, beta_angMult=1):
                # Efficient
            y1=simDf[simDf['effCat']=='E']['beta'].mean()
            x1=simDf[simDf['effCat']=='E']['intercept'].mean()
            y2=simDf[simDf['effCat']=='T']['beta'].mean()
            x2=simDf[simDf['effCat']=='T']['intercept'].mean()
            x3=catFac_int*x1+(1-catFac_int)*x2
            y3=catFac_beta*y1+(1-catFac_beta)*y2
            x4=np.sqrt(x3*x3+y3*y3*beta_angMult*beta_angMult)/np.cos(np.arctan(abs(y3*beta_angMult/x3)))
            #y4=0
            x5=x3-(x4-x3)
            y5=2*y3
            pointsE=np.zeros((3,2))
            pointsE[1][0]=x4
            pointsE[2][0]=x5
            pointsE[2][1]=y5
            
            #Tek
            pointsT=np.zeros((4,2))
            pointsT[0]=pointsE[1]
            pointsT[1][0]=x4+0.5*x4
            pointsT[2][0]=x5+0.5*x5
            pointsT[2][1]=y5+0.5*y5
            pointsT[3]=pointsE[2]
            
            #Regular
            pointsR=np.zeros((4,2))
            pointsR[0]=pointsT[1]
            pointsR[1][0]=pointsT[1][0]*10
            pointsR[2][0]=pointsT[2][0]*10
            pointsR[2][1]=pointsT[2][1]*10
            pointsR[3]=pointsT[2]
            
            return pointsE, pointsT, pointsR
        
def dailyScatterPlotBeta_wdvsIntercept2(bDict, predMod='dailySS', r2Tresh=0.5, ann=False, cat=False):
    fig,ax = plt.subplots(2,1)
    bTypeAxDict={'Apt':ax[0], 'Off':ax[1]}
    effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
    simDf=pd.DataFrame(columns=['bType','effCat', 'intercept', 'beta'])
    meaDf=pd.DataFrame(columns=['bType','effCat_old', 'intercept', 'beta'])
    for key in bDict:
        bType=key.split('_')[0].split('-')[1]
        if bType in bTypeAxDict.keys():
            if bDict[key].predModels[predMod].Winter_wd.r2 >= r2Tresh:
                effCat=key.split('_')[2]
                mea=True if int(key.split('_')[1])<8000 else False
                if mea and effCat=='R':
                    try:
                        year=int(float(bDict[key].zenMetaData['Year of construction']))
                        effCat='T' if year>2012 else 'R'
                    except:  
                        pass
                simien=True if int(key.split('_')[1])>9000 else False
                try:
                    intercept=(bDict[key].predModels[predMod].Winter_wd.intercept)/float(bDict[key].zenMetaData['Floor area [m2]'])
                except:
                    print(key)
                    continue
                beta=(bDict[key].predModels[predMod].Winter_wd.ToutLP_beta+bDict[key].predModels[predMod].Winter_wd.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]'])
                bTypeAxDict[bType].plot(intercept, beta, 'o' if mea else 'x', color=effCatColDict[effCat])
                if ann: bTypeAxDict[bType].annotate(key.split('_')[1], (intercept, beta))
                if mea:
                    meaDf.loc[key]=[bType, effCat, intercept, beta]
                else:
                    simDf.loc[key]=[bType, effCat, intercept, beta]

    for key in bTypeAxDict:
        bTypeAxDict[key].set_title(key)
        bTypeAxDict[key].set_xlabel('intercept [kWh/m2/day]')
        bTypeAxDict[key].set_ylabel('beta_Ta [kWh/degC/m2/day]')
        bTypeAxDict[key].set_ylim(top=0)
        bTypeAxDict[key].set_xlim(left=0)
    if cat:
        catFac_beta=0.3
        catFac_int=0.3
        for bType in bTypeAxDict.keys():
            # Efficient
            y1=simDf[simDf['bType']==bType][simDf['effCat']=='E']['beta'].mean()
            x1=simDf[simDf['bType']==bType][simDf['effCat']=='E']['intercept'].mean()
            y2=simDf[simDf['bType']==bType][simDf['effCat']=='T']['beta'].mean()
            x2=simDf[simDf['bType']==bType][simDf['effCat']=='T']['intercept'].mean()
            x3=catFac_int*x1+(1-catFac_int)*x2
            y3=catFac_beta*y1+(1-catFac_beta)*y2
            x4=np.sqrt(x3*x3+y3*y3)/np.cos(np.arctan(abs(y3/x3)))
            y4=0
            x5=x3-(x4-x3)
            y5=2*y3
            pointsE=np.zeros((3,2))
            pointsE[1][0]=x4
            pointsE[2][0]=x5
            pointsE[2][1]=y5
            polE = plt.Polygon(pointsE, facecolor="green", alpha=0.1)
            bTypeAxDict[bType].add_patch(polE)
            
            #Tek
            pointsT=np.zeros((4,2))
            pointsT[0]=pointsE[1]
            pointsT[1][0]=x4+0.5*x4
            pointsT[2][0]=x5+0.5*x5
            pointsT[2][1]=y5+0.5*y5
            pointsT[3]=pointsE[2]
            polT = plt.Polygon(pointsT, facecolor="blue", alpha=0.1)
            bTypeAxDict[bType].add_patch(polT)

        #Categorize
        pathE = mpltPath.Path(pointsE)
        pathT = mpltPath.Path(pointsT)
        
        meaDf['effCat_new']=False
        meaDf.loc[pathE.contains_points(meaDf[['intercept','beta']]),'effCat_new']='E'
        meaDf.loc[pathT.contains_points(meaDf[['intercept','beta']]),'effCat_new']='T'

    return meaDf

def dailyScatterPlotBeta_wdvsInterceptPolyAll(bDict, predMod='dailySS', 
                                              bTypeLst=['Apt', 'Off', 'Shp', 'Htl', 'CuS', 'Kdg', 'Sch', 'Hsp', 'Uni', 'Nsh'],
                                              r2Tresh=0.5, ann=False, cat=False, plot=True,saveFig=False, close=False):
    d_mea={}
    d_poly={}
    for bType in bTypeLst:
        fig,ax = plt.subplots(1,1, figsize=(15,7))
        effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
        simDf=pd.DataFrame(columns=['bType','effCat', 'intercept', 'beta'])
        meaDf=pd.DataFrame(columns=['bType','effCat_old', 'intercept', 'beta'])
        for key in bDict:
            if bType in key:
                if bDict[key].predModels[predMod].Winter_wd.r2 >= r2Tresh:
                    effCat=key.split('_')[2]
                    mea=True if int(key.split('_')[1])<8000 else False
                    if mea and effCat=='R':
                        try:
                            year=int(float(bDict[key].zenMetaData['Year of construction']))
                            #effCat='T' if year>2012 else 'R'
                        except:  
                            pass
#                    simien=True if int(key.split('_')[1])>9000 else False
                    try:
                        intercept=(bDict[key].predModels[predMod].Winter_wd.intercept)/float(bDict[key].zenMetaData['Floor area [m2]'])
                    except:
                        print(key)
                        continue
                    beta=(bDict[key].predModels[predMod].Winter_wd.ToutLP_beta+bDict[key].predModels[predMod].Winter_wd.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]'])
                    if plot:
                        ax.plot(intercept, beta, 'o' if mea else 'x', color=effCatColDict[effCat])
                        if ann: ax.annotate(key.split('_')[1], (intercept, beta))
                    if mea:
                        meaDf.loc[key]=[bType, effCat, intercept, beta]
                    else:
                        simDf.loc[key]=[bType, effCat, intercept, beta]
        if plot:                
            ax.set_title(bType)
            ax.set_xlabel('intercept [kWh/m2/day]')
            ax.set_ylabel('beta_Ta [kWh/degC/m2/day]')
            ax.set_ylim(top=0)
            ax.set_xlim(left=0)
        if cat:
            if bType == 'Apt' or bType=='Off':
                pointsE, pointsT, pointsR = calcPolygons(simDf, catFac_beta=0.3, catFac_int=0.3, beta_angMult=10)
            else:
                pointsE = d_poly['Off']['pointsE']
                pointsT = d_poly['Off']['pointsT']
                pointsR = d_poly['Off']['pointsR']
            polE = plt.Polygon(pointsE, facecolor="green", alpha=0.1)
            polT = plt.Polygon(pointsT, facecolor="blue", alpha=0.1)
            polR = plt.Polygon(pointsR, facecolor="red", alpha=0.1)
            if plot:
                ax.add_patch(polE)
                ax.add_patch(polT)
                ax.add_patch(polR)
    
            #Categorize
            pathE = mpltPath.Path(pointsE)
            pathT = mpltPath.Path(pointsT)
            pathR = mpltPath.Path(pointsR)
            
            meaDf['effCat_new']=False
            meaDf.loc[pathE.contains_points(meaDf[['intercept','beta']]),'effCat_new']='E'
            meaDf.loc[pathT.contains_points(meaDf[['intercept','beta']]),'effCat_new']='T'
            meaDf.loc[pathR.contains_points(meaDf[['intercept','beta']]),'effCat_new']='R'
            
        d_mea[bType]=meaDf
        d_poly[bType]={}
        d_poly[bType]['pointsE']=pointsE
        d_poly[bType]['pointsT']=pointsT
        d_poly[bType]['pointsR']=pointsR

        if plot and saveFig:
            plt.savefig('plots/betaVsIntercept_Cat_'+bType+'_'+predMod+'.png', dpi=600, bbox_inches='tight')
        if plot and close:
            plt.close()
    return d_mea

     
def dailyScatterPlotBeta_wevsHtTot(bDict, predMod='dailySS', r2Tresh=0.5, ann=False):
    fig,ax = plt.subplots(2,2)
    bTypeAxDict={'Apt':ax[0][0], 'Off':ax[1][0], 'Sch':ax[0][1], 'Nsh':ax[1][1]}
    effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
    for key in bDict:
        bType=key.split('_')[0].split('-')[1]
        if bType in bTypeAxDict.keys():
            if bDict[key].predModels[predMod].Winter_we.r2 >= r2Tresh:
                effCat=key.split('_')[2]
                mea=True if int(key.split('_')[1])<8000 else False
                try:
                    HtTot=bDict[key].yearlyHeatConsumption/float(bDict[key].zenMetaData['Floor area [m2]'])
                except:
                    print(key)
                    continue
                beta=(bDict[key].predModels[predMod].Winter_we.ToutLP_beta+bDict[key].predModels[predMod].Winter_we.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]'])
                bTypeAxDict[bType].plot(HtTot, beta, 'o' if mea else 'x', color=effCatColDict[effCat], label=key)
                if ann: bTypeAxDict[bType].annotate(key.split('_')[1], (HtTot, beta))
    
    for key in bTypeAxDict:
        bTypeAxDict[key].set_title(key)
        bTypeAxDict[key].set_xlabel('HtTot [kWh/m2/year]')
        bTypeAxDict[key].set_ylabel('beta_Ta [kWh/m2/day]')
        bTypeAxDict[key].set_ylim(top=0)
        bTypeAxDict[key].set_xlim(left=0)

def dailyScatterPlotBeta_wevsHtSpace(bDict, predMod='dailySS', r2Tresh=0.5, ann=False):
    fig,ax = plt.subplots(2,2)
    bTypeAxDict={'Apt':ax[0][0], 'Off':ax[1][0], 'Sch':ax[0][1], 'Nsh':ax[1][1]}
    effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
    for key in bDict:
        bType=key.split('_')[0].split('-')[1]
        if bType in bTypeAxDict.keys():
            if bDict[key].predModels[predMod].Winter_we.r2 >= r2Tresh:
                effCat=key.split('_')[2]
                mea=True if int(key.split('_')[1])<8000 else False
                try:
                    HtSpace=bDict[key].yearlyHtSpace/float(bDict[key].zenMetaData['Floor area [m2]'])
                except:
                    print(key)
                    continue
                beta=(bDict[key].predModels[predMod].Winter_we.ToutLP_beta+bDict[key].predModels[predMod].Winter_we.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]'])
                bTypeAxDict[bType].plot(HtSpace, beta, 'o' if mea else 'x', color=effCatColDict[effCat])
                if ann: bTypeAxDict[bType].annotate(key.split('_')[1], (HtSpace, beta))

    for key in bTypeAxDict:
        bTypeAxDict[key].set_title(key)
        bTypeAxDict[key].set_xlabel('Yearly heat demand [kWh/m2/year]')
        bTypeAxDict[key].set_ylabel('beta_Ta [kWh/m2/day]')
        bTypeAxDict[key].set_ylim(top=0)
        bTypeAxDict[key].set_xlim(left=0)
        
def dailyScatterPlotBetavsHtSpace(bDict, predMod='dailySS', r2Tresh=0.5, ann=False):
    fig,ax = plt.subplots(2,2)
    bTypeAxDict={'Apt':ax[0][0], 'Off':ax[0][1]}
    bTypeAxDict2={'Apt':ax[1][0], 'Off':ax[1][1]}
    effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
    for key in bDict:
        bType=key.split('_')[0].split('-')[1]
        if bType in bTypeAxDict.keys():
            if bDict[key].predModels[predMod].Winter_we.r2 >= r2Tresh:
                effCat=key.split('_')[2]
                mea=True if int(key.split('_')[1])<8000 else False
                try:
                    HtSpace=bDict[key].yearlyHtSpace/float(bDict[key].zenMetaData['Floor area [m2]'])
                except:
                    print(key)
                    continue
                bWd=(bDict[key].predModels[predMod].Winter_wd.ToutLP_beta+bDict[key].predModels[predMod].Winter_wd.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]'])
                bWe=(bDict[key].predModels[predMod].Winter_we.ToutLP_beta+bDict[key].predModels[predMod].Winter_we.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]'])
                bTypeAxDict[bType].plot(HtSpace, bWd, 'o' if mea else 'x', color=effCatColDict[effCat])
                bTypeAxDict2[bType].plot(HtSpace, bWe, 'o' if mea else 'x', color=effCatColDict[effCat])
                if ann: bTypeAxDict[bType].annotate(key.split('_')[1], (HtSpace, bWd))
                if ann: bTypeAxDict2[bType].annotate(key.split('_')[1], (HtSpace, bWe))

    for key in bTypeAxDict:
        bTypeAxDict[key].set_title(key+'Weekday')
        bTypeAxDict[key].set_xlabel('Yearly heat demand [kWh/m2/year]')
        bTypeAxDict[key].set_ylabel('beta_Ta [kWh/m2/day]')
        bTypeAxDict[key].set_ylim(top=0)
        bTypeAxDict[key].set_xlim(left=0)
        bTypeAxDict2[key].set_title(key+'Weekend')
        bTypeAxDict2[key].set_xlabel('Yearly heat demand [kWh/m2/year]')
        bTypeAxDict2[key].set_ylabel('beta_Ta [kWh/m2/day]')
        bTypeAxDict2[key].set_ylim(top=0)
        bTypeAxDict2[key].set_xlim(left=0)

def dailyScatterPlotBetaWdvsBetaWe(bDict, predMod='dailySS', r2Tresh=0.5, ann=False):
    fig,ax = plt.subplots(2,1)
    bTypeAxDict={'Apt':ax[0], 'Off':ax[1]}
    effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
    for key in bDict:
        bType=key.split('_')[0].split('-')[1]
        if bType in bTypeAxDict.keys():
            if bDict[key].predModels[predMod].Winter_wd.r2 >= r2Tresh:
                effCat=key.split('_')[2]
                mea=True if int(key.split('_')[1])<8000 else False
                bWd=(bDict[key].predModels[predMod].Winter_wd.ToutLP_beta+bDict[key].predModels[predMod].Winter_wd.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]'])
                bWe=(bDict[key].predModels[predMod].Winter_we.ToutLP_beta+bDict[key].predModels[predMod].Winter_we.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]'])
                bTypeAxDict[bType].plot(bWd, bWe, 'o' if mea else 'x', color=effCatColDict[effCat])
                if ann: bTypeAxDict[bType].annotate(key.split('_')[1], (bWd, bWe))
    
    line0 = mlines.Line2D([0, -0.06], [0, -0.06], color='black', lw=0.5)
    ax[0].add_line(line0)
    line1 = mlines.Line2D([0, -0.06], [0, -0.06], color='black', lw=0.5)
    ax[1].add_line(line1)
    
    ax[1].set_xlabel('beta_Ta Weekdays [kWh/m2/day]')
    for key in bTypeAxDict:
        bTypeAxDict[key].set_title(key)
        bTypeAxDict[key].set_ylabel('beta_Ta Weekends [kWh/m2/day]')
        bTypeAxDict[key].set_ylim(top=0, bottom=-0.06)
        bTypeAxDict[key].set_xlim(right=0, left=-0.06)

def dailyScatterPlotCompBeta(bDict, Mod1='dailySS', Mod2='dailyOS', r2Tresh=0.5, ann=False):
    fig,ax = plt.subplots(2,1)
    bTypeAxDict={'Apt':ax[0], 'Off':ax[1]}
    effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
    for key in bDict:
        bType=key.split('_')[0].split('-')[1]
        if bType in bTypeAxDict.keys():
            if (bDict[key].predModels[Mod1].Winter_wd.r2 >= r2Tresh) and (bDict[key].predModels[Mod2].Winter_wd.r2 >= r2Tresh):
                effCat=key.split('_')[2]
                mea=True if int(key.split('_')[1])<8000 else False
                b1=(bDict[key].predModels[Mod1].Winter_wd.ToutLP_beta+bDict[key].predModels[Mod1].Winter_wd.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]'])
                b2=(bDict[key].predModels[Mod2].Winter_wd.ToutLP_beta+bDict[key].predModels[Mod2].Winter_wd.Tout_beta)/float(bDict[key].zenMetaData['Floor area [m2]'])
                bTypeAxDict[bType].plot(b1, b2, 'o' if mea else 'x', color=effCatColDict[effCat])
                if ann: bTypeAxDict[bType].annotate(key.split('_')[1], (b1, b2))
    
    line0 = mlines.Line2D([0, -0.06], [0, -0.06], color='black', lw=0.5)
    ax[0].add_line(line0)
    line1 = mlines.Line2D([0, -0.06], [0, -0.06], color='black', lw=0.5)
    ax[1].add_line(line1)
    
    ax[1].set_xlabel('beta_Ta ' + Mod1 +' [kWh/m2/day]')
    for key in bTypeAxDict:
        bTypeAxDict[key].set_title(key)
        bTypeAxDict[key].set_ylabel('beta_Ta ' + Mod2 +' [kWh/m2/day]')
        bTypeAxDict[key].set_ylim(top=0, bottom=-0.06)
        bTypeAxDict[key].set_xlim(right=0, left=-0.06)
        
def dailyScatterPlotLpAlphaHtSpace(bDict, predMod='dailyOS', r2Tresh=0.5, ann=False):
    fig,ax = plt.subplots(2,2)
    bTypeAxDict={'Apt':ax[0][0], 'Off':ax[1][0], 'Sch':ax[0][1], 'Nsh':ax[1][1]}
    effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
    for key in bDict:
        bType=key.split('_')[0].split('-')[1]
        if bType in bTypeAxDict.keys():
            if bDict[key].predModels[predMod].Winter_we.r2 >= r2Tresh:
                effCat=key.split('_')[2]
                mea=True if int(key.split('_')[1])<8000 else False
                try:
                    HtSpace=bDict[key].yearlyHtSpace/float(bDict[key].zenMetaData['Floor area [m2]'])
                except:
                    print(key)
                    continue
                alpha=(bDict[key].predModels[predMod].Winter_we.lpAlpha)
                bTypeAxDict[bType].plot(HtSpace, alpha, 'o' if mea else 'x', color=effCatColDict[effCat], label=key)
                if ann: bTypeAxDict[bType].annotate(key.split('_')[1], (HtSpace, alpha))
    
    for key in bTypeAxDict:
        bTypeAxDict[key].set_title(key)
        bTypeAxDict[key].set_xlabel('HtTot [kWh/m2/year]')
        bTypeAxDict[key].set_ylabel('lp_Alpha [-]')
        bTypeAxDict[key].set_ylim(bottom=0)
        bTypeAxDict[key].set_xlim(left=0)

def dailyScatterPlotLpAlphaHtHtTot(bDict, predMod='dailyOS', r2Tresh=0.5, ann=False):
    fig,ax = plt.subplots(2,2)
    bTypeAxDict={'Apt':ax[0][0], 'Off':ax[1][0], 'Sch':ax[0][1], 'Nsh':ax[1][1]}
    effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
    for key in bDict:
        bType=key.split('_')[0].split('-')[1]
        if bType in bTypeAxDict.keys():
            if bDict[key].predModels[predMod].Winter_we.r2 >= r2Tresh:
                effCat=key.split('_')[2]
                mea=True if int(key.split('_')[1])<8000 else False
                try:
                    HtTot=bDict[key].yearlyHeatConsumption/float(bDict[key].zenMetaData['Floor area [m2]'])
                except:
                    print(key)
                    continue
                alpha=(bDict[key].predModels[predMod].Winter_we.lpAlpha)
                bTypeAxDict[bType].plot(HtTot, alpha, 'o' if mea else 'x', color=effCatColDict[effCat], label=key)
                if ann: bTypeAxDict[bType].annotate(key.split('_')[1], (HtTot, alpha))
    
    for key in bTypeAxDict:
        bTypeAxDict[key].set_title(key)
        bTypeAxDict[key].set_xlabel('HtTot [kWh/m2/year]')
        bTypeAxDict[key].set_ylabel('lp_Alpha [-]')
        bTypeAxDict[key].set_ylim(bottom=0)
        bTypeAxDict[key].set_xlim(left=0)

def plotR2DailySSvsOS(bDict, SS='dailySS', OS='dailyOS',  bTypeLst=['Apt', 'Off'], eps=0.01):
    fig, ax = plt.subplots(2,1)
    for key in bDict:
        if any(bTypeLst) in key:
            r2SSwd=bDict[key].predModels[SS].Winter_wd.r2
            r2SSwe=bDict[key].predModels[SS].Winter_we.r2
            r2OSwd=bDict[key].predModels[OS].Winter_wd.r2
            r2OSwe=bDict[key].predModels[OS].Winter_we.r2
            ax[0].plot(r2SSwd, r2OSwd, 'o', color='blue' if r2SSwd>(r2OSwd+eps) else ('green' if r2OSwd>(r2SSwd+eps) else 'black'))
            ax[1].plot(r2SSwe, r2OSwe, 'o', color='blue' if r2SSwe>(r2OSwe+eps) else ('green' if (r2OSwe>r2SSwe+eps) else 'black'))
            
            ax[0].set_title('Weekday')
            ax[1].set_title('Weekend')
            
            for a in ax:
                a.set_xlabel('steadyState')
                a.set_ylabel('oneState')


def plotR2WdVsWe(bDict, pred='dailySS',  bTypeLst=['Apt', 'Off'], eps=0.01):
    fig, ax = plt.subplots()
    for key in bDict:
        if any(b in key for b in bTypeLst):
            r2wd=bDict[key].predModels[pred].Winter_wd.r2
            r2we=bDict[key].predModels[pred].Winter_we.r2
            ax.plot(r2wd, r2we, 'o', color='blue' if r2wd>(r2we+eps) else ('green' if r2we>(r2wd+eps) else 'black'))
            
            ax.set_xlabel('Weekday')
            ax.set_ylabel('Weekend')

def plotYearlyHtSpaceVSHtDHW(bDict, bTypeLst=['Apt', 'Off', 'Sch', 'Nsh'], ann=False):
    effCatColDict={'R':'red', 'E':'green', 'T':'blue'}
    for bType in bTypeLst:
        fig,ax = plt.subplots()
        for key in bDict:
            if bType in key:
                effCat=key.split('_')[2]
                mea=True if int(key.split('_')[1])<8000 else False
                try:
                    HtSpace=bDict[key].yearlyHtSpace/float(bDict[key].zenMetaData['Floor area [m2]'])
                except:
                    print(key)
                    continue
                try:
                    HtDHW=bDict[key].yearlyHtDHW/float(bDict[key].zenMetaData['Floor area [m2]'])
                except:
                    print(key)
                    continue
                ax.plot(HtSpace, HtDHW,'o' if mea else 'x', color=effCatColDict[effCat], label=key)
                if ann: ax.annotate(key.split('_')[1], (HtSpace, HtDHW))
                
        ax.set_title(bType)
        ax.set_xlabel('HtSpace [kWh/m2/year]')
        ax.set_ylabel('HtDHW [kWh/m2/day]')
        ax.set_ylim(bottom=0)
        ax.set_xlim(left=0)

def getlpAlpha(bDict, period='2017-02', aLst=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]):
    Tout=bDict['1-Apt-xxx_1001_R'].data_reg.Tout.copy()
    df=Tout.resample('1D').mean().to_frame(name='alpha=0')
    
    for a in aLst:
        df['alpha='+str(a)]=bd.lpSeries(Tout.resample('1D').mean(), a)
      
    return df[period]     
    
def getAlphaWeighingFactors(aLst=[0,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]):
    
    pLst=range(0,11)
    df=pd.DataFrame(index=pLst)
    for a in aLst:
        wf=[]
        for p in pLst:
            wf.append((1-a)*pow(a,p))
        df['alpha='+str(a)]=wf
    return df

def plotAlphaLP(bDict,aLst=[0,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]):
    fig,ax = plt.subplots(1,2)
    getlpAlpha(bDict, period='2017-02', aLst=aLst).reset_index(drop=True).plot(ax=ax[1], legend=False, x_compat=True)
    getAlphaWeighingFactors(aLst=aLst).plot(ax=ax[0])
    
    ax[0].set_xlabel('Previous days')
    ax[0].set_ylabel('Weighting factor')
    ax[1].set_xlabel('Day')
    ax[1].set_ylabel('Temperature [C]')
    
def renameFiles(chanName='changedEfficiencyCategory.csv', oldDir='zenCSV/', newDir='zenCSV_new/'):
    import os
    import shutil
    df = pd.read_csv(chanName, sep=';', index_col=0, encoding='mbcs')
    for oldname in os.listdir(oldDir):
        if oldname.endswith('.txt'):
            key=oldname.split('.')[0]
            if key in df.index:
                if df.loc[key, 'New'] in ['R', 'T', 'E']:
                    newname=key[:-1]+df.loc[key, 'New']+'.txt'
                    shutil.copy2(oldDir+oldname, newDir+newname)
            else:
                shutil.copy2(oldDir+oldname, newDir+oldname)             
    return