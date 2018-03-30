# loop shaping control class
class LSFControl:
    def __init__(self):
        self.u1 = 0.0
        self.e1 = 0.0

        # # use these for a = 2.75 (slow response)
        # self.b0 = 0.03323
        # self.b1 = 0.03323
        # self.a1 = -0.9335

        # use these for a = 7 (no peak)
        self.b0 = 0.08046
        self.b1 = self.b0
        self.a1 = -0.8391

        # # use these for a = 8 (little peak)
        # self.b0 = 0.09091
        # self.b1 = self.b0
        # self.a1 = -0.8182

        # # use these for a = 15 (really fast response)
        # self.b0 = 0.1579
        # self.b1 = 0.1579
        # self.a1 = -0.6842

    def d(self, y_r):
        '''
            Discretized preFilter
        '''

        # Compute the current error
        e0 = y_r[0]

        # implement discretized controller
        u0 = -self.a1*self.u1+self.b0*e0+self.b1*self.e1

        # age data
        self.u1 = u0
        self.e1 = e0

        return [u0]
