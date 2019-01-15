# Kalman Filter 1D
def correction(mean, var, sensor_mean, sensor_var):
    new_mean = (sensor_mean*var + mean*sensor_var)/(var + sensor_var)
    new_var = var*sensor_var/(var + sensor_var)
    return new_mean, new_var

def prediction(mean, var, motion_mean, motion_var):
    new_mean = mean + motion_mean
    new_var = var + motion_var
    return new_mean, new_var

sensor = [5, 6, 7, 9, 10]
sensor_var = 4

motion = [1, 1, 2, 1, 1]
motion_var = 2

mean = 0
var = 1000

for i in range(len(sensor)):
    # Step 1: State Prediction
    mean, var = prediction(mean, var, motion[i], motion_var)
    print i
    print "- prediction -"
    print "mean:", mean
    print "var:", var
    # Step 2 : Correction
    mean, var = correction(mean, var, sensor[i], sensor_var)
    print "- correction -"
    print "mean:", mean
    print "var:", var
    print '-------------------------------------------'