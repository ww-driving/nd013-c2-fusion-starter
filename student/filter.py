# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Kalman filter class
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# add project directory to python path to enable relative imports
import os
import sys

# imports
import numpy as np

from misc import params

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


class Filter:
    '''Kalman filter class'''

    def __init__(self):
        self.q = params.q
        self.dim_state = params.dim_state
        self.dt = params.dt
        self.log = {'x': [], 'P': [], 'z': [], 'gamma': [], 'S': []}

    def F(self):
        ############
        # TODO Step 1: implement and return system matrix F
        ############

        return np.array([[1, 0, 0, self.dt, 0, 0],
                         [0, 1, 0, 0, self.dt, 0],
                         [0, 0, 1, 0, 0, self.dt],
                         [0, 0, 0, 1, 0, 0],
                         [0, 0, 0, 0, 1, 0],
                         [0, 0, 0, 0, 0, 1]])

        ############
        # END student code
        ############ 

    def Q(self):
        ############
        # TODO Step 1: implement and return process noise covariance Q
        ############
        Q = np.diag([0, 0, 0, self.q, self.q, self.q])
        F = self.F()
        FQF = F @ Q @ F.T
        integral_factor = np.array([[self.dt / 3, 0, 0, self.dt / 2, 0, 0],
                                    [0, self.dt / 3, 0, 0, self.dt / 2, 0],
                                    [0, 0, self.dt / 3, 0, 0, self.dt / 2],
                                    [self.dt / 2, 0, 0, self.dt, 0, 0],
                                    [0, self.dt / 2, 0, 0, self.dt, 0],
                                    [0, 0, self.dt / 2, 0, 0, self.dt]])
        QT = integral_factor * FQF
        return QT

        ############
        # END student code
        ############ 

    def predict(self, track):
        ############
        # TODO Step 1: predict state x and estimation error covariance P to next timestep, save x and P in track
        ############

        F = self.F()
        x = F @ track.x  # state prediction
        P = F @ track.P @ F.transpose() + self.Q()  # covariance prediction
        track.set_x(x)
        track.set_P(P)
        self.log['x'].append(x)
        self.log['P'].append(P)

        ############
        # END student code
        ############ 

    def update(self, track, meas):
        ############
        # TODO Step 1: update state x and covariance P with associated measurement, save x and P in track
        ############

        H = meas.sensor.get_H(track.x)
        K = track.P @ H.T @ np.linalg.inv(self.S(track, meas, H))
        x = track.x + K * self.gamma(track, meas)
        P = (np.identity(self.dim_state) - K @ H) @ track.P
        track.set_x(x)
        track.set_P(P)
        self.log['x'].append(x)
        self.log['P'].append(P)

        ############
        # END student code
        ############ 
        track.update_attributes(meas)

    def gamma(self, track, meas):
        ############
        # TODO Step 1: calculate and return residual gamma
        ############

        gamma = meas.z - meas.sensor.get_hx(track.x)
        self.log['gamma'].append(gamma)
        self.log['z'].append(meas.z)

        return gamma

        ############
        # END student code
        ############ 

    def S(self, track, meas, H):
        ############
        # TODO Step 1: calculate and return covariance of residual S
        ############

        S = H @ track.P @ H.T + meas.R
        self.log['S'].append(S)

        return S

        ############
        # END student code
        ############

    def __repr__(self):
        return str({k: np.array(v) for k, v in self.log.items()})
