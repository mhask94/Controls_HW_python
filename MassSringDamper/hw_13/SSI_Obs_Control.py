import numpy as np
import D_param as P
import control as cnt

# loop shaping control class
class SSI_Obs_Control:
    def __init__(self, limit):
        self.limit = limit           # The output will saturate at this limit
        z_e = 0.0
        self.z_dot = 0.0
        self.y_d1 = 0.0
        self.r_e = z_e
        self.u_e = 0.0
        self.x_e = np.mat([[z_e],[0.]])

        self.A = np.mat([[0,1],[-0.6,-0.1]])
        self.B = np.mat([[0.],[0.2]])
        self.C = np.mat([[1.,0.]])

        A1 = np.mat([[0,1,0],[-.6,-.1,0],[-1.,0,0]])
        B1 = np.mat([[0],[.2],[0]])

        # self.K = np.mat([4.45,9.5])
        # self.kr = -1.0 / (self.C*np.linalg.inv(self.A-self.B*self.K)*self.B)

        # Integrator variables
        tr = 1
        Wn = 2.2 / tr
        h = .7
        int_pole = -5.
        Wn_obs = 10 * Wn
        h_obs = .7

        des_char_poly = np.convolve(
            [1,2*h*Wn,Wn**2],np.poly(int_pole))
        des_poles = np.roots(des_char_poly)

        # Check for controllability
        if np.linalg.matrix_rank(cnt.ctrb(A1,B1)) != 3:
            print('Warning: Not Controllable')

        K1 = cnt.place(A1,B1,des_poles)
        self.K = np.mat([K1.item(0),K1.item(1)])
        self.ki = K1.item(2)

        # Observer/Estimator Design
        des_obsv_char_poly = [1,2*h_obs*Wn_obs,Wn_obs**2]
        des_obsv_poles = np.roots(des_obsv_char_poly)

        # Check for observability
        if np.linalg.matrix_rank(cnt.ctrb(self.A.T,self.C.T)) != 2:
            print('Warning: Not Observerable')

        self.L = cnt.place(self.A.T,self.C.T,des_obsv_poles).T

        # self.K = np.mat([15.0858,14.5])
        # self.ki = -8.0585
        # self.K = np.mat([9.45,12.0])
        # self.ki = -3.725
        self.integrator = 0.0
        self.error_d1 = 0.0

        # Observer variables
        self.x_hat = np.mat([[0.],[0.]])
        self.u = 0.0
        self.force_d1 = 0.
        # self.L = np.mat([[14.04, 97.996]])
        # self.L = np.mat([[16.868],[141.7132]])

        sys = cnt.ss(self.A,self.B,self.C,np.mat([0]))
        sys_d = cnt.matlab.c2d(sys,P.Ts)
        self.Ad = sys_d.A
        self.Bd = sys_d.B
        self.Cd = sys_d.C

        des_obsv_poles_d = np.exp(P.Ts*des_obsv_poles)
        self.Ld = cnt.place(self.Ad.T,self.Cd.T,des_obsv_poles_d).T
        # self.Ad = np.mat([[.9998,.02497],[-.01498,.9973]])
        # self.Bd = np.mat([[.00006245],[.004993]])
        # self.Ld = np.mat([[16.1],[4609.9]])
        # self.Ld = np.mat([[19.0],[6485.2]])

    def Ctrl(self, y_r, y):
        '''
            State-space controller
        '''
        # get states
        z = y
        z_r = y_r

        # Observer
        # possibly need to update equilibrium force with z here
        # self.x_hat = self.Ad*(self.x_hat-self.x_e)+self.Bd*(self.u-self.u_e)+self.Ld*(y-self.C*self.x_hat)
        self.updateObserver(y)
        zhat = self.x_hat[0]
        error = y_r - y # zhat

        # error = y_r - y
        self.integrator += (P.Ts/2) * (error + self.error_d1)
        self.error_d1 = error

        # self.z_dot = P.beta*self.z_dot + (1-P.beta)*((y - self.y_d1) / P.Ts)
        self.y_d1 = y
        zhat = self.x_hat[0]
        self.u_e = P.k*zhat*0
        # state vector x
        # x = np.mat([[z],[self.z_dot]])
        # self.x_hat = np.mat([[z],[self.z_dot]])

        # solve for tilde values for control
        # x_tilde = x - self.x_e
        # r_tilde = y_r - self.r_e

        # for no integrator
        # u_tilde = -self.K*x_tilde + self.kr*y_r
        # for no integrator
        # u_tilde = -self.K*x_tilde - self.ki*self.integrator
        # for observer and integrator
        u_tilde = -self.K*self.x_hat - self.ki*self.integrator

        # disturbance = np.mat([[0.25]])
        disturbance = np.mat([[0.]])

        # solve for u
        u_unsat = self.u_e + u_tilde + disturbance
        u = self.sat(u_unsat)
        self.updateForce(u)

        # integrator anti-windup
        if self.ki != 0:
            self.integrator += (P.Ts/self.ki) * (u - u_unsat)

        return u

    def updateObserver(self,y_m):
        # possibly need to update equilibrium force with z here
        zhat = self.x_hat[0]
        u_e = 3*zhat*0
        self.x_hat = self.Ad*(self.x_hat-self.x_e)+self.Bd*(self.u-self.u_e)+self.Ld*(y_m-self.Cd*self.x_hat)

        # N = 10
        # for i in range(0,N):
        #     self.x_hat += P.Ts/float(N)*(self.A*self.x_hat
        #         + self.B*(self.force_d1 - u_e)
        #         + self.L*(y_m-self.C*self.x_hat))

    def updateForce(self,force):
        self.force_d1 = force
        self.u = force

    def sat(self, u):
        if abs(u) > self.limit:
            u = self.limit*np.sign(u)
        return u
