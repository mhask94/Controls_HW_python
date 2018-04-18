import numpy as np
import sys
# sys.path.append('..')  # add parent directory
import D_param as P
# from PIDControl import PIDControl
# from LSControl import LSControl
# from SSControl import SSControl
# from SSIControl import SSIControl
from SSI_Obs_Control import SSI_Obs_Control

class D_controller:

    def __init__(self):
        # Instantiates the PD object
        # self.zCtrl = PIDControl(P.kp, P.kd, P.force_max, P.beta, P.Ts)
        # self.zCtrl = LSControl(P.force_max)
        # self.zCtrl = SSIControl(P.force_max)
        self.zCtrl = SSI_Obs_Control(P.force_max)
        self.limit = P.force_max

    def u(self, y_r, y):
        # y_r is the referenced input
        # y is the current state
        z_r = y_r[0]
        z = y[0]
        z = z[0]
        z_e = 0.

        # compute equilibrium force force_e
        force_e = P.k * z_e
        # compute the linearized torque using PD
        # force_tilde = self.zCtrl.PID(z_r, z,False)

        # for loop shaping method
        # force_tilde = self.zCtrl.D(z_r, z)

        # for state-space control w/ or w/o integrator
        force_tilde = self.zCtrl.Ctrl(z_r, z)

        # for observer with state-space control
        # force_tilde = self.zCtrl.Ctrl(z_r, z)

        disturbance = 0.25

        # compute total torque
        force = force_e + force_tilde + disturbance
        force = self.saturate(force)
        # print([force,self.zCtrl.x_hat])

        # return [force]
        return [force,self.zCtrl.x_hat[0,0]-z]    # for observer

    def saturate(self, u):
        if abs(u) > self.limit:
            u = self.limit*np.sign(u)
        return u
