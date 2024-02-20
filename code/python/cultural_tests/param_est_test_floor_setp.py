#from ast import Param
from ocp.param_est import ParameterEstimation
import numpy as np
import json
import casadi as ca
import ocp.dae as dae
import ocp.integrators as integrators
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint
from matplotlib import rc
from ocp.tests.utils import get_opt_config_path, get_data_path
import os
from ocp.dae import DAE
from ocp.integrators import RK4, IRK
# text:
rc('mathtext', default='regular')
# datetime:
#plt.rcParams["date.autoformatter.minute"] = "%Y-%m-%d %H:%M"
import matplotlib.dates as mdates
import stats
import analyse
from pprint import pprint

if __name__ == "__main__":
    
    #dat = pd.read_excel("eiksveien.xlsx")
    #dat.to_csv("eiksveien.csv", index=True)
    #dat = pd.read_csv("eiksveien.csv", sep=";", index_col=0)
    #dat.index = pd.to_datetime(dat.index)  
    #dat = pd.read_csv("parsed/20230319_20230326.csv", sep=";", index_col=0)
    dat = pd.read_csv("parsed/20230326_20230409.csv", sep=";", index_col=0)
    dat.index = pd.to_datetime(dat.index)
    #dat = dat.loc["2023-03-19 23:00:00+0100":"2023-03-23 23:00:00+0100"]
    dat = dat.loc["2023-03-29 06:00:00+0100":"2023-03-30 23:00:00+0100"]
    #analyse.plot_apt(df, apt='H0101', freq='5T', acc=True)
    analyse.plot_agg_apt(dat, analyse.first_floor, freq='1H', acc=False)
    plt.show()
    analyse.plot_agg_apt(dat, analyse.second_floor, freq='1H', acc=False)
    plt.show()
    analyse.plot_apt(dat, apt="H0205", freq='5T', acc=False)
    plt.show()
    
    u_cols = [col for col in dat.columns if "2042" in col]
    
    floor_cols = [col for col in dat.columns if "_320_" in col]
    vent_cols = [col for col in dat.columns if "_360_" in col]
    temp_cols = [col for col in dat.columns if "_563_" in col]
    en_cols = [col for col in dat.columns if "_OE2" in col]
    scnd_flr_tmps = [col for col in temp_cols if "_20" in col and col.endswith("RT601") and not col.split("_")[2].endswith("4")]
    av_cols = [col for col in dat.columns if "_360_" in col and "_RT501" in col and "_20" in col]
    
    """
    dat[av_cols].mean(axis=1).plot()
    
    tur = '1273_320_001_RT401'
    retur = '1273_320_001_RT501'
    flow = '1273_320_002_JP402_Flow'
    
    ax = dat[tur].plot()
    dat[retur].plot(color="r", linestyle="dashed", ax=ax)
    ax1 = ax.twinx()
    dat[flow].plot(color="m", ax=ax1, drawstyle="steps")
    plt.show()
    """
    til = '1273_360_201_RT401'
    av = '1273_360_201_RT501'
    flo = '1273_360_201_JV401_C'
    rho = 1.293
    cp = 1005 # kJ/(kg*K)
    
    # estimate air exchange in (m^3/s):
    diff = dat[til] - dat[av]
    Q_dot_vent = dat[flo]*0.01*diff*cp*rho
    
    """
    ax = dat[til].plot(drawstyle="steps")
    dat[av].plot(color="r", linestyle="dashed", ax=ax, drawstyle="steps")
    ax1 = ax.twinx()
    dat[flo].plot(color="m", ax=ax1, drawstyle="steps")
    plt.show()
    """
    
    data = pd.DataFrame()
    data[scnd_flr_tmps] = dat[scnd_flr_tmps]
    data["Ti"] = dat[scnd_flr_tmps].mean(axis=1)
    #col = '1273_563_2063_RT601'
    #col = '1273_360_201_RT501'
    #en_col = '1273_320_002_OE201.Energy'
    #data["Ti"] = dat[col]
    #data["Ti"] = dat[col]
    data["Q_dot_vent"] = Q_dot_vent
    data["phi_h_act"] = dat[en_cols].sum(axis=1).diff().fillna(0)*1000
    #data["phi_h"] = dat[en_col].diff().fillna(0)*1000
    #data["phi_h"] = dat[en_col]
    data["phi_s"] = dat["SolGlob"]
    data["Ta"] = dat["Tout"]
    
    data["Ta"] += 273.15
    data["Ti"] += 273.15
    
    # resample:
    #phi_h = data[["phi_h", "Q_dot_vent"]].resample(rule="15min").mean()
    #wea = data[["Ti", "Ta", "phi_s"]].resample(rule="15min").asfreq()
    #phi_h = data[["phi_h", "Q_dot_vent"]].resample(rule="1H").mean()
    #wea = data[["Ti", "Ta", "phi_s"]].resample(rule="1H").asfreq()
    
    #data = pd.concat([phi_h, wea], axis=1)
    #data = dat
    
    #data.to_csv("eiksveien_Q_vent.csv")
    
    """
    ax = data["Ti"].plot()
    ax1 = ax.twinx()
    data["phi_h"].diff().plot(ax=ax1, color="k", linestyle="dashed", drawstyle="steps")
    plt.show()
    """
    
    y_data = data
    
    #ax = data[["Ti"]].plot(color="r")
    #ax1 = ax.twinx()
    #data[["phi_h"]].plot(ax=ax1, color="g", drawstyle="steps")
    #plt.show()
    #start = "2023-02-06 00:00:00+01:00"
    #stop = "2023-02-13 00:00:00+01:00"
    
    #y_data = data.loc[start:stop]
    y_data["y1"] = data["Ti"]
    dt = (y_data.index[1] - y_data.index[0]).seconds
    
    y_data.index = np.arange(0, len(y_data)*dt, dt)
    #cfg_path = "2R2C.json"
    cfg_path = "3R3C_novent_eiv.json"
    N = len(y_data)
    #dt = y_data.index[1] - y_data.index[0]
    
    #y_data.to_csv("1st_floor.csv", index=True)
    
    #param_guess = ca.DM([0.1,0.1,0.1,1E6,1E6,1E7,5,1])
    param_guess = ca.DM([0.1,0.1,0.1,1E6,1E7,1E7,5])
    #lbp = ca.DM([0.001,0.01,1E5,1E6,1])
    #ubp = ca.DM([0.1,0.1,1E7,1E8,50])
    lbp = 0.01*param_guess
    ubp = 100*param_guess
    lbx = np.repeat((y_data[["y1"]].values - 15), 3)
    ubx = np.repeat((y_data[["y1"]].values + 15), 3)
    #lbp = -np.inf
    #ubp = np.inf
    #param_guess = ca.DM([0.001,0.009,1,1E6,1E7,1])
    #param_est = ParameterEstimation(cfg_path, y_data, param_guess)
    
    #    with ParameterEstimation(config=cfg_path,
    #                             data=y_data,
    #                             param_guess=param_guess) as param_est:
    
    x_nom = 300
    
    kwargs = {
        "x_nom": x_nom,
        "u_nom": 5000,
        "r_nom": 300,
        "y_nom": 300,
        #"slack": True
        "slack": True
    }
    
    
    with ParameterEstimation(config=cfg_path,
                             N=N,
                             dt=dt,
                             param_guess=param_guess,
                             **kwargs) as param_est:
        
        Q = ca.DM.eye(3)
        #Q[1,0] = 1
        #Q[0,1] = 1
        R = ca.DM.eye(1)
        # provide Q, R in solve here:
        # provide lb, ub for p here:
        sol, params = param_est.solve(
                                      y_data,
                                      param_guess,
                                      lbx=lbx/x_nom,
                                      ubx=ubx/x_nom,
                                      lbp=lbp,
                                      ubp=ubp,
                                      covar=ca.veccat(Q, R)
                                      )
    
        pprint(params)
        
        ax = sol["Ti"].plot(color="grey")
        ax = y_data["y1"].plot(color="black", linestyle="dashed", drawstyle="steps")
        ax.legend(["Estimated", "True"])
        plt.show()
        

        # check simulation:
        order = 2
        method = "radau"
        
        with open(cfg_path) as file:
            config = json.load(file)

        model = config["model"]
        #dt = config["dt"]
        dt = 900
        #N = config["N"]
        N = len(y_data)
        #n_steps = config["n_steps"]

        # create a dae
        dae = DAE(model)    
        # integrator:
        cfg = config["integrator"]
        cfg["dt"] = dt
        Coll = IRK(dae, **cfg)

        # true parameters:
        param_arr = params.values
        u_data = y_data[["phi_h", "Ta", "phi_s", "Q_dot_vent"]]
        #X = Coll.simulate(x0, u_data, param_truth)
        X = sol[["Ti","Th","Te"]].iloc[0].values
        #res = np.array([])
        df = pd.DataFrame(columns=["Ti", "Th", "Te"])
        df.loc[0] = X
        for n in range(N):
            X = Coll.one_sample(X, 0, u_data.iloc[n], param_arr, 0, 0)
            #xf = Coll.one_sample(X, u_data[n], param_truth[0], param_truth[1], param_truth[2], param_truth[3])
            #X = xf[0]
            #res = np.append(res, X)
            df.loc[(n+1)*dt] = np.array(X).flatten()

        # measurement data
        #y_data = X[0,:].T
        #y_data = res
        ###################################################

        #df = pd.DataFrame(data=res, columns=["Ti", "Te"])
        #dt = np.arange(0, config["dt"]*len(df), config["dt"])
        #df["u1"] = np.array(u_data).flatten()
        #df["y_own"] = np.array(y_data).flatten()
        #df["y_sim"] = np.array(y_data).flatten()
        df.Ti.plot()
        plt.show()
        #df.index = np.arange(0, cfg["dt"]*N, cfg["dt"])
                
        #assert(ca.norm_inf(p_sol-true_params)<1e-8)