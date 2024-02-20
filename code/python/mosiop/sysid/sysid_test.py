from casadi import *
import json
from dae import DAE
from integrators import RungeKutta4, Collocation
import pandas as pd
import os
import numpy
import subprocess
import time

"""
Test simple parameter identification problem
with collocation-based multiple shooting.

Handling of quadrature:
  - take X at shooting gaps
"""

########################## SIMULATE ####################

# collocation settings:
order = 2
method = "legendre"

with open("sysid/param_est_config_ms.json", "r") as file:
    config = json.load(file)
    
model = config["model"]
dt = config["dt"]
N = config["N"]
n_steps = config["n_steps"]

# generate some data:
numpy.random.seed(0)
u_data = DM(0.1*numpy.random.random(N))

# create a dae
dae = DAE(model)    
# integrator:
Coll = Collocation(dt, dae, order, n=3, method=method)

# true parameters:
x0 = DM([0,0])
param_truth = DM([5.625e-6,2.3e-4,1,4.69])
X = Coll.simulate(x0, u_data, param_truth)

# measurement data
y_data = X[0,:].T
###################################################

df = pd.DataFrame()
#dt = np.arange(0, config["dt"]*len(df), config["dt"])
df["u1"] = np.array(u_data).flatten()
df["y1"] = np.array(y_data).flatten()
df.index = np.arange(0, config["dt"]*N, config["dt"])


# You may add some noise here
#y_data+= 0.001*numpy.random.random(N)
# When noise is absent, the fit will be perfect.

# Use just-in-time compilation to speed up the evaluation
if Importer.has_plugin('clang'):
  with_jit = True
  compiler = 'clang'
elif Importer.has_plugin('shell'):
  with_jit = True
  compiler = 'shell'
else:
  print("WARNING; running without jit. This may result in very slow evaluation times")
  with_jit = False
  compiler = ''

############ Create a Gauss-Newton solver ##########
def gauss_newton(e,nlp,V):
  # objective only indirectly affected by collocation points...
  J = jacobian(e,V)
  H = triu(mtimes(J.T, J))
  sigma = MX.sym("sigma")
  opt = {
    "verbose": 0,
    "ipopt.linear_solver": "ma27",
    "ipopt.max_iter": 1000,
    "ipopt.print_level": 5,
    "ipopt.ma57_pre_alloc": 10,
    #"ipopt.hessian_approximation": "limited-memory",
    "ipopt.ma57_automatic_scaling" : "yes"}
  
  hessLag = Function('nlp_hess_l',{'x':V,'lam_f':sigma, 'hess_gamma_x_x':sigma*H},
                     ['x','p','lam_f','lam_g'], ['hess_gamma_x_x'],
                     dict(jit=with_jit, compiler=compiler))
  
  return nlpsol("solver", \
                "ipopt", \
                nlp, \
                dict(hess_lag=hessLag, \
                jit=with_jit, \
                compiler=compiler, \
                **opt),
                )
########################################################

# multiple-shooting: 

with_jit = True
fs = 1/dt

# All states become decision variables
X = MX.sym("X", 2, N)

# create an algebraic variable corresponding to the measurement:
scale = vertcat(1e-6,1e-4,1,1)
param_guess = DM([5,2,1,5])
params = vertcat(*dae.dae.p)

p_coll_symbolic = vertcat(u_data.T, scale*repmat(params, 1, N))
coll_one_step = Coll.one_sample.map(N, "openmp")
Xn = coll_one_step(x0=X, p=p_coll_symbolic)["xf"]
#Xn = coll_mapped["xf"]
#Xn = coll_mapped["xf"]
#e_coll = coll_mapped["qf"].T

#Xn.generate_dependencies("icfn.c")

# try to generate code for the N-step integrator:
#C = CodeGenerator("gen.c")
#C.add(coll_one_step)
#C.generate()


# gaps at sfinite elements:
#gaps = Xn[:,:-1]-X[:,1:]
#gaps = Xn[:,(order-1):-1:order]-X[:,1:]

#e = y_data - Xn[0,(order-1)::order].T

V = veccat(params, X)
gaps = Xn[:,:-1]-X[:,1:]
e = y_data - Xn[0,:].T;

g = vec(gaps)
nlp = {'x': V, 'f': 0.5*dot(e,e), 'g': g}

# Multipleshooting allows for careful initialization
yd = np.diff(y_data,axis=0)*fs
X_guess = horzcat(y_data , vertcat(yd, yd[-1])).T
X_coll_guess = horzcat(y_data , vertcat(yd, yd[-1])).T

#x0 = veccat(param_guess,X_guess,X_coll_guess)
x0 = veccat(param_guess,X_guess)

solver = gauss_newton(e, nlp, V)
#gen_opts = {}
#solver.generate_dependencies("nlp.c", gen_opts)
#start = time.time()
#subprocess.Popen("gcc -fPIC -shared -O1 nlp.c -o nlp.so", shell=True).wait()
#print("Compile time was: {}".format(time.time()-start))

#solver = nlpsol("solver","ipopt", nlp)

sol = solver(x0=x0,lbg=0,ubg=0)

print(sol["x"][:4]*scale)

assert(norm_inf(sol["x"][:4]*scale-param_truth)<1e-8)
