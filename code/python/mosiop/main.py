from opt.mpc.mpc import ConfigJson
from opt.mpc.mpc import MPC
from api.boptest_api import Boptest
import casadi as ca
import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np
import pprint

from model import TestCase6, TestCase7, TestCase5, TestCase1

if __name__ == '__main__':

    cfg = ConfigJson().associate(TestCase6)
    
    # MPC settings:
    T = cfg['mosiop']['MPC']['temporal']['T']
    h = cfg['mosiop']['MPC']['temporal']['h']
    N = cfg['mosiop']['MPC']['temporal']['N']

    # initialize MPC
    mpc = MPC(cfg)

    # frame for closed-loop results
    df_cl = pd.DataFrame(columns=mpc.df_labels['df'])

    # initialize BOPTEST
    boptest = Boptest(cfg)

    y_meas = mpc.y0['y0']
    r = boptest.forcast()

    #dae = ca.DaeBuilder()
    #dae.parse_fmi("test.xml")

    #"parameters" : [1.124e-3, 1.515e-2, 4.029e5, 2.022e7, 1.022e-1, 295.15, 0, 1, 0],

    #Read models and replace.

    with open('3R3C_models.json', 'r') as f:
        results = json.load(f)

    params_old = mpc.get_parameter()
    attempt = 0
    params_new = list(results[str(attempt)]["params"].values())
    params_new.extend(params_old[-4:])
    #mpc.set_parameter(ca.DM(params_new))
    mpc.set_parameter(np.array(params_new))

    for k in range(int(T/h)):

        # solve MPC for control law
        df_ol, u_0, y_hat = mpc.solve_open_loop(y_meas, r, k)

        # evolve BOPTEST emulator
        r, y_meas = boptest.evolve(u_0)
        #r, y_meas = boptest.evolve()

        # dump-closed loop results
        df_cl = df_cl.append(df_ol.loc[1:1, mpc.df_labels['df']], ignore_index=True)
        df_cl['time'].iloc[-1] = k*h

    t = df_cl['time']
    data = df_cl.loc[:,df_cl.columns != 'time']
    fig, axs = plt.subplots(data.columns.size)

    for i in range(data.columns.size):
        axs[i].step(t, data[data.columns[i]], 'b', label=data.columns[i])
        axs[i].legend(loc='upper right', prop={'size': 10}, ncol=1)
    plt.show()


    data = boptest.get_results(T)
    #data.to_csv("mpc_test.csv")
    fig, axs = boptest.plot_results(T)
    plt.show()

    #fig, axs = boptest.plot_results(T)


