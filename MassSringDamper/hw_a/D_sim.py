import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('..')  # add parent directory
import D_param as P
# from signalGenerator import signalGenerator
from D_animation import D_animation
# from plotData import plotData
import matplotlib.patches as patches

# instantiate reference input classes
# reference = signalGenerator(amplitude=0.5, frequency=0.1)
# thetaRef = signalGenerator(amplitude=2.0*np.pi, frequency=0.1)
# tauRef = signalGenerator(amplitude=5, frequency=.5)

# instantiate the simulation plots and animation
# dataPlot = plotData()
animation = D_animation()

t = P.t_start  # time starts at t_start
z = P.x0
while t < P.t_end:  # main simulation loop
    # set variables
    if t < 6:
        z = z - .2
    if t >= 6:
        z = z + .2

    # r = reference.square(t)
    # theta = thetaRef.sin(t)
    # tau = tauRef.sawtooth(t)
    # update animation
    # state = [theta[0], 0.0]
    animation.drawAll([z])
    #dataPlot.updatePlots(t, r, state, tau)

    t = t + P.t_plot  # advance time by t_plot
    plt.pause(0.1)

# Keeps the program from closing until the user presses a button.
print('Press key to close')
plt.waitforbuttonpress()
plt.close()
