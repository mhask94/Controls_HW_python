import sys
sys.path.append('..')  # add parent directory
import matplotlib.pyplot as plt
# import numpy as np
import D_param as P
from D_dynamics import D_dynamics
from D_controller import D_controller
from signalGenerator import signalGenerator
from D_animation import D_animation
from plotData import plotData
from preFilter import LSFControl as LSF

# instantiate arm, controller, and reference classes
msd = D_dynamics()
ctrl = D_controller()
F = LSF()
reference = signalGenerator(amplitude=1.0, frequency=0.05, y_offset=0.0)

# instantiate the simulation plots and animation
dataPlot = plotData()
animation = D_animation()

t = P.t_start  # time starts at t_start
while t < P.t_end:  # main simulation loop
    # Get referenced inputs from signal generators
    # ref_input = F.d(reference.square(t))
    ref_input = reference.square(t)
    # Propagate dynamics in between plot samples
    t_next_plot = t + P.t_plot
    while t < t_next_plot: # updates control and dynamics at faster simulation rate
        u = ctrl.u(ref_input, msd.outputs())  # Calculate the control value
        msd.propagateDynamics(u)  # Propagate the dynamics
        t = t + P.Ts  # advance time by Ts
    # update animation and data plots
    animation.drawAll(msd.states())
    dataPlot.updatePlots(t, ref_input, msd.states(), u)
    plt.pause(0.0001)  # the pause causes the figure to be displayed during the simulation

# Keeps the program from closing until the user presses a button.
print('Press key to close')
plt.waitforbuttonpress()
plt.close()
