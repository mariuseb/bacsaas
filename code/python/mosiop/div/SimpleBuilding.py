from pylab import *
from casadi import *
from rockit import * # From https://gitlab.kuleuven.be/meco-software/rockit
from XML_edit import patch_xml, inspect_xml
import pandas as pd

try: # CasADi develop
  model = DaeBuilder("foo")
except: # CasADi 3.5.5
  model = DaeBuilder()

patch_xml('parameter_estimation/SimpleBuildings.SimpleBuilding4.xml','simplebuilding4_processed.xml')

print("Check states and equations")

inspect_xml('simplebuilding4_processed.xml')
model.parse_fmi('simplebuilding4_processed.xml')

model.disp(True)

sdot = model.sdot

model.make_explicit()
model.sort_d()
model.split_d()

print(model.x)
print(model.d)
print(model.ddef)
print(model.u)

# TODO: get time horizon from model
days = 10
step = 6
T = 84600*days
ocp = Ocp(t0=0,T=T)

# Register model states and controls as rockit states and variables
ocp.register_state(model.x)
# ocp.register_control(model.u)

data = {k.lower():v for k,v in pd.read_csv("parameter_estimation\data.csv", header=0, dtype=str, squeeze=True).to_dict(orient='list').items()}
for key, values in data.items():
  try:
      [float(i) for i in values]
  except:
      continue
  else:
      data[key]=[float(i) for i in values]


start = 0
end = start + 288*days

for u in model.u:
  ocp.register_parameter(u,grid='control')
  name = u.name().lower()
  ocp.set_value(u, data[name][start:end:step])

# Let rockit know about system equations
for x, rhs in zip(model.x, model.ode):
  ocp.set_der(x, rhs)

# Set optimization parameters
#Parameters SimpleBuilding2
# mapping = {
# 'resWalInt.r': 1e-3,
# 'resWalExt.r': 1e-3,
# 'capZon.c': 666144,
# 'gaiHP.k': 1,
# 'capWal.c': 1e9,
# 'win[1].gA': 20,
# 'gaiIG.k': 1,
# 'capZon.TSta': 293.15,
# 'capWal.TSta': 293.15,
##Optimal collocation parameters as initial values for MS
# 'resWalInt.r': 0.0006147057183308194,
# 'resWalExt.r': 0.0151327626565652,
# 'capZon.c': 10887483.182149153,
# 'gaiHP.k': 0.5000012376282079,
# 'capWal.c': 9999999409.251953,
# 'win[1].gA': 3.0000001811146144,
# 'gaiIG.k': 6.362503916521005,
# 'capZon.TSta': 294.320551801767,
# 'capWal.TSta': 293.5230030464414,
# }
# Parameters SimpleBuilding4
mapping = {
'resWalInt.r': 1e-3,
'resWalExt.r': 1e-3,
'capZon.c': 666144,
'gaiHP.k': 1,
'capWal.c': 1e9,
'win[1].gA': 20,
'gaiIG.k': 1,
'capZon.TSta': 293.15,
'capWal.TSta': 293.15,
'capInt.TSta': 293.15,
'capEmb.TSta': 293.15,
'resInt.r': 1e-3,
'capInt.c': 1e9,
'capEmb.c': 1e9,
'resEmb.r': 1e-3,
}
# Parameters SimpleBuilding1
# mapping = {
# 'resWal.r': 1e-3,
# 'capZon.c': 666144,
# 'gai.k': 1,
# 'capZon.TSta': 293.15
# }

for par in mapping.keys():
    ocp.register_variable(model(par))
    ocp.set_initial(model(par), mapping[par])
    # ocp.subject_to( 0 <= model(par))
# ocp.subject_to(1e-6 <= (model('resWal.r') <= 1e0))
ocp.subject_to(1e-6 <= (model('resWalInt.r') <= 1e0))
ocp.subject_to(1e-6 <= (model('resWalExt.r') <= 1e0))
ocp.subject_to(1e4 <= (model('capZon.c') <= 1e8))
ocp.subject_to(0.5 <= (model('gaiHP.k') <= 10))
ocp.subject_to(1e6 <= (model('capWal.c') <= 1e10))
ocp.subject_to(3 <= (model('win[1].gA') <= 30))
ocp.subject_to(0.5 <= (model('gaiIG.k') <= 10))
# ocp.subject_to(1e-9 <= (model("resInt.r") <= 1e1))
# ocp.subject_to(1e4 <= (model("capInt.c") <= 1e10))
# ocp.subject_to(1e2 <= (model("capEmb.c") <= 1e10))
# ocp.subject_to(1e-9 <= (model("resEmb.r") <= 1e1))
# ocp.subject_to(1e-9 <= (model("resFlo.r") <= 1e1))
# ocp.subject_to(1e2 <= (model("capFlo.c") <= 1e10))
# ocp.subject_to(1e-9 <= (model("resInf.r") <= 1e1))
# ocp.subject_to(0.5 <= (model('gai.k') <= 10))
ocp.subject_to(280 <= (model('capZon.TSta') <= 300))
ocp.subject_to(280 <= (model('capWal.TSta') <= 300))
# ocp.subject_to(280 <= (model('capInt.TSta') <= 300))
# ocp.subject_to(280 <= (model('capEmb.TSta') <= 300))
# ocp.subject_to(280 <= (model('capFlo.TSta') <= 300))

# Create parameters (not-to-be-optimized)
params = []
param_vals = []
for par, value in zip(model.d, model.ddef):
  if par.name() not in mapping.keys():
    if value.is_constant():
        params.append(par)
        param_vals.append(evalf(value))
        ocp.set_value(ocp.register_parameter(par),evalf(value))
        print("constant param", par, value)
    elif depends_on(value,vcat(model.x)):
        print("Ignored", par)
    else:
        if ocp.is_signal(value):
            ocp.register_variable(par,grid='control')
            print("signal", par, value)
        else:
            ocp.register_variable(par)
            print("New param", par, value)
            ocp.subject_to(par==value,include_last=False)

orphaned_parameters = list(set(symvar(vcat(model.ode)))-set(symvar(vcat(model.d+model.x+model.u))))

for p in orphaned_parameters:
  print('"%s": ?' % p.name())

for p in orphaned_parameters:
  if p.name() not in mapping:
    raise Exception("Orphaned parameter '%s' undefined." % p.name())

# for name,value in mapping.items():
#     ocp.set_value(ocp.register_parameter(model(name)),evalf(value))

# ==========================
# Boundary conditions at t0
# ==========================

handled = []
for e in model.init:
    if not depends_on(e, vcat(sdot)):

        # Avoid duplicate constraints (violates LICQ condition of solver)
        already_added = False
        depth = 1
        for h in handled:
            if is_equal(e, h, depth):
                already_added = True
                break
        if already_added: continue

        # elif 'capZon.heaPor.T' in str(e):
        #     ocp.subject_to(ocp.at_t0(model('capZon.heaPor.T') == data['tzon'][start:end:step][0]))
        #
        # else:
        ocp.subject_to(ocp.at_t0(e) == 0)
        handled.append(e)
    pass

print(model.init)
print(model.ode)
print(model.ddef)

# Add objective function
meas = data['tzon'][start:end:step]
meas_param = ocp.parameter(grid='control')
ocp.set_value(meas_param, meas)
ocp.add_objective(ocp.integral((model('capZon.heaPor.T')-meas_param)**2))

N=288*days//step
# method = DirectCollocation(N=N, M=3)
method = MultipleShooting(N=N, intg='rk')
# ocp.method(SingleShooting(N=N))
ocp.method(method)
# options = {"ipopt": {"nlp_scaling_method":"none","mumps_permuting_scaling":0,"mumps_scaling":0}}
ocp.solver('ipopt')

# =========================
# Solving
# =========================

sol = ocp.solve()

# =========================
# Post processing
# =========================

results = {}

# for x in model.x:
#     if x.name() == 'capZon.heaPor.T':
#         [ts, xs] = sol.sample(x, grid='integrator', refine=100)
#         plot(ts, xs, '-', label=x.name())
#         results[str(x)] = sol.sample(x, grid='control')[1]
#
# for u in model.u:
#     [ts, us] = sol.sample(u, grid='integrator', refine=100)
#     plot(ts, us, '--', label=u.name())
#     results[str(u)] = sol.sample(u, grid='control')[1][:-1]

print("Optimal values:")
for par in mapping.keys():
    value = sol.value(model(par))
    print("'{par}': {val},".format(par=par, val=value))

for x in model.x:
    if x.name() == 'capZon.heaPor.T':
        [ts, xs] = sol.sample(x, grid='integrator', refine=100)
        plot(ts, xs, '-', label=x.name())
        results[str(x)] = sol.sample(x, grid='control')[1]

import pickle
pickle.dump(results,open("results.dat","wb"))
meas = data['tzon'][start:end+1:step]
plot(ts[::100],meas, '-', label='T_meas')
axvline(x=86400*10,linestyle='--')
xticks(np.arange(0,86400*(days+1),3600*24),range(days+1))
xlabel('Time [days]')
ylabel('Temperature [K]')
legend()

print("Optimal values:")
for par in mapping.keys():
    value = sol.value(model(par))
    print("'{par}': {val},".format(par=par, val=value))


show()

