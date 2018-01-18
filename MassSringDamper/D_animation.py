import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import D_param as P

class D_animation:
    '''
        Create Mass Spring Damper animation
    '''
    def __init__(self):
        self.flagInit = True                  # Used to indicate initialization
        self.fig, self.ax = plt.subplots()    # Initializes a figure and axes object
        self.handle = []                      # Initializes a list object that will
                                              # be used to contain handles to the
                                              # patches and line objects.
        self.length=P.length
        self.width=P.width
        plt.axis([P.l_lim, P.u_lim, P.l_lim, P.u_lim]) # Change the x,y axis limits
        plt.plot([P.l_lim, P.u_lim], [0, 0],'k--')    # Draw ground
        plt.title('Mass Spring Damper')
        plt.xlabel('X [m]')

        # Draw pendulum is the main function that will call the functions:
        # drawCart, drawCircle, and drawRod to create the animation.
    def drawAll(self, u):
        # Process inputs to function
        x = u[0]        # Horizontal position of cart, m
        #theta = u[1]   # Angle of pendulum, rads

        self.drawMass(x)
        self.drawSpring(x)
        self.drawDamper(x)
        self.ax.axis('equal') # This will cause the image to not distort

        # After each function has been called, initialization is over.
        if self.flagInit == True:
            self.flagInit = False

    def drawMass(self, u):
        # Process inputs to function
        x = u  # x coordinate
        y = P.gap      # y coordinate
        xy = (x, y)     # Bottom left corner of rectangle

        # When the class is initialized, a Rectangle patch object will be
        # created and added to the axes. After initialization, the Rectangle
        # patch object will only be updated.
        if self.flagInit == True:
            # Create the Rectangle patch and append its handle
            # to the handle list
            self.handle.append(mpatches.Rectangle(xy,
                P.length,P.length, fc = 'blue', ec = 'black'))
            self.ax.add_patch(self.handle[0]) # Add the patch to the axes
        else:
            self.handle[0].set_xy(xy)         # Update patch

    def drawSpring(self, u):
        # Process inputs to function
        x = u   # x position of cube, m
        h = P.length*.25
        dh = P.length*.1
        xl = P.l_lim
        dx = (x-P.l_lim)/3.0
        ddx = dx/6.0
        points_x = [xl,xl+dx,xl+dx+.5*ddx,xl+dx+1.5*ddx,xl+dx+2.5*ddx,xl+dx+3.5*ddx,xl+dx+4.5*ddx,xl+dx+5.5*ddx,xl+2*dx,x]
        points_y = [h,h,h+dh,h-dh,h+dh,h-dh,h+dh,h-dh,h,h]

        # When the class is initialized, a line object will be
        # created and added to the axes. After initialization, the
        # line object will only be update
        if self.flagInit == True:
            # Create the line object and append its handle
            # to the handle list.
            line, =self.ax.plot(points_x, points_y, lw=1, c='black')
            self.handle.append(line)
        else:
            self.handle[1].set_xdata(points_x)   # Update the line
            self.handle[1].set_ydata(points_y)

    def drawDamper(self, u):
        # Process inputs to function
        x = u   # angle of arm, rads

        X = [P.l_lim, x]  # X data points
        Y = [P.length*.75, P.length*.75]  # Y data points

        # When the class is initialized, a line object will be
        # created and added to the axes. After initialization, the
        # line object will only be update
        if self.flagInit == True:
            # Create the line object and append its handle
            # to the handle list.
            line, =self.ax.plot(X, Y, lw=1, c='black')
            self.handle.append(line)
        else:
            self.handle[2].set_xdata(X)   # Update the line
            self.handle[2].set_ydata(Y)


# Used see the animation from the command line
# if __name__ == "__main__":
#
#     simAnimation = D_animation()    # Create Animate object
#     #theta = 0.0*np.pi/180                 # Angle of arm, rads
#     simAnimation.drawAll([x])  # Draw the arm
#     #plt.show()
#     # Keeps the program from closing until the user presses a button.
#     print('Press key to close')
#     plt.waitforbuttonpress()
#     plt.close()
