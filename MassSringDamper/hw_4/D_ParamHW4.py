# Mass Spring Damper Parameter File
import numpy as np
# import control as cnt
import sys
sys.path.append('..')  # add parent directory
import D_param as P

Ts = P.Ts  # sample rate of the controller
beta = P.beta  # dirty derivative gain
force_max = P.force_max  # limit on control signal

# PD gains
kp = 4.5
kd = 12.0

print('kp: ', kp)
print('kd: ', kd)
