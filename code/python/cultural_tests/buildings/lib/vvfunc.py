def d_water (t):
    a = 1.51728258718231E-05
    b = -5.79814298131964E-03
    c = 0.012190155722692
    d = 1000.26519274006
    rho =a*t**3+b*t**2+c*t+d #kg/m3
    return rho;

def h_water (t):
    a = 4.18575022797163
    b = 0.568872214709824
    enthalpy = (a*t+b)*1000 #J/kg
    return enthalpy;
