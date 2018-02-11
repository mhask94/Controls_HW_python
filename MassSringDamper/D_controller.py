import numpy as np
import sys
sys.path.append('..')  # add parent directory
import D_param as P
from PDControl import PDControl


class D_controller:

    def __init__(self):
        # Instantiates the PD object
        self.zCtrl = PDControl(P.kp, P.kd, P.force_max, P.beta, P.Ts)
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
        force_tilde = self.zCtrl.PD(z_r, z, False)
        # compute total torque
        force = force_e + force_tilde
        force = self.saturate(force)
        return [force]

    def saturate(self, u):
        if abs(u) > self.limit:
            u = self.limit*np.sign(u)
        return u
