import numpy as np
import D_param as P

# loop shaping control class
class SSIControl:
    def __init__(self, limit):
        self.limit = limit           # The output will saturate at this limit
        z_e = 0.0
        self.z_dot = 0.0
        self.y_d1 = 0.0
        self.r_e = z_e
        self.u_e = 0.0
        self.x_e = np.mat([[z_e],[0.]])

        self.A = np.mat([[0,1],[-0.6,-0.1]])
        self.B = np.mat([[0.],[0.2]])
        self.C = np.mat([[1.,0.]])
        # self.K = np.mat([3.05,7.2])

        # self.K = np.mat([4.45,9.5])
        # self.kr = -1.0 / (self.C*np.linalg.inv(self.A-self.B*self.K)*self.B)

        # Integrator variables
        self.K = np.mat([15.0858,14.5])
        self.ki = -8.0585
        # self.K = np.mat([28.25,19.5])
        # self.ki = -16.25
        self.integrator = 0.0
        self.error_d1 = 0.0

    def Ctrl(self, y_r, y):
        '''
            State-space controller
        '''
        # get states
        z = y
        self.z_dot = P.beta*self.z_dot + (1-P.beta)*((y - self.y_d1) / P.Ts)
        self.y_d1 = y
        error = y_r - y
        self.integrator += (P.Ts/2) * (error + self.error_d1)
        self.error_d1 = error

        # state vector x
        x = np.mat([[z],[self.z_dot]])

        # solve for tilde values for control
        x_tilde = x - self.x_e
        # r_tilde = y_r - self.r_e
        # u_tilde = -self.K*x_tilde + self.kr*y_r
        u_tilde = -self.K*x_tilde - self.ki*self.integrator

        disturbance = np.mat([[0.25]])
        # solve for u
        u_unsat = self.u_e + u_tilde + disturbance
        u = self.sat(u_unsat)

        # integrator anti-windup
        if self.ki != 0:
            self.integrator += (P.Ts/self.ki) * (u - u_unsat)

        return u

    def sat(self, u):
        if abs(u) > self.limit:
            u = self.limit*np.sign(u)
        return u
