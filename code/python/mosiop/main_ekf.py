from filters import EKF
from opt.mpc.mpc import ConfigJson
from opt.mpc.mpc import MPC
from api.boptest_api import Boptest
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdb

import casadi as ca

from model import TestCase1, TestCase2, TestCase3, TestCase4, TestCase5, TestCase6

if __name__ == '__main__':

    # read mpc problem config file
    #cfg = ConfigJson().associate(TestCase4)
    #cfg = ConfigJson().associate(TestCase2)
    cfg = ConfigJson().associate(TestCase6)

    # initialize mpc
    mpc = MPC(cfg)

    # initialize BOPTEST
    boptest = Boptest(cfg)

    # frame for closed-loop results
    #df_cl = pd.DataFrame(columns=mpc.df_labels['df'])

    # mpc settings:
    T = cfg['mosiop']['MPC']['temporal']['T']
    h = cfg['mosiop']['MPC']['temporal']['h']
    N = cfg['mosiop']['MPC']['temporal']['N']

    # use those for boptest:
    boptest.set_step(h)
    boptest.set_forecast_params({"horizon": h*N, "interval": h})

    y_hat = cfg['mosiop']['PLANT']["initial"]["y0"]
    r_mpc = None

    #R = ca.DM.eye(3)
    R = ca.DM.eye(1)
    R[0,0] = 1
    #R[1,1] = 0.001
    #R[2,2] = 0.001
    #R[1,1] = 100


    Q = ca.DM.eye(2)
    Q[0,0] = 1
    Q[1,1] = 1
    #Q[2,2] = 1


    # consider how to pass these settings to the filter
    # should have a config similar to mpc, boptest
    # "Te": "TRooEnv_y", "Th": "TRooHea_y"}
    ekf = EKF(mpc.ocp, R=R, \
              grid=mpc.grid, \
              h=h, \
              params=cfg["mosiop"]["PLANT"]["parameters"])
    ################################ EKF #####################################

    r_mpc = boptest.forcast()

    for k in range(int(T/h)):

        # solve mpc for control law
        df_ol, u_0, _ = mpc.solve_open_loop(y_hat, r_mpc, k)
        # evolve BOPTEST emulator
        r_mpc, y_0 = boptest.evolve(u_0)
        # estimate state with ekf
        y_hat = ekf.step(df_ol, y_0, k)



    fig, axs = boptest.plot_results(T)
    plt.show()
    
    names = {**boptest.maps["y"], **{"Te": "TRooEnv_y", "Th": "TRooHea_y"}}

    fig, axs = ekf.plot_results(boptest.get_results(T), names)
    plt.show()
