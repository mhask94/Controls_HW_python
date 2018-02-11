import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('..')  # add parent directory
import D_param as P
from signalGenerator import signalGenerator
from D_animation import D_animation
# from plotData import plotData
# import matplotlib.patches as patches
from D_dynamics import D_dynamics

# instantiate reference input classes
reference = signalGenerator(amplitude=2.5, frequency=0.01)
# thetaRef = signalGenerator(amplitude=2.0*np.pi, frequency=0.01)
# tauRef = signalGenerator(amplitude=5, frequency=.5)

# instantiate the simulation plots and animation
system = D_dynamics()
# dataPlot = plotData()
animation = D_animation()

t = P.t_start  # time starts at t_start
z = P.z0
while t < P.t_end:  # main simulation loop
    # set variables
    # f = 2*P.k*P.z0

    t_next_plot = t + P.t_plot
    while t < t_next_plot:
        f = reference.sin(t)
        system.propagateDynamics([f])
        z = system.state[0,0]
        t = t + P.Ts
    # update animation
    # state = [theta[0], 0.0]
    animation.drawAll([z])
    # dataPlot.updatePlots(t, r, state, tau)
    t = t + P.t_plot  # advance time by t_plot
    plt.pause(0.0001)

# t = P.t_start  # time starts at t_start
# while t < P.t_end:  # main simulation loop
#     # Get referenced inputs from signal generators
#     ref_input = reference.square(t)
#     # Propagate dynamics in between plot samples
#     t_next_plot = t + P.t_plot
#     while t < t_next_plot:  # updates control and dynamics at faster simulation rate
#         f = force.sin(t)
#         pendulum.propagateDynamics(f)  # Propagate the dynamics
#         t = t + P.Ts  # advance time by Ts
#     # update animation and data plots
#     animation.drawPendulum(pendulum.states())
#     dataPlot.updatePlots(t, ref_input, pendulum.states(), f)
#     plt.pause(0.0001)  # the pause causes the figure to be displayed during the simulation

# Keeps the program from closing until the user presses a button.
print('Press key to close')
plt.waitforbuttonpress()
plt.close()
