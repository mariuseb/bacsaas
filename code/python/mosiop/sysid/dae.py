from casadi import *

class DAE(object):
    """
    class to be used as input for parameter estimation
    """
    def __init__(self, config):

        self.dae = DaeBuilder()
        self.config = config
        self.add_params()
        self.add_states()
        #self.add_alg_states()
        self.add_controls()
        #self.add_meas()
        self.add_odes()
        #self.add_algs()
        # self.add_meas_eqs()


    def add_params(self):
        """ Add param names..."""
        for name in self.config["p"]:
            param = self.dae.add_p(name)
            self.__setattr__(name, param)

        self.__setattr__("p", self.config["p"])

    def add_controls(self):
        self.u_names = []
        for name in self.config["u"]:
            control = self.dae.add_u(name)
            self.__setattr__(name, control)
            self.u_names.append(name)

    def add_states(self):
        for name in self.config["x"]:
            state = self.dae.add_x(name)
            self.__setattr__(name, state)

        self.__setattr__("x", self.config["x"])

    def add_alg_states(self):
        """
        Add algebraic states.
        """
        try:
            for name in self.config["z"]:
                alg_state = self.dae.add_z(name)
                #noise = MX.sym(name)
                self.__setattr__(name, alg_state)

            self.__setattr__("z", self.config["z"])
        except KeyError:
            # to logger / warning 
            pass

    def add_meas(self):
        """ 
        Add measurement. 
        """

        meas_exprs = {}

        repl_table = {k: "self." + k for k in self.__dict__.keys() if k not in ["dae", "config"]}
        pattern = re.compile(r'\b(' + '|'.join(repl_table.keys()) + r')\b')

        for name, eq_string in self.config["y"]:
            # expects name, definition:

            eq_string = pattern.sub(lambda x: repl_table[x.group()], eq_string)
            
            #exec(f'self.algs["{alg_name}"] =' + alg_string)

            exec("meas_exprs[name] = " + eq_string)

            meas_eq = self.dae.add_y(name, meas_exprs[name])
            #noise = MX.sym(name)
            self.__setattr__(name, meas_eq)

        # keep for later lookup:
        self.__setattr__("y", meas_exprs)
    
    @property
    def n_x(self):
        return len(self.dae.x)

    @property
    def n_z(self):
        return len(self.dae.z)

    @property
    def n_p(self):
        return len(self.dae.p)

    @property
    def n_u(self):
        return len(self.dae.u)

    @property
    def n_h(self):
        return len(self.dae.alg)

    @property
    def g(self):
        """
        trivial equations must be filtered out.
        """
        #eqs = []
        #for eq in self.dae.alg:
        #    if is_symbolic(eq):
        #        eqs.appe

        return [eq for eq in self.dae.alg if not eq.is_zero()]
                



    """
    @property
    def p(self):
        return vertcat(*self.dae.p)

    @property
    def x(self):
        return vertcat(*self.dae.p)

    @property
    def u(self):
        return vertcat(*self.dae.u)
    """

    """
    Can generalize the below to add equation.
    """

    def add_odes(self):
        # get params, states, to local scope
        
        repl_table = {k: "self." + k for k in self.__dict__.keys() if k not in ["dae", "config"]}
        self.odes = {}

        for ode_name, ode_string in self.config["ode"].items():

            pattern = re.compile(r'\b(' + '|'.join(repl_table.keys()) + r')\b')
            ode_string = pattern.sub(lambda x: repl_table[x.group()], ode_string)

            #exec('ode =' + ode_string, globals())
            exec(f'self.odes["{ode_name}"] =' + ode_string)
            self.dae.add_ode(ode_name, self.odes[ode_name])
            #self.dae.add_aux(ode_name, self.odes[ode_name])

    def add_daes(self):
        # get params, states, to local scope
        
        repl_table = {k: "self." + k for k in self.__dict__.keys() if k not in ["dae", "config"]}
        self.daes = {}

        for dae_name, dae_string in self.config["dae"].items():

            pattern = re.compile(r'\b(' + '|'.join(repl_table.keys()) + r')\b')
            dae_string = pattern.sub(lambda x: repl_table[x.group()], dae_string)

            #exec('ode =' + ode_string, globals())
            exec(f'self.daes["{dae_name}"] =' + dae_string)
            self.dae.add_dae(dae_name, self.daes[dae_name])
            #self.dae.add_aux(ode_name, self.odes[ode_name])

    def add_algs(self):
        
        repl_table = {k: "self." + k for k in self.__dict__.keys() if k not in ["dae", "config"]}
        self.algs = {}

        for alg_name, alg_string in self.config["alg"].items():

            pattern = re.compile(r'\b(' + '|'.join(repl_table.keys()) + r')\b')
            alg_string = pattern.sub(lambda x: repl_table[x.group()], alg_string)
            
            exec(f'self.algs["{alg_name}"] =' + alg_string)
            self.dae.add_alg(alg_name, self.algs[alg_name])