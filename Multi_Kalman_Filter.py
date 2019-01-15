# Kalman Filter multi-dimensional

import numpy as np

def correction(mean_bar, var_bar, sensor):
    K = var_bar * C.transpose() * np.linalg.inv(C * var_bar * C.transpose() + Q)
    z = np.matrix([[sensor]])
    mean = mean_bar + K * (z - C * mean_bar)
    var = (I - K * C) * var_bar
    return mean, var

def prediction(mean, var):
    mean_bar = A * mean + B * u
    var_bar = A * var * A.transpose()
    return mean_bar, var_bar

sensors = [1, 2, 3, 4, 5]
# initial state (location, vel)
mean = np.matrix([[0.],\
                  [0.]])
# initial uncertainty
var = np.matrix([[1000., 0.],\
                 [0., 1000.]])
# initaial motion
u = np.matrix([[0.],\
               [0.]])

A = np.matrix([[1., 1.],\
               [0., 1.]])
B = np.eye(2)
C = np.matrix([[1., 0.]])
Q = np.matrix([[1.]])
I = np.eye(2)

for i in range(len(sensors)):
    # Step 1: State Prediction
    mean, var = prediction(mean, var)
    print i
    print "- prediction -"
    print "mean:", mean
    print "var:", var
    # Step 2 : Correction
    mean, var = correction(mean, var, sensors[i])
    print "- correction -"
    print "mean:", mean
    print "var:", var
    print '-------------------------------------------'
