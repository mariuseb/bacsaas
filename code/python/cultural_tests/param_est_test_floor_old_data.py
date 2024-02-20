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

if __name__ == "__main__":
    
    """
    wea = pd.read_excel("Energi/2022_1361.xlsx")
    #wea = wea.ffill()
    wea.index = pd.to_datetime(wea.TimeStamp)
    wea = wea.resample(rule="15min").ffill()
    cfg_path = os.path.join(get_opt_config_path(), "2R2C.json")
    
    first_floor = ["H101", "H102", "H103",
                   "H104", "H105", "H106"]
    
    en_path = os.path.join("Energi", "apt", "ht_1flo.txt")
    heat = pd.read_csv(en_path, sep=";")
    heat.index = pd.to_datetime(heat.Timestamp)
    heat.drop(columns=["Timestamp"], inplace=True)
    heat = heat.diff().bfill()
    
    for apt in first_floor:
        
        data_path = os.path.join("Energi", "apt", apt + ".txt")
        
        data = pd.read_csv(data_path, sep=";")
        data.index = pd.to_datetime(data.Timestamp)

        
        # extract only 2022 from 'data'
        inds_keep = [ndx for ndx in data.index if ndx.year == 2022]
        
        # merge data and wea for 2022
        data["phi_s"] = wea["SolGlob"].loc[inds_keep]
        data["Ta"] = wea["Tout"].loc[inds_keep]
        
        # NB! has outliers
        #df = heat
        #col = "1273_320_002_OE%s.Energy(kW-hr)" % (apt.lstrip("H0"), )
        #data["phi_h"] = df[col]
    
        # write:
        filename = apt + "_wea.csv"
        data.to_csv(filename, index=True)
        print("Wrote " + filename)
    """
    #q_low = df[col].quantile(0.01)
    #q_hi  = df[col].quantile(0.99)

    # write:
    #data.to_csv("H101_wea.csv", index=True)
    
    #q_low = df[col].quantile(0.01)
    #q_hi  = df[col].quantile(0.99)
    
    #heat_filt = df[(df[col] < q_hi) & (df[col] > q_low)]
    """
    files = ["H101_wea.csv", "H102_wea.csv", "H103_wea.csv",
             "H104_wea.csv", "H105_wea.csv", "H106_wea.csv"]
    
    dfs = []
    for file in files:
        df = pd.read_csv(file, index_col=0)
        dfs.append(df)
        
    df = pd.concat(dfs, axis=1)
    
    # extract only temperatures:
    temp_cols = [col for col in df.columns if "°C" in col and not col.split("_")[2].endswith("4")]
    temp = df[temp_cols]
    temp.index = pd.to_datetime(temp.index)
    #equiv_temp = temp.mean(axis=1)
    
    en_path = os.path.join("Energi", "apt", "ht_1flo.txt")
    heat = pd.read_csv(en_path, sep=";")
    heat.index = pd.to_datetime(heat.Timestamp)
    heat.drop(columns=["Timestamp"], inplace=True)
    heat = heat.diff().bfill()
    
    wea = pd.read_excel("Energi/2022_1361.xlsx")
    #wea = wea.ffill()
    wea.index = pd.to_datetime(wea.TimeStamp)
    wea = wea.resample(rule="15min").ffill()
    cfg_path = os.path.join(get_opt_config_path(), "2R2C.json")
    
    data = wea[["SolGlob", "Tout"]]
    data.columns = ["phi_s", "Ta"]
    
    keep_inds = [ndx for ndx in data.index if ndx.month == 4 and ndx.day < 7]
    data = data.loc[keep_inds]
    
    data["phi_h"] = heat.sum(axis=1).loc[keep_inds]
    data["Ti"] = temp.mean(axis=1).loc[keep_inds]
    """
    #data = pd.read_csv("H101_wea.csv", index_col=0)
    #data.index = pd.to_datetime(data.index)
    
    #keep_inds = [ndx for ndx in data.index if ndx.month < 6]
    #data = data.loc[keep_inds]
    
    #inds_keep = [ndx for ndx in data.index if ndx.year == 2022]
    #data = data.loc[inds_keep]
    
    
    # plot actuator pos, heat
    '''     
    heat_col = "phi_h"
    act_col = data.columns[3]
    
    ax = data[act_col].apply(lambda x: 0 if x == "Av" else 1).plot(color="b", drawstyle="steps")
    ax1 = ax.twinx()
    data[heat_col].plot(color="k", ax=ax1, linestyle="dashed", drawstyle="steps")
    
    plt.show()
    
    # plot temperature, actuator position together:
    temp_col = data.columns[1]
    act_col = data.columns[1]
    
    ax = data[act_col].apply(lambda x: 0 if x == "Av" else 1).plot(color="b", drawstyle="steps")
    ax1 = ax.twinx()
    data[temp_col].plot(color="k", ax=ax1)
    
    plt.show() 
    '''
    
    """
    First, take temperature of living room as only temp.
    #data["Ti"] = data['1273_563_1063_RT601(°C)'] + 273.15
    data["Ti"] += 273.15
    
    #keep_inds = [ndx for ndx in data.index if ndx.month == 4 and ndx.day < 7]
    #data = data.loc[keep_inds]
    
    data["phi_s"] = data["phi_s"].astype(float)
    data["phi_h"] *= 1000
    data["Ta"] += 273.15
    
    downsample = False
    sampling_time = "15min"
    dt = 900
    
    if downsample:
        
        heat = data[["phi_h", "phi_s"]]
        heat = heat.resample(sampling_time).mean()

        rest = data[["Ti", "Ta"]]
        rest = rest.resample(sampling_time).first()

        y_data = pd.merge(heat, rest, left_index=True, right_index=True)
        y_data["y1"] = y_data.Ti
        y_data.index = np.arange(0, len(y_data)*900, 900)
        
    else:
        
        y_data = data
        y_data["y1"] = y_data.Ti
        y_data.index = np.arange(0, len(y_data)*dt, dt)
    """
    
    """
    fig, ax = plt.subplots(2,1)
    (y_data.Ti-273.15).plot(color="k", ax=ax[0])
    y_data.phi_h.plot(color="k", ax=ax[1])
    ax[0].set_ylabel(r"Temperature [$^\circ$C]")
    ax[1].set_ylabel(r"Power [W]")
    fig.tight_layout()
    plt.show()
    """
    #y_data = y_data.iloc[0:2]
    
    #y_data = y_data[["phi_h", "phi_s", "y1", "Ti", "Ta"]]
    
    y_data = pd.read_csv("1st_floor.csv", index_col=0)
    
    #cfg_path = "2R2C.json"
    cfg_path = "3R3C_novent.json"
    N = len(y_data)
    dt = y_data.index[1] - y_data.index[0]
    
    #y_data.to_csv("1st_floor.csv", index=True)
    
    param_guess = ca.DM([0.01,0.1,0.01,1E6,1E6,1E7,5])
    #param_guess = ca.DM([0.01,0.01,1E6,1E7,5])
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
    
    with ParameterEstimation(config=cfg_path,
                             N=N,
                             dt=dt,
                             param_guess=param_guess) as param_est:
        
        Q = ca.DM.eye(3)
        #Q[1,0] = 1
        #Q[0,1] = 1
        R = ca.DM.eye(1)
        # provide Q, R in solve here:
        # provide lb, ub for p here:
        sol, params = param_est.solve(
                                      y_data,
                                      param_guess,
                                      lbx=lbx,
                                      ubx=ubx,
                                      lbp=lbp,
                                      ubp=ubp,
                                      covar=ca.veccat(Q, R)
                                      )
    
        pprint(params)
        
        ax = (sol["Ti"]-273.15).plot(color="grey")
        ax = (y_data["Ti"]-273.15).plot(color="black", linestyle="dashed")
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
        u_data = y_data[["phi_h", "Ta", "phi_s"]]
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