import numpy as np

# loop shaping control class
class LSControl:
    def __init__(self, limit):
        self.limit = limit           # The output will saturate at this limit

        self.u1 = 0.0
        self.u2 = 0.0

        self.e1 = 0.0
        self.e2 = 0.0

        # use these if Ts = 0.025
        self.b0 = 413.8
        self.b1 = -813.1
        self.b2 = 399.4
        self.a1 = -1.618
        self.a2 = 0.6181

        # # use these if Ts = 0.05
        # self.b0 = 353.6
        # self.b1 = -682.6
        # self.b2 = 329.4
        # self.a1 = -1.359
        # self.a2 = 0.3587

    def D(self, y_r, y):
        '''
            Discretized controller
        '''

        # Compute the current error
        e0 = y_r - y

        # implement discretized controller
        u0 = -self.a1*self.u1-self.a2*self.u2+self.b0*e0+self.b1*self.e1+self.b2*self.e2

        # age data
        self.u2 = self.u1
        self.u1 = u0
        self.e2 = self.e1
        self.e1 = e0

        return u0
