from opt.mpc.mpc import ConfigJson
from opt.mpc.mpc import MPC
from model import TestCase5

from api.aiohttp_api import Server, Client
from api.boptest_api import Boptest
from api.database_api import Database
from http import HTTPStatus

from datetime import datetime
import pandas as pd
import numpy as np
import time, json

class Mosiop:

    def __init__(self):

        # instantiate testcase of bootsampling
        self.cfg = ConfigJson().associate(TestCase5)

        # initiate communication with microservices
        self.orchestrator = Client(self, 'http://bacssaas_orchestrator:6000')
        self.neuron = Client(self, 'http://bacssaas_neuron:6000')
        
        # instantiate controll
        self.mpc_int = MPC(self.cfg) 

        # instantiate boptest after MPC
        self.boptest = Boptest(self.cfg)   
        
        # instantiate database
        self.db = Database('./database.ini', 'postgresql','bacssaas')
       
  
    def handler(self, payload):

        print('\033[92mHandler routine of {} running for incomping request of {}\033[0m'.format(self.__class__.__name__,payload['meta']['source']))

        if payload['meta']['meta']['request'] == 'health':

            resp = self.neuron.request({'request':'health'})[1]
            if resp['meta']['health'] == HTTPStatus.OK.value:
                print('\033[92m[{}] BACSSaaS:Neuron Online\033[0m'.format(datetime.now().strftime("%y-%m-%d %H:%M:%S")))
            else:
                return {'health':HTTPStatus.BAD_GATEWAY}
            
            return {'health':HTTPStatus.OK}
        
        if payload['meta']['meta']['request'] == 'advance':
            pass

        else:
            return HTTPStatus.BAD_REQUEST

    def internal(self, y_meas, r):
        
        # solve MPC for control law
        df_ol, u_0, y_hat = self.mpc_int.solve_open_loop(y_meas, r)

        # evolve BOPTEST emulator
        r, y_meas = self.boptest.evolve(u_0)

        # shape control 
        resp = self.neuron.request({'request':'adapt','u_0':u_0.to_json()})[1] 
        u_nn = json.loads(resp['meta']['adapt'])['u_nn']

        # log to database 
        df = pd.DataFrame(columns=['time','phi_h','Ti_hat', 'Te_hat', 'Th_hat','Ti_meas','phi_h_nn'],data=[list(np.hstack([datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], np.hstack((u_0.values, y_hat.values, y_meas,u_nn))]))])
        
        # dump to database
        self.db.write('internal',self.boptest.name, df)

        return df
        
    def main(self):

        print('Main routine of {} running'.format(self.__class__.__name__))

        # initial warmstart to internal learning process
        y_meas = self.mpc_int.y0['y0']
        r = self.boptest.forcast()

        while True:
            self.internal(y_meas, r)
            time.sleep(1)
            print('{} Idle..'.format(self.__class__.__name__))

if __name__ == '__main__':
    Server(Mosiop()).main()