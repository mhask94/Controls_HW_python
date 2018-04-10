import numpy as np
import sys
# sys.path.append('..')  # add parent directory
import D_param as P
# from PIDControl import PIDControl
# from LSControl import LSControl
from SSControl import SSControl

class D_controller:

    def __init__(self):
        # Instantiates the PD object
        # self.zCtrl = PIDControl(P.kp, P.kd, P.force_max, P.beta, P.Ts)
        # self.zCtrl = LSControl(P.force_max)
        self.zCtrl = SSControl(P.force_max)
        self.limit = P.force_max

    def u(self, y_r, y):
        # y_r is the referenced input
        # y is the current state
        z_r = y_r[0]
        z = y[0]
        z = z[0]

        # compute equilibrium force force_e
        force_e = P.k * z
        # compute the linearized torque using PD
        # force_tilde = self.zCtrl.PID(z_r, z,False)
        # force_tilde = self.zCtrl.D(z_r, z)
        force_tilde = self.zCtrl.Ctrl(z_r, z)
        # compute total torque
        # force = force_e + force_tilde
        force = force_tilde
        force = self.saturate(force)
        return [force]

    def saturate(self, u):
        if abs(u) > self.limit:
            u = self.limit*np.sign(u)
        return u
