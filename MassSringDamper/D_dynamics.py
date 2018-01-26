import numpy as np
import random
from D_param import D_param as P


class D_dynamics:
    '''
        Model the physical system
    '''

    def __init__(self):
        # Initial state conditions
        self.state = np.matrix([[P.z0],          # z initial position
                                [P.zdot0]]),       # zdot initial velocity
        #################################################
        # The parameters for any physical system are never known exactly.  Feedback
        # systems need to be designed to be robust to this uncertainty.  In the simulation
        # we model uncertainty by changing the physical parameters by a uniform random variable
        # that represents alpha*100 % of the parameter, i.e., alpha = 0.2, means that the parameter
        # may change by up to 20%.  A different parameter value is chosen every time the simulation
        # is run.
        alpha = 0.0  # Uncertainty parameter
        self.m = P.m * (1+2*alpha*np.random.rand()-alpha)  # Mass, kg
        self.k = P.k * (1+2*alpha*np.random.rand()-alpha)  # Spring constant, N/m
        self.b = P.b * (1+2*alpha*np.random.rand()-alpha)  # Damping coefficient, Ns/m

    def propagateDynamics(self, u):
        '''
            Integrate the differential equations defining dynamics
            P.Ts is the time step between function calls.
            u contains the system input(s).
        '''
        # Integrate ODE using Runge-Kutta RK4 algorithm
        k1 = self.derivatives(self.state, u)
        k2 = self.derivatives(self.state + P.Ts/2*k1, u)
        k3 = self.derivatives(self.state + P.Ts/2*k2, u)
        k4 = self.derivatives(self.state + P.Ts*k3, u)
        self.state += P.Ts/6 * (k1 + 2*k2 + 2*k3 + k4)

    def derivatives(self, state, u):
        '''
            Return xdot = f(x,u), the derivatives of the continuous states, as a matrix
        '''
        # re-label states and inputs for readability
        z = state.item(0)
        zdot = state.item(1)
        F = u[0]
        # The equations of motion.
        M = np.matrix([[self.m1+self.m2, self.m1*(self.ell/2.0)*np.cos(theta)],
                       [self.m1*(self.ell/2.0)*np.cos(theta), self.m1*(self.ell/2.0)**2]])
        C = np.matrix([[self.m1*(self.ell/2.0)*thetadot**2*np.sin(theta) + F - self.b*zdot],
                       [self.m1*self.g*(self.ell/2.0)*np.sin(theta)]])
        tmp = np.linalg.inv(M)*C
        zddot = 1.0/self.m

        # build xdot and return
        xdot = np.matrix([[zdot], [zddot]])
        return xdot

    def outputs(self):
        '''
            Returns the measured outputs as a list
            [z, theta] with added Gaussian noise
        '''
        # re-label states for readability
        z = self.state.item(0)
        theta = self.state.item(1)
        # add Gaussian noise to outputs
        z_m = z + random.gauss(0, 0.01)
        theta_m = theta + random.gauss(0, 0.001)
        # return measured outputs
        return [z_m, theta_m]

    def states(self):
        '''
            Returns all current states as a list
        '''
        return self.state.T.tolist()[0]