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

def readRFitResultFile(fname):
    res={}
    par={}
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
        coef[row[0]]=row[1]
        row = next(reader)
        coef['Intercept']=row[1]
        nc_tday = int(par['degf_tday'])
        nc_Ta = int(par['degf_Ta'])
        ctday=[]
        cTa=[]
        for i, row in enumerate(reader):
            if i>(nc_tday+nc_Ta-1):
                break
            if not row:
                break
            if i<(nc_tday):
                ctday.append(row[1])
            else:
                cTa.append(row[1])
        coef['c_tday']=ctday
        coef['c_Ta']=cTa
        coef[row[0]]=row[1]
    return res, par, coef

def genSplineFromRFitResulsts(fname):
    res, par, coef = readRFitResultFile(fname)
    z=[0]
    c=z+coef['c_tday']
    t=np.linspace(0,23,int(par['degf_tday'])-1)
    spl=genSplineFromCoefficients(t,c)
    return spl

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
    for i in s.index:
        s_i=s.loc[i]
        slp_i1=slp.loc[i-1] if i > 0 else s.loc[i]
        slp.loc[i] = a1*slp_i1+(1-a1)*s_i
    return slp

