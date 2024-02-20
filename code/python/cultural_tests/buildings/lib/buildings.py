# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 06:59:21 2018

@author: hwaln
"""

import scipy.interpolate as si
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import os

#bspline test

#k=3
#t1=np.full(k,float(0))
#t2=np.linspace(0, 23, 7)
#t3=np.full(k,float(23))
#t=np.concatenate((t1,t2,t3))
#c=[0., 38.25882, -145.81501, 202.95329, 36.56135, 69.96107, 79.55251, 55.60450, 53.73915]
#sp1= si.BSpline(t,c,k, extrapolate=False)
#x96=np.linspace(0, 23, 96)
#sp1(x96)
#plt.plot(x96, sp1(x96), 'b-', lw=2, alpha=0.7, label='BSpline')
#plt.show()

class building():
    
    def __init__(self,name='Building'):
        """create buliding class containing prediction parameters
            and functions
        """
        self.name = name
                
        #metadata
        self.zenMetaData=0
        self.yearlyHeatConsumption = np.nan
                
        #data
        self.data_reg=pd.DataFrame()
        self.data_new=pd.DataFrame()
        
        #prediction models
        self.predModels={}

        return
      
    def setRegData(self, df):
        self.data_reg=df
        #check if data contains date info
        if not 'tday' in self.data_reg.columns:
            addDateInfo(self.data_reg)
        #check if data_reg contains outdoor temperature    
        if not 'Tout' in self.data_reg.columns:
            print('Warning: dataset does not contain outdoor temperature (Tout)')
        return
    
    def setNewData(self, df):
        self.data_new=df.copy()
        #check if data contains date info
        if not 'tday' in self.data_new.columns:
            addDateInfo(self.data_new)
        #check if data_reg contains outdoor temperature    
        if not 'Tout' in self.data_new.columns:
            print('Warning: dataset does not contain outdoor temperature (Tout)')
        return
    
    def setBildingPredModelsFromDir(self,directory, name='main', modType='Season', r2Tresh=False):
        if modType=='Season':
            pc=seasonPredCont(name=name)
            self.predModels[name]=pc
            for filename in os.listdir(directory):
                if filename.endswith('.dat'):
                    fname = filename.split('.')[0]
                    if self.name in fname:
                        season=fname.split('_')[-2]
                        day=fname.split('_')[-1]
                        if season=='w':
                            if day=='wd':
                                pc.Winter_wd.setPredictorFromRegFile(directory+filename, r2Tresh=r2Tresh)
                                if pc.Winter_wd.set : pc.setlp_alpha(pc.Winter_wd.lpAlpha)
                            elif day=='we':
                                pc.Winter_we.setPredictorFromRegFile(directory+filename, r2Tresh=r2Tresh)
                                if pc.Winter_we.set : pc.setlp_alpha(pc.Winter_we.lpAlpha)
                            else:
                                print('Warning:Full week predictor not available:'+filename)
                        elif season=='s':
                            if day=='wd':
                                pc.Summer_wd.setPredictorFromRegFile(directory+filename, r2Tresh=r2Tresh)
                                if pc.Summer_wd.set : pc.setlp_alpha(pc.Summer_wd.lpAlpha)
                            elif day=='we':
                                pc.Summer_we.setPredictorFromRegFile(directory+filename, r2Tresh=r2Tresh)
                                if pc.Summer_we.set : pc.setlp_alpha(pc.Summer_we.lpAlpha)
                            else:
                                print('Warning:Full week predictor not available:'+filename)
                        elif season=='m':
                            if day=='wd':
                                pc.Middle_wd.setPredictorFromRegFile(directory+filename, r2Tresh=r2Tresh)
                                if pc.Middle_wd.set : pc.setlp_alpha(pc.Middle_wd.lpAlpha)
                            elif day=='we':
                                pc.Middle_we.setPredictorFromRegFile(directory+filename, r2Tresh=r2Tresh)
                                if pc.Middle_we.set : pc.setlp_alpha(pc.Middle_we.lpAlpha)
                            else:
                                print('Warning:Full week predictor not available:'+filename)                       
                        elif season=='a':
                            if day=='wd':
                                pc.Winter_wd.setPredictorFromRegFile(directory+filename, r2Tresh=r2Tresh)
                                if pc.Winter_wd.set : pc.setlp_alpha(pc.Winter_wd.lpAlpha)
                                pc.Summer_wd=pc.Winter_wd
                                pc.Middle_wd=pc.Winter_wd
                            elif day=='we':
                                pc.Winter_we.setPredictorFromRegFile(directory+filename, r2Tresh=r2Tresh)
                                if pc.Winter_we.set : pc.setlp_alpha(pc.Winter_we.lpAlpha)
                                pc.Summer_we=pc.Winter_we
                                pc.Middle_we=pc.Winter_we
                            else:
                                print('Warning:Full week predictor not available:'+filename)
                        else:
                            print('Warning:Predictor not available:'+filename)
        elif modType=='Year':
            pc=yearlyPredCont(name=name)
            self.predModels[name]=pc
            for filename in os.listdir(directory):
                if filename.endswith('.dat'):
                    fname = filename.split('.')[0]
                    if self.name in fname:
                        season=fname.split('_')[-2]
                        day=fname.split('_')[-1]                    
                        if season=='Tot':
                            if day=='wd':
                                pc.Year_wd.setPredictorFromRegFile(directory+filename, r2Tresh=r2Tresh)
                                if pc.Year_wd.set : pc.setlp_alpha(pc.Year_wd.lpAlpha)
                            elif day=='we':
                                pc.Year_we.setPredictorFromRegFile(directory+filename, r2Tresh=r2Tresh)
                                if pc.Year_we.set : pc.setlp_alpha(pc.Year_we.lpAlpha)
                            else:
                                print('Warning:Full week predictor not available:'+filename)
                        
                        else:
                            print('Warning:Predictor not available:'+filename)
        else:
            print('Error: unknown prediction model type')
            return
        return
      
    def predictRegData(self, model='Season'):
        #check that data exists
        if self.data_reg.empty:
            print('ERROR: Prediction data not set')
            return
        
        #get prediction model container
        try:
            pc=self.predModels[model]
        except:
            print('ERROR: Prediction model not set')
            return
    
#        if year:
            #run outdoor temperature through lp_filter
            if pc.lpAlpha==None:
                return print(f'Warning: {self.name} predModel {pc.name} lpAlpha is not set. Aborting prediction')
            elif self.lpAlpha==0:
                self.data_reg['Toutlp_' + model]=self.data_new['Tout']
            else:
                self.data_reg['Toutlp_' + model]=lpSeries(self.data_reg['Tout'], pc.lpAlpha)
            #predict
            self.data_reg['HtTot_pred_' + model]=self.data_reg.apply(pc.predictRow, axis=1, year=True)
        return
    
    def predictNewData(self, model='Season'):
        #check that data exists
        if self.data_new.empty:
            print('ERROR: Prediction data not set')
            return
        
        #get prediction model container
        try:
            pc=self.predModels[model]
        except:
            print('ERROR: Prediction model not set')
            return
    
        #run outdoor temperature through lp_filter
        if pc.lpAlpha==None:
            return print(f'Warning: {self.name} predModel {pc.name} lpAlpha is not set. Aborting prediction')
        elif pc.lpAlpha==0:
            self.data_new['Toutlp_' + model]=self.data_new['Tout']
        else:
            self.data_new['Toutlp_' + model]=lpSeries(self.data_new['Tout'], pc.lpAlpha)
        #predict
        self.data_new['HtTot_pred_' + model]=self.data_new.apply(pc.predictRow, axis=1)
    

    
    def getSummaryDict(self):
        d={}
        df=self.data_reg
        d['name']=self.name
        d['bTypeId']=self.name.split('_')[0]
        d['bEnum']='_'.join(self.name.split('_')[1:])
        #d['fname']=filename
        #metadata
        d['Year']=self.zenMetaData['Year_of_construction']
        d['Area']=self.zenMetaData['Floor_area_heat'] if 'Floor_area_heat' in self.zenMetaData else self.zenMetaData['Floor_area_total']
        #Weather data
        if 'Tout' in df:
            d['ToutMean']=df['Tout'].groupby([df.index.month, df.index.day, df.index.hour]).mean().mean()   
            d['ToutMin']=df['Tout'].min()
        #energy data
        if 'HtTot' in df:
            d['sumHeat']=df['HtTot'].groupby([df.index.month, df.index.day, df.index.hour]).mean().mean()*365*24 #assuming representative period
            d['peakHeat']=df['HtTot'].max()
            d['beta_Tout_w_wd']=self.Winter_wd.Tout_beta
            d['R^2_w_wd']=self.Winter_wd.r2
        if 'ElTot' in df:
            d['sumEl']=df['ElTot'].groupby([df.index.month, df.index.day, df.index.hour]).mean().mean()*365*24 #assuming representative period
            d['peakEl']=df['ElTot'].max()
        ##counter values
        d['total rows']=df.shape[0]
        #weather data
        if 'Tout' in df : d['countToutNaN']=df['Tout'].isnull().sum()
        if 'WindSpd' in df : d['countToutNaN']=df['WindSpd'].isnull().sum()
        if 'SolGlob' in df : d['countToutNaN']=df['SolGlob'].isnull().sum()
        #energy data
        if 'HtTot' in df:
            d['countHeatNaN']=df['HtTot'].isnull().sum()
            d['countHeatNaNorZero']=df.shape[0]-df.HtTot[df.HtTot>0].count()
        #energy data
        if 'ElTot' in df:
            d['countElNaN']=df['ElTot'].isnull().sum()
            d['countElNaNorZero']=df.shape[0]-df.ElTot[df.ElTot>0].count()
        return d
    
class seasonPredCont():
    def __init__(self, name="", bname=""):
        self.name=name
        self.bname=bname

        self.resample=None
        self.lpAlpha=None
        #predictors
        self.Winter_wd=predictor()
        self.Winter_we=predictor()
        self.Summer_wd=predictor()
        self.Summer_we=predictor()
        self.Middle_wd=predictor()
        self.Middle_we=predictor()
        
    def setlp_alpha(self, lp_a):
        #check if lp_alpha already set
        if self.lpAlpha==None:
            self.lpAlpha=lp_a
            return
        #check if equal
        if not self.lpAlpha==lp_a:
            print(f'Warning: {self.name} lp_alpha is changed from {self.lpAlpha:.2f} to  {lp_a:.2f}')
            self.lpAlpha=lp_a
        return
    
    def predictRow(self, row):
        #predict each point in dataset
        HtTot_pred=0
        tday=row['tday']
        Tout=row['Tout']
        Toutlp=row['Toutlp_' + self.name]
        
        if row.Season =='Winter':
            if row.WorkingDay==1:
                if self.Winter_wd.set: 
                    HtTot_pred=self.Winter_wd.predictValue(Tout,Toutlp, tday)
            elif row.WorkingDay==0:
                if self.Winter_we.set: 
                    HtTot_pred=self.Winter_we.predictValue(Tout, Toutlp, tday)
        if row.Season =='Summer':
            if row.WorkingDay==1:
                if self.Summer_wd.set: 
                    HtTot_pred=self.Summer_wd.predictValue(Tout, Toutlp, tday)
            elif row.WorkingDay==0:
                if self.Summer_we.set: 
                    HtTot_pred=self.Summer_we.predictValue(Tout, Toutlp, tday)
        if row.Season =='Middle':
            if row.WorkingDay==1:
                if self.Middle_wd.set: 
                    HtTot_pred=self.Middle_wd.predictValue(Tout, Toutlp, tday)
            elif row.WorkingDay==0:
                if self.Middle_we.set: 
                    HtTot_pred=self.Middle_we.predictValue(Tout, Toutlp, tday)
        
        return HtTot_pred

        
class yearlyPredCont():
    def __init__(self, name="", bname=""):
        self.name=name
        self.bname=bname
        
        self.resample=None
        self.lpAlpha=None
        #predictors
        self.Year_wd=predictor()
        self.Year_we=predictor()

    def setlp_alpha(self, lp_a):
        #check if lp_alpha already set
        if self.lpAlpha==None:
            self.lpAlpha=lp_a
            return
        #check if equal
        if not self.lpAlpha==lp_a:
            print(f'Warning: {self.name} lp_alpha is changed from {self.lpAlpha:.2f} to  {lp_a:.2f}')
            self.lpAlpha=lp_a
        return
    
    def predictRow(self, row):
        #predict each point in dataset
        HtTot_pred=0
        tday=row['tday']
        Tout=row['Tout']
        Toutlp=row['Toutlp_' + self.name]
        if row.WorkingDay==1:
            if self.Year_wd.set: 
                HtTot_pred=self.Year_wd.predictValue(Tout, Toutlp, tday)
        elif row.WorkingDay==0:
            if self.Year_we.set: 
                HtTot_pred=self.Year_we.predictValue(Tout, Toutlp, tday)
        return HtTot_pred

class predictor():
    def __init__(self):
        
        self.set = False
        #Prediction data
        self.intercept = 0
        self.tday_spl = 0
        self.Tout_beta = 0
        self.Tout_spl = 0
        self.lpAlpha = 0
        self.ToutLP_beta = 0
        self.ToutLP_spl = 0
        self.G_beta = 0
        self.G_spl = 0
        self.G_lpAlpha = 0
        self.CPT = False
        
        #regression data
        self.r2=0

    def setPredictorFromRegFile(self, fname, r2Tresh=False):
        try:
            res, par, coef = readRFitResultFile(fname)
        except: 
            print(f'Warning: {fname} error in result file reading')
        if r2Tresh:
            if float(res['R^2'])<r2Tresh:
                self.r2=float(res['R^2'])
                self.set=False
                return print(f'Warning: {fname} R^2= {self.r2:.2f} < {r2Tresh:.2f} predictor not set')
        if 'CPT' in par:
            self.CPT = float(par['CPT'])

        self.intercept=float(coef['Intercept'])
        self.tday_spl=genSplineFromRFitResulsts(len(coef['c_tday']),coef['c_tday'])

        try:
            self.Tout_beta = [float(i) for i in coef['cpt_Ta']] if self.CPT else float(coef['Ta']) if 'Ta' in coef else 0
        except ValueError:
            return print(f'Warning: {fname} Tout_beta not float, predictor not set')
        self.Tout_spl=genSplineFromRFitResulsts(len(coef['c_Ta']),coef['c_Ta'])
        
        try:
            self.ToutLP_beta = [float(i) for i in coef['cpt_Ta1']] if self.CPT else float(coef['Ta1']) if 'Ta1' in coef else 0
        except ValueError:
            return print(f'Warning: {fname} ToutLP_beta not float, predictor not set')
        self.ToutLP_spl=genSplineFromRFitResulsts(len(coef['c_Ta1']),coef['c_Ta1'])
        
        try:
            self.lpAlpha=float(coef['lp_Ta1']) if 'lp_Ta1' in coef else 0
        except ValueError:
            return print(f'Warning: {fname} LP_alpha not float, predictor not set')
        
        try:
            self.G_beta = float(coef['G']) if 'G' in coef else 0
        except ValueError:
            return print(f'Warning: {fname} G_beta not float, predictor not set')
        self.G_spl=genSplineFromRFitResulsts(len(coef['c_G']),coef['c_G'])
        
        try:
            self.G_lpAlpha=float(coef['lp_G']) if 'lp_G' in coef else 0
        except ValueError:
            return print(f'Warning: {fname} G_LP_alpha not float, predictor not set')
        
        self.r2=float(res['R^2'])
        self.set = True
        return
    
    def predictValue(self, Tout, Toutlp, tday):
        if self.CPT:
            if Toutlp<self.CPT:
                HtTot=self.intercept+self.ToutLP_beta[1] + self.tday_spl(tday)+ Toutlp*(self.ToutLP_beta[0]+self.ToutLP_beta[2])
            else:
                HtTot=self.intercept + self.tday_spl(tday)+ Toutlp*(self.ToutLP_beta[0])
        else:
            HtTot=self.intercept+self.tday_spl(tday)+Tout*(self.Tout_beta+self.Tout_spl(tday)) + Toutlp*(self.ToutLP_beta+self.ToutLP_spl(tday))
        return HtTot

def genSplineFromCoefficients (t,c,k=3):
    """
    generate scipy bspline based coeffisents from R
    t = knots array boundary knots and internal knots
    c = coeffcients from R. remember to include first coeffisient =0 if intercept=False
    k = degrees (order) k=3 equals cubic spline
    """
    t1=np.full(k,float(0))
    t3=np.full(k,float(23))
    t=np.concatenate((t1,t,t3))
    spl= si.BSpline(t,c,k, extrapolate=True)
    return spl

def plotDaySpline(spl, lw=1):
    x=np.linspace(0, 23, 24)
    return plt.plot(x, spl(x), lw=lw)

def readRFitResultFile(fname):
    res={}
    par={}
    c={}
    coef={}
    with open(fname, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        row = next(reader)
        res[row[0]]=row[1]
        nres = int(row[1])
        for i, row in enumerate(reader):
            if i>(nres-1):
                break
            if not row:
                break
            #k, v = row
            #d[k] = v
            res[row[0]]=row[1]
        par[row[0]]=row[1]
        npar = int(row[1])
        for i, row in enumerate(reader):
            if i>(npar-1):
                break
            if not row:
                break
            #k, v = row
            #d[k] = v
            par[row[0]]=row[1]
        for i, row in enumerate(reader):
            c[row[0]]=row[1]

    coef['Intercept'] = c['(Intercept)'] if '(Intercept)' in c else 0
    if 'CPT' in par:
        coef['cpt_Ta']=[]
        coef['cpt_Ta'].append(c['Ta'] if 'Ta' in c else 0)
        coef['cpt_Ta'].append(c['Ta < CPTTRUE'] if 'Ta < CPTTRUE' in c else 0)        
        coef['cpt_Ta'].append(c['Ta:Ta < CPTTRUE'] if 'Ta:Ta < CPTTRUE' in c else 0)
        coef['cpt_Ta1']=[]
        coef['cpt_Ta1'].append(c['Ta1'] if 'Ta1' in c else 0)
        coef['cpt_Ta1'].append(c['Ta1 < CPTTRUE'] if 'Ta1 < CPTTRUE' in c else 0)        
        coef['cpt_Ta1'].append(c['Ta1:Ta1 < CPTTRUE'] if 'Ta1:Ta1 < CPTTRUE' in c else 0)
    else:
        coef['Ta']=c['Ta'] if 'Ta' in c else 0
        coef['Ta1']=c['Ta1'] if 'Ta1' in c else 0
    coef['G']=c['G'] if 'G' in c else 0
    coef['lp_Ta1']=c['lp_Ta1'] if 'lp_Ta1' in c else 0
    coef['lp_G']=c['lp_G'] if 'lp_G' in c else 0
    if 'lp_Ta' in c:
        return print((f'Warning: {fname} lp_Ta not allowed. Should be lp_Ta1. Predictor not set'))
    if 'degf_tday' in par:
        ctday=[]
        for key in c:
            if 'bs(tday,' in key: ctday.append(c[key])
    else:
        ctday=[0]
    coef['c_tday']=ctday
    
    if 'degf_Ta' in par:
        cTa=[]
        for key in c:
            if 'bs(Ta,' in key: cTa.append(c[key])
    else:
        cTa=[0]
    coef['c_Ta']=cTa
    if 'degf_Ta1' in par:
        cTa1=[]
        for key in c:
            if 'bs(Ta1,' in key: cTa1.append(c[key])
    else:
        cTa1=[0]
    coef['c_Ta1']=cTa1
    if 'degf_G' in par:
        cG=[]
        for key in c:
            if 'bs(G,' in key: cG.append(c[key])
    else:
        cG=[0]
    coef['c_G']=cG

    return res, par, coef

def genSplineFromRFitResulsts(degf, c):
    if degf==1:
        if c[0]==0: return dumspl0
        if c[0]==1: return dumspl1
    z=[0]
    c=z+c
    t=np.linspace(0,23,int(degf)-1)
    spl=genSplineFromCoefficients(t,c)
    return spl

def dumspl0(v):
    return 0

def dumspl1(v):
    return 1

def predictFromCoef(coef, t_day, Tout):
    #get time of day spline
    z=[0]
    c=z+coef['c_tday']
    t=np.linspace(0,23,int(len(coef['c_tday']))-1)
    spl=genSplineFromCoefficients(t,c)
    Q=float(coef['Intercept'])+spl(t_day)+float(coef['c_Ta'][0])*Tout
    
    return Q


def lpSeries(s,a1):
    slp=pd.Series(index=s.index)
    j=0
    for i in s.index:
        s_i=s.iloc[j]
        if j > 0:
            slp_i1=slp.iloc[j-1] if not np.isnan(slp.iloc[j-1]) else s.iloc[j]
            slp.iloc[j] = a1*slp_i1+(1-a1)*s_i
        else:
            slp.iloc[j]=s.iloc[j]
        j+=1
    return slp



#def createBulidingFromRegFile(fname):
#    b=predBuilding(fname.split('.')[0])
#    res, par, coef = readRFitResultFile(fname)
#    b.intercept=float(coef['Intercept'])
#    b.spl=genSplineFromRFitResulsts(par,coef)
#    b.ToutLP_beta=float(coef['c_Ta'][0])
#    b.lpAlpha=float(coef['lp_Ta'])
#    return b
    
#add date information
def addDateInfo (df):
    df['tday']=df.index.hour
    #add weekend (=0) and not weekend (=1) info
    df['WorkingDay']=(df.index.dayofweek<5).astype(int)
    df['Season']=df.index.map(get_season)
    return df

def resampleBuildingData(df, freq):
    #resamples data frame according to zen specification
    #df = dataframe
    #freq = resampling frequency
    
    #function to only include days with full dataset
    def nansumwrapper(a, **kwargs):
        if np.isnan(a).any():
            return np.nan
        else:
            return np.nansum(a, **kwargs)    
    #create dictionary of resampling methods
    d={}
    meanLst=['Tout', 'WindSpd','WindDir','RH','Ti', 'tday', 'WorkingDay', 'DHTs', 'DHTr']
    sumLst=['SolGlob','SolDir','SolDiff','HtMass','HtSup','HtRet','ElTot','ElLight','ElPlug','ElAux', 'ElHP','ElHeat','ElOth','HtTot','HtSpace','HtRoom','HtVent','HtDHW', 'HtSnow', 'DHVF']
    firstLst=['Season']
    for col in df.columns:
        if col in meanLst:
            d[col]='mean'
        elif col in sumLst:
            d[col]=nansumwrapper
        elif col in firstLst:
            d[col] = 'first'
        else:
            print('Warning: resampleBuildingData: '+ col +' not in resample method list. Variaable not included')
 
    df=df.resample(freq).agg(d)
    return df
    
    

def get_season(date):
    Y=2016 #leap year to be sure
#    if (date.year):
#        Y = date.year
    seasons = {'Summer':(pd.Timestamp(Y,6,1), pd.Timestamp(Y,9,1)),
               'Autumn':(pd.Timestamp(Y,9,1), pd.Timestamp(Y,12,1)),
               'Spring':(pd.Timestamp(Y,3,1), pd.Timestamp(Y,6,1))}
    date=date.replace(year=Y)
    for season,(season_start, season_end) in seasons.items():
        if date>=season_start and date<= season_end:
            return season
    else:
        return 'Winter'    
    

def get_seasonID(date):
    Y = 2017
    seasons = {3:(pd.Timestamp(Y,6,1), pd.Timestamp(Y,9,1)),
               4:(pd.Timestamp(Y,9,1), pd.Timestamp(Y,12,1)),
               2:(pd.Timestamp(Y,3,1), pd.Timestamp(Y,6,1))}
    date=date.replace(year=Y)
    for season,(season_start, season_end) in seasons.items():
        if date>=season_start and date<= season_end:
            return season
    else:
        return 1

def splitSeasons(df):
    df_W = df.loc[df.Season == 'Winter']
    df_S = df.loc[df.Season == 'Summer']
    df_M = df.loc[(df.Season != 'Winter') & (df.Season != 'Summer')]
    return df_W, df_S, df_M
    
def testForHoliday(df, openingHours=[8,16]):
    if not 'tday' in df : df=addDateInfo(df)
    wd_mean=((df.HtTot[(df.index.dayofweek<5) & (df.tday<16) & (df.tday>8)].resample('1D').mean()
            -df.HtTot[(df.index.dayofweek<5) & ((df.tday>16) | (df.tday<8))].resample('1D').mean())
            /df.HtTot.resample('1D').mean()).mean()
    we_mean=((df.HtTot[(df.index.dayofweek>4) & (df.tday<16) & (df.tday>8)].resample('1D').mean()
            -df.HtTot[(df.index.dayofweek>4) & ((df.tday>16) | (df.tday<8))].resample('1D').mean())
            /df.HtTot.resample('1D').mean()).mean()
    h_tresh=we_mean+(wd_mean-we_mean)*0.2
    wd=((df.HtTot[(df.index.dayofweek<5) & (df.tday<16) & (df.tday>8)].resample('1D').mean()
            -df.HtTot[(df.index.dayofweek<5) & ((df.tday>16) | (df.tday<8))].resample('1D').mean())
            /df.HtTot.resample('1D').mean())
    h=wd[wd<h_tresh]
    return h