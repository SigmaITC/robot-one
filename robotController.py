import piconzero as pz, time    # get the servo module
import math

from init import *   # hardware configuration

import hcsr04       # get the ultrasonic module

ultrasonicInitialized = False;

channels=[rotChannel,tiltChannel,liftChannel,gripChannel]
limMax=[rotMax, tiltMax, liftMax, gripMax]
limMin=[rotMin, tiltMin, liftMin, gripMin]
positions=[rotInit, tiltInit, liftInit, gripInit]      # Position variable that the program operates on
speed=speedInit

#=====================================================================
# Initializes the robot arm to it's start position
def init():
    print "Initialization started"
    pz.init() # load servo operation library

    # Set output mode to Servo
    pz.setOutputConfig(rotChannel, 2)
    pz.setOutputConfig(tiltChannel, 2)
    pz.setOutputConfig(liftChannel, 2)
    pz.setOutputConfig(gripChannel, 2)

    # Sets the robot to the initial position. 
    # Possible issue: rapid movement from the previous operation stop point.
    for i in channels:
        _safeSetAngle(i, positions[i])
        time.sleep(.5) # Sleep to reduce violent motions if arm is way off start target
    return 0
#=====================================================================

#=====================================================================
# Initializes the ultrasonic module
def initUltrasonic():
    hcsr04.init()
    global ultrasonicInitialized
    ultrasonicInitialized = True;
#=====================================================================


#=====================================================================
# Prepares robot arm for turning off
def shutdown():
    resetPosition()
    pz.cleanup()
    if ultrasonicInitialized:
        hcsr04.cleanup()

#=====================================================================

#=====================================================================
# Resets robot arm to default location
def resetPosition():
    _smoothMotion(rotChannel, rotInit)
    _smoothMotion(tiltChannel, tiltInit)
    _smoothMotion(liftChannel, liftInit)
    _smoothMotion(gripChannel, gripInit)
#=====================================================================

#=========================================================================================
# Determines range to the nearest object, taking the mean value of several measurements
def texasRanger():
    i = 0     # measurement counter
    imax = 5 # total measurement number
    distances = []
    while i < imax:
        distances.append(hcsr04.getDistance())
        time.sleep(0.05) # Sleep needed to allow pings from previous measurements to dissipate
        i += 1
    distances.sort()
    return distances[2]
#=========================================================================================

#=====================================================================
# A function to make roboArm operation movement smoother, please use for all servo operations
# Will return False if angle exceeds maximum range or True when the servo has been moved
def _smoothMotion(channel,stop):
    if not _canSetAngle(channel, stop):
        print "Operational range exceeded"
        return False

    while positions[channel] != stop:
        diff = stop - positions[channel]
        positions[channel] += math.copysign(min(1, abs(diff)), diff)
        _safeSetAngle(channel, int(positions[channel]))
        time.sleep(speed)
    return True
#=====================================================================

#=====================================================================
# Set servo with limit check
def _safeSetAngle(channel, angle):
    if _canSetAngle(channel, angle):
        pz.setOutput(channel, angle)
        return True
    return False
#=====================================================================

#=====================================================================
# Returns true if angle is valid for channel
def _canSetAngle(channel, angle):
    if angle > limMax[channel] or angle < limMin[channel]:
        return False
    return True
#=====================================================================

#=====================================================================
# Increase/decrease rotation number of degrees
def rotate(offset):
    return _smoothMotion(rotChannel, positions[rotChannel] + offset)
#=====================================================================

#=====================================================================
# Increase/decrease tilt number of degrees
def tilt(offset):
    return _smoothMotion(tiltChannel, positions[tiltChannel] + offset)
#=====================================================================

#=====================================================================
# Increase/decrease lift number of degrees
def lift(offset):
    return _smoothMotion(liftChannel, positions[liftChannel] + offset)
#=====================================================================

#=====================================================================
# Increase/decrease grip number of degrees
def grip(offset):
    return _smoothMotion(gripChannel, positions[gripChannel] + offset)
#=====================================================================

#=====================================================================
# Sets rotation to number of degrees
def setRotation(angle):
    return _smoothMotion(rotChannel, angle)
#=====================================================================

#=====================================================================
# Sets tilt to number of degrees
def setTilt(angle):
    return _smoothMotion(tiltChannel, angle)
#=====================================================================

#=====================================================================
# Sets lift to number of degrees
def setLift(angle):
    return _smoothMotion(liftChannel, angle)
#=====================================================================

#=====================================================================
# Sets grip to number of degrees
def setGrip(angle):
    return _smoothMotion(gripChannel, angle)
#=====================================================================

#=====================================================================
# Sets all to number of degrees
def setAll(rotation, tilt, lift, grip):
    targetValues = [rotation, tilt, lift, grip]
    diffs = []
    for i in channels:
        if not _canSetAngle(i, targetValues[i]):
            print "Operational range exceeded"
            return False
        else:
            diffs.append(abs(targetValues[i] - positions[i]))

    # Number of iterations set so that max change per iteration is
    # 1 degree, to give uniform servo speed.
    deltas = []
    iterations = int(max(diffs))

    if iterations == 0: # No change needed
        return True

    for i in channels:
        deltas.append((targetValues[i] - positions[i]) / iterations)

    for x in range(0, iterations):
        for i in channels:
            if positions[i] != targetValues[i]:
                positions[i] += deltas[i]
                _safeSetAngle(i, int(positions[i]))
        time.sleep(speed)
    return True

#=====================================================================

#=====================================================================
# Gets rotation to number of degrees
def getRotation():
    return positions[rotChannel]
#=====================================================================

#=====================================================================
# Gets tilt to number of degrees
def getTilt():
    return positions[tiltChannel]
#=====================================================================

#=====================================================================
# Gets lift to number of degrees
def getLift():
    return positions[liftChannel]
#=====================================================================

#=====================================================================
# Gets grip to number of degrees
def getGrip():
    return positions[gripChannel]
#=====================================================================

#=====================================================================
# Sets servo speed
def setSpeed(newSpeed):
    global speed
    speed = newSpeed
#=====================================================================


