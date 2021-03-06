import numpy as np
import D_param as P

# loop shaping control class
class SSControl:
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
        self.K = np.mat([4.45,9.5])
        self.kr = -1.0 / (self.C*np.linalg.inv(self.A-self.B*self.K)*self.B)

    def Ctrl(self, y_r, y):
        '''
            State-space controller
        '''
        # get states
        z = y
        self.z_dot = P.beta*self.z_dot + (1-P.beta)*((y - self.y_d1) / P.Ts)
        self.y_d1 = y

        # state vector x
        x = np.mat([[z],[self.z_dot]])

        # solve for tilde values for control
        x_tilde = x - self.x_e
        r_tilde = y_r - self.r_e
        u_tilde = -self.K*x_tilde + self.kr*y_r

        disturbance = np.mat([[0.25]])
        # solve for u
        u = self.u_e + u_tilde + disturbance
        return u
