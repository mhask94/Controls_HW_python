# Mass Spring Damper Parameter File
# import numpy as np
# import control as cnt

# Physical parameters of the arm known to the controller
m = 5.0      # Mass of the block, kg
k = 3.0      # spring constant, m
b = 0.5      # Damping coefficient, Nms

# parameters for animation
length = 2    # height of mass in animation
width = 0.3   # width of mass in animation
gap = .005
l_lim = -5
u_lim = 5

# Initial Conditions
z0 = 0.0  # ,m
zdot0 = 0.0         # ,rads/s

# Simulation Parameters
t_start = 0.0  # Start time of simulation
t_end = 30.0  # End time of simulation
Ts = .05  # sample time for simulation
t_plot = 1.0  # the plotting and animation is updated at this rate

# dirty derivative parameters
sigma = 0.05  # cutoff freq for dirty derivative
beta = (2.0*sigma-Ts)/(2.0*sigma+Ts)  # dirty derivative gain

# saturation limits
force_max = 2.0                # Max force, N

# gains
tr = 2.2
h = 0.7
Wn = 2.2 / tr
kp = m*Wn*Wn-k
kd = 2*m*h*Wn-b
