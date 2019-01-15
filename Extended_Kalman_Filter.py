import numpy as np


'''
sensors = [1, 2, 3, 4, 5]
# initial state (location, vel)
mean = np.matrix([[0.], [0.]])
# initial uncertainty
var = np.matrix([[1000., 0.], [0., 1000.]])
# initaial motion
u = np.matrix([[0.], [0.]])

# A = np.matrix([[1., 1.], [0., 1.]]) -> Jacobian G
B = np.eye(2)
# C = np.matrix([[1., 0.]]) -> Jacobian H

I = np.eye(2)
'''

def correction(sensors, mean, var, landmarks):
    x = mean[0]
    y = mean[1]
    theta = mean[2]

    # i, sensor
    id = sensors['id']
    ranges = sensors['range']

    H = []
    Z = []
    expected_ranges = []

    for i in range(len(id)):
        lm_id = id[i]
        means_range = ranges[i]
        lx = landmarks[lm_id][0]
        ly = landmarks[lm_id][1]

        range_exp = np.sqrt( (lx-x)**2 + (ly-y)**2 )
        H_i = [(x-lx)/range_exp, (y-ly)/range_exp, 0]
        H.append(H_i)
        Z.append(range[i])
        expected_ranges.append(range_exp)

    R = 0.5 * np.eye(len(id))

    # Kalman Gain
    K = mean * H.transpose() * np.linalg.inv( H * var * H.transpose() + R)

    # Sensor Update
    mean = mean + K * (np.array(Z) - np.array(expected_ranges))
    var = (np.eye(len(var))- ( K * H )) * var

    return mean, var


def prediction(odometry, mean, var):
    x = mean[0]
    y = mean[1]
    theta = mean[2]

    delta_rot1 = odometry['r1']
    delta_trans = odometry['t']
    delta_rot2 = odometry['r2']

    Q = np.array([[0.2, 0.0, 0.0], \
                  [0.0, 0.2, 0.0], \
                  [0.0, 0.0, 0.02]])

    x_new = x + delta_trans * np.cos(theta + delta_rot1)
    y_new = y + delta_trans * np.sin(theta + delta_rot1)
    theta_new = theta + delta_rot1 + delta_rot2

    G = np.array([[1.0, 0.0, -delta_trans * np.sin(theta + delta_rot1)], \
                  [0.0, 1.0, delta_trans * np.cos(theta + delta_rot1), \
                  [0.0, 0.0, 1.0]])

    mean_new = [x_new, y_new, theta_new]
    var_new = G * var * np.transpose(G) + Q

    return mean_new, var_new


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
