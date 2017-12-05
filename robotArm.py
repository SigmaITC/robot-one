# yevgeniy.korniyenko@sigma.se and henrik.svensson@sigma.se
# Picon Zero Servo Test
# Use arrow keys to move servos on outputs 0,1 for Pan and Tilt
# Use Q and E to lift up and down
# Use G and H to open and close the Gripper arm
# Press Ctrl-C to stop
#

from operationModes import *
import robotController as rc 

# main loop
rc.init()

print "Main loop started"
try:
    print "Select operation mode: automatic (y) or manual (n)"
    keyp = readkey()
    if keyp == 'n':
        manualMode()
    elif keyp == 'y':
        automaticMode()
    else:
        print "You are a smart one, aren't you?"
except KeyboardInterrupt:
    print " "
finally:    # sets the robot back to the initial position
    rc.shutdown()