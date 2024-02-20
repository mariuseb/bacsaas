import random
from opt.mpc.mpc import ConfigJson
from opt.mpc.mpc import MPC
from api.boptest_api import Boptest
from sysid.param_est import ParameterEstimation
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sysid.prbs import randomizer_prbs_4, randomizer_prbs_6
import random

from model import TestCase5, TestCase1, TestCase6

if __name__ == '__main__':

    cfg = ConfigJson().associate(TestCase6)
    
    # MPC settings:
    T = cfg['mosiop']['MPC']['temporal']['T']
    h = cfg['mosiop']['MPC']['temporal']['h']
    N = cfg['mosiop']['MPC']['temporal']['N']

    # run for two days, then do identification
    #stop = (24*3600*31*3)/h
    #stop = 2

    mpc = MPC(cfg)
    boptest = Boptest(cfg)

    boptest.set_forecast_params({"horizon": N, "interval": h})

    #y_meas = mpc.y0['y0']
    #r = boptest.forcast()

    #stop = 1400

    np.random.seed(42)

    perturb = -5

    for k in range(int(T/h)):
        
        if k == 0:
            # set up PRBS:
            """
            prbs6 = randomizer_prbs_6()
            # say T=15 mins for simplicity
            
            prbs6_ser = pd.Series(index=range(len(prbs6)), data=prbs6)

            prbs4 = randomizer_prbs_4()
            # T=20H -> repeat 20/0.25 = 80x
            prbs4_ser = pd.Series(index=range(len(prbs4)), data=prbs4)
            
            prbs = pd.concat([prbs6_ser, prbs4_ser.repeat(80)])
            prbs.index = range(len(prbs.index))
            """
            
            #
            data = pd.read_csv("inputPRBS1.csv", sep=";")
            prbs = data.Ph/5
            stop = len(prbs)

            u_0 = pd.Series(index=['phi_h'], data=prbs.loc[k]*5000)

        elif k < stop:
        # solve MPC for control law
            #df_ol, u_0, y_hat = mpc.solve_open_loop(y_meas, r, k)
            #u_0 = {}

            #u_0 = pd.Series(index=["phi_h"], data=np.array([round(np.random.random(1)[0])])*5000)
            #u_0 = pd.Series(index=["phi_h"], data=np.random.random(1)*5000)
            u_0 = pd.Series(index=['phi_h'], data=prbs.loc[k]*5000)
            #u_0 = {}

            #u_0 = {"phi_h": np.random.random(1)*10000}fig.savefig('temp.png', dpi=fig.dpi)
        """
        # alternate every 200 timesteps between 300 degrees and 290 degrees
        if k % 200 == 0:
            #perturb *= -1
            action = random.uniform(0, 1)*3000
            #u_0 = pd.Series(index=['phi_h'], data = [295.15 + perturb])
            u_0 = pd.Series(index=['phi_h'], data = [action])
        """

        if k == stop:
            # do param est
            data = boptest.get_data(k*h, downsample=False)
            data.to_csv("data_ZEBLL_PRBS2.csv")
            param_est = ParameterEstimation("3R3C.json", codegen=True)

            # parameter guess:
            #param_guess = [1e-2, 1e6]
            param_guess = [6e-4, 5.7e-3, 1e-3, 0.1, 166860.0, 4e5, 1.224e6, 10, 10]
            scale = [1e-4, 1e-3, 1e-3, 1e-1, 1e5, 1e5, 1e6, 1e1, 1e1]
            #scale = [1]*len(param_guess)
            #scale = [1e-2, 1e6]

            params, states = param_est.estimate(data, param_guess=param_guess, scale=scale)

            fig, ax = plt.subplots(3,1)
            data[["Ti"]].plot(ax=ax[0])
            data[["phi_h"]].plot(ax=ax[1], drawstyle="steps")
            data[["Ta"]].plot(ax=ax[2], drawstyle="default")
            plt.show()

            fig, ax = plt.subplots(1,1)
            data[["Ti"]].plot(ax=ax, drawstyle="default")
            states[["Ti"]].plot(ax=ax, drawstyle="default")
            ax.legend(["Measured", "Estimated"])
            plt.show()


        elif k == stop + 1:

            cfg = ConfigJson().associate(TestCase5)

            #params = list(params.values())
            params = param_guess

            params.extend([294.15, 1, 0])

            cfg["mosiop"]["PLANT"]["parameters"] = params

            # initialize MPC
            mpc = MPC(cfg)
            
            df_ol, u_0, y_hat = mpc.solve_open_loop(y_meas, r, k)

            # frame for closed-loop results
            df_cl = pd.DataFrame(columns=mpc.df_labels['df'])

            # use mpc
            df_cl = df_cl.append(df_ol.loc[1:1, mpc.df_labels['df']], ignore_index=True)
            df_cl['time'].iloc[-1] = k*h
            """
            df_ol, u_0, y_hat = mpc.solve_open_loop(y_meas, r, k)
            df_cl = df_cl.append(df_ol.loc[1:1, mpc.df_labels['df']], ignore_index=True)
            df_cl['time'].iloc[-1] = k*h
            """
            #u_0 = pd.Series(index=['phi_h'], data = [295.15 + perturb])

            #action = random.uniform(0, 1)*3000
            #u_0 = pd.Series(index=['phi_h'], data = [295.15 + perturb])
            #u_0 = pd.Series(index=['phi_h'], data = [action])

        # evolve BOPTEST emulator
        r, y_meas = boptest.evolve(u_0)
        #r, y_meas = boptest.evolve()

            # dump-closed loop results

    t = df_cl['time']
    data = df_cl.loc[:,df_cl.columns != 'time']
    fig, axs = plt.subplots(data.columns.size)

    for i in range(data.columns.size):
        axs[i].step(t, data[data.columns[i]], 'b', label=data.columns[i])
        axs[i].legend(loc='upper right', prop={'size': 10}, ncol=1)
    plt.show()
    fig.savefig('correct_model.png', dpi=fig.dpi)

