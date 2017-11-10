# yevgeniy.korniyenko@sigma.se and henrik.svensson@sigma.se
# Picon Zero Servo Test
# Use arrow keys to move servos on outputs 0,1 for Pan and Tilt
# Use Q and E to lift up and down
# Use G and H to open and close the Gripper arm
# Press Ctrl-C to stop
#


import piconzero as pz, time    # get the servo module

import hcsr04       # get the ultrasonic module

from init import limMin,limMax,positions

from operationModes import *



 
#======================================================
# Initialization
print("Initialization started")
pz.init() # load servo operation library

# Set output mode to Servo
pz.setOutputConfig(rot, 2)
pz.setOutputConfig(tilt, 2)
pz.setOutputConfig(lift, 2)
pz.setOutputConfig(grip, 2)

# Sets the robot to the initial position. 
# Possible issue: rapid movement from the previous operation stop point.
for i in channels:
    smoothMotion(i,positions[i])

# End of initialization of operation
#======================================================

# main loop
print("Main loop started")
try:
    print("Select operation mode: automatic (y) or manual (n)")
    keyp=readkey()
    if keyp=='n':
        manualMode()
    elif keyp=='y':
        automaticMode()
    else:
        print("You are a smart one, aren't you?")
except KeyboardInterrupt:
    print()
finally:    # sets the robot back to the initial position
    smoothMotion(rot, rotInit)
    smoothMotion(tilt, tiltInit)
    smoothMotion(lift, liftInit)
    smoothMotion(grip, gripInit)
    
    pz.cleanup()