import piconzero as pz, time    # get the servo module

from init import *   # hardware configuration

import hcsr04       # get the ultrasonic module

ultrasonicInitialized = False;

channels=[rotChannel,tiltChannel,liftChannel,gripChannel]
limMax=[rotMax, tiltMax, liftMax, gripMax]
limMin=[rotMin, tiltMin, liftMin, gripMin]
positions=[rotInit,tiltInit,liftInit,gripInit]      # Position variable that the program operates on

#=====================================================================
# Initializes the robot arm to it's start position
def init():
    print("Initialization started")
    pz.init() # load servo operation library

    # Set output mode to Servo
    pz.setOutputConfig(rotChannel, 2)
    pz.setOutputConfig(tiltChannel, 2)
    pz.setOutputConfig(liftChannel, 2)
    pz.setOutputConfig(gripChannel, 2)

    # Sets the robot to the initial position. 
    # Possible issue: rapid movement from the previous operation stop point.
    for i in channels:
        pz.setOutput (i,positions[i])
        time.sleep(.5) # Sleep to reduce violent motions if arm is way off start target
    return 0
#=====================================================================

#=====================================================================
# Initializes the ultrasonic module
def initUltrasonic():
    hcsr04.init()
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
# Determines range to the nearest object, taking the minimal value of several measurements
def texasRanger():
    a=0     # distance sum dummy
    i=0     # measurement counter
    imax=10 # total measurement number
    while i<imax:
        a+=hcsr04.getDistance()
        i+=1
    return a/imax
#=========================================================================================

#======================================================================
# A function to make roboArm operation movement smoother, please use for all servo operations
def _smoothMotion(channel,stop):
    if (stop>limMax[channel]) or (stop<limMin[channel]):
        print ("Operational range exceeded")
        return 0
    while positions[channel]>stop:
        positions[channel]-=1
        pz.setOutput (channel, positions[channel])
        time.sleep(0.02)        # time.sleep(...) prevents rapid rotation
    while positions[channel]<stop:
        positions[channel]+=1
        pz.setOutput (channel, positions[channel])
        time.sleep(0.02)
    return 0
#=====================================================================

#=====================================================================
# Increase/decrease rotation number of degrees
def rotate(offset):
    _smoothMotion(rotChannel, positions[rotChannel] + offset)
#=====================================================================

#=====================================================================
# Increase/decrease tilt number of degrees
def tilt(offset):
    _smoothMotion(tiltChannel, positions[tiltChannel] + offset)
#=====================================================================

#=====================================================================
# Increase/decrease lift number of degrees
def lift(offset):
    _smoothMotion(liftChannel, positions[liftChannel] + offset)
#=====================================================================

#=====================================================================
# Increase/decrease grip number of degrees
def grip(offset):
    _smoothMotion(gripChannel, positions[gripChannel] + offset)
#=====================================================================

#=====================================================================
# Sets rotation to number of degrees
def setRotation(angle):
    _smoothMotion(rotChannel, angle)
#=====================================================================

#=====================================================================
# Sets tilt to number of degrees
def setTilt(angle):
    _smoothMotion(tiltChannel, angle)
#=====================================================================

#=====================================================================
# Sets lift to number of degrees
def setLift(angle):
    _smoothMotion(liftChannel, angle)
#=====================================================================

#=====================================================================
# Sets grip to number of degrees
def setGrip(angle):
    _smoothMotion(gripChannel, angle)
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

