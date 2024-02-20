from casadi import *
from abc import ABC, abstractmethod, ABCMeta
import numpy as np

class Integrator(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'dae')) #and 
                #hasattr(subclass, 'get_one_sample') and 
                #callable(subclass.get_one_sample))

#    @abstractmethod
#    def get_one_sample(self): 
#        raise NotImplementedError
    
    @property
    def x(self):
         return vertcat(*self.dae.dae.x)

    @property
    def u(self):
         return vertcat(*self.dae.dae.u)

    @property
    def p(self):
         return vertcat(*self.dae.dae.p)

    @property
    def z(self):
         return vertcat(*self.dae.dae.z)
        

class Cvodes(Integrator):
    """
    Wrapper for Cvodes functionality in Casadi.

    TODO: how to do n-step? i.e. sub-sampling.
    For now, only n_step = 1.

    TODO: handling of DAE's
    """ 
    
    def __init__(self, dt, dae):

        self.dae = dae
        opts = {
            "step0":    dt,
            #"min_step_size": dt,
            #"max_step_size": dt,
            "t0"      : 0.0,
            "tf"      : 1,
            "abstol"  : 1E-4
                }

        self.set_ode_func()
        # u->z in integrator call (algebraic var, constant on between phase boundaries (check term. in Betts ch. 4))
        self.I = integrator("I", "idas", {"x": self.x, "p": vertcat(self.p, self.u), "ode": self.ode}, opts)
        #elf.I.set_option("abstol", 1E-4)
        #I(x0=0)
        #stats = I.stats()
        #self.one_step = self.get_one_step()
        #self.one_sample = self.get_one_sample()


    def one_sample(self, x0=None, p=None):
        """
        x0, p
        """
        return self.I(x0=x0, p=p)
    
    """
    @property
    def final_expr(self):
        pass

    def get_one_step(self): # return Function-object
        pass

    """
    def set_ode_func(self):
        """
        Deine as expr, not Function-obj.
        """
        self.ode = vertcat(*self.dae.dae.ode)


class Collocation(Integrator):
    
    def __init__(self, dt, dae, d, n=1, method="radau"):
        """
        Parameter listing.
        
        n: int - finite elements
        """
        
        self.dae = dae
        self.set_ode_expr()
        self.set_ode_func() 
        self.d = d
        self.n = n
        self.h = dt/n
        self.method = method   
        self.set_coll_coeffs()
        self.init_integrator()
        #self.one_sample = self.get_one_sample()
    
        
    def set_ode_expr(self):
        self.ode = vertcat(*self.dae.dae.ode)
        
    def set_ode_func(self):
        #self.x = vertcat(*self.dae.dae.x)
        #self.u = vertcat(*self.dae.dae.u)
        #self.p = vertcat(*self.dae.dae.p)
        self.f = Function('f', [self.x, vertcat(self.u, self.p)], [self.ode], ["x", "u"], ["f"])
        
    def set_coll_coeffs(self):
        """
        Get collocation coefficients
        by degree of interpolating polynomial.s
        """
        
        # degree
        d = self.d
        
        tau_root = [0] + collocation_points(d, self.method)

        # Coefficients of the collocation equation
        C = np.zeros((d+1,d+1))

        # Coefficients of the continuity equation
        D = np.zeros(d+1)

        # Dimensionless time inside one control interval
        tau = SX.sym('tau')

        # For all collocation points
        for j in range(d+1):
        # Construct Lagrange polynomials to get the polynomial basis at the collocation point
            L = 1
            for r in range(d+1):
                if r != j:
                    L *= (tau-tau_root[r])/(tau_root[j]-tau_root[r])

            # Evaluate the polynomial at the final time to get the coefficients of the continuity equation
            lfcn = Function('lfcn', [tau], [L])
            D[j] = lfcn(1.0)

            # Evaluate the time derivative of the polynomial at all collocation points to get the coefficients of the continuity equation
            tfcn = Function('tfcn', [tau], [tangent(L,tau)])
            for r in range(d+1): C[j,r] = tfcn(tau_root[r])
            
        self.C = C
        self.D = D
        # and B for quadrature?

    def init_integrator(self):
        
        # improve handling:
        d, C, D, h, n, f = self.d, self.C, self.D, self.h, self.n, self.f
        
        nx = len(self.dae.dae.x)
        nu = (len(self.dae.dae.u) + len(self.dae.dae.p))
        
        # keep:
        #self.X0 = X0 = MX.sym('X0',nx)
        X0 = MX.sym('X0',nx)
        # u, p:
        #self.P = P = MX.sym('P',nu)
        P = MX.sym('P',nu)
        V = MX.sym('V', d*nx)

        # Get the state at each collocation point
        X = [X0] + vertsplit(V, [r*nx for r in range(d+1)])

        # Get the collocation quations (that define V)
        V_eq = []
        for j in range(1,d+1):
            # Expression for the state derivative at the collocation point
            xp_j = 0
            for r in range (d+1):
                xp_j += C[r,j]*X[r]

            # Append collocation equations
            f_j = f(X[j], P)
            V_eq.append(h*f_j - xp_j)

        # Concatenate constraints
        V_eq = vertcat(*V_eq)

        # Root-finding function, implicitly defines V as a function of X0 and P
        vfcn = Function('vfcn', [V, X0, P], [V_eq])

        # Convert to SX to decrease overhead
        vfcn_sx = vfcn.expand()

        # Create a implicit function instance to solve the system of equations
        ifcn = rootfinder('ifcn', 'fast_newton', vfcn_sx)
        V = ifcn(MX(), X0, P)
        X = [X0 if r==0 else V[(r-1)*nx:r*nx] for r in range(d+1)]

        # Get an expression for the state at the end of the finie element
        XF = 0
        for r in range(d+1):
            XF += D[r]*X[r]

        # Get the discrete time dynamics
        F = Function('F', [X0, P], [XF])

        # Do this iteratively for all finite elements
        X = X0
        for i in range(n):
            X = F(X, P)       
        # keep X:
        #self.X = X
        
        #self.one_sample = Function('irk_integrator', {'x0': X0, \
        #                                              'p': P, \
        #                                              'xf': X \
        #                                              },
        #                                            integrator_in(), \
        #                                            integrator_out())
        
        self.one_sample = Function('irk_integrator', [X0, P], [X], ["x0", "p"], ["xf"])
        
    def simulate(self, x0, U, params):
        """ 
        Simulate with given:
            - x0
            - U
            - params

        TODO: what about z/noise states?
        """
        if U.shape[1] == 1:
            N = U.shape[0]
        else:
            N = U.shape[1]

        #all_samples = self.get_one_sample().mapaccum("all_samples", N)
        all_samples = self.one_sample.mapaccum("all_samples", N)
        u_coll = vertcat(U.T, repmat(params, 1, N))

        # TODO: fix case of more inputs
        #return all_samples(x0, u_coll, 0, 0, 0, 0)[0]
        return all_samples(x0, u_coll)
        


class RungeKutta4(Integrator):
    ''' 
    Simple RK4 implementation. 

    TODO: Fix for simple algebraic (i.e. noise)
    states. Do as if n_step == 1, i.e. no
    need to enforce equality of w_n[t, i] = w_n[t, i+1]
    (on sub-intervals).
    
    TODO: can we generalize this to n-step RK-methods?
    '''
    def __init__(self, dt, n_steps, dae):
        self.dae = dae
        self.dt = dt/n_steps # corrected

        assert n_steps >= 1

        self.n_steps = n_steps
        self.set_ode_func()
        self.one_step = self.get_one_step()
        self.one_sample = self.get_one_sample()

    def set_ode_func(self):
        self.ode = Function('ode',[self.x,self.u,self.p],[vertcat(*self.dae.dae.ode)])
        
    @property
    def k1(self):
        return self.ode(self.x, self.u, self.p)

    @property
    def k2(self):
        return self.ode(self.x + self.dt/2.0*self.k1, self.u, self.p)

    @property
    def k3(self):
        return self.ode(self.x + self.dt/2.0*self.k2, self.u, self.p)
    #X = self.x
    @property
    def k4(self):
        return self.ode(self.x + self.dt*self.k3, self.u, self.p)
    
    @property
    def states_final(self):
        return self.x + self.dt/6.0*(self.k1 + 2*self.k2 + 2*self.k3 + self.k4)
    

    @property
    def final_expr(self):
        X = self.x
        for i in range(self.n_steps):
            X = self.one_step(X, self.u, self.p)
        return X

    def get_one_sample(self):
        return Function('one_sample',[self.x, self.u, self.p], [self.final_expr], ["x", "u", "p"], ["X"])  
    

    def get_one_step(self): # return Function-object
        return Function('one_step',[self.x, self.u, self.p], [self.states_final], ["x", "u", "p"], ["x"]) 

    def simulate(self, x0, U, params):
        """ 
        Simulate with given:
            - x0
            - U
            - params

        TODO: what about z/noise states?
        """

        if U.shape[1] == 1:
            N = U.shape[0]
        else:
            N = U.shape[1]

        all_samples = self.get_one_sample().mapaccum("all_samples", N)

        return all_samples(x0, U, repmat(params,1,N)) # -> empty z 
        